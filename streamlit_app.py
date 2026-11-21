
import streamlit as st
import pandas as pd
from datetime import date, timedelta

from database import (
    init_db, list_tasks, create_task, update_task,
    get_task, employee_stats, get_employee_overview,
    chat_history, save_chat
)
from project_manager import answer_boss_question, try_create_task_from_chat
from google_sheets import sync_task_to_sheet, sheet_is_configured
from email_report import build_daily_report, send_daily_report
from agent_runner import EMPLOYEES

st.set_page_config(
    page_title="Autonomous SEO Agency",
    page_icon="📈",
    layout="wide"
)

init_db()

# Boss login
if not st.session_state.get("authenticated", False):
    st.title("Autonomous SEO Agency")
    st.subheader("Boss Login")

    try:
        username = st.secrets["BOSS_USERNAME"]
        password = st.secrets["BOSS_PASSWORD"]
    except Exception:
        st.error("Please configure BOSS_USERNAME and BOSS_PASSWORD in Streamlit Secrets.")
        st.stop()

    entered_user = st.text_input("Username")
    entered_password = st.text_input("Password", type="password")

    if st.button("Sign in"):
        if entered_user == username and entered_password == password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect login details.")

    st.stop()

# Navigation
st.sidebar.title("SEO Agency")
page = st.sidebar.radio(
    "Dashboard",
    [
        "Agency Overview",
        "Task Assignment",
        "Live Task Board",
        "Reports & KPIs",
        "Boss Chat",
        "Employee Overview",
        "Integrations"
    ]
)

if st.sidebar.button("Sign out"):
    st.session_state["authenticated"] = False
    st.rerun()

st.title(page)

# 1. Agency Overview
if page == "Agency Overview":
    tasks = list_tasks()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total tasks", len(tasks))
    c2.metric("Queued", sum(t["status"] == "Queued" for t in tasks))
    c3.metric("In progress", sum(t["status"] == "In Progress" for t in tasks))
    c4.metric("Blocked", sum(t["status"] == "Blocked" for t in tasks))

    st.subheader("Agency workflow")
    st.markdown(
        "Boss → Project Manager → Seven SEO Employees "
        "→ Database → Google Sheets → Reports and Email"
    )

    if tasks:
        st.dataframe(pd.DataFrame(tasks), use_container_width=True)
    else:
        st.info("No tasks have been created yet.")

# 2. Task Assignment
elif page == "Task Assignment":
    with st.form("task_form"):
        title = st.text_input("Task title")
        description = st.text_area("Task description")
        employee = st.selectbox("Assign employee", list(EMPLOYEES.keys()))
        priority = st.selectbox(
            "Priority", ["Low", "Medium", "High", "Urgent"]
        )
        deadline = st.date_input(
            "Deadline", value=date.today() + timedelta(days=1)
        )

        submitted = st.form_submit_button("Create task")

    if submitted:
        if title.strip() and description.strip():
            task_id = create_task(
                title, description, employee, priority,
                deadline.isoformat(), "Boss"
            )
            sync_task_to_sheet(get_task(task_id))
            st.success(f"Task #{task_id} created.")
        else:
            st.error("Please enter a title and description.")

# 3. Live Task Board
elif page == "Live Task Board":
    tasks = list_tasks()

    if tasks:
        df = pd.DataFrame(tasks)

        employee_filter = st.selectbox(
            "Filter employee",
            ["All"] + sorted(df["agent_name"].unique().tolist())
        )
        status_filter = st.selectbox(
            "Filter status",
            ["All", "Queued", "In Progress", "Blocked", "Completed"]
        )

        if employee_filter != "All":
            df = df[df["agent_name"] == employee_filter]

        if status_filter != "All":
            df = df[df["status"] == status_filter]

        st.dataframe(df, use_container_width=True)

        task_id = st.selectbox("Select task", df["id"].tolist())
        task = get_task(int(task_id))

        st.write("Description:", task["description"])
        st.write("Output:", task["output_link"] or "Not recorded")
        st.write("Blocked reason:", task["blocked_reason"] or "None")

        with st.form("status_form"):
            status = st.selectbox(
                "New status",
                ["Queued", "In Progress", "Blocked", "Completed"]
            )
            output = st.text_input("Output or result link")
            reason = st.text_input("Blocked reason")

            if st.form_submit_button("Update task"):
                if status == "Blocked" and not reason.strip():
                    st.error("Please enter the blocked reason.")
                else:
                    update_task(task_id, status, output, reason)
                    sync_task_to_sheet(get_task(task_id))
                    st.success("Task updated.")
                    st.rerun()
    else:
        st.info("No tasks available.")

# 4. Reports
elif page == "Reports & KPIs":
    st.subheader("Employee performance")
    st.dataframe(
        pd.DataFrame(employee_stats()),
        use_container_width=True
    )

    tasks = list_tasks()
    if tasks:
        df = pd.DataFrame(tasks)
        st.bar_chart(df["status"].value_counts())
        st.download_button(
            "Download CSV report",
            df.to_csv(index=False).encode("utf-8"),
            "agency_report.csv",
            "text/csv"
        )
    else:
        st.info("Reports will appear after tasks are recorded.")

# 5. Boss Chat
elif page == "Boss Chat":
    role = st.selectbox(
        "Chat with",
        ["Project Manager"] + list(EMPLOYEES.keys())[1:]
    )

    for message in chat_history(role)[-30:]:
        with st.chat_message(message["speaker"]):
            st.write(message["message"])

    prompt = st.chat_input("Ask your Project Manager...")

    if prompt:
        save_chat(role, "user", prompt)

        task_id = try_create_task_from_chat(prompt)

        if task_id:
            response = f"Task #{task_id} created and queued."
            sync_task_to_sheet(get_task(task_id))
        else:
            response = answer_boss_question(prompt)

        save_chat(role, "assistant", response)
        st.rerun()

# 6. Employee Overview
elif page == "Employee Overview":
    employees = get_employee_overview()

    for employee in employees:
        with st.container(border=True):
            st.subheader(employee["name"])
            st.write("Role:", employee["role"])
            st.write("Status:", employee["status"])
            st.write("Current task:", employee["current_task"] or "Idle")
            st.write("Today's completed outputs:", employee["today_outputs"])

# 7. Integrations
elif page == "Integrations":
    st.write(
        "Google Sheets:",
        "Configured" if sheet_is_configured() else "Not configured"
    )

    st.subheader("Daily email report")

    if st.button("Send report now"):
        try:
            send_daily_report()
            st.success("Email report sent.")
        except Exception as error:
            st.error(str(error))

    st.text(build_daily_report())
