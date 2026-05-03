from dotenv import load_dotenv
load_dotenv()

import os, datetime
from database import init_db, insert_job_if_new, update_job_ai_results, get_profile
from scraper import scrape_jobs
from ai import score_job
from notifications import notify


def main():
    print(f"\n{'='*50}")
    print(f"NandoHunting run started: {datetime.datetime.now().isoformat()}")
    print(f"{'='*50}")

    init_db()

    profile = get_profile()
    if not profile or not profile.get("target_description"):
        print("ERROR: No target profile saved. Go to Settings and save one.")
        return

    query = os.getenv("JOB_QUERY", "office services coordinator")
    location = os.getenv("JOB_LOCATION", "Toronto, ON")

    print(f"Searching: {query} | {location}")
    jobs = scrape_jobs(query, location)
    print(f"Scraped {len(jobs)} jobs from all sources")

    new_count = 0
    skipped_count = 0
    alerted_count = 0

    for job in jobs:
        inserted = insert_job_if_new(job)
        if not inserted:
            skipped_count += 1
            continue

        # Score the job
        ai_result = score_job(job["description_raw"],
                              profile["target_description"])
        score = ai_result.get("score", 0)
        summary = ai_result.get("summary", "")
        reasons = ai_result.get("reasons", "")
        if isinstance(reasons, list):
            reasons = "\n".join(f"- {r}" for r in reasons)

        # Find the inserted job id by hash
        from database import get_job_by_hash
        inserted_job = get_job_by_hash(job["hash"])
        if inserted_job:
            update_job_ai_results(inserted_job["id"], score, summary, reasons)

            if score >= int(os.getenv("ALERT_THRESHOLD", "7")):
                job_with_score = {**job, "ai_score": score,
                                  "ai_summary": summary, "ai_reasons": reasons}
                notify(job_with_score)
                alerted_count += 1

        new_count += 1

    print(f"\nDone. New: {new_count} | Skipped: {skipped_count} | Alerts: {alerted_count}")
    print(f"Run completed: {datetime.datetime.now().isoformat()}\n")


if __name__ == "__main__":
    main()
