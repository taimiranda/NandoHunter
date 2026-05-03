"""Notification helpers for Discord and email alerts."""

import os
import smtplib
import ssl
from email.message import EmailMessage

import requests
from dotenv import load_dotenv

load_dotenv()

ALERT_SCORE_THRESHOLD = 7


def send_discord_alert(job: dict) -> None:
	"""Send Discord alert for high-scoring job matches."""
	score = job.get("ai_score") or 0
	try:
		score = float(score)
	except (TypeError, ValueError):
		score = 0

	if score < ALERT_SCORE_THRESHOLD:
		return

	webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
	if not webhook_url:
		print("Warning: DISCORD_WEBHOOK_URL not set. Skipping Discord alert.")
		return

	content = (
		f"🎯 **New Match: {job.get('title', 'Unknown Role')} at {job.get('company', 'Unknown Company')}**\n"
		f"Score: **{score}/10**\n"
		f"Location: {job.get('location', 'Unknown')}\n"
		f"Salary: {job.get('salary_raw') or 'Not listed'}\n"
		f"URL: {job.get('url', '')}"
	)

	try:
		response = requests.post(webhook_url, json={"content": content}, timeout=10)
		response.raise_for_status()
	except Exception as e:
		print(f"Discord alert failed: {e}")


def send_email_alert(job: dict) -> None:
	"""Send Gmail SMTP alert for high-scoring job matches."""
	score = job.get("ai_score") or 0
	try:
		score = float(score)
	except (TypeError, ValueError):
		score = 0

	if score < ALERT_SCORE_THRESHOLD:
		return

	email_from = os.getenv("EMAIL_FROM", "").strip()
	email_to = os.getenv("EMAIL_TO", "").strip()
	email_app_password = os.getenv("EMAIL_APP_PASSWORD", "").strip()

	if not email_from or not email_to or not email_app_password:
		print("Warning: Email env vars missing. Skipping email alert.")
		return

	subject = (
		f"🎯 New Match: {job.get('title', 'Unknown Role')} at "
		f"{job.get('company', 'Unknown Company')} — Score {score}/10"
	)
	body = f"""
New job match found by NandoHunting.

Role: {job.get('title', '')}
Company: {job.get('company', '')}
Location: {job.get('location', '')}
Score: {score}/10
Salary: {job.get('salary_raw', 'Not listed')}

Summary: {job.get('ai_summary', '')}

Why it matches:
{job.get('ai_reasons', '')}

View job: {job.get('url', '')}

---
Open NandoHunting at http://localhost:8501 to Accept or Reject.
"""

	message = EmailMessage()
	message["Subject"] = subject
	message["From"] = email_from
	message["To"] = email_to
	message.set_content(body)

	try:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(email_from, email_app_password)
			server.send_message(message)
	except Exception as e:
		print(f"Email alert failed: {e}")


def notify(job: dict) -> None:
	"""Send all configured notifications for a job."""
	send_discord_alert(job)
	send_email_alert(job)
