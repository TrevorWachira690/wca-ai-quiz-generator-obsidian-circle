# This is the codespace where all the codes will go to
import streamlit as st
import google.generativeai as genai
import json

# ---------------------------------------------------
# 🔐 SAFE API KEY LOADING (STREAMLIT CLOUD)
# ---------------------------------------------------
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Missing API Key. Please add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# ---------------------------------------------------
# 🧠 STABLE MODEL (GUARANTEED AVAILABLE)
# ---------------------------------------------------
MODEL_NAME = "gemini-1.5-flash"

# ---------------------------------------------------
# 📦 EXPECTED JSON FORMAT
# ---------------------------------------------------
response_format = {
    "mcqs": [
        {
            "mcq": "question text",
            "options": {
                "a": "option 1",
                "b": "option 2",
                "c": "option 3",
                "d": "option 4"
            },
            "correct": "a"
        }
    ]
}

# ---------------------------------------------------
# 🤖 GEMINI CALL (NO CACHE = NO CLOUD ISSUES)
# ---------------------------------------------------
def call_gemini(prompt: str):

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return ""


# ---------------------------------------------------
# 🧠 PARAGRAPH QUIZ
# ---------------------------------------------------
def generate_from_paragraph(text, level):

    prompt = f"""
    You are an expert quiz generator.

    Create 5 multiple choice questions from the paragraph below.

    Difficulty: {level}

    Paragraph:
    {text}

    Return ONLY valid JSON in this format:
    {json.dumps(response_format)}
    """

    raw = call_gemini(prompt)

    cleaned = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except:
        st.error("Failed to parse AI response.")
        st.write(cleaned)
        return {"mcqs": []}


# ---------------------------------------------------
# 🧠 TOPIC QUIZ
# ---------------------------------------------------
def generate_from_topic(topic, level):

    prompt = f"""
    You are an expert quiz generator.

    Create 5 multiple choice questions about this topic.

    Topic: {topic}
    Difficulty: {level}

    Return ONLY valid JSON in this format:
    {json.dumps(response_format)}
    """

    raw = call_gemini(prompt)

    cleaned = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except:
        st.error("Failed to parse AI response.")
        st.write(cleaned)
        return {"mcqs": []}


# ---------------------------------------------------
# 🎮 STREAMLIT UI
# ---------------------------------------------------
def main():

    st.title("🧠 AI Quiz Generator (Gemini Powered)")

    # ---------------- INPUT MODE ----------------
    mode = st.radio("Choose input type:", ["Paragraph", "Topic"])

    if mode == "Paragraph":
        user_input = st.text_area("Paste your paragraph here:", height=200)
    else:
        user_input = st.text_input("Enter a topic:")

    # ---------------- DIFFICULTY ----------------
    level = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

    # ---------------- GENERATE BUTTON ----------------
    if st.button("Generate Quiz"):

        if not user_input:
            st.warning("Please enter input first.")
            return

        with st.spinner("Generating quiz..."):

            if mode == "Paragraph":
                data = generate_from_paragraph(user_input, level.lower())
            else:
                data = generate_from_topic(user_input, level.lower())

            st.session_state.questions = data.get("mcqs", [])
            st.session_state.generated = True

    # ---------------- QUIZ DISPLAY ----------------
    if "generated" in st.session_state and st.session_state.generated:

        score = 0
        answers = {}

        for i, q in enumerate(st.session_state.questions):

            st.write(f"**Q{i+1}: {q['mcq']}**")

            options = q["options"]

            answers[i] = st.radio(
                f"Select answer for Q{i+1}",
                list(options.keys()),
                format_func=lambda x: f"{x}) {options[x]}",
                key=f"q_{i}"
            )

        # ---------------- SUBMIT ----------------
        if st.button("Submit Quiz"):

            for i, q in enumerate(st.session_state.questions):

                if answers[i] == q["correct"]:
                    score += 1
                    st.success(f"Q{i+1}: Correct")
                else:
                    st.error(f"Q{i+1}: Wrong (Correct: {q['correct']})")

            st.metric("Final Score", f"{score}/{len(st.session_state.questions)}")


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    main()
