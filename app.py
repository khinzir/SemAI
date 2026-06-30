
"""
SemAI - Complete Intelligent Tutoring System
Semester 1 Prototype with Full Features
"""
import streamlit as st
import os
import json
import uuid
import time
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SemAI - Intelligent Tutoring System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from config.course_structure import COURSE_STRUCTURE, get_chapters, get_subjects
from database.cosmos_client import CosmosClientManager
from utils.llm_client import LLMClient
from rag.search_client import SearchClientManager

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    /* Subject cards */
    .subject-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: 1px solid #e5e7eb;
        height: 260px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .subject-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }

    .subject-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .subject-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0.5rem 0;
        text-align: center;
    }

    .subject-code {
        font-size: 0.875rem;
        color: #6b7280;
        text-align: center;
    }

    /* Progress bar styling */
    .progress-container {
        margin: 1rem 0;
    }

    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
        font-size: 0.875rem;
        color: #4b5563;
    }

    .progress-bar {
        background-color: #e5e7eb;
        border-radius: 0.5rem;
        overflow: hidden;
        height: 0.75rem;
    }

    .progress-fill {
        background: linear-gradient(90deg, #10b981, #34d399);
        height: 100%;
        transition: width 0.3s ease;
        border-radius: 0.5rem;
    }

    /* Feature buttons */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .feature-card {
        background: #f9fafb;
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }

    .feature-card:hover {
        border-color: #667eea;
        background: #f3f4f6;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        font-weight: 600;
        color: #374151;
    }

    /* Chat interface */
    .chat-container {
        position: fixed;
        bottom: 0;
        right: 0;
        width: 400px;
        z-index: 1000;
    }

    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 1rem 1rem 0 0;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .chat-body {
        background: white;
        border-left: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
    }

    .message-user {
        background: #667eea;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        text-align: right;
        margin-left: 20%;
    }

    .message-bot {
        background: #f3f4f6;
        color: #1f2937;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 4px solid #667eea;
    }

    /* Syllabus styling */
    .syllabus-section {
        background: #f9fafb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: inherit;
        line-height: 1.6;
    }

    /* Sticky navigation */


    .nav-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .chat-container {
            width: 100%;
        }
        .nav-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .message-user {
            margin-left: 10%;
        }
        .message-bot {
            margin-right: 10%;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'selected_semester' not in st.session_state:
    st.session_state.selected_semester = 1
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'study_timers' not in st.session_state:
    st.session_state.study_timers = {}
if 'chat_expanded' not in st.session_state:
    st.session_state.chat_expanded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'subject_feature' not in st.session_state:
    st.session_state.subject_feature = "syllabus"

# Global clean naming map to ensure paths look up correctly
SUBJECT_FOLDER_MAP = {
    "C_Programming": "C_Programming",
    "DL": "DL",
    "IIT": "IIT",
    "Maths": "Maths",
    "Physics": "Physics"
}


# Initialize database and LLM clients
@st.cache_resource
def init_clients():
    db_client = CosmosClientManager()
    llm_client = LLMClient()
    search_client = SearchClientManager()
    return db_client, llm_client, search_client


db_client, llm_client, search_client = init_clients()


# ==================== UTILITY FUNCTIONS ====================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_icon(subject_code):
    icons = {
        "C_Programming": "⌨️",
        "DL": "🔌",
        "IIT": "💻",
        "Maths": "📐",
        "Physics": "⚡",
        "Discrete_Structures": "🔢"
    }
    return icons.get(subject_code, "📚")


def load_user_data():
    """Load all user data from database into session state"""
    if not st.session_state.user_id:
        return

    # Load progress for all subjects
    for sem in COURSE_STRUCTURE.keys():
        for subj in get_subjects(sem).keys():
            mins = db_client.get_progress(st.session_state.user_id, sem, subj)
            if mins > 0:
                key = f"{st.session_state.user_id}_{sem}_{subj}"
                st.session_state.study_timers[key] = mins

    # Load semester preference
    pref = db_client.get_user_preference(st.session_state.user_id, "selected_semester")
    if pref:
        st.session_state.selected_semester = int(pref)

    # Load chat history for general
    st.session_state.chat_history = db_client.load_chat_history(st.session_state.user_id, "General")


def save_preference(key, value):
    if st.session_state.user_id:
        db_client.save_preference(st.session_state.user_id, key, value)


def update_progress(subject_code, mins=1):
    """Update study time for a subject"""
    if not st.session_state.user_id:
        return

    semester = st.session_state.selected_semester
    key = f"{st.session_state.user_id}_{semester}_{subject_code}"

    if key not in st.session_state.study_timers:
        st.session_state.study_timers[key] = 0

    st.session_state.study_timers[key] += mins
    db_client.save_progress(st.session_state.user_id, semester, subject_code,
                            st.session_state.study_timers[key])


def get_progress_percentage(subject_code):
    """Calculate progress percentage (2 hours = 100%)"""
    if not st.session_state.user_id:
        return 0

    semester = st.session_state.selected_semester
    key = f"{st.session_state.user_id}_{semester}_{subject_code}"
    minutes_studied = st.session_state.study_timers.get(key, 0)

    # 120 minutes (2 hours) = 100%
    percentage = min(100, (minutes_studied / 120) * 100)
    return percentage


# ==================== AUTHENTICATION ====================

def show_login():
    """Display login/signup interface"""
    st.markdown("""
    <div class='header-container'>
        <h1>🎓 SemAI</h1>
        <p>Intelligent Tutoring System for CSIT Students</p>
        <p style='font-size: 0.9rem; opacity: 0.9'>Semester 1 • 5 Subjects • AI-Powered Learning</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Institutional Email")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Sign In", use_container_width=True):
                    if email and password:
                        user = db_client.get_user(email)
                        if user and user.get("password") == hash_password(password):
                            st.session_state.authenticated = True
                            st.session_state.user_id = user["user_id"]
                            # Load all user data
                            load_user_data()
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    else:
                        st.warning("Please fill out all fields.")

        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Academic Email")
                password = st.text_input("Password (min. 6 chars)", type="password")
                confirm = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("Register Account", use_container_width=True):
                    is_valid, err_msg = db_client.validate_signup_inputs(email, password)

                    if not name:
                        st.error("Please enter your full name.")
                    elif not is_valid:
                        st.error(err_msg)
                    elif password != confirm:
                        st.error("Passwords do not match.")
                    elif db_client.get_user(email):
                        st.error("This email is already registered.")
                    else:
                        # Create new user
                        u_id = db_client.save_user(email, hash_password(password), name, 1)
                        st.session_state.authenticated = True
                        st.session_state.user_id = u_id
                        st.session_state.selected_semester = 1

                        # Initialize tracking for all subjects
                        for subj_code in get_subjects(1).keys():
                            key = f"{u_id}_1_{subj_code}"
                            st.session_state.study_timers[key] = 0
                            db_client.save_progress(u_id, 1, subj_code, 0)

                        st.success("Registration successful!")
                        st.rerun()


# ==================== SEMESTER DASHBOARD ====================

def show_semester_dashboard():
    """Display semester dashboard with all subjects and progress"""
    semester = st.session_state.selected_semester
    semester_data = COURSE_STRUCTURE.get(semester, {})

    st.markdown(f"""
    <div class='header-container'>
        <h1>📚 {semester_data.get('name', f'Semester {semester}')}</h1>
        <p>Track your progress and continue learning</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🎯 Navigation Control")
        available_sems = list(COURSE_STRUCTURE.keys())
        selected_sem = st.selectbox(
            "Change Semester",
            available_sems,
            format_func=lambda x: f"Semester {x} - {COURSE_STRUCTURE[x]['name']}",
            index=available_sems.index(semester) if semester in available_sems else 0
        )
        if selected_sem != semester:
            st.session_state.selected_semester = selected_sem
            save_preference("selected_semester", str(selected_sem))
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Your Stats")
        total_progress = 0
        subject_count = len(get_subjects(semester))
        for subject_code in get_subjects(semester).keys():
            total_progress += get_progress_percentage(subject_code)
        avg_progress = total_progress / subject_count if subject_count > 0 else 0
        st.metric("Average Progress", f"{avg_progress:.0f}%")
        st.metric("Subjects Enrolled", subject_count)

        st.markdown("---")
        # Study Assistant Button
        st.markdown("""
        <a href="#sem-ai-study-assistant" style="text-decoration: none; display: block;">
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                margin: 10px 0;
                transition: all 0.3s ease;
                cursor: pointer;
            ">
                💬 Study Assistant
            </div>
        </a>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.chat_history = []
            st.rerun()

    # Display subjects in grid
    st.markdown("### 📖 Your Subjects")

    subjects = get_subjects(semester)
    cols = st.columns(3)

    from streamlit_card import card

    for idx, (subject_code, subject_info) in enumerate(subjects.items()):
        with cols[idx % 3]:
            progress = get_progress_percentage(subject_code)
            clicked = card(
                title=f"{get_icon(subject_code)}  {subject_info['full_name']}",
                text=[subject_code, f"Progress: {progress:.0f}%",
                      "▰" * int(progress / 10) + "▱" * (10 - int(progress / 10))],
                key=f"card_{subject_code}",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "260px",
                        "border-radius": "1rem",
                        "box-shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "border": "1px solid #e5e7eb",
                        "background-color": "white",
                        "cursor": "pointer",
                        "margin": "1rem 0",
                        "color": "#1f2937",
                    },
                    "title": {
                        "font-size": "1.2rem",
                        "font-weight": "600",
                        "color": "#1f2937",
                        "font-family": "inherit",
                    },
                    "text": {
                        "font-size": "0.875rem",
                        "color": "#6b7280",
                        "font-family": "inherit",
                    },
                    "filter": {
                        "background-color": "rgba(0,0,0,0)"
                    }
                }
            )
            if clicked:
                st.session_state.selected_subject = subject_code
                st.session_state.current_page = "subject"
                st.session_state.subject_feature = "syllabus"
                st.session_state.chat_history = db_client.load_chat_history(st.session_state.user_id, subject_code)
                update_progress(subject_code, 0)
                st.rerun()


# ==================== SUBJECT PAGE ====================

def show_subject_page():
    """Display detailed subject page with all features"""
    semester = st.session_state.selected_semester
    subject_code = st.session_state.selected_subject
    subject_info = get_subjects(semester).get(subject_code, {})
    subject_name = subject_info.get("full_name", subject_code)

    # Update study timer (active studying)
    update_progress(subject_code, 1)


    # ================= SUBJECT SIDEBAR =================

    progress = get_progress_percentage(subject_code)

    with st.sidebar:

        # Dashboard button
        if st.button(
                "← Dashboard",
                use_container_width=True,
                key="sidebar_dashboard",
        ):
            st.session_state.current_page = "dashboard"
            st.session_state.selected_subject = None
            st.session_state.chat_history = db_client.load_chat_history(
                st.session_state.user_id,
                "General",
            )
            st.rerun()

        # Subject header
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px 0;">
                <div style="font-size:30px;">{get_icon(subject_code)}</div>
                <h3 style="margin:5px 0;">{subject_name}</h2>
                <p style="margin:12px 0 8px 0; font-size:17px;">
                    Overall Progress:
                    <span style="font-weight:bold; font-size:16px; color:#4CAF50;">
                        {progress:.0f}%
                    </span>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(progress / 100)

        st.markdown(
            "<h4 style='text-align:center; margin-bottom:10px;'>Navigation</h4>",
            unsafe_allow_html=True,
        )

        nav_items = [
            ("📋 Syllabus", "syllabus"),
            ("📖 Chapter Notes", "notes"),
            ("⭐ Core Questions", "questions"),
            ("📝 Assessment Quiz", "quiz"),
        ]

        for label, feat in nav_items:
            if st.button(
                    label,
                    key=f"sidebar_{feat}",
                    use_container_width=True,
                    type="primary" if st.session_state.subject_feature == feat else "secondary",
            ):
                st.session_state.subject_feature = feat
                st.rerun()

        # Study Assistant Button
        st.markdown("""
        <a href="#sem-ai-study-assistant" style="text-decoration: none; display: block;">
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                margin: 10px 0;
                transition: all 0.3s ease;
                cursor: pointer;
            ">
                💬 Study Assistant
            </div>
        </a>
        """, unsafe_allow_html=True)

    # ================= PAGE TITLE =================

    st.title(f"{get_icon(subject_code)} {subject_name}")

    st.caption(
        f"Overall Progress: {progress:.0f}%"
    )

    st.divider()

    # Display selected feature
    feature = st.session_state.subject_feature

    if feature == "syllabus":
        show_syllabus(subject_code)
    elif feature == "notes":
        show_chapter_notes(subject_code)
    elif feature == "questions":
        show_important_questions(subject_code)
    elif feature == "quiz":
        show_quiz(subject_code)


def show_syllabus(subject_code):
    """Display syllabus from file"""
    st.markdown("### 📋 Course Syllabus")

    folder = SUBJECT_FOLDER_MAP.get(subject_code, subject_code)
    syllabus_path = f"data/semester1/{folder}/syllabus.txt"

    if os.path.exists(syllabus_path):
        with open(syllabus_path, 'r', encoding='utf-8', errors='ignore') as f:
            syllabus_content = f.read()
        st.markdown(f"<div class='syllabus-section'>{syllabus_content}</div>", unsafe_allow_html=True)
    else:
        st.info("Course syllabus will be added soon. Meanwhile, explore other features!")

        # Display chapters from config
        chapters = get_chapters(st.session_state.selected_semester, subject_code)
        if chapters:
            st.markdown("#### Topics Covered:")
            for i, chapter in enumerate(chapters, 1):
                st.markdown(f"{i}. {chapter}")


def show_chapter_notes(subject_code):
    """Generate notes for selected chapter"""
    st.markdown("### 📖 Chapter-wise Notes")

    chapters = get_chapters(st.session_state.selected_semester, subject_code)

    if not chapters:
        st.warning("Chapter list not available yet.")
        return

    selected_chapter = st.selectbox("Select Chapter:", chapters)

    if st.button("Generate Notes", type="primary", use_container_width=True):
        with st.spinner("📚 Generating notes from textbooks..."):
            # Search for relevant content
            query = f"{selected_chapter} detailed notes explanation"
            results = search_client.search(query, semester=1, subject=subject_code, top=3)

            if results:
                context = "\n\n".join([r["content"] for r in results])

                # Generate notes using LLM
                prompt = f"""
                Based on the following textbook content, create comprehensive study notes for the chapter: "{selected_chapter}"

                Textbook Content:
                {context[:4000]}

                Create notes with:
                1. Key concepts and definitions
                2. Important formulas or rules (if any)
                3. Examples or applications
                4. Key points to remember

                Format the notes clearly with headings and bullet points.
                """

                response = llm_client.chat([
                    {"role": "system", "content": "You are a CSIT professor creating study notes."},
                    {"role": "user", "content": prompt}
                ])

                st.markdown(response)

                # Update study time for generating notes
                update_progress(subject_code, 5)
            else:
                st.info("📚 Textbook content will be available after indexing. For now, here's a sample:")
                st.markdown(f"""
                ### {selected_chapter}

                *Study notes will be generated from your textbooks once they are indexed in Azure AI Search.*

                **Topics to cover:**
                - Core concepts and definitions
                - Practical applications
                - Common examples
                - Review questions
                """)


def show_important_questions(subject_code):
    """Display important questions from Q&A pairs"""
    st.markdown("### ⭐ Important Questions")

    folder = SUBJECT_FOLDER_MAP.get(subject_code, subject_code)
    qna_path = f"data/semester1/{folder}/qna_pairs.json"

    if os.path.exists(qna_path):
        with open(qna_path, 'r', encoding='utf-8', errors='ignore') as f:
            qna_data = json.load(f)

        qa_pairs = qna_data.get("qa_pairs", [])

        if qa_pairs:
            st.info(f"📚 Found {len(qa_pairs)} important questions with answers")

            for i, qa in enumerate(qa_pairs, 1):
                with st.expander(f"Q{i}. {qa['question']}"):
                    st.markdown(f"**Answer:** {qa['answer']}")
                    if 'topic' in qa:
                        st.caption(f"📌 Topic: {qa['topic']}")
                    if 'year' in qa:
                        st.caption(f"📅 Year: {qa['year']}")
        else:
            st.info("No questions available yet.")
    else:
        st.info("📝 Q&A pairs will be added soon.")


def show_quiz(subject_code):
    """Interactive quiz with random topic generation"""
    st.markdown("### 📝 Practice Quiz")

    # Quiz options
    quiz_type = st.radio("Quiz Type:", ["Quick 5 Questions", "Full Chapter Quiz", "Mixed Topics"], horizontal=True)

    if st.button("Start Quiz", type="primary", use_container_width=True):
        with st.spinner("Generating fresh quiz questions..."):
            # Fetch real chapters for this subject
            chapters = get_chapters(st.session_state.selected_semester, subject_code)

            # Pick a shifting mix of chapters
            import random
            sampled_chapters = random.sample(chapters, min(3, len(chapters))) if chapters else ["General concepts"]

            # Create a unique seed token
            random_seed = random.randint(1000, 9999)

            # Build dynamic prompt
            prompt = f"""
            Generate a completely unique and original set of 5 multiple-choice questions for the CSIT subject: {subject_code}.

            Focus heavily on these specific topics/chapters: {', '.join(sampled_chapters)}.

            Random Session ID Token: {random_seed}

            CRITICAL REQUIREMENTS:
            - Do not generate the same questions as previous sessions.
            - Vary the difficulty across questions (conceptual, code/logic tracking, and problem-solving).
            - Ensure options are plausible but only one is explicitly correct.

            Format your response STRICTLY as valid JSON matching this exact schema:
            {{
                "questions": [
                    {{
                        "question": "Clear question text here",
                        "options": ["A) first option", "B) second option", "C) third option", "D) fourth option"],
                        "correct": "A",
                        "explanation": "Detailed pedagogical explanation of why this answer is correct"
                    }}
                ]
            }}
            """

            response = llm_client.chat([
                {"role": "system",
                 "content": "You are an expert university CSIT professor and strict quiz generator. You must return ONLY valid, raw JSON. Do not include markdown code blocks like ```json or any conversational filler text."},
                {"role": "user", "content": prompt}
            ])

            try:
                # Parse JSON response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    quiz_data = json.loads(json_match.group())
                    questions = quiz_data.get("questions", [])

                    # Store in session state
                    st.session_state.active_quiz = questions
                    st.session_state.quiz_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_current = 0
                    st.session_state.quiz_answered = False

                    st.toast("🎯 Fresh quiz generated successfully!", icon="✅")
                    st.rerun()
            except Exception as e:
                st.error("Could not parse the AI's quiz JSON structure. Falling back to default questions.")
                # Fallback questions
                fallback_qs = [
                    {"question": f"What is a fundamental concept in {subject_code}?",
                     "options": ["A) Option One", "B) Option Two", "C) Option Three", "D) Option Four"],
                     "correct": "A",
                     "explanation": "Review your course syllabus materials for this specific domain."}
                ]
                st.session_state.active_quiz = fallback_qs * 5
                st.session_state.quiz_answers = []
                st.session_state.quiz_score = 0
                st.session_state.quiz_current = 0
                st.session_state.quiz_answered = False
                st.rerun()

    # Display active quiz
    if 'active_quiz' in st.session_state and st.session_state.active_quiz:
        quiz = st.session_state.active_quiz
        current_idx = st.session_state.get('quiz_current', 0)

        if current_idx < len(quiz):
            q = quiz[current_idx]

            # Progress bar
            st.progress((current_idx + 1) / len(quiz))
            st.markdown(f"### Question {current_idx + 1} of {len(quiz)}")
            st.markdown(f"**{q['question']}**")

            # Check if user has evaluated this question yet
            is_answered = st.session_state.get('quiz_answered', False)

            # Disable option selection after submitting
            selected = st.radio("Select your answer:", q['options'], key=f"q_{current_idx}", disabled=is_answered)

            col1, col2 = st.columns(2)

            if not is_answered:
                with col1:
                    if st.button("Submit Answer", use_container_width=True):
                        is_correct = selected.strip().startswith(q['correct']) or selected[0] == q['correct']
                        if is_correct:
                            st.session_state.quiz_score += 1
                            st.toast("✅ Correct!", icon="✅")
                        else:
                            st.toast("❌ Incorrect", icon="❌")

                        st.session_state.quiz_answered = True
                        st.rerun()

                with col2:
                    if st.button("Skip Question", use_container_width=True):
                        st.session_state.quiz_answered = True
                        st.rerun()
            else:
                # Show evaluation
                if selected.strip().startswith(q['correct']) or selected[0] == q['correct']:
                    st.success(f"✅ **Correct!** The answer is indeed option {q['correct']}.")
                else:
                    st.error(f"❌ **Incorrect.** The correct answer was option {q['correct']}.")

                st.info(f"📖 **Explanation:** {q['explanation']}")

                if st.button("Next Question →", type="primary", use_container_width=True):
                    st.session_state.quiz_current = current_idx + 1
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            # Quiz completed
            st.balloons()
            st.markdown(f"## 🎉 Quiz Completed!")
            st.markdown(f"### Your Final Score: {st.session_state.quiz_score}/{len(quiz)}")

            percentage = (st.session_state.quiz_score / len(quiz)) * 100
            if percentage >= 80:
                st.success("🌟 Excellent! You've completely mastered this topic zone!")
            elif percentage >= 60:
                st.info("👍 Good job! Take some time to review the questions you missed.")
            else:
                st.warning("📚 More practice needed. Review your chapter study notes and try again!")

            # Update progress
            update_progress(subject_code, 10)

            if st.button("Take Another Quiz", use_container_width=True):
                del st.session_state.active_quiz
                del st.session_state.quiz_current
                del st.session_state.quiz_answered
                st.session_state.subject_feature = "quiz"
                st.rerun()


# ==================== CHAT ASSISTANT ====================

def show_chat_assistant():
    """Production-Ready Chat Assistant with Database Integration"""
    semester = st.session_state.selected_semester or 1
    subject = st.session_state.selected_subject or "General"
    subject_name = get_subjects(semester).get(subject, {}).get("full_name",
                                                               subject) if subject != "General" else "General"

    st.markdown("---")
    st.markdown("### 🤖 SemAI Study Assistant")
    st.caption(f"Context: Semester {semester} | {subject_name}")

    # Configuration panel
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        model_choice = st.selectbox(
            "🤖 Active Model",
            ["Free (GitHub Models)", "Premium (Azure OpenAI)"],
            key="model_choice"
        )
    with col2:
        manual_sem = st.number_input("Semester", min_value=1, max_value=8, value=semester, key="manual_sem")
    with col3:
        all_subjects = list(get_subjects(semester).keys()) + ["General"]
        manual_subj = st.selectbox("Subject Code", all_subjects,
                                   index=all_subjects.index(subject) if subject in all_subjects else 0,
                                   key="manual_subj")

    # Sources Selection Filter
    selected_sources = st.multiselect(
        "📚 Active Data Sources for Next Answer:",
        ["Syllabus", "Past Questions Solutions (Q&A)", "Chapter Notes", "Past Questions", "Textbooks"],
        default=["Syllabus", "Past Questions Solutions (Q&A)", "Textbooks"],
        key="chat_sources_filter"
    )

    # Optional file attachment
    uploaded_file = st.file_uploader("📎 Upload file for context (optional)", type=['txt', 'pdf', 'md'])

    # Chat history display
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_history[-20:]:
            if msg["role"] == "user":
                st.markdown(f"<div class='message-user'><strong>You:</strong><br>{msg['content']}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-bot'><strong>🤖 SemAI:</strong><br>{msg['content']}</div>",
                            unsafe_allow_html=True)
                if "citations" in msg and msg["citations"]:
                    st.caption(f"📖 Sources: {', '.join(msg['citations'])}")

    # Chat input
    user_query = st.chat_input("Ask the SemAI Study Assistant...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.spinner("🔍 Scanning multi-source databases..."):
            local_context_buffer = ""
            sources_found = []

            # ==========================================
            # LOCAL DISK READ
            # ==========================================
            if manual_subj != "General":
                folder_mapping = {
                    "C_Programming": "C_Programming",
                    "DL": "DL",
                    "IIT": "IIT",
                    "Maths": "Maths",
                    "Physics": "Physics"
                }

                folder_name = folder_mapping.get(manual_subj, manual_subj)
                target_dir = f"data/semester1/{folder_name}"

                if os.path.exists(target_dir):
                    # A. Syllabus Check
                    if "Syllabus" in selected_sources:
                        syllabus_file = os.path.join(target_dir, "syllabus.txt")
                        if os.path.exists(syllabus_file):
                            try:
                                with open(syllabus_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    local_context_buffer += f"\n--- OFFICIAL SYLLABUS GUIDELINES ---\n{f.read()[:2000]}\n"
                                    sources_found.append("Local Syllabus File")
                            except Exception:
                                pass

                    # B. Q&A Pairs Check
                    if "Past Questions Solutions (Q&A)" in selected_sources:
                        qna_file = os.path.join(target_dir, "qna_pairs.json")
                        if os.path.exists(qna_file):
                            try:
                                with open(qna_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    qna_data = json.load(f)
                                qa_pairs = qna_data.get("qa_pairs", [])
                                query_words = [w.lower() for w in user_query.split() if len(w) > 3]
                                matched_qnas = []

                                for pair in qa_pairs:
                                    if not query_words or any(
                                            word in pair['question'].lower() or word in pair.get('answer', '').lower()
                                            for word in query_words):
                                        matched_qnas.append(f"Question: {pair['question']}\nAnswer: {pair['answer']}")

                                if matched_qnas:
                                    local_context_buffer += f"\n--- EXAM QUESTION BANK MATCHES ---\n" + "\n\n".join(
                                        matched_qnas[:4]) + "\n"
                                    sources_found.append("Exam Q&A Bank")
                            except Exception:
                                pass

                    # C. Notes Check
                    if "Chapter Notes" in selected_sources:
                        notes_dir = os.path.join(target_dir, "notes")
                        if os.path.exists(notes_dir):
                            try:
                                notes_content = ""
                                for file in os.listdir(notes_dir)[:3]:
                                    if file.endswith(('.txt', '.md')):
                                        with open(os.path.join(notes_dir, file), 'r', encoding='utf-8',
                                                  errors='ignore') as f:
                                            notes_content += f"\n[Notes File: {file}]\n{f.read()[:1000]}\n"
                                if notes_content:
                                    local_context_buffer += f"\n--- LOCAL CHAPTER NOTES OVERVIEWS ---\n{notes_content}\n"
                                    sources_found.append("Local Notes Folder")
                            except Exception:
                                pass

            # ==========================================
            # REMOTE RAG CLOUD SEARCH
            # ==========================================
            search_results = []
            if manual_subj != "General" and "Textbooks" in selected_sources:
                try:
                    search_results = search_client.search(user_query, semester=int(manual_sem), subject=manual_subj,
                                                          top=3)
                    for r in search_results:
                        sources_found.append(f"Indexed Textbook ({r['source']})")
                except Exception:
                    pass

            if uploaded_file:
                local_context_buffer += f"\n\n[Attached File Context - {uploaded_file.name}]\n"
                sources_found.append("User Upload")

            # ==========================================
            # SYSTEM CONTEXT INJECTION
            # ==========================================
            system_prompt = f"""You are SemAI, an expert university professor and personal AI tutor for CSIT students.
Current Academic Scope: Semester {manual_sem}, Subject Domain: {manual_subj}

INSTRUCTIONS FOR GENERATION:
- You have direct access to course items, question papers, and textbook materials provided below.
- Prioritize data from 'OFFICIAL SYLLABUS GUIDELINES' and 'EXAM QUESTION BANK MATCHES' to format your response.
- Use the structural contexts below to build comprehensive responses with headings, step-by-step code proofs, or numbered listings.
- CRITICAL: If the localized context sections below are empty, do NOT refuse the question. Instead, answer completely and comprehensively using your internal deep knowledge of the standard university {manual_subj} curriculum. Never tell the user you don't have access.

--- SYSTEM GROUNDING KNOWLEDGE CONTEXT ---
{local_context_buffer if local_context_buffer else "No localized document overrides found on disk."}

--- PARSED TEXTBOOK RETRIEVED CHUNKS ---
{"".join([f'[{doc["source"]}]: {doc["content"]}\n' for doc in search_results]) if search_results else "No cloud textbook chunks returned."}
"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]

            # ==========================================
            # MODEL CALL
            # ==========================================
            try:
                if model_choice == "Free (GitHub Models)":
                    response = llm_client._github_chat(messages, temperature=0.7)
                else:
                    if hasattr(llm_client, '_azure_chat'):
                        response = llm_client._azure_chat(messages, temperature=0.7)
                    else:
                        response = "Azure Premium endpoint is missing structural bindings. Defaulting to free engine."
            except Exception as model_err:
                response = f"Critical engine crash during inference call: {str(model_err)}"

            # Format final message
            bot_message = {
                "role": "assistant",
                "content": response,
                "citations": list(set(sources_found))
            }
            st.session_state.chat_history.append(bot_message)

            # Save to database
            try:
                db_client.save_message(st.session_state.user_id, manual_subj, "user", user_query)
                db_client.save_message(st.session_state.user_id, manual_subj, "assistant", response)
            except Exception:
                pass

            if manual_subj != "General":
                update_progress(manual_subj, 2)

            st.rerun()

    if st.button("🗑️ Clear Chat History", use_container_width=False):
        st.session_state.chat_history = []
        # Also clear from database if needed
        st.rerun()


# ==================== MAIN APP ====================

def main():
    """Main application controller"""

    # Check authentication
    if not st.session_state.authenticated:
        show_login()
        return

    # Main navigation
    if st.session_state.current_page == "dashboard":
        show_semester_dashboard()
    elif st.session_state.current_page == "subject":
        show_subject_page()

    # Show chat assistant at bottom
    show_chat_assistant()


if __name__ == "__main__":
    main()



