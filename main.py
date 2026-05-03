"""
FastAPI backend for NandoHunting career agent.
Local-only, no auth, no middleware (except CORS).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import re

from database import (
    init_db, get_jobs_by_status, get_job_by_id, get_job_by_hash,
    update_job_status, get_profile, save_profile, insert_job_if_new,
    update_job_ai_results, save_generated_docs, get_job_docx_bytes
)
from ai import score_job, generate_full_resume, generate_cover_letter
from resume_builder import save_all_formats
from scraper import scrape_jobs

load_dotenv()

# Initialize app
app = FastAPI(title="NandoHunting Career Agent")

# CORS middleware (allow all origins — local personal tool)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()


# Pydantic model for POST /profile
class ProfileRequest(BaseModel):
    master_resume: str
    target_description: str


# GET /jobs?status=new
@app.get("/jobs")
def get_jobs(status: str = "new"):
    """Get all jobs with given status (default: 'new')"""
    jobs = get_jobs_by_status(status)
    return jobs


# GET /jobs/{job_id}
@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    """Get single job by ID"""
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# POST /jobs/{job_id}/accept
@app.post("/jobs/{job_id}/accept")
def accept_job(job_id: int):
    """Accept job and generate tailored resume and cover letter."""
    # Update status to accepted
    update_job_status(job_id, "accepted", datetime.now().isoformat())
    
    # Fetch job and profile
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    profile = get_profile()
    
    # If no master resume, return placeholder message
    if not profile or not profile.get("master_resume"):
        return {
            "status": "accepted",
            "resume_md": "No master resume saved. Go to Settings to add one.",
            "cover_letter_md": "No master resume saved. Go to Settings to add one.",
        }
    
    # Generate full tailored resume markdown
    resume_md = generate_full_resume(
        job.get("description_raw", ""),
        profile.get("master_resume", ""),
        job.get("title", ""),
        job.get("company", ""),
    )

    cover_letter = generate_cover_letter(
        job.get("description_raw", ""),
        profile.get("master_resume", ""),
        job.get("title", ""),
        job.get("company", ""),
    )

    paths = save_all_formats(
        job_id=job_id,
        resume_md=resume_md,
        cover_letter_md=cover_letter,
        job_title=job.get("title", ""),
        company=job.get("company", ""),
    )

    with open(paths["resume_docx_path"], "rb") as resume_file:
        resume_docx_bytes = resume_file.read()
    with open(paths["cover_docx_path"], "rb") as cover_file:
        cover_docx_bytes = cover_file.read()

    save_generated_docs(
        job_id,
        resume_md,
        cover_letter,
        resume_docx_bytes,
        cover_docx_bytes,
    )
    
    return {
        "status": "accepted",
        "resume_md": resume_md,
        "cover_letter_md": cover_letter,
    }


@app.post("/jobs/{job_id}/reopen")
def reopen_job(job_id: int):
    """Move a previously reviewed job back to inbox."""
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_job_status(job_id, "new", datetime.now().isoformat())
    return {"status": "new"}


@app.get("/jobs/{job_id}/resume.docx")
def download_resume_docx(job_id: int):
    """Download generated resume .docx for a job."""
    blob_data = get_job_docx_bytes(job_id)
    if not blob_data or not blob_data.get("resume_docx"):
        raise HTTPException(status_code=404, detail="Resume .docx not found")

    output_dir = Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_path = output_dir / f"resume_{job_id}_download.docx"
    temp_path.write_bytes(blob_data["resume_docx"])

    job = get_job_by_id(job_id)
    company = (job or {}).get("company", "company")
    company_slug = re.sub(r"[^a-zA-Z0-9]+", "", company).lower() or "company"

    return FileResponse(
        str(temp_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=resume-{company_slug}.docx"},
    )


@app.get("/jobs/{job_id}/cover.docx")
def download_cover_docx(job_id: int):
    """Download generated cover letter .docx for a job."""
    blob_data = get_job_docx_bytes(job_id)
    if not blob_data or not blob_data.get("cover_letter_docx"):
        raise HTTPException(status_code=404, detail="Cover letter .docx not found")

    output_dir = Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_path = output_dir / f"cover_{job_id}_download.docx"
    temp_path.write_bytes(blob_data["cover_letter_docx"])

    job = get_job_by_id(job_id)
    company = (job or {}).get("company", "company")
    company_slug = re.sub(r"[^a-zA-Z0-9]+", "", company).lower() or "company"

    return FileResponse(
        str(temp_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=cover-letter-{company_slug}.docx"},
    )


# POST /jobs/{job_id}/reject
@app.post("/jobs/{job_id}/reject")
def reject_job(job_id: int):
    """Reject a job"""
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_job_status(job_id, "rejected", datetime.now().isoformat())
    return {"status": "rejected"}


# GET /profile
@app.get("/profile")
def get_user_profile():
    """Get user profile or empty dict if not set"""
    profile = get_profile()
    if not profile:
        return {"master_resume": "", "target_description": ""}
    return profile


# POST /profile
@app.post("/profile")
def save_user_profile(req: ProfileRequest):
    """Save or update user profile"""
    save_profile(req.master_resume, req.target_description)
    return {"status": "saved"}


# POST /scrape
@app.post("/scrape")
def trigger_scrape():
    """
    Scrape Indeed, score jobs, and insert into DB.
    Returns count of scraped, new, and skipped jobs.
    """
    # Load query and location from environment
    query = os.getenv("JOB_QUERY", "python engineer")
    location = os.getenv("JOB_LOCATION", "remote")
    
    # Fetch profile for scoring
    profile = get_profile()
    target_description = profile.get("target_description", "") if profile else ""
    
    if not target_description:
        return {
            "scraped": 0,
            "new": 0,
            "skipped": 0,
            "error": "No target description in profile. Please set it in Settings."
        }
    
    # Scrape jobs from all configured sources
    jobs = scrape_jobs(query, location)
    
    total_scraped = len(jobs)
    new_count = 0
    skipped_count = 0
    
    # Score and insert each job
    for job in jobs:
        # Score the job
        ai_result = score_job(job.get("description_raw", ""), target_description)
        raw_score = ai_result.get("score", 0)

        try:
            score = float(raw_score)
        except (TypeError, ValueError):
            score = 0.0

        reasons = ai_result.get("reasons", "")
        if isinstance(reasons, list):
            reasons = "\n".join(f"- {r}" for r in reasons)
        elif not isinstance(reasons, str):
            reasons = str(reasons)

        summary = ai_result.get("summary", "")
        if isinstance(summary, list):
            summary = " ".join(summary)
        elif not isinstance(summary, str):
            summary = str(summary)
        
        # Add AI results to job dict
        job["ai_score"] = score
        job["ai_summary"] = summary
        job["ai_reasons"] = reasons
        
        # Try to insert (returns True if new, False if duplicate)
        if insert_job_if_new(job):
            new_count += 1
            # Find the newly inserted job by hash and update its AI results
            inserted_job = get_job_by_hash(job.get("hash"))
            if inserted_job:
                update_job_ai_results(inserted_job["id"], score, summary, reasons)
        else:
            skipped_count += 1
    
    return {
        "scraped": total_scraped,
        "new": new_count,
        "skipped": skipped_count
    }
