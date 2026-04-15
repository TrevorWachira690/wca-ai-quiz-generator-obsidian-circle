# This is the codespace where all the codes will go to
import streamlit as st              # Used to build the web app interface
import google.generativeai as genai # Gemini AI library
import os                           # Helps access environment variables
import json                         # Helps work with JSON data
from dotenv import load_dotenv      # Loads variables from a .env file

# Load environment variables (like your API key)
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
@st.cache_data  # This prevents repeated API calls for the same input (saves time & cost)
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
@st.cache_data
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

