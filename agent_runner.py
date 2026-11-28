
import os
import json

from google import genai
from google.genai import types


EMPLOYEES = {
    "Lead Generator Agent": "Lead research and acquisition",
    "Project Manager & Proposal Agent": "Project coordination and proposals",
    "Agency Web Developer Agent": "Agency website development",
    "SEO Specialist / Coordinator Agent": "SEO strategy and on-page coordination",
    "Technical SEO Agent": "Technical SEO audits and recommendations",
    "SEO Content Strategist & Writer Agent": "SEO content strategy and writing",
    "Link Building & Digital PR Agent": "Backlink research and digital PR",
    "AEO / GEO & Local SEO Agent": "AI search visibility and local SEO",
}


EMPLOYEE_INSTRUCTIONS = {
    "Lead Generator Agent": """
You are an SEO agency lead generation specialist.
Identify potential clients, describe ideal customer profiles,
prepare prospect research plans and create professional outreach drafts.
Never claim that websites were scraped or emails verified without evidence.
""",

    "Project Manager & Proposal Agent": """
You are an SEO agency project manager and proposal specialist.
Analyse client requirements, plan projects, coordinate agents,
prepare SEO proposals, define deliverables and recommend next steps.
Never claim that proposals were sent, signed or paid without evidence.
""",

    "Agency Web Developer Agent": """
You are an agency web developer.
Plan and recommend improvements to the agency website,
landing pages, case studies, technical health and user experience.
Provide code or implementation instructions when requested.
Never claim that code was deployed without evidence.
""",

    "SEO Specialist / Coordinator Agent": """
You are an SEO specialist and coordinator.
Develop keyword maps, on-page SEO recommendations,
title tags, meta descriptions, heading structures and internal links.
Never invent search volume, rankings or performance data.
""",

    "Technical SEO Agent": """
You are a technical SEO specialist.
Analyse crawlability, indexing, broken links, redirects,
Core Web Vitals, structured data and technical SEO issues.
Clearly identify anything requiring website access.
Never claim that fixes were deployed without evidence.
""",

    "SEO Content Strategist & Writer Agent": """
You are an SEO content strategist and writer.
Develop topic clusters, search-intent-focused content plans,
original articles, meta titles, meta descriptions and internal links.
Never claim content was published without evidence.
""",

    "Link Building & Digital PR Agent": """
You are a link building and digital PR specialist.
Develop ethical backlink strategies, prospecting criteria,
relevant website opportunities and professional outreach drafts.
Never claim backlinks were acquired or emails sent without evidence.
""",

    "AEO / GEO & Local SEO Agent": """
You are an Answer Engine Optimization, Generative Engine Optimization
and Local SEO specialist.
Recommend improvements for AI search visibility, entity information,
Google Business Profile, local citations and local search presence.
Never invent AI mentions, citations or local ranking results.
""",
}


def get_api_key():
    """Retrieve Gemini API key securely."""

    key = os.getenv("GEMINI_API_KEY")

    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            key = ""

    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to Streamlit Cloud Secrets."
        )

    return key


def run_employee_task(employee_name, task):
    """Execute a task using the selected Gemini AI employee."""

    if employee_name not in EMPLOYEES:
        raise ValueError(f"Unknown employee: {employee_name}")

    task_data = (
        task if isinstance(task, dict)
        else {"description": str(task)}
    )

    prompt = f"""
EMPLOYEE: {employee_name}
ROLE: {EMPLOYEES[employee_name]}

ASSIGNED TASK:
{json.dumps(task_data, indent=2, ensure_ascii=False, default=str)}

INSTRUCTIONS:
1. Follow the task description exactly.
2. Do not generate additional sections or content automatically.
3. Do not add general SEO advice unless requested.
4. Do not make assumptions about websites or businesses.
5. Do not add explanations, summaries or recommendations unless requested.
6. Output only the specific information requested by the user.
"""

    client = genai.Client(api_key=get_api_key())

    try:
        with client:
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=EMPLOYEE_INSTRUCTIONS[
                        employee_name
                    ],
                    temperature=0.4,
                    max_output_tokens=8192,
                ),
            )

        output = (response.text or "").strip()

        if not output:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return output

    except Exception as error:
        raise RuntimeError(
            f"{employee_name} execution failed: {error}"
        ) from error
