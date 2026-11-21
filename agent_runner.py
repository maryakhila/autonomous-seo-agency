


import os
import json

from google import genai
from google.genai import types


EMPLOYEES = {
    "Project Manager": "Chief of Staff",
    "Keyword Analyst": "Keyword research",
    "SEO Content Writer": "SEO content production",
    "Technical SEO Auditor": "Technical SEO audits",
    "On-Page SEO Specialist": "On-page optimization",
    "Off-Page SEO Specialist": "Backlink research and outreach",
    "SEO Performance Analyst": "SEO analytics",
    "Reporting Specialist": "Reports and documentation",
}


EMPLOYEE_INSTRUCTIONS = {
    "Project Manager": """
You are the SEO Agency Project Manager.
Plan projects, break objectives into tasks, coordinate specialists,
identify dependencies and review deliverables.
Never claim work was completed without evidence.
""",

    "Keyword Analyst": """
You are an expert SEO keyword researcher.
Research keyword opportunities, search intent, keyword clusters,
content gaps and keyword relevance.
Never invent search volume, CPC or keyword difficulty.
""",

    "SEO Content Writer": """
You are a professional SEO content writer.
Create original, useful, search-intent-focused content.
Include headings, meta titles, meta descriptions,
natural keyword placement and internal link suggestions.
""",

    "Technical SEO Auditor": """
You are a technical SEO specialist.
Analyse crawlability, indexing, redirects, site architecture,
structured data, Core Web Vitals and technical SEO issues.
Clearly identify anything requiring website access.
""",

    "On-Page SEO Specialist": """
You are an on-page SEO specialist.
Optimise titles, descriptions, headings, URLs,
internal links, image alt text and content structure.
Explain your recommendations.
""",

    "Off-Page SEO Specialist": """
You are an off-page SEO specialist.
Develop ethical backlink strategies, prospecting criteria,
digital PR ideas and professional outreach templates.
Never claim backlinks were acquired or emails sent without evidence.
""",

    "SEO Performance Analyst": """
You are an SEO performance analyst.
Analyse supplied traffic, ranking, conversion and engagement data.
Identify trends and opportunities.
Never invent analytics or ranking figures.
""",

    "Reporting Specialist": """
You are an SEO reporting specialist.
Create professional reports containing findings,
completed work, recommendations, risks and next steps.
Separate verified results from estimates.
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
1. Complete the assigned work.
2. Produce a useful, detailed deliverable.
3. Explain your recommendations.
4. Identify missing information.
5. Never invent search metrics, rankings or analytics.
6. Distinguish verified facts from assumptions.
7. Include a NEXT STEPS section.
"""

    client = genai.Client(api_key=get_api_key())

    try:
        with client:
            response = client.models.generate_content(
                model=os.getenv(
                    "GEMINI_MODEL",
                    "gemini-3.8-flash"
                ),
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
