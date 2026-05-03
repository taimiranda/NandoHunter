"""
AI layer for NandoHunting career agent.
Uses OpenAI SDK v1+ for job scoring and resume bullet generation.
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables before initializing client
load_dotenv()

# Initialize client once at module level
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def score_job(job_description: str, target_profile: str) -> dict:
    """
    Score a job listing against target profile using GPT-4o-mini.
    
    Args:
        job_description: Full job description text
        target_profile: User's target career description / profile
    
    Returns:
        Dict with keys: score (1-10), summary (2 sentence max), reasons (bullet points)
        On error: {"score": 0, "summary": "Error message", "reasons": ""}
    """
    system_prompt = (
        "You are a career advisor. Evaluate job fit strictly and honestly. "
        "Respond ONLY with valid JSON. No markdown, no explanation outside the JSON."
    )
    
    user_prompt = (
        f"Target profile:\n{target_profile}\n\n"
        f"Job description:\n{job_description}\n\n"
        'Respond with this exact JSON structure: '
        '{"score": <integer 1-10>, "summary": "<2 sentence max>", '
        '"reasons": "<bullet points of match/mismatch>"}'
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        result = json.loads(response_text)
        return result
    
    except json.JSONDecodeError:
        print(f"Warning: JSON parse error in score_job response: {response_text}")
        return {"score": 0, "summary": "Parse error", "reasons": ""}
    except Exception as e:
        print(f"Warning: API error in score_job: {e}")
        return {"score": 0, "summary": "API error", "reasons": str(e)}


def generate_full_resume(
    job_description: str,
    master_resume: str,
    job_title: str,
    company: str,
) -> str:
    """Generate a full ATS-optimized tailored resume in markdown."""
    system_prompt = (
        "You are an expert resume writer. You produce complete, ATS-optimized "
        "resumes in clean markdown. Never invent experience. Never add "
        "placeholders. Output only the resume content, nothing else. "
        "Use only facts already present in the candidate resume. If a metric, "
        "tool, title, responsibility, or project is not explicitly present in "
        "the master resume, do not add it."
    )
    
    user_prompt = (
        "Rewrite the candidate's full resume tailored for this specific job.\n\n"
        f"Job title: {job_title}\n"
        f"Company: {company}\n"
        "Job description:\n"
        f"{job_description}\n\n"
        "Candidate's current resume:\n"
        f"{master_resume}\n\n"
        "Instructions:\n"
        "1. Keep the exact same structure as the candidate's resume:\n"
        "   contact info, professional summary, core skills, professional\n"
        "   experience, additional experience, education\n"
        "2. Rewrite the Professional Summary (3-4 sentences) to directly\n"
        "   address this role and company\n"
        "3. Reorder and rewrite Core Skills to mirror the job's language\n"
        "   and requirements - do not add skills the candidate does not have\n"
        "4. For each role in Professional Experience, rewrite bullet points\n"
        "   to emphasize the most relevant responsibilities and achievements\n"
        "   for this specific job - keep all roles, do not remove any\n"
        "5. Keep Additional Experience and Education unchanged\n"
        "6. Use strong action verbs and include measurable results where\n"
        "   the original resume supports them\n"
        "7. Mirror keywords from the job description naturally - do not\n"
        "   keyword-stuff\n"
        "8. Output clean markdown:\n"
        "   # Name\n"
        "   contact line\n"
        "   ## Professional Summary\n"
        "   ## Core Skills\n"
        "   ## Professional Experience\n"
        "   ### Role - Company (dates)\n"
        "   - bullet\n"
        "   ## Additional Experience\n"
        "   ## Education\n"
        "9. Do not add any note, explanation, or preamble before or after\n"
        "   the resume\n"
        "10. HARD CONSTRAINT: do not invent any experience, numbers, tools,\n"
        "    achievements, dates, employers, or certifications not already in\n"
        "    the provided master resume"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Warning: API error in generate_full_resume: {e}")
        return f"Error generating resume: {str(e)}"


def generate_cover_letter(
    job_description: str,
    master_resume: str,
    job_title: str,
    company: str,
) -> str:
    """Generate a concise tailored cover letter using GPT-4o."""
    system_prompt = (
        "You are an expert career coach writing cover letters. "
        "Output only the cover letter, no preamble."
    )

    user_prompt = (
        "Write a concise, professional cover letter for this job.\n"
        f"Job title: {job_title} at {company}\n"
        f"Job description: {job_description}\n"
        f"My background: {master_resume}\n"
        "Rules:\n"
        "- 3 paragraphs max\n"
        "- First paragraph: why this specific role and company\n"
        "- Second paragraph: 2-3 most relevant experiences\n"
        "- Third paragraph: brief close with availability\n"
        "- Plain text, no placeholders like [Your Name]\n"
        "- Sign off as Fernando Almeida"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Warning: API error in generate_cover_letter: {e}")
        return f"Error generating cover letter: {str(e)}"


if __name__ == "__main__":
    # Test score_job with dummy data
    dummy_profile = (
        "Senior Python engineer with 5+ years of backend experience. "
        "Interested in ML/AI roles, distributed systems, and startup environments. "
        "Looking for remote or SF Bay Area positions with strong technical teams."
    )
    
    dummy_job = (
        "Job Title: Senior Backend Engineer\n\n"
        "We're looking for a Senior Backend Engineer to join our AI platform team. "
        "You'll work with Python, PostgreSQL, and Kubernetes. "
        "Requirements: 5+ years Python, experience with distributed systems, "
        "knowledge of LLMs a plus. Remote-friendly, San Francisco HQ."
    )
    
    result = score_job(dummy_job, dummy_profile)
    print("Score result:")
    print(json.dumps(result, indent=2))
