
import os
import sqlite3
from datetime import datetime, timezone, date

DB_PATH = os.getenv("SQLITE_PATH", "agency.db")

STATUSES = ("Queued", "In Progress", "Blocked", "Completed")

EMPLOYEE_ROLES = {
    "Lead Generator Agent": "Sales and acquisition; prospect research and SEO gap scoring",
    "Project Manager & Proposal Agent": "Project coordination, proposals and client onboarding",
    "Agency Web Developer Agent": "Agency website maintenance and development",
    "SEO Specialist / Coordinator Agent": "Keyword mapping and on-page SEO",
    "Technical SEO Agent": "Technical SEO audits and website health",
    "SEO Content Strategist & Writer Agent": "SEO content strategy and content creation",
    "Link Building & Digital PR Agent": "Ethical backlink research and digital PR",
    "AEO / GEO & Local SEO Agent": "AI search visibility and local SEO",
}


def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                assigned_by TEXT NOT NULL,
                deadline TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT,
                output_link TEXT,
                blocked_reason TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                speaker TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def create_task(title, description, agent_name, priority, deadline=None, assigned_by="Boss"):
    if agent_name not in EMPLOYEE_ROLES:
        raise ValueError(f"Unknown employee: {agent_name}")

    stamp = now()

    with connect() as c:
        cur = c.execute("""
            INSERT INTO tasks
            (title, description, agent_name, priority, status,
             assigned_by, deadline, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, agent_name, priority,
            "Queued", assigned_by, deadline, stamp, stamp
        ))

        return cur.lastrowid


def get_task(task_id):
    with connect() as c:
        row = c.execute(
            "SELECT * FROM tasks WHERE id=?",
            (task_id,)
        ).fetchone()

        return dict(row) if row else None


def list_tasks():
    with connect() as c:
        return [
            dict(r) for r in c.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            ).fetchall()
        ]


def update_task(task_id, status, output_link="", blocked_reason=""):
    if status not in STATUSES:
        raise ValueError("Invalid task status")

    stamp = now()
    completed = stamp if status == "Completed" else None

    with connect() as c:
        c.execute("""
            UPDATE tasks
            SET status=?, output_link=?, blocked_reason=?,
                updated_at=?, completed_at=COALESCE(?, completed_at)
            WHERE id=?
        """, (
            status, output_link, blocked_reason,
            stamp, completed, task_id
        ))


def employee_stats():
    tasks = list_tasks()
    result = []

    for name in EMPLOYEE_ROLES:
        mine = [t for t in tasks if t["agent_name"] == name]
        completed = [t for t in mine if t["status"] == "Completed"]
        pending = [t for t in mine if t["status"] != "Completed"]

        durations = []

        for t in completed:
            try:
                start = datetime.fromisoformat(t["created_at"])
                end = datetime.fromisoformat(t["completed_at"])
                durations.append(
                    (end - start).total_seconds() / 3600
                )
            except Exception:
                pass

        result.append({
            "Employee": name,
            "Completed": len(completed),
            "Pending": len(pending),
            "Average completion hours": (
                round(sum(durations) / len(durations), 2)
                if durations else "N/A"
            ),
            "KPI basis": "Recorded tasks only"
        })

    return result


def get_employee_overview():
    tasks = list_tasks()
    today = date.today().isoformat()
    out = []

    for name, role in EMPLOYEE_ROLES.items():
        active = next(
            (
                t for t in tasks
                if t["agent_name"] == name
                and t["status"] == "In Progress"
            ),
            None
        )

        count = sum(
            t["agent_name"] == name
            and t["status"] == "Completed"
            and (t["completed_at"] or "")[:10] == today
            for t in tasks
        )

        out.append({
            "name": name,
            "role": role,
            "status": "Active" if active else "Idle",
            "current_task": active["title"] if active else None,
            "today_outputs": count
        })

    return out


def chat_history(role):
    with connect() as c:
        return [
            dict(r) for r in c.execute(
                "SELECT * FROM chats WHERE role=? ORDER BY id",
                (role,)
            ).fetchall()
        ]


def save_chat(role, speaker, message):
    with connect() as c:
        c.execute("""
            INSERT INTO chats(role, speaker, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (role, speaker, message, now()))
