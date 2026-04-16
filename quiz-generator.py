import streamlit as st              # Used to build the web app interface
import google.generativeai as genai # Gemini AI library
import os                           # Helps access environment variables
import json                         # Helps work with JSON data
from dotenv import load_dotenv      # Loads variables from a .env file

# Load environment variables (like your API key)
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("_MY_GOOGLE_API_KEY"))

# This defines the structure (format) we expect from Gemini's response
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

# -----------------------------------------------------------
# FUNCTION 1: Generate questions from a PARAGRAPH
# -----------------------------------------------------------
def fetch_questions(text_content, quiz_level):

    # Create the Gemini model (this is the AI we are using)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    # This is the instruction we send to Gemini
    prompt = f"""
    You are an expert quiz creator. Based on the text below, create a quiz with 5 multiple choice questions.
    Difficulty Level: {quiz_level}
    Text: {text_content}
    
    Return the response strictly as a JSON object following this format:
    {json.dumps(response_format)}
    """

    # Send the prompt to Gemini and get a response
    response = model.generate_content(prompt)

    # Clean the response (sometimes Gemini adds ```json or ``` around the output)
    raw_text = response.text.strip().replace("```json", "").replace("```", "")

    # Convert the JSON string into a Python dictionary
    return json.loads(raw_text)


# -----------------------------------------------------------
# FUNCTION 2: Generate questions from a TOPIC
# -----------------------------------------------------------
def fetch_questions_from_topic(topic, quiz_level):

    # Create the same Gemini model
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    # Prompt for topic-based question generation
    prompt = f"""
    You are an expert quiz creator. Create a quiz with 5 multiple choice questions based on the topic below.
    Difficulty Level: {quiz_level}
    Topic: {topic}

    The questions should test general understanding of the topic.

    Return the response strictly as a JSON object following this format:
    {json.dumps(response_format)}
    """

    # Send request to Gemini
    response = model.generate_content(prompt)

    # Clean response text
    raw_text = response.text.strip().replace("```json", "").replace("```", "")

    # Convert to Python dictionary
    return json.loads(raw_text)


# -----------------------------------------------------------
# MAIN FUNCTION (Runs the Streamlit App)
# -----------------------------------------------------------
def main():

    # Title shown on the web app
    st.title("Obsidian Circle Quiz Generator")

    # ---------------------------
    # SESSION STATE SETUP
    # ---------------------------
    # These store values so they don't reset every time the app refreshes
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "questions" not in st.session_state:
        st.session_state.questions = None

    # ---------------------------
    # INPUT MODE SELECTION
    # ---------------------------
    # User chooses whether to input a paragraph or a topic
    mode = st.radio("Choose input type:", ["Paragraph", "Topic"])

    # Show input field depending on selection
    if mode == "Paragraph":
        user_input = st.text_area("Paste your content here:", height=200)
    else:
        user_input = st.text_input("Enter a topic:")

    # Dropdown for selecting difficulty level
    level = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

    # ---------------------------
    # GENERATE QUIZ BUTTON
    # ---------------------------
    if st.button("Generate Quiz"):

        # Check if user entered something
        if user_input:
            with st.spinner("Generating..."):

                # Call the correct function depending on mode
                if mode == "Paragraph":
                    data = fetch_questions(user_input, level.lower())
                else:
                    data = fetch_questions_from_topic(user_input, level.lower())

                # Store the questions in session state
                st.session_state.questions = data["mcqs"]
                st.session_state.quiz_generated = True

        else:
            st.error("Please provide input first!")

    # ---------------------------
    # DISPLAY QUIZ QUESTIONS
    # ---------------------------
    if st.session_state.quiz_generated:

        user_answers = {}  # Store user's answers

        # Loop through each question
        for i, q in enumerate(st.session_state.questions):

            # Display the question
            st.write(f"**Q{i+1}: {q['mcq']}**")

            options = q['options']

            # Create radio buttons for answer choices
            user_answers[i] = st.radio(
                f"Select an option for Q{i+1}",
                options=list(options.keys()),  # a, b, c, d
                format_func=lambda x: f"{x}) {options[x]}",  # show full text
                key=f"q_{i}"  # unique key for each question
            )

        # ---------------------------
        # SUBMIT QUIZ BUTTON
        # ---------------------------
        if st.button("Submit Quiz"):

            score = 0  # Track correct answers

            # Check each answer
            for i, q in enumerate(st.session_state.questions):

                if user_answers[i] == q['correct']:
                    score += 1
                    st.success(f"Q{i+1} is Correct!")
                else:
                    st.error(f"Q{i+1} is Incorrect. Correct answer: {q['correct']}")

            # Display final score
            st.metric("Final Score", f"{score}/{len(st.session_state.questions)}")


# This makes sure the app runs when you execute the script
if __name__ == "__main__":
    main()

# HOW TO ACTIVATE IT:
# 1. navigate to the folder where this script is located in your terminal (using `cd` command)
# 2. run: streamlit run quiz-generator.py

