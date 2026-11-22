
import requests
import streamlit as st


def sheet_is_configured():
    return bool(
        st.secrets.get("APPS_SCRIPT_WEB_APP_URL")
        and st.secrets.get("APPS_SCRIPT_SHARED_SECRET")
    )


def sync_task_to_sheet(task):
    if not sheet_is_configured():
        st.warning("Google Sheets settings are missing.")
        return False

    try:
        task_data = dict(task)

        payload = {
            "token": st.secrets["APPS_SCRIPT_SHARED_SECRET"],
            "action": "upsertTask",
            "task": {
                "id": task_data.get("id", ""),
                "created_at": task_data.get("created_at", ""),
                "assigned_by": task_data.get("assigned_by", ""),
                "agent_name": task_data.get("agent_name", ""),
                "description": task_data.get("description", ""),
                "priority": task_data.get("priority", ""),
                "status": task_data.get("status", "Pending"),
                "output_link": task_data.get("output_link", ""),
                "completed_at": task_data.get("completed_at", "")
            }
        }

        response = requests.post(
            st.secrets["APPS_SCRIPT_WEB_APP_URL"],
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            st.error(
                "Google Sheets rejected the task: "
                + str(result.get("error", result.get("message", "Unknown error")))
            )
            return False

        return True

    except Exception as error:
        st.error(f"Google Sheets sync failed: {error}")
        return False
