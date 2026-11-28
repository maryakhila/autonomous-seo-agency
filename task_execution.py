
"""Connect saved agency tasks to the Gemini employee runner."""

from database import get_task, update_task


def run_employee_task(employee_name, task):
    """Run the selected AI employee."""

    from agent_runner import run_employee_task as employee_runner

    return employee_runner(employee_name, task)


def execute_task(task_id, sync_callback=None):
    """Execute a saved task and save its result."""

    task = get_task(task_id)

    if task is None:
        raise ValueError(f"Task {task_id} does not exist")

    update_task(
        task_id,
        "In Progress",
        output_link="",
        blocked_reason=""
    )

    task = get_task(task_id)

    if sync_callback:
        sync_callback(task)

    try:
        output = run_employee_task(
            task["agent_name"],
            task
        )

        update_task(
            task_id,
            "Completed",
            output_link=output,
            blocked_reason=""
        )

        succeeded = True

    except Exception as exc:

        update_task(
            task_id,
            "Blocked",
            output_link="",
            blocked_reason=str(exc)
        )

        succeeded = False

    final_task = get_task(task_id)

    if sync_callback:
        sync_callback(final_task)

    return {
        "success": succeeded,
        "task": final_task
    }
