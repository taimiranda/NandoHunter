"""Streamlit frontend for Nando the Hunter career agent."""

import base64
import hashlib
import os
from pathlib import Path

import requests
import streamlit as st


def check_password():
    app_password = os.getenv("APP_PASSWORD", "hunter2026")

    if st.session_state.get("authenticated"):
        return

    st.markdown(
        """
    <div style="display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:60vh;">
        <div style="font-family:Georgia,serif; font-size:2em;
                    color:#c9952a; letter-spacing:3px; margin-bottom:8px;">
            🎯 NANDO THE HUNTER
        </div>
        <div style="color:#7a6840; font-family:Georgia,serif;
                    letter-spacing:2px; margin-bottom:32px;">
            ⚔ Track. Hunt. Land. ⚔
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    pwd = st.text_input(
        "Enter password",
        type="password",
        key="login_input",
        placeholder="Enter the hunter's password...",
    )

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        login_btn = st.button("🗝 Enter", use_container_width=True)

    if login_btn:
        entered_hash = hashlib.sha256(pwd.encode()).hexdigest()
        correct_hash = hashlib.sha256(app_password.encode()).hexdigest()
        if entered_hash == correct_hash:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Wrong password. The gates remain closed.")

    st.stop()


check_password()

st.set_page_config(
    page_title="Nando the Hunter",
    page_icon="assets/nando_portrait.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

:root {
    --background: oklch(0.22 0.03 140);
    --foreground: oklch(0.95 0.04 90);
    --card: oklch(0.28 0.04 60);
    --primary: oklch(0.65 0.16 145);
    --primary-foreground: oklch(0.18 0.02 140);
    --secondary: oklch(0.42 0.08 50);
    --secondary-foreground: oklch(0.95 0.04 90);
    --muted-foreground: oklch(0.78 0.04 90);
    --accent: oklch(0.78 0.17 75);
    --accent-foreground: oklch(0.18 0.02 140);
    --destructive: oklch(0.62 0.22 25);
    --border: oklch(0.42 0.05 60);
    --input: oklch(0.32 0.04 60);
    --hp: oklch(0.62 0.22 25);
    --mp: oklch(0.62 0.18 245);
    --gold: oklch(0.82 0.17 85);
}

* {
    image-rendering: pixelated;
    border-color: var(--border);
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"],
.main .block-container {
    background-color: var(--background) !important;
    color: var(--foreground) !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse at top, oklch(0.32 0.06 140) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent 0 3px, oklch(0 0 0 / 0.06) 3px 4px) !important;
}

.main .block-container {
    max-width: 1280px;
    padding-top: 0.8rem;
}

h1,
h2,
h3,
.pixel,
.stButton button,
[data-testid="stLinkButton"] a,
.stRadio p {
    font-family: 'Press Start 2P', monospace !important;
}

body,
p,
li,
td,
.stMarkdown,
[data-testid="stMarkdownContainer"],
.stTextInput input,
.stTextArea textarea {
    font-family: 'VT323', monospace !important;
    font-size: 1.5rem !important;
}

.st-emotion-cache-1ab9dzl {
    gap: 0 !important;
}

p,
li {
    color: var(--foreground);
}

.stRadio [role="radiogroup"] {
    gap: 0.45rem;
    width: 100%;
}

.stRadio [role="radiogroup"] label {
    border: 2px solid var(--border);
    background: linear-gradient(180deg, var(--card) 0%, oklch(0.24 0.04 60) 100%);
    border-radius: 0;
    padding: 0.55rem 0.65rem;
    width: 100% !important;
    display: flex !important;
}

.stRadio [role="radiogroup"] p {
    font-size: 0.9rem !important;
    color: var(--muted-foreground) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, var(--card) 0%, oklch(0.24 0.04 60) 100%) !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: inset 0 0 0 1px oklch(1 0 0 / 0.05), 0 4px 0 0 oklch(0 0 0 / 0.4) !important;
}

.stButton > button,
[data-testid="stLinkButton"] > a {
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    font-size: 0.95rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    width: 100%;
}

.stButton > button {
    background: var(--secondary) !important;
    color: var(--secondary-foreground) !important;
    padding: 0.75rem 1rem !important;
}

.stButton > button[kind="primary"] {
    background: var(--primary) !important;
    color: var(--primary-foreground) !important;
}

.stButton > button:hover,
[data-testid="stLinkButton"] > a:hover {
    background: var(--accent) !important;
    color: var(--accent-foreground) !important;
}

[data-testid="stLinkButton"] > a {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    background: var(--gold) !important;
    color: oklch(0.18 0.02 140) !important;
    padding: 0.65rem 0.9rem !important;
}

.tier-legendary {
    color: var(--accent) !important;
    font-weight: bold;
}

.tier-rare {
    color: var(--primary) !important;
    font-weight: bold;
}

.tier-common {
    color: var(--muted-foreground) !important;
    font-weight: bold;
}

.score-high {
    color: #22c55e !important;
}

.score-mid {
    color: #eab308 !important;
}

.score-low {
    color: #ef4444 !important;
}

.stTextArea textarea,
.stTextInput input {
    background-color: var(--input) !important;
    color: var(--foreground) !important;
    border: none !important;
    border-radius: 0 !important;
}

/* Remove default box/border around expander details */
[data-testid="stExpander"] {
    border: 2px solid var(--border) !important;
    background: var(--input) !important;
    box-shadow: inset 0 0 0 1px oklch(1 0 0 / 0.05) !important;
}

[data-testid="stExpanderDetails"] {
    border-top: 1px dashed var(--border) !important;
    background: var(--card) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

for key, value in {
    "new_jobs": [],
    "accepted_jobs": [],
    "rejected_jobs": [],
    "profile": {"master_resume": "", "target_description": ""},
    "accepted_previews": {},
    "show_low_scores": False,
    "active_view": "QUESTS",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def fetch_jobs(status: str) -> list:
    try:
        response = requests.get(f"{API_BASE}/jobs?status={status}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching jobs: {e}")
        return []


def fetch_profile() -> dict:
    try:
        response = requests.get(f"{API_BASE}/profile", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching profile: {e}")
        return {"master_resume": "", "target_description": ""}


def trigger_scraper():
    try:
        response = requests.post(f"{API_BASE}/scrape", timeout=180)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error triggering scraper: {e}")
        return None


def accept_job(job_id: int) -> dict | None:
    try:
        response = requests.post(f"{API_BASE}/jobs/{job_id}/accept", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error accepting job: {e}")
        return None


def reject_job(job_id: int) -> bool:
    try:
        response = requests.post(f"{API_BASE}/jobs/{job_id}/reject", timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error rejecting job: {e}")
        return False


def reopen_job(job_id: int) -> bool:
    try:
        response = requests.post(f"{API_BASE}/jobs/{job_id}/reopen", timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error moving job to inbox: {e}")
        return False


def save_profile(master_resume: str, target_description: str) -> bool:
    try:
        response = requests.post(
            f"{API_BASE}/profile",
            json={"master_resume": master_resume, "target_description": target_description},
            timeout=10,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error saving profile: {e}")
        return False


def refresh_jobs_in_state(state_key: str, status: str) -> None:
    jobs = fetch_jobs(status)
    if status == "new":
        jobs = sorted(jobs, key=lambda x: (x.get("ai_score") or 0), reverse=True)
    st.session_state[state_key] = jobs


def get_tier(score) -> tuple[str, str]:
    score = score or 0
    if score >= 8:
        return "LEGENDARY", "tier-legendary"
    if score >= 5:
        return "RARE", "tier-rare"
    return "COMMON", "tier-common"


def render_hunter_hud(hp: int = 78, xp: int = 62, level: int = 7, quests: int = 0) -> None:
    portrait_path = Path("assets/nando_portrait.png")
    if portrait_path.exists():
        img_b64 = base64.b64encode(portrait_path.read_bytes()).decode()
        avatar = f'<img src="data:image/png;base64,{img_b64}" style="width:72px;height:72px;border:2px solid var(--border);object-fit:cover;" />'
    else:
        avatar = '<div style="width:72px;height:72px;border:2px solid var(--border);background:var(--input);"></div>'

    st.markdown(
        f"""
<div style="display:flex;align-items:center;gap:14px;">
  {avatar}
  <div style="flex:1;min-width:0;">
        <div style="font-size:0.7rem;color:var(--accent);margin-bottom:6px;">NANDO</div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
      <span style="font-size:0.48rem;width:20px;color:var(--muted-foreground);">HP</span>
      <div style="flex:1;height:10px;border:2px solid var(--border);background:var(--input);"><div style="height:100%;width:{max(0, min(100, hp))}%;background:var(--hp);"></div></div>
    </div>
    <div style="font-size:0.48rem;color:var(--muted-foreground);">QUESTS <span style="color:var(--gold);">◆ {quests}</span></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_job_card(job: dict) -> None:
    score = float(job.get("ai_score") or 0)
    tier_label, tier_class = get_tier(score)
    if score >= 8:
        score_class = "score-high"
    elif score >= 5:
        score_class = "score-mid"
    else:
        score_class = "score-low"

    st.markdown(
        f"""
<div style="font-family: Arial, Verdana, sans-serif;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem;">
  <span class="{tier_class}" style="font-size:0.56rem;">★ {tier_label}</span>
    <span class="{score_class}" style="font-size:1.35rem;font-weight:bold;">{score:.1f}/10</span>
</div>
<div style="font-size:1.75rem;font-weight:700;color:var(--foreground);margin:0.25rem 0 0.35rem 0;">{job.get('title', 'Untitled')}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div style='font-family: Arial, Verdana, sans-serif; font-size:1.08rem; color:var(--muted-foreground);'><strong>⚒ {job.get('company', 'Unknown')}</strong></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div style="background:var(--input);border:2px solid var(--border);height:8px;margin:0.45rem 0 0.65rem 0;">
  <div style="background:var(--gold);height:100%;width:{min(100.0, score * 10)}%;"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    if job.get("ai_summary"):
        st.markdown(f"<div style='font-family: Arial, Verdana, sans-serif;'><em>{job.get('ai_summary')}</em></div>", unsafe_allow_html=True)

    if job.get("ai_reasons"):
        reasons = str(job.get("ai_reasons") or "")
        lines = [ln.strip().lstrip("- ").strip() for ln in reasons.splitlines() if ln.strip()]
        reasons_html = "<br>".join(lines) if lines else reasons
        with st.expander("MATCH DETAILS", expanded=False):
            st.markdown(
                f"<div style='font-family: Arial, Verdana, sans-serif; font-size:0.92rem; line-height:1.25; background:transparent; margin:0; padding:0;'>{reasons_html}</div>",
                unsafe_allow_html=True,
            )


def _render_preview_content(job_id: int, payload: dict) -> None:
    company = payload.get("company", "company")
    resume_docx_url = f"{API_BASE}/jobs/{job_id}/resume.docx"
    cover_docx_url = f"{API_BASE}/jobs/{job_id}/cover.docx"

    st.markdown(
        f"""
<div style="font-family: Arial, Verdana, sans-serif; margin-bottom: 10px;">
  <div style="font-size: 0.9rem; letter-spacing: 1px; color: var(--accent);">ACCEPTED</div>
  <div style="font-size: 1.45rem; font-weight: 700; color: var(--foreground);">{payload.get('title', '')}</div>
  <div style="font-size: 1.0rem; color: var(--muted-foreground);">{company}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Resume (.docx)", resume_docx_url)
    with col2:
        st.link_button("Cover (.docx)", cover_docx_url)


def render_post_accept_modal(job_id: int, payload: dict) -> None:
    if hasattr(st, "dialog"):
        @st.dialog(f"Accepted Job {job_id}")
        def _show_dialog():
            _render_preview_content(job_id, payload)
            if st.button("Close", key=f"close_modal_{job_id}"):
                st.session_state[f"show_modal_{job_id}"] = False
                st.rerun()

        _show_dialog()
        return

    # Fallback for older Streamlit: render as internal panel instead of expander.
    st.markdown("### Quest Files")
    _render_preview_content(job_id, payload)
    if st.button("Close", key=f"close_panel_{job_id}"):
        st.session_state[f"show_modal_{job_id}"] = False
        st.rerun()


st.markdown(
    """
<div style="text-align:center;margin-bottom:1rem;">
    <p style="font-size:0.85rem;color:var(--accent);letter-spacing:2px;margin-top:50px;">EST. MMXXVI</p>
    <h1 style="font-size:3.2rem;color:var(--foreground);margin:0.55rem 0;line-height:1.1;">NANDO <span style="color:var(--primary);">THE HUNTER</span></h1>
    <p style="font-size:0.8rem;color:var(--muted-foreground);">— QUEST BOARD —</p>
</div>
""",
    unsafe_allow_html=True,
)

shell_left, shell_right = st.columns([1.1, 4.0], gap="large")

with shell_left:
    with st.container(border=True):
        st.markdown("<div style='text-align:center;font-size:0.76rem;color:var(--accent);margin-bottom:10px;'>✦ MENU ✦</div>", unsafe_allow_html=True)
        if "left_menu_radio" not in st.session_state:
            st.session_state["left_menu_radio"] = st.session_state["active_view"]

        st.radio(
            "Menu",
            ["QUESTS", "JOURNAL", "GEAR"],
            label_visibility="collapsed",
            key="left_menu_radio",
        )
        st.session_state["active_view"] = st.session_state["left_menu_radio"]

active_view = st.session_state["active_view"]

with shell_right:
    if active_view == "QUESTS":
        if not st.session_state["new_jobs"]:
            refresh_jobs_in_state("new_jobs", "new")

        with st.container(border=True):
            if st.button("▶ HUNT", key="run_scraper", use_container_width=True, type="primary"):
                with st.spinner("Hunting new quests..."):
                    result = trigger_scraper()
                    if result:
                        st.success(
                            f"Scraped {result.get('scraped', 0)} jobs - {result.get('new', 0)} new, {result.get('skipped', 0)} duplicates"
                        )
                        refresh_jobs_in_state("new_jobs", "new")
                        st.rerun()
            show_low = st.checkbox("Show low-tier (below 5)", value=st.session_state["show_low_scores"], key="show_low_scores")

        jobs = sorted(st.session_state["new_jobs"], key=lambda x: (x.get("ai_score") or 0), reverse=True)
        display_jobs = jobs if show_low else [j for j in jobs if (j.get("ai_score") or 0) >= 5]

        active_preview_ids = [pid for pid in st.session_state["accepted_previews"] if st.session_state.get(f"show_modal_{pid}", False)]
        if active_preview_ids:
            selected_id = active_preview_ids[0]
            with st.container(border=True):
                render_post_accept_modal(int(selected_id), st.session_state["accepted_previews"].get(selected_id, {}))

        if jobs and not display_jobs:
            st.info("All matches are below 5. Enable low-tier to view them.")

        for job in display_jobs:
            with st.container(border=True):
                render_job_card(job)
                a1, a2, a3 = st.columns([1, 1, 1])
                with a1:
                    if st.button("⚔ ACCEPT", key=f"accept_{job.get('id')}", use_container_width=True):
                        result = accept_job(job.get("id"))
                        if result:
                            job_id = job.get("id")
                            st.session_state[f"show_modal_{job_id}"] = True
                            st.session_state["accepted_previews"][str(job_id)] = {
                                "title": job.get("title", ""),
                                "company": job.get("company", ""),
                                "resume_md": result.get("resume_md", ""),
                                "cover_letter_md": result.get("cover_letter_md", ""),
                            }
                            st.session_state["new_jobs"] = [j for j in st.session_state["new_jobs"] if j.get("id") != job.get("id")]
                            st.session_state["accepted_jobs"] = []
                            st.rerun()
                with a2:
                    if st.button("❌ REJECT", key=f"reject_{job.get('id')}", use_container_width=True):
                        if reject_job(job.get("id")):
                            st.session_state["new_jobs"] = [j for j in st.session_state["new_jobs"] if j.get("id") != job.get("id")]
                            st.rerun()
                with a3:
                    if job.get("url"):
                        st.link_button("✦ VIEW QUEST", job.get("url"), use_container_width=True)

    elif active_view == "JOURNAL":
        if not st.session_state["accepted_jobs"]:
            st.session_state["accepted_jobs"] = fetch_jobs("accepted")
        if not st.session_state["rejected_jobs"]:
            st.session_state["rejected_jobs"] = fetch_jobs("rejected")

        entries = [{**j, "entry_type": "accepted"} for j in st.session_state["accepted_jobs"]] + [{**j, "entry_type": "rejected"} for j in st.session_state["rejected_jobs"]]

        for job in entries:
            with st.container(border=True):
                render_job_card(job)
                if job.get("entry_type") == "accepted":
                    d1, d2, d3, d4 = st.columns(4)
                    with d1:
                        st.link_button("Resume (.docx)", f"{API_BASE}/jobs/{job.get('id')}/resume.docx", use_container_width=True)
                    with d2:
                        st.link_button("Cover (.docx)", f"{API_BASE}/jobs/{job.get('id')}/cover.docx", use_container_width=True)
                    with d3:
                        if st.button("↩ REOPEN", key=f"reopen_{job.get('id')}", use_container_width=True):
                            if reopen_job(job.get("id")):
                                st.session_state["accepted_jobs"] = [x for x in st.session_state["accepted_jobs"] if x.get("id") != job.get("id")]
                                st.session_state["rejected_jobs"] = [x for x in st.session_state["rejected_jobs"] if x.get("id") != job.get("id")]
                                st.session_state["new_jobs"] = []
                                st.rerun()
                    with d4:
                        if job.get("url"):
                            st.link_button("✦ VIEW QUEST", job.get("url"), use_container_width=True)
                else:
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("↩ REOPEN", key=f"reopen_{job.get('id')}", use_container_width=True):
                            if reopen_job(job.get("id")):
                                st.session_state["accepted_jobs"] = [x for x in st.session_state["accepted_jobs"] if x.get("id") != job.get("id")]
                                st.session_state["rejected_jobs"] = [x for x in st.session_state["rejected_jobs"] if x.get("id") != job.get("id")]
                                st.session_state["new_jobs"] = []
                                st.rerun()
                    with b2:
                        if job.get("url"):
                            st.link_button("✦ VIEW QUEST", job.get("url"), use_container_width=True)

    else:
        if st.session_state["profile"] == {"master_resume": "", "target_description": ""}:
            st.session_state["profile"] = fetch_profile()

        with st.container(border=True):
            st.markdown("<div style='text-align:center;font-size:0.66rem;color:var(--accent);'>⚙ HUNTER'S GEAR</div>", unsafe_allow_html=True)
            st.markdown("Configure your combat profile and hunting parameters.")

        with st.container(border=True):
            st.markdown("**📜 ADVENTURER'S CHRONICLE**")
            resume = st.text_area("Master Resume", value=st.session_state["profile"].get("master_resume", ""), height=230, key="input_resume")

        with st.container(border=True):
            st.markdown("**🎯 HUNTING PARAMETERS**")
            target = st.text_area("Target Profile", value=st.session_state["profile"].get("target_description", ""), height=160, key="input_target")

        if st.button("💾 SAVE GEAR", key="save_profile", use_container_width=True):
            if save_profile(resume, target):
                st.session_state["profile"] = {"master_resume": resume, "target_description": target}
                st.success("Gear saved.")
