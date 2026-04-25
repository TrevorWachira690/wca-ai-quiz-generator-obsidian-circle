# WCA-AI-QUIZ-GENERATOR

## 1. Coverpage
- Group name=Obsidian Circle
- Member names=Trevor Mbiriri, Joy Cindy, Mary Ayako Khamati, Blessy Muigai, Peace Mwende
- Github link= https://github.com/TrevorWachira690/wca-ai-quiz-generator-obsidian-circle.git
- Tool name= Obsidian Circle Quiz Generator
- Date= 26th April 2026

## 2. Problem Statement
Creating quiz questions manually is usually:
- Time-consuming
- Difficult without structured materials
- Limited in customization in existing tools

However, this tool automates quiz creation by:

- Generating MCQs instantly
- Allowing difficulty selection (Easy, Medium, Hard)
- Providing structured questions with answers

This benefits professionals such as teachers or even examiners since they'll spend less time on conducting research so as to provide questions to their students. 
This also benefits students who are revising coursework or even self learners who are exploring new topics.

## 3. Tool description(How It Works)
1. The user selects an input type (Either Topic or paragraph)
2. User selects a difficulty level(Easy, Medium or Hard)
3. The system sends a structured prompt to the AI model.
4. The AI model responds by displaying quiz questions.
6. It then accepts the users answers.
7. After, it compares the user's answers with the actual answers and calculates the final score

## 4. AI Instruction Design (R-T-C-C-O Framework)

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

## 5. Technical overview (How the code works)
1. First, the tool imports the required libraaries (google.generativeai, os, JSON)
2. It then loads an API key from a .env file, whch is then connected to gemini AI
3. We then create a response format wwich the AI model should follow when returning questions.
4. Then we create a function which generates questions using Gemini with its stated parameters
5. The AI model is then created after creating the function above.
6. We then build a prompt which follows the R-T-C-C-O framework. This prompt will be sent to the AI model so that it can generate questions, multiple chices and the correct answer for the user. Inside this prompt, we have variables such as quiz_level and prompt_text which are given certain values by the user.
7. The prompt is then sent to Gemini AI and the tool receives a response
8. The response text is then cleaned because our AI model can wrap the JSON in certain markdowns
9. Afterwards, the JSON is converted into a python dictionary and incase of an error, an error message is displayed.
10. The main programe then runs under the function **main()**
11. First, the program displays the title, which is the name of our tool
12. It then asks the user what input they want to put in (Either a paragraph or a topic) **Incase the user puts a different input, the program sends an error message and asks the user to put the right input**
13. After selecting, the user either pastes their selected input choice or types it out on the input area.
14. The program then asks the user the difficulty that they prefer.
15. Afterwards, the function to get quiz data from gemini is called, and given a variable called data, If anything went wrong in between, for example a JSON parsing failure, the program stops.
16. ...

## 6. Challenges & Solutions
These are some of the errors that we encountered when running the code of the tool:

|Challenge|Solution|
|---------|--------|
|API Key error|Using a .gitignore file to prevent exposure of API key|
|Complications from using streamlit|Used the terminal to run it instead|
|Unresolveable merge conflicts|Made commits one by one before editing anything else|
|User could use different values for input|The tool returns an error message when different values are used|

## 7. Ethics Reflection
Bias: AI may generate biased questions → use neutral prompts
Privacy: No user data stored
Responsibility: Output should be reviewed for accuracy

## 8. Conclusion and future improvements
In the future, we plan to add some improvents to the tool such as:
- Add a method of data storage of previous questions asked.
- Add a method of rewarding users who have higher scores.
- Make the tool have a capability of reading through pdf files or txt files so that it can obtain questions from it.
- Make the tool accessible to other users through browsers by making it into a live website.
- Make the tool provide solid explanations about each choice rather than just providing the correct choice.
- Make the tool have a leader board for the users as they answer questions more frequently.

## 9. Appendix

```python
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

```
