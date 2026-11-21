
import streamlit as st
import pandas as pd
from datetime import datetime, date
import uuid

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Autonomous SEO Agency",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# AGENCY INFORMATION
# --------------------------------------------------

EMPLOYEES = [
    {
        "name": "Keyword Analyst",
        "role": "Keyword research and search intent analysis",
        "responsibility": "Find relevant keywords and analyze search opportunities."
    },
    {
        "name": "SEO Content Writer",
        "role": "SEO content creation",
        "responsibility": "Prepare SEO-friendly articles and website content."
    },
    {
        "name": "Technical SEO Auditor",
        "role": "Technical website auditing",
        "responsibility": "Identify technical SEO issues and recommend fixes."
    },
    {
        "name": "On-Page SEO Specialist",
        "role": "On-page optimization",
        "responsibility": "Optimize titles, headings, metadata and page content."
    },
    {
        "name": "Off-Page SEO Specialist",
        "role": "Off-page optimization",
        "responsibility": "Research backlink opportunities and external SEO activities."
    },
    {
        "name": "SEO Performance Analyst",
        "role": "SEO performance analysis",
        "responsibility": "Analyze traffic, rankings and SEO performance data."
    },
    {
        "name": "Reporting Specialist",
        "role": "Reporting and documentation",
        "responsibility": "Prepare reports and communicate project progress."
    }
]

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "ID": "TASK-001",
            "Task": "Research target keywords",
            "Employee": "Keyword Analyst",
            "Priority": "High",
            "Status": "Completed",
            "Created": str(date.today())
        },
        {
            "ID": "TASK-002",
            "Task": "Prepare SEO article",
            "Employee": "SEO Content Writer",
            "Priority": "Medium",
            "Status": "In Progress",
            "Created": str(date.today())
        },
        {
            "ID": "TASK-003",
            "Task": "Perform technical SEO audit",
            "Employee": "Technical SEO Auditor",
            "Priority": "High",
            "Status": "Pending",
            "Created": str(date.today())
        }
    ]

if "clients" not in st.session_state:
    st.session_state.clients = []

if "audits" not in st.session_state:
    st.session_state.audits = {
        employee["name"]: "Not Audited"
        for employee in EMPLOYEES
    }

if "chat" not in st.session_state:
    st.session_state.chat = []

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_task_dataframe():
    return pd.DataFrame(st.session_state.tasks)


def get_daily_summary():
    tasks = get_task_dataframe()

    if tasks.empty:
        return "No tasks have been created yet."

    completed = len(tasks[tasks["Status"] == "Completed"])
    progress = len(tasks[tasks["Status"] == "In Progress"])
    pending = len(tasks[tasks["Status"] == "Pending"])

    summary = f"""
AUTONOMOUS SEO AGENCY
DAILY PROJECT MANAGER SUMMARY

Date: {date.today()}

Total Tasks: {len(tasks)}
Completed Tasks: {completed}
In Progress Tasks: {progress}
Pending Tasks: {pending}

TASK DETAILS
"""

    for _, task in tasks.iterrows():
        summary += (
            f"\n{task['ID']} | {task['Task']} | "
            f"{task['Employee']} | {task['Status']}"
        )

    return summary


