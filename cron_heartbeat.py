from dotenv import load_dotenv
load_dotenv()

import datetime
import os


PROJECT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT, "logs")
HEARTBEAT_LOG = os.path.join(LOG_DIR, "cron_heartbeat.log")
LAST_RUN_FILE = os.path.join(LOG_DIR, "cron_last_run.txt")


def main() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    now = datetime.datetime.now().isoformat()

    with open(HEARTBEAT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} heartbeat\n")

    with open(LAST_RUN_FILE, "w", encoding="utf-8") as f:
        f.write(now)

    print(f"Heartbeat recorded: {now}")


if __name__ == "__main__":
    main()
