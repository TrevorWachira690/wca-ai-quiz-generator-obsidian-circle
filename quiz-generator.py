# Import required libraries
import google.generativeai as genai   # Gemini AI library (used to generate quiz questions)
import os                             # Helps access environment variables (like API keys)
import json                           # Helps convert JSON text into Python dictionaries
from dotenv import load_dotenv        # Loads variables from a .env file into your program

# STEP 1: Loading API key from .env file
load_dotenv()  # This reads your .env file and loads environment variables

# This code gets your API key from the environment and connect to Gemini
genai.configure(api_key=os.getenv("_MY_GOOGLE_API_KEY"))
# os.getenv("_MY_GOOGLE_API_KEY") retrieves the API key securely from the .env file

# STEP 2: Define the expected response format

# This is the structure we expect Gemini to follow when returning questions
# It ensures the AI response is predictable and easy to process later

response_format = {
    "mcqs": [
        {
            "mcq": "question text",   # The actual question
            "options": {
                "a": "choice 1",      # Option A
                "b": "choice 2",      # Option B
                "c": "choice 3",      # Option C
                "d": "choice 4"       # Option D
            },
            "correct": "a"            # The correct answer (must match one of the options)
        }
    ]
}

# STEP 3: Function to generate questions using Gemini

def fetch_questions(prompt_text, quiz_level, is_topic=True):
#This function sends a request to Gemini AI and gets quiz questions.

    # Parameters:
    #- prompt_text: either a paragraph or a topic
    #- quiz_level: difficulty level (easy, medium, hard)
    #- is_topic: True if input is a topic, False if it's a paragraph
    
    # Create the Gemini model (this is the AI engine being used)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

   
    # Building the prompt that will be sent to gemini(The prompt follows the R-T-C-C-O framework)   
    # If the user input is a topic
    if is_topic:
        prompt = f"""
Role:
You are an expert quiz generator that creates high-quality multiple choice questions.

Task:
Generate 5 multiple choice questions based on the given topic.

Context:
- Difficulty level: {quiz_level}
- Topic: {prompt_text}

Constraints:
- Each question must have exactly 4 options (a, b, c, d)
- Only one correct answer per question
- Questions must match the specified difficulty level
- Do NOT include explanations
- Do NOT include any text outside the JSON format

Output:
Return ONLY valid JSON in the following structure:
{json.dumps(response_format)}
"""
    else:
        # If the user input is a paragraph
        prompt = f"""
Role:
You are an expert quiz generator that creates high-quality multiple choice questions.

Task:
Generate 5 multiple choice questions based on the provided text.

Context:
- Difficulty level: {quiz_level}
- Text: {prompt_text}

Constraints:
- Each question must have exactly 4 options (a, b, c, d)
- Only one correct answer per question
- Questions must be derived strictly from the provided text
- Do NOT include explanations
- Do NOT include any text outside the JSON format

Output:
Return ONLY valid JSON in the following structure:
{json.dumps(response_format)}
"""
    # Send request to Gemini AI

    response = model.generate_content(prompt)
    # Sends the prompt to Gemini and receives a response

    # Cleaning the response text
    # Sometimes Gemini wraps JSON in markdown like ```json ... ```
    # This removes those wrappers so we can process the JSON properly
    raw_text = response.text.strip().replace("```json", "").replace("```", "")

    # Convert JSONs into python dictionary    
    try:
        return json.loads(raw_text)
        # Converts the cleaned JSON string into a Python dictionary

    except:
        # If something goes wrong (e.g., invalid JSON format)
        print("Error parsing quiz. Try again.")
        return None

# STEP 4: Main Program (Function that runs EVERYTHING)

def main():

    # Display program title
    print("Obsidian Circle Quiz Generator\n")

    
    # Get user input type

    # This code asks the user what input they would like to put, whether its a paragraph or a topic 
    while True:   
        mode = input("Choose input type (1 = Paragraph, 2 = Topic): ").strip()

        # If user chooses paragraph input
        if mode == "1":
            user_input = input("\nPaste your paragraph:\n")
            is_topic = False  # Indicates the input is a paragraph
            break  #Exits the while loop after valid input

        elif mode == "2":
            # Otherwise treat input as a topic
            user_input = input("\nEnter a topic: ")
            is_topic = True  # Indicates the input is a topic
            break  # Exit loop after valid input

        else:
            # Invalid input, show this error message and repeats loop
            print("\n Invalid choice. Please select either:")
            print("1 → Paragraph")
            print("2 → Topic\n")
    
    # Get difficulty level
    
    level = input("Select difficulty (easy / medium / hard): ").lower()
    # Converts input to lowercase to avoid case mismatch issues
    
    # Generate quiz

    print("\nGenerating quiz...\n")

    # Call the function to get quiz data from Gemini
    data = fetch_questions(user_input, level, is_topic)

    # If something went wrong (e.g., JSON parsing failed), stop program
    if not data:
        return

    # Extract list of questions from returned data
    questions = data["mcqs"]

    score = 0  # Keeps track of correct answers

    # Loop through questions

    for i, q in enumerate(questions, 1):
     # enumerate() is a function that goes through each question and adds a number (i) starting from number 1, the q is the actual question data
        # Display the question
        print(f"\nQ{i}: {q['mcq']}")
        # Q{i} is the question number and {q[',mcq']} is the question text

        # Display all answer options (a, b, c, d)
        for key, value in q["options"].items():
          # q["options"] are the actual options provided by the model and .items() splits the dictionary of the choices into keys("a", "b", "c", "d") and their values, which are the answer texts  
            print(f"{key}) {value}")
          # This print function just prints each key and their value

        # Get user's answer
        answer = input("Your answer: ").lower().strip()
        # .lower() ensures case-insensitive comparison
        # .strip() removes extra spaces
 
        # Checking the user's answers

        if answer == q["correct"]:
            print("Correct!")
            score += 1  # Increase score for correct answer

        else:
            print(f"Incorrect. Correct answer: {q['correct']}")

    # DISPLAY FINAL SCORE

    print(f"\n Final Score: {score}/{len(questions)}")
    # Shows how many questions were answered correctly, {len(questions)} counts how many items were in the questions list

# STEP 5: Running the program

# This ensures the program runs only when the file is executed directly (and not when imported into another file)
# without the  __name__ == "__main__", the code would run when imported into another file
if __name__ == "__main__":
    main()
# main() is the function that runs all the codes encircled inside def main():
# How to run the program in terminal:
# python quiz_generator.py
