"""HTTP-based job scraping from Indeed RSS and SerpAPI Google Jobs."""

import hashlib
import html
import os
import re
from datetime import datetime
import xml.etree.ElementTree as ET

import httpx
from dotenv import load_dotenv


def _is_direct_apply_link(url: str) -> bool:
    """Return True for non-Google links that look like direct apply destinations."""
    if not url:
        return False
    lower = url.lower()
    if "google.com" in lower:
        return False
    return lower.startswith("http://") or lower.startswith("https://")


def _strip_html(raw: str) -> str:
    if not raw:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", raw, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def _extract_field(description_text: str, field_name: str) -> str:
    pattern = rf"{re.escape(field_name)}\s*:\s*([^\n]+)"
    match = re.search(pattern, description_text, flags=re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip()


def _normalize_job(
    title: str,
    company: str,
    location: str,
    salary_raw: str,
    url: str,
    description_raw: str,
) -> dict:
    combined_text = f"{title} {location}".lower()
    remote = 1 if "remote" in combined_text else 0
    job_hash = hashlib.sha256(f"{company}{title}{url}".encode()).hexdigest()
    return {
        "title": title or "",
        "company": company or "",
        "location": location or "",
        "salary_raw": salary_raw or "",
        "url": url or "",
        "description_raw": description_raw or "",
        "remote": remote,
        "hash": job_hash,
        "scraped_at": datetime.now().isoformat(),
    }


def _scrape_indeed_rss(query: str, location: str) -> list[dict]:
    rss_url = "https://www.indeed.com/rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }
    jobs = []
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                rss_url,
                params={"q": query, "l": location},
                headers=headers,
            )
            response.raise_for_status()

        root = ET.fromstring(response.text)
        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").strip()
            url = (item.findtext("link") or "").strip()
            raw_description = item.findtext("description") or ""
            description_text = _strip_html(raw_description)
            company = _extract_field(description_text, "Company")
            item_location = _extract_field(description_text, "Location")

            jobs.append(
                _normalize_job(
                    title=title,
                    company=company,
                    location=item_location,
                    salary_raw="",
                    url=url,
                    description_raw=description_text,
                )
            )
    except Exception as e:
        print(f"Warning: Indeed RSS scrape failed: {e}")
    return jobs


def _scrape_serpapi_google_jobs(query: str, location: str, api_key: str) -> list[dict]:
    if not api_key:
        print("Warning: SERPAPI_KEY not set; skipping SerpAPI source.")
        return []

    jobs = []
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://serpapi.com/search",
                params={
                    "engine": "google_jobs",
                    "q": f"{query} {location}",
                    "hl": "en",
                    "api_key": api_key,
                },
            )
            response.raise_for_status()
            payload = response.json()

        for item in payload.get("jobs_results", []):
            title = (item.get("title") or "").strip()
            company = (item.get("company_name") or "").strip()
            item_location = (item.get("location") or "").strip()
            salary_raw = (item.get("salary") or "").strip()
            description_raw = (item.get("description") or "").strip()
            url = ""

            # Prefer direct application URLs from apply options.
            apply_options = item.get("apply_options") or []
            for option in apply_options:
                if not isinstance(option, dict):
                    continue
                candidate = (option.get("link") or "").strip()
                if _is_direct_apply_link(candidate):
                    url = candidate
                    break

            if not url:
                primary_url = (item.get("url") or "").strip()
                share_link = item.get("share_link")
                share_link = share_link.strip() if isinstance(share_link, str) else ""
                if _is_direct_apply_link(primary_url):
                    url = primary_url
                elif _is_direct_apply_link(share_link):
                    url = share_link
                else:
                    # Final fallback keeps row usable even if only Google link exists.
                    url = primary_url or share_link

            if not url:
                continue

            jobs.append(
                _normalize_job(
                    title=title,
                    company=company,
                    location=item_location,
                    salary_raw=salary_raw,
                    url=url,
                    description_raw=description_raw,
                )
            )
    except Exception as e:
        print(f"Warning: SerpAPI scrape failed: {e}")
    return jobs


def scrape_jobs(query: str, location: str) -> list[dict]:
    """Scrape jobs from Indeed RSS and SerpAPI, then deduplicate by hash."""
    serpapi_key = os.getenv("SERPAPI_KEY", "")
    combined = _scrape_indeed_rss(query, location) + _scrape_serpapi_google_jobs(
        query, location, serpapi_key
    )

    deduped = []
    seen_hashes = set()
    for job in combined:
        job_hash = job.get("hash")
        if not job_hash or job_hash in seen_hashes:
            continue
        seen_hashes.add(job_hash)
        deduped.append(job)
    return deduped


if __name__ == "__main__":
    load_dotenv()
    query = os.getenv("JOB_QUERY", "python engineer")
    location = os.getenv("JOB_LOCATION", "remote")
    jobs = scrape_jobs(query, location)
    print(f"Scraped {len(jobs)} jobs.")
