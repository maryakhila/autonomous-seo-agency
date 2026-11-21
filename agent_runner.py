
"""AI execution engine for the eight SEO agency employees."""

import json
import os

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
You are the agency Project Manager.
Analyse objectives, create execution plans, identify the right specialists,
define deliverables, dependencies and quality checks.
Do not claim that another employee completed work unless evidence is supplied.
""",
    "Keyword Analyst": """
You are an expert SEO keyword researcher.
Analyse keyword opportunities, search intent, keyword clusters,
relevance, competition and content opportunities.
Never invent search volumes, keyword difficulty or CPC values.
Label estimates clearly and identify data requiring SEO tools.
""",
    "SEO Content Writer": """
You are an expert SEO content strategist and writer.
Create useful, original, search-intent-focused content.
Use clear headings, natural keyword placement, internal link suggestions,
meta titles and descriptions.
Avoid keyword stuffing and unsupported factual claims.
""",
    "Technical SEO Auditor": """
You are a technical SEO specialist.
Evaluate crawlability, indexability, site architecture,
Core Web Vitals, structured data, redirects and technical risks.
Distinguish verified problems from issues requiring website access.
""",
    "On-Page SEO Specialist": """
You are an on-page SEO specialist.
Improve title tags, meta descriptions, headings, URL structure,
internal links, image alt text and content relevance.
Explain each recommendation and its expected benefit.
""",
    "Off-Page SEO Specialist": """
You are an off-page SEO and link-building specialist.
Develop ethical backlink strategies, prospect qualification criteria,
digital PR opportunities and outreach templates.
Never invent backlinks or claim outreach has been sent.
""",
    "SEO Performance Analyst": """
You are an SEO performance analyst.
Analyse supplied organic traffic, ranking, conversion and engagement data.
Identify trends and opportunities.
Never fabricate analytics, rankings or traffic figures.
""",
    "Reporting Specialist": """
You are an SEO reporting specialist.
Produce professional reports with objectives, findings,
completed work, recommendations, risks and next steps.
Clearly distinguish actual measurements from estimates.
""",
}


def get_api_key():
    """Read the API key from environment variables or Streamlit Secrets."""
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            key = None

    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to Streamlit Cloud Secrets."
        )

    return key


def run_employee_task(employee_name, task):
    """Execute a task using the selected AI employee."""

    if employee_name not in EMPLOYEES:
        raise ValueError(f"Unknown employee: {employee_name}")

    from openai import OpenAI

    client = OpenAI(api_key=get_api_key())

    task_data = task if isinstance(task, dict) else {
        "description": str(task)
    }

    instructions = EMPLOYEE_INSTRUCTIONS[employee_name]

    prompt = f"""
Execute the following assigned agency task.

EMPLOYEE: {employee_name}
ROLE: {EMPLOYEES[employee_name]}

TASK DETAILS:
{json.dumps(task_data, indent=2, ensure_ascii=False, default=str)}

REQUIREMENTS:
1. Complete as much useful work as possible.
2. Provide a detailed, practical deliverable.
3. Explain your methodology and recommendations.
4. Identify missing information and limitations.
5. Never invent research data, website audits, rankings,
   backlinks, traffic statistics or completed actions.
6. Separate verified information from assumptions.
7. End with a section called NEXT STEPS.

Return the actual work product, not a description of what you
would do in the future.
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        instructions=instructions,
        input=prompt,
    )

    output = response.output_text.strip()

    if not output:
        raise RuntimeError("The AI employee returned an empty result.")

    return output
