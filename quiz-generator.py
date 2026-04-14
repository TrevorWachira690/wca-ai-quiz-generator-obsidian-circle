# This is the codespace where all the codes will go to
# import necessary libraries
import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use st.cache_data to prevent re-running the API call on every refresh
@st.cache_data
def fetch_questions(text_content, quiz_level):
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Define the JSON structure we want
    response_format = {
        "mcqs": [
            {
                "mcq": "question text",
                "options": {"a": "choice 1", "b": "choice 2", "c": "choice 3", "d": "choice 4"},
                "correct": "a"
            }
        ]
    }

    prompt = f"""
    You are an expert quiz creator. Based on the text below, create a quiz with 5 multiple choice questions.
    Difficulty Level: {quiz_level}
    Text: {text_content}
    
    Return the response strictly as a JSON object following this format:
    {json.dumps(response_format)}
    """

    response = model.generate_content(prompt)
    
    # Clean up the response text (Gemini sometimes adds markdown backticks)
    raw_text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(raw_text)
