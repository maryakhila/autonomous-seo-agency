
"""Gemini-powered SEO lead analysis."""

import os
import re
import streamlit as st
from google import genai
from google.genai import types


def get_gemini_client():
    """Create Gemini client using configured API key."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from Streamlit Secrets."
        )

    return genai.Client(api_key=api_key)


def analyze_seo_lead(
    business_name,
    website,
    city="",
    country="",
    niche="Other",
):
    """Analyze supplied website content with Gemini."""

    if not business_name.strip():
        raise ValueError("Business name is required.")

    if not website.strip():
        raise ValueError("Website URL is required.")

    client = get_gemini_client()

    prompt = f"""
You are an expert local SEO consultant and lead qualification agent.

Analyze this potential SEO client.

Business name: {business_name}
Website: {website}
City: {city}
Country: {country}
Business niche: {niche}

IMPORTANT:
- You may not be able to access the live website.
- Do not claim that you visited or crawled the website.
- Do not invent SEO errors or technical findings.
- Clearly separate observations from items that need verification.
- Return a practical sales opportunity assessment.

Provide:

1. Business overview
2. Potential SEO opportunities
3. Local SEO improvement opportunities
4. Website content recommendations
5. Technical SEO checks that should be performed
6. Suggested SEO services to offer
7. Suggested personalized outreach message
8. SEO opportunity score from 0 to 100
9. Confidence level: Low, Medium, or High
10. Information that still needs verification

Return the answer in clear Markdown.

At the end include exactly:

SEO_SCORE: [number]
CONFIDENCE: [Low/Medium/High]
"""

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=4096,
        ),
    )

    output = response.text

    if not output:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    score_match = re.search(
        r"SEO_SCORE:\s*(\d{1,3})",
        output,
        re.IGNORECASE,
    )

    confidence_match = re.search(
        r"CONFIDENCE:\s*(Low|Medium|High)",
        output,
        re.IGNORECASE,
    )

    score = 0

    if score_match:
        score = min(100, max(0, int(score_match.group(1))))

    confidence = (
        confidence_match.group(1).capitalize()
        if confidence_match
        else "Low"
    )

    return {
        "business_name": business_name,
        "website": website,
        "seo_score": score,
        "confidence": confidence,
        "analysis": output,
    }

