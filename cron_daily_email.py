from dotenv import load_dotenv
load_dotenv()

import datetime
import os
import smtplib
import ssl
from email.message import EmailMessage


PROJECT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT, "logs")
HEARTBEAT_LOG = os.path.join(LOG_DIR, "cron_heartbeat.log")
TARGET_EMAIL = "eu@tainamiranda.com.br"


def read_heartbeat_last_24h() -> tuple[int, str]:
    if not os.path.exists(HEARTBEAT_LOG):
        return 0, "No heartbeat file found yet."

    cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
    count = 0
    last_seen = "No runs detected in last 24h."

    with open(HEARTBEAT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ts = line.split(" ")[0]
            try:
                dt = datetime.datetime.fromisoformat(ts)
            except ValueError:
                continue
            if dt >= cutoff:
                count += 1
                last_seen = ts

    return count, last_seen


def send_daily_health_email() -> None:
    email_from = os.getenv("EMAIL_FROM", "").strip()
    email_password = os.getenv("EMAIL_APP_PASSWORD", "").strip()

    if not email_from or not email_password:
        print("Missing EMAIL_FROM or EMAIL_APP_PASSWORD. Skipping daily cron email.")
        return

    count_24h, last_seen = read_heartbeat_last_24h()

    subject = f"NandoHunting Cron Daily Check - {datetime.date.today().isoformat()}"
    body = f"""
Daily cron status report for NandoHunting.

Expected heartbeat frequency: once per hour.
Heartbeats detected in last 24 hours: {count_24h}
Last heartbeat timestamp: {last_seen}

Project path: {PROJECT}
Heartbeat log: {HEARTBEAT_LOG}

If the heartbeat count is much lower than expected, verify crontab and system cron service.
"""

    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = TARGET_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_from, email_password)
            server.send_message(msg)
        print(f"Daily cron email sent to {TARGET_EMAIL}")
    except Exception as e:
        print(f"Daily cron email failed: {e}")


if __name__ == "__main__":
    os.makedirs(LOG_DIR, exist_ok=True)
    send_daily_health_email()
