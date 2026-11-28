
import streamlit as st
import pandas as pd
from datetime import date, timedelta

from database import (
    init_db,
    list_tasks,
    create_task,
    update_task,
    get_task,
    employee_stats,
    get_employee_overview,
    chat_history,
    save_chat,
)
from project_manager import (
    answer_boss_question,
    try_create_task_from_chat,
)
from google_sheets import (
    sync_task_to_sheet,
    sheet_is_configured,
)
from email_report import (
    build_daily_report,
    send_daily_report,
)
from agent_runner import EMPLOYEES
from task_execution import execute_task


st.set_page_config(
    page_title="Autonomous SEO Agency | Boss Command Center",
    page_icon="📈",
    layout="wide",
)

init_db()


def is_logged_in():
    try:
        expected_user = st.secrets["BOSS_USERNAME"]
        expected_password = st.secrets["BOSS_PASSWORD"]
    except Exception:
        st.error(
            "Login is not configured. Add BOSS_USERNAME "
            "and BOSS_PASSWORD to Streamlit Secrets."
        )
        return False

    with st.sidebar:
        st.subheader("Boss Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button("Sign in", use_container_width=True):
            if (
                username == expected_user
                and password == expected_password
            ):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    return st.session_state.get("authenticated", False)


if not st.session_state.get("authenticated", False):
    st.title("📈 Autonomous SEO Agency")
    st.write(
        "Boss-only command center. Sign in using the "
        "credentials configured by the administrator."
    )
    is_logged_in()
    st.stop()


with st.sidebar:
    st.title("📈 SEO Agency")
    st.caption("Boss Command Center")

    page = st.radio(
        "Navigation",
        [
            "Agency Overview",
            "Task Assignment",
            "Live Task Board",
            "Reports & KPIs",
            "Boss / Employee Chat",
            "Employee Overview",
            "Integrations",
        ],
    )

    if st.button("Sign out"):
        st.session_state["authenticated"] = False
        st.rerun()


st.title(page)


# AGENCY OVERVIEW

if page == "Agency Overview":

    tasks = list_tasks()
    df = pd.DataFrame(tasks)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("All tasks", len(tasks))
    c2.metric(
        "Queued",
        sum(t["status"] == "Queued" for t in tasks),
    )
    c3.metric(
        "In progress",
        sum(t["status"] == "In Progress" for t in tasks),
    )
    c4.metric(
        "Blocked",
        sum(t["status"] == "Blocked" for t in tasks),
    )

    st.subheader("Task status")

    if tasks:
        st.bar_chart(
            pd.Series(
                [t["status"] for t in tasks]
            ).value_counts()
        )
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No tasks have been recorded yet.")

    st.caption(
        "Task progress and completion are based on saved task records."
    )


# TASK ASSIGNMENT

elif page == "Task Assignment":

    st.subheader("Create a task")

    with st.form("new_task"):

        title = st.text_input("Task title")
        description = st.text_area("Task description")

        assignee = st.selectbox(
            "Assign to",
            list(EMPLOYEES.keys()),
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Urgent"],
            index=1,
        )

        deadline = st.date_input(
            "Deadline",
            value=date.today() + timedelta(days=1),
        )

        submitted = st.form_submit_button("Create task")

    if submitted:

        if not title.strip() or not description.strip():
            st.error("Enter both a title and a description.")

        else:

            task_id = create_task(
                title,
                description,
                assignee,
                priority,
                deadline.isoformat(),
                "Boss",
            )

            sync_task_to_sheet(get_task(task_id))

            st.success(
                f"Task {task_id} assigned to {assignee}."
            )

            st.info(
                "Task status: Queued. "
                "Open Live Task Board and click Run AI Agent to execute it."
            )

            if not sheet_is_configured():
                st.warning(
                    "Google Sheets is not configured. "
                    "The task is saved in the local database."
                )

    st.divider()

    st.subheader("Assign via Project Manager")

    st.write(
        "The Project Manager is also an assignable role. "
        "Assigning to the Project Manager records a coordination task."
    )


# LIVE TASK BOARD

elif page == "Live Task Board":

    tasks = list_tasks()

    if not tasks:
        st.info("No tasks yet.")

    else:

        d = pd.DataFrame(tasks)

        f1, f2, f3 = st.columns(3)

        employees = (
            ["All"]
            + sorted(
                d["agent_name"].dropna().unique().tolist()
            )
        )

        statuses = [
            "All",
            "Queued",
            "In Progress",
            "Blocked",
            "Completed",
        ]

        priorities = [
            "All",
            "Low",
            "Medium",
            "High",
            "Urgent",
        ]

        emp = f1.selectbox("Employee", employees)
        status = f2.selectbox("Status", statuses)
        priority = f3.selectbox("Priority", priorities)

        if emp != "All":
            d = d[d.agent_name == emp]

        if status != "All":
            d = d[d.status == status]

        if priority != "All":
            d = d[d.priority == priority]

        st.dataframe(
            d,
            use_container_width=True,
            hide_index=True,
        )

        ids = [int(x) for x in d["id"].tolist()]

        if ids:

            selected = st.selectbox(
                "Open task details",
                ids,
                format_func=lambda x: (
                    f"#{x} — "
                    f"{next(t['title'] for t in tasks if t['id'] == x)}"
                ),
            )

            task = get_task(selected)

            st.markdown(
                f"**Description:** {task['description']}"
            )

            st.write("Assigned to:", task["agent_name"])
            st.write("Created:", task["created_at"])
            st.write(
                "Deadline:",
                task["deadline"] or "Not set",
            )
            st.write("Priority:", task["priority"])
            st.write("Current status:", task["status"])

            st.write(
                "Output/result:",
                task["output_link"] or "No output recorded",
            )

            st.write(
                "Blocked reason:",
                task["blocked_reason"] or "—",
            )

            # RUN AI AGENT

            if task["status"] in ["Queued", "Blocked"]:

                if st.button(
                    "🚀 Run AI Agent",
                    use_container_width=True,
                ):

                    with st.spinner(
                        f"{task['agent_name']} is working..."
                    ):

                        try:
                            result = execute_task(
                                selected,
                                sync_callback=sync_task_to_sheet,
                            )

                            if result["success"]:
                                st.success(
                                    "AI task completed successfully!"
                                )
                                st.write(
                                    result["task"]["output_link"]
                                )
                            else:
                                st.error("AI task failed.")
                                st.write(
                                    result["task"]["blocked_reason"]
                                )

                        except Exception as error:
                            st.error(
                                f"Task execution error: {error}"
                            )

                    st.rerun()

            elif task["status"] == "In Progress":
                st.warning(
                    "This task is already marked In Progress."
                )

            elif task["status"] == "Completed":
                st.success(
                    "This task has already been completed."
                )

            # MANUAL TASK UPDATE

            with st.expander("Manual task update"):

                with st.form("update_task"):

                    status_options = [
                        "Queued",
                        "In Progress",
                        "Blocked",
                        "Completed",
                    ]

                    current_status = task["status"]

                    if current_status not in status_options:
                        current_status = "Queued"

                    new_status = st.selectbox(
                        "Update status",
                        status_options,
                        index=status_options.index(current_status),
                    )

                    output = st.text_area(
                        "Output / result",
                        value=task["output_link"] or "",
                    )

                    reason = st.text_input(
                        "Reason (required when blocked)",
                        value=task["blocked_reason"] or "",
                    )

                    save_update = st.form_submit_button(
                        "Save task update"
                    )

                if save_update:

                    if new_status == "Blocked" and not reason.strip():
                        st.error(
                            "Please explain why this task is blocked."
                        )

                    else:

                        update_task(
                            selected,
                            new_status,
                            output,
                            reason,
                        )

                        sync_task_to_sheet(get_task(selected))

                        st.success("Task updated successfully.")
                        st.rerun()


# REPORTS & KPIs

elif page == "Reports & KPIs":

    tasks = list_tasks()
    stats = employee_stats()

    st.subheader(
        "Employee performance (from saved task records)"
    )

    st.dataframe(
        pd.DataFrame(stats),
        use_container_width=True,
        hide_index=True,
    )

    if tasks:

        df = pd.DataFrame(tasks)

        st.subheader("Daily / weekly task summary")

        today = date.today().isoformat()

        week_start = (
            date.today()
            - timedelta(days=date.today().weekday())
        ).isoformat()

        tasks_created_today = sum(
            1
            for t in tasks
            if (t.get("created_at") or "")[:10] == today
        )

        completed_this_week = sum(
            1
            for t in tasks
            if t["status"] == "Completed"
            and (t.get("completed_at") or "")[:10] >= week_start
        )

        st.write(
            f"Tasks created today: **{tasks_created_today}**"
        )

        st.write(
            f"Tasks completed this week: **{completed_this_week}**"
        )

        st.bar_chart(df["status"].value_counts())

        st.download_button(
            "Download task report (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "seo_agency_tasks.csv",
            "text/csv",
        )

    else:
        st.info(
            "Reports will appear when tasks have been recorded."
        )

    st.caption(
        "Lead, published-content and support-ticket KPIs "
        "require dedicated records and integrations."
    )


# BOSS / EMPLOYEE CHAT

elif page == "Boss / Employee Chat":

    chat_roles = (
        ["Project Manager & Proposal Agent"]
        + [
            name
            for name in EMPLOYEES
            if name != "Project Manager & Proposal Agent"
        ]
    )

    role = st.selectbox("Chat with", chat_roles)

    history = chat_history(role)

    for item in history[-30:]:
        with st.chat_message(item["speaker"]):
            st.write(item["message"])

    prompt = st.chat_input(
        "Ask about actual tasks, blocked work, employee output, "
        "or create a task…"
    )

    if prompt:

        save_chat(role, "user", prompt)

        new_task_id = try_create_task_from_chat(prompt)

        if new_task_id:

            response = (
                f"Created task #{new_task_id} in the database "
                "with Queued status. Review it in Live Task Board."
            )

            sync_task_to_sheet(get_task(new_task_id))

        else:
            response = answer_boss_question(prompt)

        save_chat(role, "assistant", response)

        st.rerun()


# EMPLOYEE OVERVIEW

elif page == "Employee Overview":

    overview = get_employee_overview()

    cols = st.columns(2)

    for i, emp in enumerate(overview):

        with cols[i % 2]:

            with st.container(border=True):

                st.subheader(emp["name"])
                st.caption(emp["role"])
                st.write("Status:", emp["status"])
                st.write(
                    "Current task:",
                    emp["current_task"] or "Idle",
                )
                st.write(
                    "Today's completed outputs:",
                    emp["today_outputs"],
                )


# INTEGRATIONS

elif page == "Integrations":

    st.subheader("Integration status")

    st.write(
        "Google Sheets:",
        "Configured" if sheet_is_configured()
        else "Not configured",
    )

    email_configured = all(
        key in st.secrets
        for key in [
            "SMTP_HOST",
            "SMTP_PORT",
            "SMTP_USER",
            "SMTP_PASSWORD",
            "BOSS_EMAIL",
        ]
    )

    st.write(
        "Email:",
        "Configured" if email_configured
        else "Not configured",
    )

    st.info(
        "For reliable daily email, configure an external "
        "scheduler to run python send_daily_email.py once per day."
    )

    if st.button("Send daily report now"):

        try:
            send_daily_report()
            st.success("Daily report sent.")

        except Exception as error:
            st.error(
                f"Email was not sent: {error}"
            )

    st.subheader("Preview daily report")

    st.code(build_daily_report())

    st.caption(
        "Secrets must be entered in Streamlit Community Cloud "
        "→ App → Settings → Secrets. Never commit real credentials."
    )
