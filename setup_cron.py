import subprocess, sys, os

PYTHON = sys.executable  # full path to venv python
PROJECT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(PROJECT, "logs", "scrape.log")

# Run at 8:00 AM and 6:00 PM every day
CRON_LINE = f"0 8,18 * * * cd {PROJECT} && {PYTHON} run_scrape.py >> {LOG} 2>&1"


def install():
    # Get existing crontab
    result = subprocess.run(["crontab", "-l"],
                            capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    if CRON_LINE in existing:
        print("Cron job already installed.")
        return

    # Create logs dir
    os.makedirs(os.path.join(PROJECT, "logs"), exist_ok=True)

    # Append new line
    new_crontab = existing.rstrip("\n") + "\n" + CRON_LINE + "\n"
    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True)

    if proc.returncode == 0:
        print(f"Cron installed successfully.")
        print(f"Runs at 8:00 AM and 6:00 PM daily.")
        print(f"Logs: {LOG}")
        print(f"\nTo verify: crontab -l")
        print(f"To remove: crontab -e (then delete the line)")
    else:
        print("Failed to install cron. Try manually:")
        print(f"  crontab -e")
        print(f"  Add this line:")
        print(f"  {CRON_LINE}")


if __name__ == "__main__":
    install()