def answer_boss_question(question):
    tasks = get_task_dataframe()
    q = question.lower()

    if tasks.empty:
        return "There are currently no tasks in the agency ledger."

    if "completed" in q:
        count = len(tasks[tasks["Status"] == "Completed"])
        return f"The agency has completed {count} task(s)."

    if "pending" in q:
        count = len(tasks[tasks["Status"] == "Pending"])
        return f"There are {count} pending task(s)."

    if "employee" in q or "team" in q:
        return (
            "The agency has 7 specialist AI employees "
            "managed by the Project Manager."
        )

    if "task" in q or "project" in q or "status" in q:
        return (
            f"The agency currently has {len(tasks)} tasks. "
            f"{len(tasks[tasks['Status'] == 'Completed'])} completed, "
            f"{len(tasks[tasks['Status'] == 'In Progress'])} in progress, "
            f"and {len(tasks[tasks['Status'] == 'Pending'])} pending."
        )

    return (
        "I can report on agency tasks, completed work, pending work "
        "and the seven AI employees. Ask me a question about these areas."
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 Autonomous SEO Agency")
st.sidebar.caption("AI Agency Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Agency Overview",
        "Project Manager",
        "AI Employees",
        "Client Management",
        "Task Management",
        "SEO Performance",
        "Reports"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Prototype mode: dashboard data is stored in the current "
    "application session. External integrations are not connected yet."
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 Autonomous SEO Agency")
st.caption(
    "AI-powered SEO management | Human supervision | "
    "Automated workflow prototype"
)

st.divider()

# --------------------------------------------------
# 1. AGENCY OVERVIEW
# --------------------------------------------------

if page == "Agency Overview":

    st.header("📊 Agency Overview")

    tasks = get_task_dataframe()

    total = len(tasks)
    completed = len(tasks[tasks["Status"] == "Completed"]) if total else 0
    progress = len(tasks[tasks["Status"] == "In Progress"]) if total else 0
    pending = len(tasks[tasks["Status"] == "Pending"]) if total else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("AI Employees", "7")
    c2.metric("Total Tasks", total)
    c3.metric("Completed", completed)
    c4.metric("Pending", pending)

    st.subheader("Agency Team")

    st.write(
        "The Project Manager supervises seven specialist AI employees."
    )

    st.subheader("Task Overview")

    if not tasks.empty:
        st.dataframe(tasks, use_container_width=True)

        status_counts = (
            tasks["Status"]
            .value_counts()
            .reindex(
                ["Completed", "In Progress", "Pending"],
                fill_value=0
            )
        )

        st.subheader("Task Status Distribution")
        st.bar_chart(status_counts)
    else:
        st.info("No tasks have been created.")

    st.info(
        "Metrics above are calculated from the agency's current "
        "prototype task ledger."
    )

# --------------------------------------------------
# 2. PROJECT MANAGER
# --------------------------------------------------

elif page == "Project Manager":

    st.header("👔 Project Manager — Chief of Staff")

    st.write(
        "The Project Manager is responsible for supervising "
        "all seven AI employees and coordinating agency operations."
    )

    st.subheader("Six Core Responsibilities")

    responsibilities = [
        "Audit all seven AI employees",
        "Assign tasks to the correct employees",
        "Track employee tasks and progress",
        "Maintain the shared Google Sheets ledger",
        "Prepare and email the Boss a daily summary",
        "Answer the Boss's questions in dashboard chat"
    ]

    for item in responsibilities:
        st.write("✅", item)

    st.divider()

    # EMPLOYEE AUDIT

    st.subheader("1. Employee Audit Dashboard")

    st.caption(
        "Select an audit status after reviewing each employee. "
        "These statuses are manually recorded in this prototype."
    )

    for employee in EMPLOYEES:

        name = employee["name"]

        with st.expander(name):

            st.write("**Role:**", employee["role"])
            st.write("**Responsibility:**", employee["responsibility"])

            status = st.selectbox(
                "Audit status",
                [
                    "Not Audited",
                    "Under Review",
                    "Approved",
                    "Needs Improvement"
                ],
                index=[
                    "Not Audited",
                    "Under Review",
                    "Approved",
                    "Needs Improvement"
                ].index(st.session_state.audits[name]),
                key=f"audit_{name}"
            )

            st.session_state.audits[name] = status

    audit_df = pd.DataFrame([
        {"Employee": name, "Audit Status": status}
        for name, status in st.session_state.audits.items()
    ])

    st.dataframe(audit_df, use_container_width=True)

    st.divider()

    # DAILY SUMMARY

    st.subheader("2. Daily Summary for the Boss")

    summary = get_daily_summary()

    st.text_area(
        "Daily management summary",
        value=summary,
        height=220
    )

    st.download_button(
        "Download Daily Summary",
        data=summary,
        file_name=f"agency_summary_{date.today()}.txt",
        mime="text/plain"
    )

    st.warning(
        "Email is not connected yet. Downloading this summary does "
        "not send an email to the Boss."
    )

    st.divider()

    # GOOGLE SHEETS

    st.subheader("3. Shared Google Sheets Ledger")

    st.write(
        "The current task ledger can be downloaded as CSV. "
        "Google Sheets synchronization requires account credentials "
        "and a configured spreadsheet."
    )

    tasks = get_task_dataframe()

    if not tasks.empty:
        csv = tasks.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Task Ledger CSV",
            data=csv,
            file_name="agency_task_ledger.csv",
            mime="text/csv"
        )

    st.info("Google Sheets connection: Not configured")

    st.divider()

    # BOSS CHAT

    st.subheader("4. Ask the Project Manager")

    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask about employees, tasks or agency progress..."
    )

    if question:
        st.session_state.chat.append(
            {"role": "user", "content": question}
        )

        response = answer_boss_question(question)

        st.session_state.chat.append(
            {"role": "assistant", "content": response}
        )

        st.rerun()

    st.caption(
        "The current chat uses predefined responses based on dashboard "
        "data. An AI model connection is required for intelligent answers."
    )

# --------------------------------------------------
# 3. AI EMPLOYEES
# --------------------------------------------------

elif page == "AI Employees":

    st.header("🤖 Seven AI Employees")

    st.write(
        "The specialist team works under the supervision "
        "of the Project Manager."
    )

    for number, employee in enumerate(EMPLOYEES, start=1):

        with st.container(border=True):

            st.subheader(
                f"{number}. {employee['name']}"
            )

            st.write("**Role:**", employee["role"])
            st.write("**Responsibilities:**", employee["responsibility"])

            st.write(
                "**Audit Status:**",
                st.session_state.audits[employee["name"]]
            )

