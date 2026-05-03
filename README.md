# NandoHunting - Local-First AI Personal Career Agent

Automatically scrapes job listings from Indeed and Google Jobs twice daily, scores them against your career profile using GPT-4o-mini, and presents a simple UI to accept/reject matches. Accepted jobs trigger tailored resume bullet generation. High-score matches (≥8) send Discord alerts.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key and Discord webhook
```

## Architecture

- **scraper.py** — Playwright job board scraper with deduplication
- **database.py** — SQLite jobs and profile storage
- **ai.py** — GPT-4o scoring and bullet generation
- **main.py** — FastAPI REST backend
- **app.py** — Streamlit UI (Inbox, History, Settings)
- **resume_builder.py** — python-docx .docx generation
- **notifications.py** — Discord webhook alerts
- **run_scrape.py** — Scheduled scraper runner (Cron/Task Scheduler)

## Usage

Start backend:
```bash
uvicorn main:app --reload
```

Start frontend:
```bash
streamlit run app.py
```

Schedule scraper (Cron):
```
0 9,17 * * * cd /path/to/NandoHunting && python run_scrape.py
```
