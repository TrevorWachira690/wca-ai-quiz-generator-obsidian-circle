# This is the codespace where all the codes will go to import streamlit as st import google.generativeai as genai import os import json from dotenv import load_dotenv # Load environment variables load_dotenv() genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Use st.cache_data to prevent re-running the API call on every refresh @st.cache_data def fetch_questions(text_content, quiz_level): # Initialize the Gemini model model = genai.GenerativeModel('gemini-2.5-flash-lite') # Define the JSON structure we want response_format = { "mcqs": [ { "mcq": "question text", "options": {"a": "choice 1", "b": "choice 2", "c": "choice 3", "d": "choice 4"}, "correct": "a" } ] } prompt = f""" You are an expert quiz creator. Based on the text below, create a quiz with 5 multiple choice questions. Difficulty Level: {quiz_level} Text: {text_content} Return the response strictly as a JSON object following this format: {json.dumps(response_format)} """ response = model.generate_content(prompt) # Clean up the response text (Gemini sometimes adds markdown backticks) raw_text = response.text.strip().replace("
import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API key not found. Make sure .env file is set correctly.")
    st.stop()

genai.configure(api_key=api_key)

# -------------------------------
# STABLE MODEL
# -------------------------------
MODEL_NAME = "gemini-1.5-flash"

# -------------------------------
# QUIZ FORMAT
# -------------------------------
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

# -------------------------------
# GENERATE QUESTIONS
# -------------------------------
@st.cache_data
def fetch_questions(text_content, quiz_level):

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
    You are an expert quiz creator.

    Create 5 multiple choice questions.

    Difficulty: {quiz_level}

    Text:
    {text_content}

    Return ONLY valid JSON in this format:
    {json.dumps(response_format)}
    """

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # clean markdown if Gemini adds it
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        st.error("Failed to parse AI response.")
        st.write(cleaned)
        return {"mcqs": []}

