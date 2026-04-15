# This is the codespace where all the codes will go to
import streamlit as st
import google.generativeai as genai
import json

# ---------------------------------------------------
# 🔐 LOAD GEMINI API KEY (STREAMLIT CLOUD SAFE WAY)
# ---------------------------------------------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ---------------------------------------------------
# 🧠 USE STABLE GEMINI MODEL
# ---------------------------------------------------
MODEL_NAME = "gemini-1.5-flash"

# ---------------------------------------------------
# 📦 JSON STRUCTURE EXPECTED FROM AI
# ---------------------------------------------------
response_format = {
    "mcqs": [
        {
            "mcq": "question text",
            "options": {
                "a": "choice 1",
                "b": "choice 2",
                "c": "choice 3",
                "d": "choice 4"
            },
            "correct": "a"
        }
    ]
}

# ---------------------------------------------------
# ⚡ RAW GEMINI CALL (THIS IS WHAT WE CACHE)
# ---------------------------------------------------
@st.cache_data
def call_gemini(prompt: str):
    """
    This function calls Gemini once and caches the raw response.
    This saves API cost if the same prompt is repeated.
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text  # store raw text ONLY


# ---------------------------------------------------
# 🧠 PARAGRAPH-BASED QUIZ GENERATOR
# ---------------------------------------------------
def fetch_questions_from_paragraph(text_content, quiz_level):

    prompt = f"""
    You are an expert quiz creator.

    Create 5 multiple choice questions from the paragraph below.

    Difficulty: {quiz_level}

    Paragraph:
    {text_content}

    Return ONLY valid JSON in this format:
    {json.dumps(response_format)}
    """

    raw_text = call_gemini(prompt)

    # Clean markdown formatting if present
    cleaned = raw_text.strip().replace("```json", "").replace("```", "")

    # Safe JSON parsing
    try:
        return json.loads(cleaned)
    except Exception:
        st.error("AI returned invalid JSON. Please try again.")
        st.write(cleaned)
        return {"mcqs": []}


# ---------------------------------------------------
# 🧠 TOPIC-BASED QUIZ GENERATOR
# ---------------------------------------------------
def fetch_questions_from_topic(topic, quiz_level):

    prompt = f"""
    You are an expert quiz creator.

    Create 5 multiple choice questions based on the topic below.

    Topic: {topic}
    Difficulty: {quiz_level}

    Return ONLY valid JSON in this format:
    {json.dumps(response_format)}
    """

    raw_text = call_gemini(prompt)

    cleaned = raw_text.strip().replace("```json", "").replace("```", "")

    try:
        return json.loads(cleaned)
    except Exception:
        st.error("AI returned invalid JSON. Please try again.")
        st.write(cleaned)
        return {"mcqs": []}


# ---------------------------------------------------
# 🎮 STREAMLIT APP UI
# ---------------------------------------------------
def main():

    st.title("🧠 Obsidian Circle Quiz Generator")

    # -----------------------------
    # SESSION STATE (PREVENT RESET)
    # -----------------------------
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "questions" not in st.session_state:
        st.session_state.questions = []

    # -----------------------------
    # MODE SELECTION
    # -----------------------------
    mode = st.radio("Choose input type:", ["Paragraph", "Topic"])

    if mode == "Paragraph":
        user_input = st.text_area("Paste your paragraph:", height=200)
    else:
        user_input = st.text_input("Enter a topic:")

    # Difficulty selection
    level = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

    # -----------------------------
    # GENERATE QUIZ BUTTON
    # -----------------------------
    if st.button("Generate Quiz"):

        if not user_input:
            st.error("Please enter input first!")
            return

        with st.spinner("Generating quiz..."):

            if mode == "Paragraph":
                data = fetch_questions_from_paragraph(user_input, level.lower())
            else:
                data = fetch_questions_from_topic(user_input, level.lower())

            st.session_state.questions = data.get("mcqs", [])
            st.session_state.quiz_generated = True

    # -----------------------------
    # DISPLAY QUIZ
    # -----------------------------
    if st.session_state.quiz_generated:

        user_answers = {}

        for i, q in enumerate(st.session_state.questions):

            st.write(f"**Q{i+1}: {q['mcq']}**")

            options = q["options"]

            user_answers[i] = st.radio(
                f"Select answer for Q{i+1}",
                list(options.keys()),
                format_func=lambda x: f"{x}) {options[x]}",
                key=f"q_{i}"
            )

        # -----------------------------
        # SUBMIT QUIZ
        # -----------------------------
        if st.button("Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.questions):

                if user_answers[i] == q["correct"]:
                    score += 1
                    st.success(f"Q{i+1}: Correct ✅")
                else:
                    st.error(f"Q{i+1}: Wrong ❌ (Correct: {q['correct']})")

            st.metric("Final Score", f"{score}/{len(st.session_state.questions)}")


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    main()
