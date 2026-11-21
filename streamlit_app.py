
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Autonomous SEO Agency",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Autonomous SEO Agency")
st.caption("AI-powered SEO management and automation dashboard")

# Sidebar navigation
st.sidebar.title("Agency Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Agency Overview",
        "AI Employees",
        "Client Management",
        "Task Management",
        "SEO Performance",
        "Reports"
    ]
)

# Demo data: replace with connected agency data
tasks = pd.DataFrame([
    {"Task": "Keyword Research", "Employee": "Keyword Analyst", "Status": "Completed"},
    {"Task": "SEO Content Creation", "Employee": "Content Writer", "Status": "In Progress"},
    {"Task": "Technical SEO Audit", "Employee": "Technical SEO Auditor", "Status": "Pending"},
    {"Task": "Performance Analysis", "Employee": "SEO Analyst", "Status": "In Progress"}
])

employees = [
    "Project Manager",
    "Keyword Analyst",
    "SEO Content Writer",
    "Technical SEO Auditor",
    "On-Page SEO Specialist",
    "Off-Page SEO Specialist",
    "SEO Performance Analyst",
    "Reporting Specialist"
]

if page == "Agency Overview":
    st.header("Agency Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AI Employees", "8")
    c2.metric("Total Tasks", len(tasks))
    c3.metric("Completed Tasks", len(tasks[tasks["Status"] == "Completed"]))
    c4.metric("Pending Tasks", len(tasks[tasks["Status"] == "Pending"]))

    st.subheader("Recent Agency Tasks")
    st.dataframe(tasks, use_container_width=True)

    st.info("Dashboard currently uses sample data. Connect your agency data sources for live metrics.")

elif page == "AI Employees":
    st.header("Meet Your AI Employees")
    for employee in employees:
        st.write("🤖", employee)

elif page == "Client Management":
    st.header("Client Management")
    st.write("Manage agency clients and their SEO projects.")
    client_name = st.text_input("Client name")
    website = st.text_input("Client website")
    if st.button("Add client"):
        if client_name and website:
            st.success(f"Client {client_name} entered. Connect persistent storage to save it.")
        else:
            st.warning("Please enter both client name and website.")

elif page == "Task Management":
    st.header("Task Management")
    st.dataframe(tasks, use_container_width=True)
    new_task = st.text_input("New task")
    if st.button("Create task"):
        if new_task:
            st.success(f"Task '{new_task}' prepared. Connect task storage to save it.")
        else:
            st.warning("Enter a task name.")

elif page == "SEO Performance":
    st.header("SEO Performance Dashboard")
    performance = pd.DataFrame({
        "Metric": ["Organic Traffic", "Keywords Tracked", "Backlinks", "SEO Score"],
        "Value": [1250, 85, 240, 78]
    })
    st.bar_chart(performance.set_index("Metric"))
    st.caption("Illustrative sample metrics, not verified live SEO results.")

elif page == "Reports":
    st.header("Agency Reports")
    st.write("Generate and review agency performance reports.")
    st.write("Last dashboard view:", datetime.now().strftime("%d %B %Y, %H:%M"))

st.divider()
st.caption("Mary Akhila | Autonomous SEO Agency | AI-powered workflow prototype")
