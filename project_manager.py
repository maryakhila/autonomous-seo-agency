from datetime import date, timedelta
from database import list_tasks, create_task, EMPLOYEE_ROLES

ALIASES = {
    "content writer":"SEO Content Writer", "writer":"SEO Content Writer",
    "keyword analyst":"Keyword Analyst", "technical seo auditor":"Technical SEO Auditor",
    "on-page seo specialist":"On-Page SEO Specialist", "off-page seo specialist":"Off-Page SEO Specialist",
    "performance analyst":"SEO Performance Analyst", "reporting specialist":"Reporting Specialist",
    "project manager":"Project Manager",
}

def answer_boss_question(question):
    q=question.lower()
    tasks=list_tasks()
    if any(x in q for x in ["running","in progress","currently running"]):
        n=sum(t["status"]=="In Progress" for t in tasks)
        return f"There are {n} tasks currently In Progress in the saved task database."
    if "blocked" in q:
        blocked=[t for t in tasks if t["status"]=="Blocked"]
        if not blocked: return "There are no tasks marked Blocked in the saved task database."
        return "Blocked tasks recorded in the database:\n" + "\n".join(
            f"#{t['id']} {t['title']} — {t['agent_name']}; reason: {t['blocked_reason'] or 'No reason recorded'}" for t in blocked)
    if "most tasks" in q or "completed the most" in q:
        week_start=(date.today()-timedelta(days=date.today().weekday())).isoformat()
        counts={}
        for t in tasks:
            if t["status"]=="Completed" and (t["completed_at"] or "")[:10]>=week_start:
                counts[t["agent_name"]]=counts.get(t["agent_name"],0)+1
        if not counts: return "No tasks have been recorded as completed this week yet."
        top=max(counts.values())
        names=[n for n,v in counts.items() if v==top]
        return f"Most completed this week: {', '.join(names)} ({top} task(s)), based on recorded completion timestamps."
    if "sales" in q or "leads" in q:
        return "Sales lead data is not currently represented in the task ledger. I cannot report a lead count or lead details without a connected lead register."
    if "posts" in q or "published" in q or "platform" in q:
        return "Published-post data is not currently represented in the task ledger. I cannot report post counts or platforms until a content publication register is connected."
    if "task" in q or "project" in q:
        return f"The database contains {len(tasks)} task(s): " + ", ".join(f"#{t['id']} {t['title']} ({t['agent_name']}: {t['status']})" for t in tasks[:20])
    return "I can answer using saved task records: ask about tasks currently running, blocked tasks and reasons, or which employee completed the most tasks this week. I will not invent sales leads or published-post metrics."

def try_create_task_from_chat(prompt):
    p=prompt.strip()
    low=p.lower()
    if not (low.startswith("assign") or low.startswith("create")): return None
    employee=None
    for alias, canonical in ALIASES.items():
        if alias in low:
            employee=canonical; break
    if not employee: return None
    # Extract a readable task description after colon where possible.
    desc=p.split(":",1)[1].strip() if ":" in p else p
    desc=desc.replace("due tomorrow","").replace("Due tomorrow","").strip(" .")
    if not desc: return None
    due=(date.today()+timedelta(days=1)).isoformat() if "tomorrow" in low else None
    return create_task(desc[:100], desc, employee, "Medium", due, "Boss via Project Manager Chat")
