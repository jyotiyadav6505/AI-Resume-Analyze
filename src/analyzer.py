import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)


def analyze_resume(resume_text):
    """Analyze resume and compare it with a job description."""

    prompt = f"""
You are an expert ATS resume reviewer and technical recruiter.

Analyze the resume and job description below.

IMPORTANT:
Return ONLY valid JSON.
Do not use Markdown.
Do not use ```json.
Do not write any explanation outside the JSON.

Return exactly these fields:

{{
    "ats_score": 0,
    "job_match_score": 0,
    "summary": "",
    "skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommended_skills": [],
    "job_roles": [],
    "ats_keywords": [],
    "matching_skills": [],
    "missing_skills": [],
    "job_keywords": [],
    "improvements": []
}}

Rules:

1. ats_score must be a number from 0 to 100.
2. job_match_score must be a number from 0 to 100.
3. Calculate job_match_score by comparing the resume against the JOB DESCRIPTION.
4. If there is no job description, job_match_score must be 0.
5. skills must contain skills actually present in the resume.
6. matching_skills must contain skills present in both the resume and job description.
7. missing_skills must contain important requirements from the job description that are not clearly present in the resume.
8. job_keywords must contain important keywords from the job description.
9. Do not invent experience, education, projects, or skills.
10. strengths and weaknesses should be based on the actual resume.
11. improvements should be practical and specific.

RESUME AND JOB DESCRIPTION:
----------------------------
{resume_text}
----------------------------
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove Markdown code fences if Gemini adds them
    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json",
            ""
        )
        response_text = response_text.replace(
            "```",
            ""
        )
        response_text = response_text.strip()

    try:
        result = json.loads(response_text)

        # Make sure the required scores exist
        if "ats_score" not in result:
            result["ats_score"] = 0

        if "job_match_score" not in result:
            result["job_match_score"] = 0

        return result

    except json.JSONDecodeError:
        return response_text