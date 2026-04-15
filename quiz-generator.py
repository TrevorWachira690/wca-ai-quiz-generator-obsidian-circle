# This is the codespace where all the codes will go to
import streamlit as st
import google.generativeai as genai
import json

# ---------------------------------------------------
# 🔐 API KEY (STREAMLIT CLOUD SAFE)
# ---------------------------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing API key. Add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ---------------------------------------------------
# 🧠 STABLE MODEL (CONFIRMED WORKING)
# ---------------------------------------------------
MODEL_NAME = "models/gemini-1.5-flash-002"

# ---------------------------------------------------
# 📦 QUIZ FORMAT
# ---------------------------------------------------
JSON_FORMAT = {
    "mcqs": [
        {
            "mcq": "Question here",
            "options": {
                "a": "Option A",
                "b": "Option B",
                "c": "Option C",
                "d": "Option D"
            },
            "correct": "a"
        }
    ]
}

# ---------------------------------------------------
# 🤖 GEMINI CALL
# ---------------------------------------------------
def ask_gemini(prompt: str):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini Error: {e}")
        return ""

# ---------------------------------------------------
# 🧠 GENERATE QUIZ
# ---------------------------------------------------
def generate_quiz(input_text, level, mode):

    if mode == "Paragraph":
        instruction = "Create 5 MCQs from this paragraph."
    else:
        instruction = "Create 5 MCQs about this topic."

    prompt = f"""
    You are a quiz generator AI.

    {instruction}

    Input:
    {input_text}

    Difficulty: {level}

    Return ONLY valid JSON like this:
    {json.dumps(JSON_FORMAT)}
    """

    raw = ask_gemini(prompt)

    if not raw:
        return {"mcqs": []}

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

    st.title("🧠 AI Quiz Generator (Gemini)")

    # --- session state safe init ---
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "generated" not in st.session_state:
        st.session_state.generated = False

    # --- input mode ---
    mode = st.radio("Choose input type:", ["Paragraph", "Topic"])

    if mode == "Paragraph":
        user_input = st.text_area("Enter paragraph:", height=200)
    else:
        user_input = st.text_input("Enter topic:")

    level = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])

    # --- generate ---
    if st.button("Generate Quiz"):

        if not user_input:
            st.warning("Please enter input.")
            return

        with st.spinner("Generating..."):
            data = generate_quiz(user_input, level, mode)

            st.session_state.questions = data.get("mcqs", [])
            st.session_state.generated = True

    # --- display quiz ---
    if st.session_state.generated and st.session_state.questions:

        answers = {}
        score = 0

        for i, q in enumerate(st.session_state.questions):

            st.write(f"**Q{i+1}: {q['mcq']}**")

            options = q["options"]

            answers[i] = st.radio(
                "Select answer:",
                list(options.keys()),
                format_func=lambda x: f"{x}) {options[x]}",
                key=f"q_{i}"
            )

        # --- submit ---
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
