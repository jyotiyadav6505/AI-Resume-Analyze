import streamlit as st

from resume_parser import extract_resume_text
from analyzer import analyze_resume
from utils import clean_text


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------
# Custom Styling
# -----------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 25px;
    }

    .score-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    .score-number {
        font-size: 48px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Header
# -----------------------------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume using AI and get actionable career insights.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------
# Resume Upload
# -----------------------------------

st.subheader("📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)


# -----------------------------------
# Job Description
# -----------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here (optional)",
    height=200,
    placeholder=(
        "Example: We are looking for a Python Developer "
        "with experience in Python, SQL, Git, APIs..."
    )
)


# -----------------------------------
# Analyze Resume
# -----------------------------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name} ✅"
    )

    if st.button(
        "🤖 Analyze Resume",
        use_container_width=True
    ):

        with st.spinner(
            "AI is analyzing your resume..."
        ):

            try:

                # -----------------------------------
                # Extract Resume Text
                # -----------------------------------

                resume_text = extract_resume_text(
                    uploaded_file
                )

                resume_text = clean_text(
                    resume_text
                )

                if not resume_text:

                    st.error(
                        "Unable to extract text from this PDF."
                    )

                    st.stop()


                # -----------------------------------
                # Add Job Description
                # -----------------------------------

                if job_description.strip():

                    resume_text += f"""

JOB DESCRIPTION:
----------------
{job_description}
----------------
"""


                # -----------------------------------
                # AI Analysis
                # -----------------------------------

                result = analyze_resume(
                    resume_text
                )


                # -----------------------------------
                # Handle Text Response
                # -----------------------------------

                if isinstance(result, str):

                    st.success(
                        "Resume analysis completed! 🎉"
                    )

                    st.subheader(
                        "🤖 AI Resume Feedback"
                    )

                    st.markdown(
                        result
                    )

                    st.info(
                        "The AI returned a text-based analysis."
                    )

                    st.stop()


                # -----------------------------------
                # Success
                # -----------------------------------

                st.success(
                    "Resume analysis completed! 🎉"
                )

                st.divider()


                # -----------------------------------
                # Scores
                # -----------------------------------

                ats_score = result.get(
                    "ats_score",
                    0
                )

                job_match_score = result.get(
                    "job_match_score",
                    0
                )


                score_col1, score_col2 = st.columns(2)


                # ATS Score
                with score_col1:

                    st.subheader(
                        "📊 ATS Score"
                    )

                    st.metric(
                        "Resume ATS Score",
                        f"{ats_score}/100"
                    )

                    st.progress(
                        min(
                            max(
                                float(ats_score),
                                0
                            ),
                            100
                        ) / 100
                    )


                # Job Match Score
                with score_col2:

                    st.subheader(
                        "🎯 Job Match Score"
                    )

                    if job_description.strip():

                        st.metric(
                            "Resume ↔ Job Match",
                            f"{job_match_score}%"
                        )

                        st.progress(
                            min(
                                max(
                                    float(job_match_score),
                                    0
                                ),
                                100
                            ) / 100
                        )

                    else:

                        st.info(
                            "Add a job description "
                            "to calculate the match score."
                        )


                st.divider()


                # -----------------------------------
                # Summary
                # -----------------------------------

                st.subheader(
                    "📝 Resume Summary"
                )

                summary = result.get(
                    "summary",
                    "No summary available."
                )

                st.write(summary)


                # -----------------------------------
                # Skills
                # -----------------------------------

                st.subheader(
                    "🛠️ Skills Detected"
                )

                skills = result.get(
                    "skills",
                    []
                )

                if skills:

                    skill_columns = st.columns(
                        min(
                            len(skills),
                            4
                        )
                    )

                    for index, skill in enumerate(
                        skills
                    ):

                        skill_columns[
                            index % len(skill_columns)
                        ].success(
                            skill
                        )

                else:

                    st.info(
                        "No skills detected."
                    )


                # -----------------------------------
                # Matching & Missing Skills
                # -----------------------------------

                matching_skills = result.get(
                    "matching_skills",
                    []
                )

                missing_skills = result.get(
                    "missing_skills",
                    []
                )


                if job_description.strip():

                    match_col, missing_col = st.columns(2)


                    with match_col:

                        st.subheader(
                            "✅ Matching Skills"
                        )

                        if matching_skills:

                            for skill in matching_skills:

                                st.write(
                                    f"✅ {skill}"
                                )

                        else:

                            st.info(
                                "No matching skills detected."
                            )


                    with missing_col:

                        st.subheader(
                            "❌ Missing Skills"
                        )

                        if missing_skills:

                            for skill in missing_skills:

                                st.write(
                                    f"❌ {skill}"
                                )

                        else:

                            st.success(
                                "No major missing skills detected."
                            )


                    st.divider()


                    # -----------------------------------
                    # Job Keywords
                    # -----------------------------------

                    st.subheader(
                        "🔑 Job-Specific Keywords"
                    )

                    job_keywords = result.get(
                        "job_keywords",
                        []
                    )

                    if job_keywords:

                        st.write(
                            " • ".join(
                                job_keywords
                            )
                        )

                    else:

                        st.info(
                            "No job keywords detected."
                        )


                # -----------------------------------
                # Strengths & Weaknesses
                # -----------------------------------

                col1, col2 = st.columns(2)


                with col1:

                    st.subheader(
                        "💪 Strengths"
                    )

                    strengths = result.get(
                        "strengths",
                        []
                    )

                    for item in strengths:

                        st.write(
                            f"✅ {item}"
                        )


                with col2:

                    st.subheader(
                        "⚠️ Weaknesses"
                    )

                    weaknesses = result.get(
                        "weaknesses",
                        []
                    )

                    for item in weaknesses:

                        st.write(
                            f"⚠️ {item}"
                        )


                st.divider()


                # -----------------------------------
                # Recommended Skills
                # -----------------------------------

                st.subheader(
                    "🎯 Recommended Skills"
                )

                recommended_skills = result.get(
                    "recommended_skills",
                    []
                )

                for skill in recommended_skills:

                    st.write(
                        f"➕ {skill}"
                    )


                # -----------------------------------
                # Suitable Job Roles
                # -----------------------------------

                st.subheader(
                    "💼 Suitable Job Roles"
                )

                job_roles = result.get(
                    "job_roles",
                    []
                )

                for role in job_roles:

                    st.write(
                        f"🔹 {role}"
                    )


                # -----------------------------------
                # ATS Keywords
                # -----------------------------------

                st.subheader(
                    "🔑 Important ATS Keywords"
                )

                keywords = result.get(
                    "ats_keywords",
                    []
                )

                if keywords:

                    st.write(
                        " • ".join(
                            keywords
                        )
                    )


                # -----------------------------------
                # Improvements
                # -----------------------------------

                st.subheader(
                    "💡 Resume Improvements"
                )

                improvements = result.get(
                    "improvements",
                    []
                )

                for improvement in improvements:

                    st.write(
                        f"💡 {improvement}"
                    )


                # -----------------------------------
                # Download Report
                # -----------------------------------

                st.divider()

                st.subheader(
                    "📥 Download Analysis"
                )


                strengths_text = "\n".join(
                    f"- {item}"
                    for item in strengths
                )

                weaknesses_text = "\n".join(
                    f"- {item}"
                    for item in weaknesses
                )

                recommended_text = "\n".join(
                    f"- {item}"
                    for item in recommended_skills
                )

                job_roles_text = "\n".join(
                    f"- {item}"
                    for item in job_roles
                )

                matching_text = "\n".join(
                    f"- {item}"
                    for item in matching_skills
                )

                missing_text = "\n".join(
                    f"- {item}"
                    for item in missing_skills
                )

                improvements_text = "\n".join(
                    f"- {item}"
                    for item in improvements
                )


                report = f"""
AI RESUME ANALYZER REPORT
=========================

RESUME:
{uploaded_file.name}

ATS SCORE:
{ats_score}/100

JOB MATCH SCORE:
{
    str(job_match_score) + "%"
    if job_description.strip()
    else "N/A"
}


RESUME SUMMARY:
{summary}


SKILLS DETECTED:
{", ".join(skills)}


STRENGTHS:
{strengths_text}


WEAKNESSES:
{weaknesses_text}


RECOMMENDED SKILLS:
{recommended_text}


SUITABLE JOB ROLES:
{job_roles_text}


ATS KEYWORDS:
{", ".join(keywords)}


MATCHING SKILLS:
{matching_text}


MISSING SKILLS:
{missing_text}


JOB KEYWORDS:
{", ".join(
    result.get("job_keywords", [])
)}


IMPROVEMENTS:
{improvements_text}
"""


                st.download_button(
                    label="📥 Download Resume Analysis",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )