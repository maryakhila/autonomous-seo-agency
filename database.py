
import os
import sqlite3
from datetime import datetime, timezone, date

DB_PATH = os.getenv("SQLITE_PATH", "agency.db")

STATUSES = ("Queued", "In Progress", "Blocked", "Completed")

LEAD_STATUSES = (
    "New",
    "Qualified",
    "Contacted",
    "Converted",
    "Disqualified"
)

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


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def init_db():
    with connect() as c:

        # Tasks table
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

        # Chats table
        c.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                speaker TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Leads table
        c.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                website TEXT,
                country TEXT,
                city TEXT,
                email TEXT,
                phone TEXT,
                niche TEXT,
                seo_opportunity TEXT,
                seo_score INTEGER,
                lead_status TEXT NOT NULL DEFAULT 'New',
                source TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        c.execute("""
            CREATE INDEX IF NOT EXISTS idx_leads_status
            ON leads(lead_status)
        """)

        c.execute("""
            CREATE INDEX IF NOT EXISTS idx_leads_niche
            ON leads(niche)
        """)


# -------------------------
# TASK FUNCTIONS
# -------------------------

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


# -------------------------
# LEAD GENERATION FUNCTIONS
# -------------------------

def create_lead(
    business_name,
    website=None,
    country=None,
    city=None,
    email=None,
    phone=None,
    niche=None,
    seo_opportunity=None,
    seo_score=None,
    source=None,
    notes=None
):
    """Save a new business lead."""

    business_name = (business_name or "").strip()

    if not business_name:
        raise ValueError("Business name is required")

    if seo_score is not None:
        seo_score = int(seo_score)

        if not 0 <= seo_score <= 100:
            raise ValueError("SEO score must be between 0 and 100")

    stamp = now()

    with connect() as c:

        # Avoid duplicate websites
        if website:
            existing = c.execute("""
                SELECT id FROM leads
                WHERE LOWER(website) = LOWER(?)
                LIMIT 1
            """, (website.strip(),)).fetchone()

            if existing:
                return existing["id"]

        # Avoid duplicate business emails
        if email:
            existing = c.execute("""
                SELECT id FROM leads
                WHERE LOWER(email) = LOWER(?)
                LIMIT 1
            """, (email.strip(),)).fetchone()

            if existing:
                return existing["id"]

        cur = c.execute("""
            INSERT INTO leads (
                business_name,
                website,
                country,
                city,
                email,
                phone,
                niche,
                seo_opportunity,
                seo_score,
                lead_status,
                source,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            business_name,
            website,
            country,
            city,
            email,
            phone,
            niche,
            seo_opportunity,
            seo_score,
            "New",
            source,
            notes,
            stamp,
            stamp
        ))

        return cur.lastrowid


def get_lead(lead_id):
    """Get one lead by ID."""

    with connect() as c:
        row = c.execute(
            "SELECT * FROM leads WHERE id=?",
            (lead_id,)
        ).fetchone()

        return dict(row) if row else None


def list_leads(status=None, niche=None):
    """List leads with optional filters."""

    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if status:
        query += " AND lead_status=?"
        params.append(status)

    if niche:
        query += " AND niche=?"
        params.append(niche)

    query += " ORDER BY id DESC"

    with connect() as c:
        return [
            dict(row)
            for row in c.execute(query, params).fetchall()
        ]


def update_lead(lead_id, **fields):
    """Update permitted lead fields."""

    allowed_fields = {
        "business_name",
        "website",
        "country",
        "city",
        "email",
        "phone",
        "niche",
        "seo_opportunity",
        "seo_score",
        "lead_status",
        "source",
        "notes"
    }

    updates = {
        key: value
        for key, value in fields.items()
        if key in allowed_fields
    }

    if not updates:
        return False

    if "lead_status" in updates:
        if updates["lead_status"] not in LEAD_STATUSES:
            raise ValueError("Invalid lead status")

    if "seo_score" in updates and updates["seo_score"] is not None:
        score = int(updates["seo_score"])

        if not 0 <= score <= 100:
            raise ValueError("SEO score must be between 0 and 100")

        updates["seo_score"] = score

    updates["updated_at"] = now()

    columns = ", ".join(
        f"{key}=?" for key in updates
    )

    values = list(updates.values())
    values.append(lead_id)

    with connect() as c:
        cur = c.execute(
            f"UPDATE leads SET {columns} WHERE id=?",
            values
        )

        return cur.rowcount > 0


# -------------------------
# EMPLOYEE STATISTICS
# -------------------------

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


# -------------------------
# CHAT FUNCTIONS
# -------------------------

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
