import os
import tempfile
import json
import time
import streamlit as st

from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.search.job_matcher import recommend_jobs


st.set_page_config(
    page_title="SmartHire GenAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME-SAFE UI
# Works with Streamlit Light Mode and Dark Mode
# ============================================================

st.markdown(
    """
    <style>

    /* Main content */
    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }


    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
    }


    /* Normal text */
    p, span, label {
        color: var(--text-color);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }


    /* Metric label */
    div[data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
    }


    div[data-testid="stMetricLabel"] * {
        color: var(--text-color) !important;
    }


    /* Metric value */
    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }


    div[data-testid="stMetricValue"] * {
        color: var(--text-color) !important;
    }


    /* Metric delta */
    div[data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }


    div[data-testid="stMetricDelta"] * {
        color: var(--text-color) !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: bold;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        border: 2px dashed #2563EB;
        border-radius: 12px;
        padding: 10px;
    }


    [data-testid="stFileUploader"] label {
        color: var(--text-color) !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input,
    textarea {
        color: var(--text-color) !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }


    section[data-testid="stSidebar"] * {
        color: var(--text-color);
    }


    /* Sidebar metrics */
    section[data-testid="stSidebar"]
    div[data-testid="stMetric"] {
        background-color: var(--background-color) !important;
        border: 1px solid var(--border-color) !important;
    }


    /* ========================================================
       MARKDOWN
       ======================================================== */

    .stMarkdown {
        color: var(--text-color);
    }


    /* ========================================================
       CAPTION
       ======================================================== */

    [data-testid="stCaptionContainer"] {
        color: var(--text-color) !important;
    }


    /* ========================================================
       TEXT AREAS
       ======================================================== */

    textarea {
        background-color: var(--secondary-background-color) !important;
    }


    /* ========================================================
       ALERT BOXES
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    [data-testid="stProgress"] {
        border-radius: 10px;
    }


    /* ========================================================
       LINKS
       ======================================================== */

    a {
        color: #2563EB;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 SmartHire GenAI")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📄 Resume Parser",
        "💼 Job Matching",
        "📈 Resume Suggestions",
        "✉️ Cover Letter",
        "🎤 Interview Questions",
        "🧠 Career Mentor"
    ]
)

st.sidebar.markdown("---")

st.sidebar.metric("🤖 AI Modules", "7")
st.sidebar.metric("📄 Resume Formats", "PDF")
st.sidebar.metric("🧠 LLM", "Llama 3.1")
st.sidebar.metric("🔍 Search", "Semantic")


# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.title("🤖 SmartHire GenAI")

    st.subheader(
        "AI Powered Resume Analyzer & Job Recommendation System"
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Resume Parser", "AI")

    with col2:
        st.metric("💼 Job Matching", "RAG")

    with col3:
        st.metric("🧠 Career Mentor", "LLM")


    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("📈 Resume Review", "AI")

    with col5:
        st.metric("✉️ Cover Letter", "GenAI")

    with col6:
        st.metric("🎤 Interview", "AI")


    st.markdown("---")

    st.markdown("## ✨ Features")

    features = [
        "Resume Parsing using LLM",
        "Semantic Job Matching (RAG)",
        "Resume Suggestions",
        "AI Cover Letter Generator",
        "Interview Question Generator",
        "AI Career Mentor"
    ]

    for feature in features:
        st.write("✅", feature)

    st.markdown("---")

    st.success(
        "🚀 Upload your resume and start exploring AI-powered career assistance."
    )


# ============================================================
# RESUME PARSER
# ============================================================

elif menu == "📄 Resume Parser":

    st.header("📄 AI Resume Parser")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="parser"
    )

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        try:

            st.success("✅ Resume Uploaded Successfully")

            text = extract_text_from_pdf(pdf_path)

            with st.spinner("🤖 Parsing Resume..."):

                start = time.time()

                result = parse_resume(text)

                end = time.time()


            if "error" in result:

                st.error(result["error"])

            else:

                st.success("🎉 Resume Parsed Successfully")

                st.caption(
                    f"⚡ Parsed in {end - start:.2f} seconds"
                )


                st.download_button(
                    "📥 Download Parsed Resume",
                    data=json.dumps(result, indent=4),
                    file_name="parsed_resume.json",
                    mime="application/json"
                )


                st.markdown("## 📊 Resume Overview")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "🛠 Skills",
                    len(result.get("skills", []))
                )

                col2.metric(
                    "🎓 Education",
                    len(result.get("education", []))
                )

                col3.metric(
                    "💼 Experience",
                    len(result.get("experience", []))
                )

                col4.metric(
                    "📜 Certifications",
                    len(result.get("certifications", []))
                )


                st.markdown("---")

                st.markdown("## 👤 Personal Information")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "👤 Name",
                        result.get("name", "N/A")
                    )

                with col2:
                    st.metric(
                        "📱 Phone",
                        result.get("phone", "N/A")
                    )

                st.metric(
                    "📧 Email",
                    result.get("email", "N/A")
                )


                st.markdown("---")

                st.markdown("## 🛠 Skills")

                skills = result.get("skills", [])

                if skills:

                    skill_html = ""

                    for skill in skills:

                        skill_html += f"""
                        <span style="
                            background:#2563EB;
                            color:white !important;
                            padding:8px 15px;
                            border-radius:20px;
                            margin:5px;
                            display:inline-block;
                            font-weight:bold;
                        ">
                            {skill}
                        </span>
                        """

                    st.markdown(
                        skill_html,
                        unsafe_allow_html=True
                    )

                else:

                    st.warning("No skills detected.")


                st.markdown("## 🎓 Education")

                education = result.get("education", [])

                if education:

                    for edu in education:

                        st.info(
                            f"""
### 🎓 {edu.get("degree", "")}

🏫 **Institution:** {edu.get("institution", "")}

📅 **Duration:** {edu.get("duration", "")}

⭐ **CGPA:** {edu.get("cgpa", "")}
"""
                        )

                else:

                    st.warning(
                        "Education details not found."
                    )


                st.markdown("---")

                st.markdown("## 💼 Experience")

                experience = result.get("experience", [])

                if experience:

                    for exp in experience:

                        st.success(
                            f"""
### 💼 {exp.get("position", "")}

🏢 **Company:** {exp.get("company", "")}

📍 **Location:** {exp.get("location", "")}

📅 **Duration:** {exp.get("duration", "")}
"""
                        )

                else:

                    st.warning(
                        "Experience details not found."
                    )

        finally:

            if os.path.exists(pdf_path):
                os.remove(pdf_path)


# ============================================================
# JOB MATCHING
# ============================================================

elif menu == "💼 Job Matching":

    st.header("💼 AI Job Recommendation")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="job_match"
    )

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        try:

            st.success("✅ Resume Uploaded Successfully")

            text = extract_text_from_pdf(pdf_path)

            with st.spinner("🤖 Parsing Resume..."):

                resume = parse_resume(text)


            if "error" in resume:

                st.error(resume["error"])

            else:

                with st.spinner(
                    "🔍 Finding Best Matching Jobs..."
                ):

                    jobs = recommend_jobs(
                        resume.get("skills", [])
                    )


                st.success("🎯 Top Job Recommendations")

                if len(jobs) == 0:

                    st.warning(
                        "No matching jobs found."
                    )

                else:

                    for index, job in enumerate(jobs):

                        st.markdown("---")

                        col1, col2 = st.columns([4, 1])

                        with col1:

                            st.subheader(
                                f"💼 {job.get('title', 'Unknown Job')}"
                            )

                            st.write(
                                f"🏢 **Company:** "
                                f"{job.get('company', 'N/A')}"
                            )

                            st.write(
                                f"📍 **Location:** "
                                f"{job.get('location', 'N/A')}"
                            )

                            st.write(
                                "🛠 **Required Skills**"
                            )

                            skills = job.get(
                                "skills",
                                []
                            )

                            if skills:

                                skill_cols = st.columns(3)

                                for i, skill in enumerate(skills):

                                    skill_cols[
                                        i % 3
                                    ].info(skill)


                        with col2:

                            score = float(
                                job.get(
                                    "match_score",
                                    0
                                )
                            )

                            st.metric(
                                "Match",
                                f"{score:.1f}%"
                            )


                        progress_value = max(
                            0.0,
                            min(score / 100, 1.0)
                        )

                        st.progress(progress_value)


                        if index == 0:

                            st.success(
                                "🏆 Best Match"
                            )

                        elif score >= 80:

                            st.success(
                                "⭐ Highly Recommended"
                            )

                        elif score >= 60:

                            st.info(
                                "👍 Good Match"
                            )

                        else:

                            st.warning(
                                "⚠️ Average Match"
                            )

        finally:

            if os.path.exists(pdf_path):
                os.remove(pdf_path)


# ============================================================
# RESUME SUGGESTIONS
# ============================================================

elif menu == "📈 Resume Suggestions":

    from src.generate.resume_suggestions import improve_resume
    from src.generate.resume_score import calculate_resume_score

    st.header("📈 AI Resume Suggestions")

    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"],
        key="resume_suggestions"
    )

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        try:

            text = extract_text_from_pdf(pdf_path)

            result = parse_resume(text)

            if "error" in result:

                st.error(result["error"])

            else:

                feedback = improve_resume(result)

                score_data = calculate_resume_score(result)

                st.success(
                    "✅ AI Resume Analysis Completed"
                )


                st.subheader("⭐ Resume Score")

                score = score_data["score"]

                st.progress(score / 100)

                st.metric(
                    label="Overall Resume Score",
                    value=f"{score}/100"
                )


                st.subheader("💪 Strengths")

                if score_data["strengths"]:

                    for item in score_data["strengths"]:

                        st.success(item)

                else:

                    st.info(
                        "No strengths detected."
                    )


                st.subheader("⚠️ Weaknesses")

                if score_data["weaknesses"]:

                    for item in score_data["weaknesses"]:

                        st.error(item)

                else:

                    st.success(
                        "No major weaknesses found."
                    )


                st.subheader("🚀 Suggestions")

                if score_data["suggestions"]:

                    for item in score_data["suggestions"]:

                        st.info(item)


                st.markdown("---")

                st.subheader(
                    "🤖 AI Detailed Feedback"
                )

                st.markdown(feedback)

        finally:

            if os.path.exists(pdf_path):
                os.remove(pdf_path)


# ============================================================
# COVER LETTER
# ============================================================

elif menu == "✉️ Cover Letter":

    from src.generate.cover_letter import generate_cover_letter

    st.header(
        "✉️ AI Cover Letter Generator"
    )

    job_title = st.text_input(
        "💼 Enter Job Title",
        placeholder="Example: Python Full Stack Developer"
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"],
        key="cover_letter"
    )

    if uploaded_file is not None and job_title:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        try:

            text = extract_text_from_pdf(pdf_path)

            with st.spinner("🤖 Parsing Resume..."):

                resume = parse_resume(text)


            if "error" in resume:

                st.error(resume["error"])

            else:

                with st.spinner(
                    "✍️ Generating Cover Letter..."
                ):

                    letter = generate_cover_letter(
                        resume,
                        job_title
                    )


                st.success(
                    "✅ Cover Letter Generated Successfully"
                )

                st.markdown(
                    "## 📄 Generated Cover Letter"
                )

                st.text_area(
                    "Cover Letter",
                    value=letter,
                    height=450
                )

                st.download_button(
                    "📥 Download Cover Letter",
                    data=letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )

        finally:

            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    elif uploaded_file is not None:

        st.warning(
            "⚠️ Please enter the Job Title."
        )


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

elif menu == "🎤 Interview Questions":

    from src.generate.interview_questions import (
        generate_interview_questions
    )

    st.header(
        "🎤 AI Interview Question Generator"
    )

    job_title = st.text_input(
        "💼 Enter Job Title",
        placeholder="Example: Python Full Stack Developer",
        key="interview_job"
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"],
        key="interview_resume"
    )

    if uploaded_file is not None and job_title:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        try:

            text = extract_text_from_pdf(pdf_path)

            with st.spinner(
                "🤖 Parsing Resume..."
            ):

                resume = parse_resume(text)


            if "error" in resume:

                st.error(resume["error"])

            else:

                with st.spinner(
                    "🎯 Generating Interview Questions..."
                ):

                    questions = generate_interview_questions(
                        resume,
                        job_title
                    )


                st.success(
                    "✅ Interview Questions Generated"
                )

                st.markdown(
                    "## 📚 Practice Questions"
                )

                st.text_area(
                    "Generated Questions",
                    value=questions,
                    height=500
                )

                st.download_button(
                    "📥 Download Questions",
                    data=questions,
                    file_name="interview_questions.txt",
                    mime="text/plain"
                )

                st.info(
                    "💡 Practice answering these questions aloud "
                    "to improve confidence."
                )

        finally:

            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    elif uploaded_file is not None:

        st.warning(
            "⚠️ Please enter the Job Title."
        )


# ============================================================
# CAREER MENTOR
# ============================================================

elif menu == "🧠 Career Mentor":

    from src.mentor.career_mentor import (
        load_knowledge,
        chunk_text,
        create_chunk_embeddings,
        ask_career_mentor
    )

    st.header("🧠 AI Career Mentor")

    st.caption(
        "Ask career-related questions and receive "
        "AI-powered guidance."
    )


    if "chunks" not in st.session_state:

        knowledge = load_knowledge()

        chunks = chunk_text(knowledge)

        embeddings = create_chunk_embeddings(
            chunks
        )

        st.session_state["chunks"] = chunks
        st.session_state["embeddings"] = embeddings


    if "messages" not in st.session_state:

        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    prompt = st.chat_input(
        "Ask your career question..."
    )


    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)


        with st.spinner(
            "🤖 Thinking..."
        ):

            answer = ask_career_mentor(
                prompt,
                st.session_state["chunks"],
                st.session_state["embeddings"]
            )


        with st.chat_message("assistant"):

            st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <center>
        🤖 <b>SmartHire GenAI</b><br>
        AI Powered Resume Analyzer & Job Recommendation System
        <br><br>
        Built with ❤️ using Streamlit, Groq LLM,
        Sentence Transformers & RAG
    </center>
    """,
    unsafe_allow_html=True
)