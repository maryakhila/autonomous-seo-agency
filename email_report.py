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
    required=["SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASSWORD","BOSS_EMAIL"]
    missing=[k for k in required if not os.getenv(k)]
    # Streamlit secrets are exposed as environment variables only if configured in hosting environment.
    if missing:
        try:
            import streamlit as st
            cfg={k:st.secrets[k] for k in required}
        except Exception as e:
            raise RuntimeError("Configure SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD and BOSS_EMAIL in Streamlit Secrets.") from e
    else: cfg={k:os.getenv(k) for k in required}
    msg=EmailMessage()
    msg["Subject"]=f"SEO Agency Daily Status — {date.today().isoformat()}"
    msg["From"]=cfg["SMTP_USER"]; msg["To"]=cfg["BOSS_EMAIL"]
    msg.set_content(build_daily_report())
    with smtplib.SMTP(cfg["SMTP_HOST"], int(cfg["SMTP_PORT"])) as server:
        server.starttls()
        server.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
        server.send_message(msg)