# --------------------------------------------------
# 4. CLIENT MANAGEMENT
# --------------------------------------------------

elif page == "Client Management":

    st.header("👥 Client Management")

    st.write("Register and manage SEO agency clients.")

    with st.form("client_form"):

        client_name = st.text_input("Client name")
        website = st.text_input("Website URL")
        industry = st.text_input("Industry")

        submitted = st.form_submit_button("Add Client")

        if submitted:

            if client_name and website:

                st.session_state.clients.append({
                    "Client": client_name,
                    "Website": website,
                    "Industry": industry
                })

                st.success("Client added to this session.")

            else:
                st.warning("Please enter a client name and website.")

    st.subheader("Client List")

    if st.session_state.clients:
        st.dataframe(
            pd.DataFrame(st.session_state.clients),
            use_container_width=True
        )
    else:
        st.info("No clients registered yet.")

# --------------------------------------------------
# 5. TASK MANAGEMENT
# --------------------------------------------------

elif page == "Task Management":

    st.header("📋 Task Management")

    st.write(
        "The Project Manager assigns tasks to the seven specialist "
        "employees and tracks their progress."
    )

    with st.form("task_form"):

        task_name = st.text_input("Task description")

        employee_name = st.selectbox(
            "Assign employee",
            [employee["name"] for employee in EMPLOYEES]
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Urgent"]
        )

        submitted = st.form_submit_button("Create and Assign Task")

        if submitted:

            if task_name.strip():

                new_task = {
                    "ID": "TASK-" + uuid.uuid4().hex[:6].upper(),
                    "Task": task_name,
                    "Employee": employee_name,
                    "Priority": priority,
                    "Status": "Pending",
                    "Created": str(date.today())
                }

                st.session_state.tasks.append(new_task)

                st.success(
                    f"Task assigned to {employee_name}."
                )

            else:
                st.warning("Please enter a task description.")

    st.divider()

    st.subheader("Update Task Progress")

    tasks = get_task_dataframe()

    if not tasks.empty:

        edited_tasks = st.data_editor(
            tasks,
            use_container_width=True,
            hide_index=True,
            disabled=[
                "ID",
                "Task",
                "Employee",
                "Priority",
                "Created"
            ],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=[
                        "Pending",
                        "In Progress",
                        "Completed"
                    ],
                    required=True
                )
            },
            key="task_editor"
        )

        if st.button("Save Task Updates"):

            st.session_state.tasks = edited_tasks.to_dict(
                orient="records"
            )

            st.success("Task updates saved in this session.")
            st.rerun()

    else:
        st.info("No tasks available.")

# --------------------------------------------------
# 6. SEO PERFORMANCE
# --------------------------------------------------

elif page == "SEO Performance":

    st.header("📈 SEO Performance Dashboard")

    st.write(
        "This dashboard is prepared for website traffic, "
        "keyword rankings, backlinks and SEO health metrics."
    )

    st.warning(
        "The following figures are illustrative sample data, "
        "not live Google Analytics or Search Console results."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Organic Visitors", "1,250")
    c2.metric("Tracked Keywords", "85")
    c3.metric("Backlinks", "240")
    c4.metric("SEO Health Score", "78/100")

    performance = pd.DataFrame({
        "Month": ["January", "February", "March", "April", "May"],
        "Organic Visitors": [600, 750, 820, 1050, 1250]
    })

    st.subheader("Illustrative Organic Traffic")
    st.line_chart(
        performance.set_index("Month")
    )

    st.info(
        "Connect Google Analytics and Google Search Console "
        "to replace sample figures with actual website data."
    )

# --------------------------------------------------
# 7. REPORTS
# --------------------------------------------------

elif page == "Reports":

    st.header("📑 Agency Reports")

    tasks = get_task_dataframe()

    st.subheader("Task Report")

    if not tasks.empty:

        st.dataframe(tasks, use_container_width=True)

        report_csv = tasks.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Agency Task Report",
            data=report_csv,
            file_name="seo_agency_report.csv",
            mime="text/csv"
        )

    else:
        st.info("No task data available.")

    st.subheader("Employee Audit Report")

    audit_report = pd.DataFrame([
        {
            "Employee": employee,
            "Audit Status": status
        }
        for employee, status in st.session_state.audits.items()
    ])

    st.dataframe(audit_report, use_container_width=True)

    audit_csv = audit_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Employee Audit Report",
        data=audit_csv,
        file_name="employee_audit_report.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Autonomous SEO Agency | Developed by Mary Akhila | "
    "Management Dashboard Prototype"
)
