"""Connect saved agency tasks to the Gemini employee runner.

Execution is synchronous by design for the course demonstration: the dashboard
shows the task result immediately. For production workloads, move this function
behind a background worker/queue.
"""

from database import get_task, update_task
def run_employee_task(employee_name, task):
    # Lazy import keeps database/report utilities importable without the Gemini
    # SDK installed; the dependency is required only when an AI task is run.
    from agent_runner import run_employee_task as _run
    return _run(employee_name, task)


def execute_task(task_id, sync_callback=None):
    """Run one saved task and persist its real result or failure.

    Returns a dictionary containing the final task record and whether execution
    succeeded. A failed task is marked Blocked with the exception as its reason.
    """
    task = get_task(task_id)
    if task is None:
        raise ValueError(f"Task {task_id} does not exist")

    update_task(task_id, "In Progress", output_link="", blocked_reason="")
    task = get_task(task_id)
    if sync_callback:
        sync_callback(task)

    try:
        output = run_employee_task(task["agent_name"], task)
        update_task(task_id, "Completed", output_link=output, blocked_reason="")
        succeeded = True
    except Exception as exc:
        update_task(task_id, "Blocked", output_link="", blocked_reason=str(exc))
        succeeded = False

    final_task = get_task(task_id)
    if sync_callback:
        sync_callback(final_task)
    return {"success": succeeded, "task": final_task}
