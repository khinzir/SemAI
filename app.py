
"""
SemAI - Complete Intelligent Tutoring System
Semester 1 Prototype with Full Features
"""
import streamlit as st
import os
import json
import uuid
import time
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
    }

    
    
    .subject-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }

    .subject-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .subject-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0.5rem 0;
    }

    .subject-code {
        font-size: 0.875rem;
        color: #6b7280;
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
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        text-align: right;
    }

    .message-bot {
        background: #f3f4f6;
        color: #1f2937;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }

    /* Syllabus styling */
    .syllabus-section {
        background: #f9fafb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .chat-container {
            width: 100%;
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
    st.session_state.selected_semester = None
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


# Initialize database and LLM clients
@st.cache_resource
def init_clients():
    db_client = CosmosClientManager()
    llm_client = LLMClient()
    search_client = SearchClientManager()
    return db_client, llm_client, search_client


db_client, llm_client, search_client = init_clients()


# ==================== AUTHENTICATION ====================

# def show_login():
#     """Display login/signup interface"""
#     st.markdown("""
#     <div class='header-container'>
#         <h1>🎓 SemAI</h1>
#         <p>Intelligent Tutoring System for CSIT Students</p>
#         <p style='font-size: 0.9rem; opacity: 0.9'>Semester 1 • 5 Subjects • AI-Powered Learning</p>
#     </div>
#     """, unsafe_allow_html=True)
#
#     col1, col2, col3 = st.columns([1, 2, 1])
#
#     with col2:
#         tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
#
#         with tab1:
#             # with st.form("login_form"):
#             #     email = st.text_input("Email")
#             #     password = st.text_input("Password", type="password")
#             #
#             #     if st.form_submit_button("Login", use_container_width=True):
#             #         if email and password:
#             #             # Simple demo authentication
#             #             # In production, use proper auth
#             #             st.session_state.authenticated = True
#             #             st.session_state.user_id = email.replace("@", "_").replace(".", "_")
#             #             st.session_state.selected_semester = 1  # Default to semester 1
#             #             st.rerun()
#             #         else:
#             #             st.error("Please enter email and password")
#             with st.form("login_form"):
#                 email = st.text_input("Academic Email Address")
#                 password = st.text_input("Security Passcode", type="password")
#
#                 if st.form_submit_button("Login", use_container_width=True):
#                     if email and password:
#                         # Connect with the database user profile validation
#                         user_profile = db_client.verify_or_create_user(email, password)
#                         user_id = user_profile["user_id"]
#
#                         st.session_state.authenticated = True
#                         st.session_state.user_id = user_id
#                         st.session_state.selected_semester = 1
#
#                         # DOWNLOAD LOGGED PERSISTENT MINUTES ON LOGIN
#                         from config.course_structure import get_subjects
#                         subjects = get_subjects(1)
#                         for subj_code in subjects.keys():
#                             key = f"{user_id}_1_{subj_code}"
#                             st.session_state.study_timers[key] = db_client.get_progress(user_id, 1, subj_code)
#
#                         st.rerun()
#                     else:
#                         st.error("Please enter email and password")
#
#                 if st.form_submit_button("Verify Account Profile", use_container_width=True):
#                     if email.strip() and password.strip():
#                         # 1. Run rigorous verification check against db engine
#                         user_profile = db_client.verify_or_create_user(email, password)
#
#                         if user_profile:
#                             st.session_state.authenticated = True
#                             st.session_state.user_id = user_profile["user_id"]
#                             st.session_state.selected_semester = user_profile["selected_semester"]
#
#                             # 2. Rehydrate state progress bars across sessions
#                             st.session_state.study_timers = db_client.load_all_user_progress(user_profile["user_id"])
#
#                             st.success("Verification successful! Opening profile workspace...")
#                             st.rerun()
#                         else:
#                             st.error("Authentication failed. Invalid passcode match.")
#         with tab2:
#             with st.form("signup_form"):
#                 name = st.text_input("Full Name")
#                 email = st.text_input("Email")
#                 password = st.text_input("Password", type="password")
#                 confirm_password = st.text_input("Confirm Password", type="password")
#
#                 if st.form_submit_button("Sign Up", use_container_width=True):
#                     if password != confirm_password:
#                         st.error("Passwords don't match")
#                     elif email and password:
#                         user_profile = db_client.verify_or_create_user(email, password)
#                         user_id = user_profile["user_id"]
#
#                         st.session_state.authenticated = True
#                         st.session_state.user_id = user_id
#                         st.session_state.selected_semester = 1
#
#                         # Populate fresh entries for a new registration profile
#                         from config.course_structure import get_subjects
#                         for subj_code in get_subjects(1).keys():
#                             key = f"{user_id}_1_{subj_code}"
#                             st.session_state.study_timers[key] = 0
#                             db_client.save_progress(user_id, 1, subj_code, 0)
#                         st.rerun()
#                     else:
#                         st.error("Please fill all fields")
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
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Login", use_container_width=True):
                    if email and password:
                        # Clean local prototype authentication
                        st.session_state.authenticated = True
                        st.session_state.user_id = email.replace("@", "_").replace(".", "_")
                        st.session_state.selected_semester = 1  # Default to semester 1
                        st.rerun()
                    else:
                        st.error("Please enter email and password")

        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("Sign Up", use_container_width=True):
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    elif email and password:
                        st.session_state.authenticated = True
                        st.session_state.user_id = email.replace("@", "_").replace(".", "_")
                        st.session_state.selected_semester = 1
                        st.rerun()
                    else:
                        st.error("Please fill all fields")


# ==================== STUDY TIMER LOGIC ====================

def update_study_time(subject_code: str, duration_minutes: int = 1):
    """Update study time for a subject (simulated - time-based progress)"""
    user_id = st.session_state.user_id
    semester = st.session_state.selected_semester

    key = f"{user_id}_{semester}_{subject_code}"

    if key not in st.session_state.study_timers:
        st.session_state.study_timers[key] = 0

    st.session_state.study_timers[key] += duration_minutes

    # Save to database
    db_client.save_progress(user_id, semester, subject_code, st.session_state.study_timers[key])


def get_progress_percentage(subject_code: str) -> float:
    """Calculate progress percentage (2 hours = 100%)"""
    user_id = st.session_state.user_id
    semester = st.session_state.selected_semester

    key = f"{user_id}_{semester}_{subject_code}"
    minutes_studied = st.session_state.study_timers.get(key, 0)

    # 120 minutes (2 hours) = 100%
    percentage = min(100, (minutes_studied / 120) * 100)
    return percentage


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

    # Semester selector in sidebar
    # with st.sidebar:
    #     st.markdown("### 🎯 Semester Navigation")
    #     available_semesters = list(COURSE_STRUCTURE.keys())
    #     selected_sem = st.selectbox(
    #         "Switch Semester",
    #         available_semesters,
    #         format_func=lambda x: f"Semester {x} - {COURSE_STRUCTURE[x]['name']}",
    #         index=available_semesters.index(semester) if semester in available_semesters else 0
    #     )
    #     if selected_sem != semester:
    #         st.session_state.selected_semester = selected_sem
    #         st.rerun()
    with st.sidebar:
        st.markdown("### 🎯 Navigation Control")
        available_sems = list(COURSE_STRUCTURE.keys())
        selected_sem = st.selectbox(
            "Change Track View",
            available_sems,
            format_func=lambda x: f"Semester {x} - {COURSE_STRUCTURE[x]['name']}"
        )
        if selected_sem != semester:
            st.session_state.selected_semester = selected_sem
            # NEW: Immediately save preference to database
            db_client.save_semester_preference(st.session_state.user_id, selected_sem)
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

    # Display subjects in grid
    st.markdown("### 📖 Your Subjects")

    subjects = get_subjects(semester)
    cols = st.columns(3)

    for idx, (subject_code, subject_info) in enumerate(subjects.items()):
        with cols[idx % 3]:
            progress = get_progress_percentage(subject_code)

            st.markdown(f"""
            <div class='subject-card' onclick="alert('Navigate to {subject_info['full_name']}')">
                <div class='subject-icon'>
                    {get_subject_icon(subject_code)}
                </div>
                <div class='subject-title'>{subject_info['full_name']}</div>
                <div class='subject-code'>{subject_code}</div>
                <div class='progress-container'>
                    <div class='progress-label'>
                        <span>Progress</span>
                        <span>{progress:.0f}%</span>
                    </div>
                    <div class='progress-bar'>
                        <div class='progress-fill' style='width: {progress}%'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # if st.button(f"Study {subject_info['full_name']}", key=f"study_{subject_code}", use_container_width=True):
            #     st.session_state.selected_subject = subject_code
            #     st.session_state.current_page = "subject"
            #     # Start timer for this subject
            #     update_study_time(subject_code, 0)
            #     st.rerun()
            if st.button(f"Study {subject_info['full_name']}", key=f"btn_{subject_code}", use_container_width=True):
                st.session_state.selected_subject = subject_code
                st.session_state.current_page = "subject"

                # NEW: Hydrate chat logs exclusively for this subject channel on enter
                st.session_state.chat_history = db_client.load_chat_history(st.session_state.user_id, subject_code)

                st.session_state.subject_feature = "syllabus"
                update_study_time(subject_code, 0)
                st.rerun()


def get_subject_icon(subject_code: str) -> str:
    """Return emoji icon for subject"""
    icons = {
        "C_Programming": "⌨️",
        "DL": "🔌",
        "IIT": "💻",
        "Maths": "📐",
        "Physics": "⚡",
        "Discrete_Structures": "🔢"
    }
    return icons.get(subject_code, "📚")


# ==================== SUBJECT PAGE ====================

def show_subject_page():
    """Display detailed subject page with all features"""
    semester = st.session_state.selected_semester
    subject_code = st.session_state.selected_subject
    subject_info = get_subjects(semester).get(subject_code, {})
    subject_name = subject_info.get("full_name", subject_code)

    # Update study timer (active studying)
    update_study_time(subject_code, 1)

    # Back button and header
    col1, col2 = st.columns([1, 5])
    with col1:
        # if st.button("← Back", use_container_width=True):
        #     st.session_state.current_page = "dashboard"
        #     st.rerun()
        if st.button("← Back", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.session_state.selected_subject = "General"
            st.session_state.chat_history = db_client.load_chat_history(st.session_state.user_id, "General")
            st.rerun()

    with col2:
        st.markdown(f"## {get_subject_icon(subject_code)} {subject_name}")

    # Progress bar
    progress = get_progress_percentage(subject_code)
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-label'>
            <span>📊 Overall Progress</span>
            <span>{progress:.0f}% complete</span>
        </div>
        <div class='progress-bar'>
            <div class='progress-fill' style='width: {progress}%'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Time remaining until mastery
    remaining_minutes = max(0, 120 - (progress / 100 * 120))
    if remaining_minutes <= 0:
        st.success("Congratulations! You've mastered this subject!")

    st.markdown("---")

    # Feature grid
    st.markdown("### 🎯 Learning Tools")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📋 Syllabus", use_container_width=True, key="btn_syllabus"):
            st.session_state.subject_feature = "syllabus"

    with col2:
        if st.button("📖 Chapter Notes", use_container_width=True, key="btn_notes"):
            st.session_state.subject_feature = "notes"

    with col3:
        if st.button("⭐ Important Qs", use_container_width=True, key="btn_questions"):
            st.session_state.subject_feature = "questions"

    with col4:
        if st.button("📝 Take Quiz", use_container_width=True, key="btn_quiz"):
            st.session_state.subject_feature = "quiz"

    st.markdown("---")

    # Display selected feature
    feature = st.session_state.get("subject_feature", "syllabus")

    if feature == "syllabus":
        show_syllabus(subject_code)
    elif feature == "notes":
        show_chapter_notes(subject_code)
    elif feature == "questions":
        show_important_questions(subject_code)
    elif feature == "quiz":
        show_quiz(subject_code)


def show_syllabus(subject_code: str):
    """Display syllabus from file"""
    syllabus_path = f"data/semester1/{subject_code}/syllabus.txt"

    st.markdown("### 📋 Course Syllabus")

    if os.path.exists(syllabus_path):
        with open(syllabus_path, 'r') as f:
            syllabus_content = f.read()
        # st.markdown(f"<div class='syllabus-section'>{syllabus_content}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='syllabus-section' style='white-space: pre-wrap;'>{syllabus_content}</div>", unsafe_allow_html=True)
    else:
        st.info("Syllabus content will be added soon. Meanwhile, explore other features!")

        # Display chapters from config
        chapters = get_chapters(st.session_state.selected_semester, subject_code)
        if chapters:
            st.markdown("#### Topics Covered:")
            for i, chapter in enumerate(chapters, 1):
                st.markdown(f"{i}. {chapter}")


def show_chapter_notes(subject_code: str):
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
                update_study_time(subject_code, 5)
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


def show_important_questions(subject_code: str):
    """Display important questions from Q&A pairs"""
    st.markdown("### ⭐ Important Questions")

    qna_path = f"data/semester1/{subject_code}/qna_pairs.json"

    if os.path.exists(qna_path):
        with open(qna_path, 'r') as f:
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
        st.info("📝 Q&A pairs will be added soon. You can contribute by adding questions!")

        # Sample questions
        st.markdown("#### Example Questions (Coming Soon):")
        st.markdown("""
        - Explain the concept of [topic] with examples
        - What are the differences between X and Y?
        - Write short notes on [important topics]
        - Solve the following problem...
        """)




def show_quiz(subject_code: str):
    """Interactive quiz with random topic generation and reliable state navigation"""
    st.markdown("### 📝 Practice Quiz")

    # Quiz options
    quiz_type = st.radio("Quiz Type:", ["Quick 5 Questions", "Full Chapter Quiz", "Mixed Topics"], horizontal=True)

    if st.button("Start Quiz", type="primary", use_container_width=True):
        with st.spinner("Generating fresh quiz questions..."):
            # 1. Fetch real chapters for this subject
            chapters = get_chapters(st.session_state.selected_semester, subject_code)

            # 2. Pick a shifting mix of chapters to force variation
            import random
            sampled_chapters = random.sample(chapters, min(3, len(chapters))) if chapters else ["General concepts"]

            # 3. Create a unique seed token to bypass the LLM's pattern cache
            random_seed = random.randint(1000, 9999)

            # 4. Build a completely dynamic prompt string
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
                # Parse JSON response cleanly
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    quiz_data = json.loads(json_match.group())
                    questions = quiz_data.get("questions", [])

                    # Store pristine quiz structures into state tracking tags
                    st.session_state.active_quiz = questions
                    st.session_state.quiz_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_current = 0
                    st.session_state.quiz_answered = False  # Track if user clicked submit on current Q

                    st.toast("🎯 Fresh quiz generated successfully!", icon="✅")
                    st.rerun()
            except Exception as e:
                st.error("Could not parse the AI's quiz JSON structure. Falling back to default questions.")
                # Clean fallback system to prevent outright runtime crashes
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

    # Display active quiz gameplay loop
    if 'active_quiz' in st.session_state and st.session_state.active_quiz:
        quiz = st.session_state.active_quiz
        current_idx = st.session_state.get('quiz_current', 0)

        if current_idx < len(quiz):
            q = quiz[current_idx]

            # Progress bar visualization
            st.progress((current_idx + 1) / len(quiz))
            st.markdown(f"### Question {current_idx + 1} of {len(quiz)}")
            st.markdown(f"**{q['question']}**")

            # Check if user has evaluated this question yet
            is_answered = st.session_state.get('quiz_answered', False)

            # Disable option selection after submitting so they can't change it while reading explanation
            selected = st.radio("Select your answer:", q['options'], key=f"q_{current_idx}", disabled=is_answered)

            col1, col2 = st.columns(2)

            if not is_answered:
                with col1:
                    if st.button("Submit Answer", use_container_width=True):
                        # Graceful fallback logic matching for choice parsing formats ("A)" vs "A")
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
                # User has submitted. Reveal explicit evaluation cards.
                if selected.strip().startswith(q['correct']) or selected[0] == q['correct']:
                    st.success(f"✅ **Correct!** The answer is indeed option {q['correct']}.")
                else:
                    st.error(f"❌ **Incorrect.** The correct answer was option {q['correct']}.")

                st.info(f"📖 **Explanation:** {q['explanation']}")

                # Unnested independent Next button to increment index and flip states
                if st.button("Next Question →", type="primary", use_container_width=True):
                    st.session_state.quiz_current = current_idx + 1
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            # Quiz final completion handling
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

            # Log execution telemetry records into tracking frameworks
            update_study_time(subject_code, 10)

            if st.button("Take Another Quiz", use_container_width=True):
                del st.session_state.active_quiz
                del st.session_state.quiz_current
                del st.session_state.quiz_answered
                st.session_state.subject_feature = "quiz"
                st.rerun()




def show_chat_assistant():
    """Production-Ready Chat Assistant with Hardcoded Exact Tree Mappings"""
    semester = st.session_state.selected_semester or 1
    subject = st.session_state.selected_subject or "General"
    subject_name = get_subjects(semester).get(subject, {}).get("full_name",
                                                               subject) if subject != "General" else "General"

    st.markdown("---")
    st.markdown("### 🤖 SemAI Study Assistant")
    st.caption(f"Context: Semester {semester} | {subject_name}")


    # Configuration panel layout
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

    # NEW: Sources Selection Filter
    selected_sources = st.multiselect(
        "📚 Active Data Sources for Next Answer:",
        ["Syllabus", "Past Questions Solutions (Q&A)", "Chapter Notes", "Past Questions", "Textbooks"],
        default=["Syllabus", "Past Questions Solutions (Q&A)", "Textbooks"],
        key="chat_sources_filter"
    )

    # Optional file attachment field
    uploaded_file = st.file_uploader("📎 Upload file for context (optional)", type=['txt', 'pdf', 'md'])

    # Chat history window frame
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

    # Capture chat input
    user_query = st.chat_input("Ask the SemAI Study Assistant...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.spinner("🔍 Scanning multi-source databases..."):
            local_context_buffer = ""
            sources_found = []


            # ==========================================
            # EXACT LOCAL DISK READ (MATCHING YOUR FIXED TREE)
            # ==========================================
            if manual_subj != "General":
                folder_mapping = {
                    "C_Programming": "C-Programming",
                    "DL": "DL",
                    "IIT": "IIT",
                    "Maths": "Maths",
                    "Physics": "Physics"
                }

                folder_name = folder_mapping.get(manual_subj, manual_subj)
                target_dir = f"data/semester1/{folder_name}"

                if os.path.exists(target_dir):
                    # A. Gated Local Syllabus Check
                    if "Syllabus" in selected_sources:
                        syllabus_file = os.path.join(target_dir, "syllabus.txt")
                        if os.path.exists(syllabus_file):
                            try:
                                with open(syllabus_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    local_context_buffer += f"\n--- OFFICIAL SYLLABUS GUIDELINES ---\n{f.read()[:2000]}\n"
                                    sources_found.append("Local Syllabus File")
                            except Exception:
                                pass

                    # B. Gated Past Questions Solutions Check (qna_pairs.json)
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

                    # C. Gated Local Notes Check (Reads raw text notes files from directory if selected)
                    if "Chapter Notes" in selected_sources:
                        notes_dir = os.path.join(target_dir, "notes")
                        if os.path.exists(notes_dir):
                            try:
                                notes_content = ""
                                for file in os.listdir(notes_dir)[:3]:  # limit to top files to preserve token space
                                    if file.endswith(('.txt', '.md')):
                                        with open(os.path.join(notes_dir, file), 'r', encoding='utf-8',
                                                  errors='ignore') as f:
                                            notes_content += f"\n[Notes File: {file}]\n{f.read()[:1000]}\n"
                                if notes_content:
                                    local_context_buffer += f"\n--- LOCAL CHAPTER NOTES OVERVIEWS ---\n{notes_content}\n"
                                    sources_found.append("Local Notes Folder")
                            except Exception:
                                pass

                    # D. Gated Raw Past Questions Check
                    if "Past Questions" in selected_sources:
                        pq_dir = os.path.join(target_dir, "past_questions")
                        if os.path.exists(pq_dir):
                            # Gathers file names/structures to feed context as guidance
                            files = [f for f in os.listdir(pq_dir) if f.endswith(('.txt', '.md', '.pdf'))]
                            if files:
                                local_context_buffer += f"\n--- AVAILABLE PAST EXAM PAPERS FOUND ---\nFiles available: {', '.join(files)}\n"
                                sources_found.append("Past Exam Papers List")

            # ==========================================
            # REMOTE RAG CLOUD SEARCH
            # ==========================================
            search_results = []
            # Only trigger vector retrieval call if 'Textbooks' source filter is checked active
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
            # SYSTEM CONTEXT INJECTION ASSEMBLY
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
            # MODEL CALL EXECUTION LOOP
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

            # Format final messaging asset array
            bot_message = {
                "role": "assistant",
                "content": response,
                "citations": list(set(sources_found))
            }
            st.session_state.chat_history.append(bot_message)

            # Sync log systems
            try:
                db_client.save_message(st.session_state.user_id, manual_subj, "user", user_query)
                db_client.save_message(st.session_state.user_id, manual_subj, "assistant", response)
            except Exception:
                pass

            if manual_subj != "General":
                update_study_time(manual_subj, 2)

            st.rerun()

    if st.button("🗑️ Clear Chat History", use_container_width=False):
        st.session_state.chat_history = []
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

    # Show chat assistant at bottom (always visible)
    st.markdown("---")
    show_chat_assistant()


if __name__ == "__main__":
    main()
