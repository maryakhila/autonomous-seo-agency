import streamlit as st

HEADERS = ["Task ID","Timestamp","Assigned By","Agent Name","Task Description","Priority",
           "Status (Queued / In Progress / Blocked / Completed)","Output / Result Link","Completion Time"]

def _client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        cfg=dict(st.secrets["gcp_service_account"])
        creds=Credentials.from_service_account_info(cfg, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
        return gspread.authorize(creds)
    except Exception:
        return None

def sheet_is_configured():
    try: return bool(st.secrets["GOOGLE_SHEET_ID"]) and _client() is not None
    except Exception: return False

def sync_task_to_sheet(task):
    if not task: return False
    try:
        sheet_id=st.secrets["GOOGLE_SHEET_ID"]
        client=_client()
        if client is None: return False
        sh=client.open_by_key(sheet_id)
        ws=sh.sheet1
        if not ws.get_all_values():
            ws.append_row(HEADERS)
        values=ws.get_all_values()
        row=[
            str(task["id"]), task["created_at"], task["assigned_by"], task["agent_name"],
            task["description"], task["priority"], task["status"], task["output_link"] or "",
            task["completed_at"] or ""
        ]
        # Upsert by Task ID in first column.
        existing=next((i+1 for i,r in enumerate(values[1:], start=1) if r and r[0]==str(task["id"])),None)
        if existing: ws.update(f"A{existing}:I{existing}", [row])
        else: ws.append_row(row)
        return True
    except Exception:
        return False
