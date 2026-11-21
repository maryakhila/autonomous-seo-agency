# Autonomous SEO Agency — Boss Command Center

## Included
- Boss-only login (credentials configured in Streamlit Secrets)
- Eight employee roles: Project Manager + seven SEO specialists
- Task assignment, live task board, status updates, filters, task output and timestamps
- SQLite task and chat persistence for local development
- Google Sheets ledger upsert integration
- Daily email report generation and SMTP sending
- CSV task export and employee task KPIs
- Chat answers based on saved task records; explicitly refuses to invent missing leads/posts
- `.installed.json` employee/integration manifest

## Important limitations before grading
This is a connected foundation, not a finished autonomous agency. The employee execution adapters are intentionally unimplemented in `agent_runner.py`; connect your existing `agents/` and `src/` code there. Sales leads, content publication records and support tickets need their own real data tables/integrations before those KPIs can be reported. Chat task creation currently supports a simple phrase pattern, not unrestricted natural-language parsing.

For Streamlit Community Cloud, the local SQLite file may not be durable across restarts/redeployments. Use a managed PostgreSQL database for graded hosting and adapt `database.py` to that provider before relying on hosted persistence. Never claim data is persistent until tested.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

For local secrets, create `.streamlit/secrets.toml` from `.streamlit/secrets.toml.example` and fill in your own values. Do not commit `secrets.toml`.

## Deploy
1. Push this project to your GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the main file path to `streamlit_app.py`.
4. In App Settings → Secrets, add the values from the example secrets file.
5. Deploy and test login, task creation, status updates, Google Sheets sync and email.
6. Configure a managed database for durable hosted records.
7. Configure an external scheduler to run `python send_daily_email.py` daily. A continuously running Streamlit process is not a daily scheduler.

## Google Sheets setup
1. Create a Google Cloud service account and enable Google Sheets API and Google Drive API.
2. Download its JSON credentials.
3. Add those credentials under `[gcp_service_account]` in Streamlit Secrets.
4. Share the spreadsheet with the service account's `client_email` as Editor.
5. Put the spreadsheet ID in `GOOGLE_SHEET_ID`.

Ledger columns: Task ID, Timestamp, Assigned By, Agent Name, Task Description, Priority, Status, Output / Result Link, Completion Time.

## Gmail SMTP setup
Use a Google App Password (with 2-Step Verification enabled), not your normal Gmail password. Add SMTP settings to Streamlit Secrets. Test with the Integrations page.

## Security / academic honesty
The login is a basic single-Boss gate suitable for a course prototype, not enterprise-grade authentication. Use a strong password and do not publish credentials in GitHub. Do not use fabricated task results, leads, posts, or KPI values. Test every integration and show only real records in your demonstration.
