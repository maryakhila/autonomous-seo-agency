
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
    create_lead,
    list_leads,
    update_lead,
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
from lead_generator import analyze_seo_lead


st.set_page_config(
    page_title="Autonomous SEO Agency | Boss Command Center",
    page_icon="📈",
    layout="wide",
)

init_db()


# =====================================================
# LOGIN
# =====================================================

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
