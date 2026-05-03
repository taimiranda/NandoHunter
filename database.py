"""
SQLite database layer for NandoHunting career agent.
No ORM, no SQLAlchemy — pure sqlite3 with context managers.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = os.getenv("DATABASE_PATH", "./jobs.db")
JOB_SELECT_COLUMNS = (
    "id, hash, title, company, location, salary_raw, remote, url, "
    "description_raw, ai_score, ai_summary, ai_reasons, resume_md, "
    "cover_letter_md, status, scraped_at, reviewed_at"
)


def init_db() -> None:
    """Create jobs and profile tables if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Create jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                salary_raw TEXT,
                remote INTEGER DEFAULT 0,
                url TEXT NOT NULL,
                description_raw TEXT,
                ai_score REAL,
                ai_summary TEXT,
                ai_reasons TEXT,
                resume_md TEXT,
                cover_letter_md TEXT,
                resume_docx BLOB,
                cover_letter_docx BLOB,
                status TEXT DEFAULT 'new',
                scraped_at TEXT,
                reviewed_at TEXT
            )
        """)

        # Lightweight migrations for existing DBs.
        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN resume_md TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN cover_letter_md TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN resume_docx BLOB")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN cover_letter_docx BLOB")
        except sqlite3.OperationalError:
            pass
        
        # Create profile table (single row, id=1)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY,
                master_resume TEXT,
                target_description TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()


def insert_job_if_new(job: dict) -> bool:
    """
    Insert job using INSERT OR IGNORE (keyed on hash).
    
    Args:
        job: dict with keys: hash, title, company, location, salary_raw, remote, url, description_raw, scraped_at
    
    Returns:
        True if inserted, False if already existed.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO jobs (hash, title, company, location, salary_raw, remote, url, description_raw, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.get("hash"),
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("salary_raw"),
                job.get("remote", 0),
                job.get("url"),
                job.get("description_raw"),
                job.get("scraped_at", datetime.now().isoformat())
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # Hash already exists
            return False


def update_job_status(job_id: int, status: str, reviewed_at: str = None) -> None:
    """
    Update job status and reviewed_at timestamp.
    
    Args:
        job_id: job id
        status: 'new', 'accepted', or 'rejected'
        reviewed_at: ISO 8601 timestamp (defaults to now)
    """
    if reviewed_at is None:
        reviewed_at = datetime.now().isoformat()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE jobs
            SET status = ?, reviewed_at = ?
            WHERE id = ?
        """, (status, reviewed_at, job_id))
        conn.commit()


def update_job_ai_results(job_id: int, score: float, summary: str, reasons: str) -> None:
    """
    Update job with AI scoring and analysis results.
    
    Args:
        job_id: job id
        score: 1-10 score from GPT-4o-mini
        summary: brief summary of match
        reasons: explanation of score
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE jobs
            SET ai_score = ?, ai_summary = ?, ai_reasons = ?
            WHERE id = ?
        """, (score, summary, reasons, job_id))
        conn.commit()


def save_generated_docs(
    job_id: int,
    resume_md: str,
    cover_letter_md: str,
    resume_docx_bytes: bytes,
    cover_letter_docx_bytes: bytes,
) -> None:
    """Store generated markdown and docx content for resume and cover letter."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE jobs
            SET resume_md = ?,
                cover_letter_md = ?,
                resume_docx = ?,
                cover_letter_docx = ?
            WHERE id = ?
            """,
            (resume_md, cover_letter_md, resume_docx_bytes, cover_letter_docx_bytes, job_id),
        )
        conn.commit()


def get_jobs_by_status(status: str) -> list[dict]:
    """
    Get all jobs with given status.
    
    Args:
        status: 'new', 'accepted', or 'rejected'
    
    Returns:
        List of job dicts.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                id, hash, title, company, location, salary_raw, remote, url,
                description_raw, ai_score, ai_summary, ai_reasons, resume_md,
                cover_letter_md, status, scraped_at, reviewed_at
            FROM jobs
            WHERE status = ?
            ORDER BY scraped_at DESC
        """, (status,))
        return [dict(row) for row in cursor.fetchall()]


def get_job_by_id(job_id: int) -> dict | None:
    """
    Get single job by id.
    
    Args:
        job_id: job id
    
    Returns:
        Job dict or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {JOB_SELECT_COLUMNS} FROM jobs WHERE id = ?",
            (job_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_job_by_hash(job_hash: str) -> dict | None:
    """
    Get single job by hash.
    
    Args:
        job_hash: SHA256 hash of company+title+url
    
    Returns:
        Job dict or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {JOB_SELECT_COLUMNS} FROM jobs WHERE hash = ?",
            (job_hash,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_job_docx_bytes(job_id: int) -> dict | None:
    """Fetch stored docx blobs for a job."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT resume_docx, cover_letter_docx FROM jobs WHERE id = ?",
            (job_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_profile() -> dict | None:
    """
    Get user profile (single row, id=1).
    
    Returns:
        Profile dict or None if not set.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profile WHERE id = 1")
        row = cursor.fetchone()
        return dict(row) if row else None


def save_profile(master_resume: str, target_description: str) -> None:
    """
    Upsert profile at id=1.
    
    Args:
        master_resume: full resume text
        target_description: target job description / career goals
    """
    updated_at = datetime.now().isoformat()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO profile (id, master_resume, target_description, updated_at)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                master_resume = excluded.master_resume,
                target_description = excluded.target_description,
                updated_at = excluded.updated_at
        """, (master_resume, target_description, updated_at))
        conn.commit()


if __name__ == "__main__":
    init_db()
    print("DB initialized.")
