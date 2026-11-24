import os, smtplib
from email.message import EmailMessage
from datetime import date, timedelta
from database import list_tasks, employee_stats

def build_daily_report():
    tasks=list_tasks()
    today=date.today().isoformat()
    completed=[t for t in tasks if t["status"]=="Completed" and (t["completed_at"] or "")[:10]==today]
    progress=[t for t in tasks if t["status"]=="In Progress"]
    blocked=[t for t in tasks if t["status"]=="Blocked"]
    lines=[f"Autonomous SEO Agency — Daily Status ({today})","",
           f"Completed today: {len(completed)}",f"In progress: {len(progress)}",f"Blocked: {len(blocked)}","",
           "COMPLETED TODAY:"]
    lines += [f"- #{t['id']} {t['title']} ({t['agent_name']}) — {t['output_link'] or 'No output link recorded'}" for t in completed] or ["- None recorded"]
    lines += ["","IN PROGRESS:"] + [f"- #{t['id']} {t['title']} ({t['agent_name']})" for t in progress] or ["- None"]
    lines += ["","BLOCKED:"] + [f"- #{t['id']} {t['title']} ({t['agent_name']}) — {t['blocked_reason'] or 'Reason not recorded'}" for t in blocked] or ["- None"]
    lines += ["","EMPLOYEE KPIs (recorded task counts):"]
    for s in employee_stats():
        lines.append(f"- {s['Employee']}: {s['Completed']} completed; {s['Pending']} pending; average completion hours: {s['Average completion hours']}")
    return "\n".join(lines)


def send_daily_report():
    import os
    import json
    import urllib.request

    try:
        import streamlit as st
        script_url = st.secrets["APPS_SCRIPT_URL"]
        shared_secret = st.secrets["APPS_SCRIPT_SECRET"]
    except Exception:
        script_url = os.getenv("APPS_SCRIPT_URL")
        shared_secret = os.getenv("APPS_SCRIPT_SECRET")

    if not script_url or not shared_secret:
        raise RuntimeError("Apps Script URL or Shared Secret is missing.")

    payload = {
        "token": shared_secret,
        "action": "sendEmail",
        "subject": f"SEO Agency Daily Status — {date.today().isoformat()}",
        "body": build_daily_report()
    }

    request = urllib.request.Request(
        script_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("success"):
        raise RuntimeError(result.get("error", "Email sending failed."))

    return result
