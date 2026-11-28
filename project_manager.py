
from datetime import date, timedelta
from database import list_tasks, create_task, EMPLOYEE_ROLES


ALIASES = {
    "lead generator agent": "Lead Generator Agent",
    "lead generator": "Lead Generator Agent",

    "project manager & proposal agent": "Project Manager & Proposal Agent",
    "project manager": "Project Manager & Proposal Agent",
    "proposal agent": "Project Manager & Proposal Agent",

    "agency web developer agent": "Agency Web Developer Agent",
    "web developer": "Agency Web Developer Agent",

    "seo specialist / coordinator agent": "SEO Specialist / Coordinator Agent",
    "seo specialist": "SEO Specialist / Coordinator Agent",
    "seo coordinator": "SEO Specialist / Coordinator Agent",

    "technical seo agent": "Technical SEO Agent",
    "technical seo": "Technical SEO Agent",

    "seo content strategist & writer agent": "SEO Content Strategist & Writer Agent",
    "seo content writer": "SEO Content Strategist & Writer Agent",
    "content writer": "SEO Content Strategist & Writer Agent",
    "writer": "SEO Content Strategist & Writer Agent",

    "link building & digital pr agent": "Link Building & Digital PR Agent",
    "link building": "Link Building & Digital PR Agent",
    "digital pr": "Link Building & Digital PR Agent",

    "aeo / geo & local seo agent": "AEO / GEO & Local SEO Agent",
    "aeo": "AEO / GEO & Local SEO Agent",
    "geo": "AEO / GEO & Local SEO Agent",
    "local seo": "AEO / GEO & Local SEO Agent",
}


def answer_boss_question(question):
    q = question.lower()
    tasks = list_tasks()

    if any(x in q for x in ["running", "in progress", "currently running"]):
        n = sum(t["status"] == "In Progress" for t in tasks)
        return (
            f"There are {n} tasks currently In Progress "
            "in the saved task database."
        )

    if "blocked" in q:
        blocked = [t for t in tasks if t["status"] == "Blocked"]

        if not blocked:
            return "There are no tasks marked Blocked in the saved task database."

        return "Blocked tasks recorded in the database:\n" + "\n".join(
            f"#{t['id']} {t['title']} — {t['agent_name']}; "
            f"reason: {t['blocked_reason'] or 'No reason recorded'}"
            for t in blocked
        )

    if "most tasks" in q or "completed the most" in q:
        week_start = (
            date.today() - timedelta(days=date.today().weekday())
        ).isoformat()

        counts = {}

        for t in tasks:
            if (
                t["status"] == "Completed"
                and (t["completed_at"] or "")[:10] >= week_start
            ):
                name = t["agent_name"]
                counts[name] = counts.get(name, 0) + 1

        if not counts:
            return "No tasks have been recorded as completed this week yet."

        top = max(counts.values())
        names = [n for n, v in counts.items() if v == top]

        return (
            f"Most completed this week: {', '.join(names)} "
            f"({top} task(s)), based on recorded completion timestamps."
        )

    if "sales" in q or "leads" in q:
        return (
            "Sales lead data is not currently represented in the task ledger. "
            "A connected lead register is required to report lead counts."
        )

    if "posts" in q or "published" in q or "platform" in q:
        return (
            "Published-post data is not currently represented in the task ledger. "
            "A content publication register is required to report post counts."
        )

    if "task" in q or "project" in q:
        if not tasks:
            return "There are no saved tasks yet."

        return (
            f"The database contains {len(tasks)} task(s): "
            + ", ".join(
                f"#{t['id']} {t['title']} "
                f"({t['agent_name']}: {t['status']})"
                for t in tasks[:20]
            )
        )

    return (
        "I can answer using saved task records. Ask about running tasks, "
        "blocked tasks and reasons, or which employee completed the most "
        "tasks this week. Lead and published-post metrics need their own registers."
    )


def try_create_task_from_chat(prompt):
    p = prompt.strip()
    low = p.lower()

    if not (low.startswith("assign") or low.startswith("create")):
        return None

    employee = None

    for alias in sorted(ALIASES, key=len, reverse=True):
        if alias in low:
            employee = ALIASES[alias]
            break

    if not employee or employee not in EMPLOYEE_ROLES:
        return None

    desc = p.split(":", 1)[1].strip() if ":" in p else p

    desc = desc.replace("due tomorrow", "")
    desc = desc.replace("Due tomorrow", "")
    desc = desc.strip(" .")

    if not desc:
        return None

    due = (
        (date.today() + timedelta(days=1)).isoformat()
        if "tomorrow" in low else None
    )

    return create_task(
        desc[:100],
        desc,
        employee,
        "Medium",
        due,
        "Boss via Project Manager Chat"
    )
