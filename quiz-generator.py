# Import required libraries

import google.generativeai as genai   # Gemini AI library (used to generate quiz questions)
import os                             # Helps access environment variables (like API keys)
import json                           # Helps convert JSON text into Python dictionaries
from dotenv import load_dotenv        # Loads variables from a .env file into your program


# -----------------------------------------------------------
# STEP 1: LOAD API KEY FROM .env FILE
# -----------------------------------------------------------

load_dotenv()  # This reads your .env file

# Get your API key from the environment and connect to Gemini
genai.configure(api_key=os.getenv("_MY_GOOGLE_API_KEY"))


# -----------------------------------------------------------
# STEP 2: DEFINE THE EXPECTED RESPONSE FORMAT
# -----------------------------------------------------------

# This is the structure we EXPECT Gemini to follow when returning questions
# It helps us later when converting the response into usable Python data

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
# STEP 3: FUNCTION TO GENERATE QUESTIONS USING GEMINI
# -----------------------------------------------------------

def fetch_questions(prompt_text, quiz_level, is_topic=True):
    """
    This function sends a request to Gemini AI and gets quiz questions.

    Parameters:
    - prompt_text: either a paragraph or a topic
    - quiz_level: difficulty level (easy, medium, hard)
    - is_topic: True if input is a topic, False if it's a paragraph
    """

    # Create the Gemini model (the AI engine)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    # Build the prompt (instructions sent to Gemini)
    if is_topic:
        prompt = f"""
        Create 5 multiple choice questions based on this topic.
        Difficulty: {quiz_level}
        Topic: {prompt_text}

        Return ONLY JSON in this format:
        {json.dumps(response_format)}
        """
    else:
        prompt = f"""
        Create 5 multiple choice questions from this text.
        Difficulty: {quiz_level}
        Text: {prompt_text}

        Return ONLY JSON in this format:
        {json.dumps(response_format)}
        """

    # Send the prompt to Gemini and receive a response
    response = model.generate_content(prompt)

    # Clean the response text
    # Sometimes Gemini wraps JSON in ```json ... ```
    raw_text = response.text.strip().replace("```json", "").replace("```", "")

    # Try converting the JSON text into a Python dictionary
    try:
        return json.loads(raw_text)
    except:
        # If something goes wrong (bad format), show error
        print("❌ Error parsing quiz. Try again.")
        return None


# -----------------------------------------------------------
# STEP 4: MAIN PROGRAM (RUNS EVERYTHING)
# -----------------------------------------------------------

def main():

    # Display program title
    print("Obsidian Circle Quiz Generator\n")

    # ---------------------------
    # GET USER INPUT TYPE
    # ---------------------------

    # Ask user how they want to generate questions
    mode = input("Choose input type (1 = Paragraph, 2 = Topic): ").strip()

    # If user chooses paragraph
    if mode == "1":
        user_input = input("\nPaste your paragraph:\n")
        is_topic = False
    else:
        # Otherwise treat input as a topic
        user_input = input("\nEnter a topic: ")
        is_topic = True

    # ---------------------------
    # GET DIFFICULTY LEVEL
    # ---------------------------

    level = input("Select difficulty (easy / medium / hard): ").lower()

    # ---------------------------
    # GENERATE QUIZ
    # ---------------------------

    print("\nGenerating quiz...\n")

    # Call the function to get quiz data
    data = fetch_questions(user_input, level, is_topic)

    # If something went wrong, stop program
    if not data:
        return

    # Extract questions list from returned data
    questions = data["mcqs"]

    score = 0  # Keeps track of correct answers

    # ---------------------------
    # LOOP THROUGH QUESTIONS
    # ---------------------------

    for i, q in enumerate(questions, 1):

        # Display the question
        print(f"\nQ{i}: {q['mcq']}")

        # Display all answer options (a, b, c, d)
        for key, value in q["options"].items():
            print(f"{key}) {value}")

        # Get user's answer
        answer = input("Your answer: ").lower().strip()

        # Check if answer is correct
        if answer == q["correct"]:
            print("✅ Correct!")
            score += 1  # Increase score
        else:
            print(f"❌ Incorrect. Correct answer: {q['correct']}")

    # ---------------------------
    # DISPLAY FINAL SCORE
    # ---------------------------

    print(f"\n🎯 Final Score: {score}/{len(questions)}")


# -----------------------------------------------------------
# STEP 5: RUN THE PROGRAM
# -----------------------------------------------------------

# This ensures the program runs only when the file is executed directly
# (and not when imported into another file)

if __name__ == "__main__":
    main()

# How to run the program in terminal:
# python quiz_generator.py

