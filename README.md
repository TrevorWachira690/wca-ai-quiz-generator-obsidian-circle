# wca-ai-quiz-generator

📌 Overview

- The Obsidian Circle AI Quiz Generator is a Python-based command-line tool that uses AI from Google Gemini to automatically generate multiple-choice quiz questions from a given topic or paragraph.

❗ Problem

Creating quiz questions manually is:
- Time-consuming
- Difficult without structured materials
- Limited in customization in existing tools

✅ Solution

The system automates quiz creation by:

- Generating MCQs instantly
- Allowing difficulty selection (Easy, Medium, Hard)
- Providing structured questions with answers

✅ How It Works

User selects input type (topic or paragraph)
Enters content
Chooses difficulty level
System sends a structured prompt to AI
AI returns questions in JSON format
User answers questions and receives a score

 ✅AI Design (R-T-C-C-O Framework)

Role: AI acts as an expert quiz generator
Task: Generate 5 MCQs
Context: Based on user input
Constraints:
4 options per question
One correct answer
Fixed difficulty
Output: Clean JSON format only
✅Technologies Used

Python
google.generativeai (AI integration)
dotenv (API security)
json (data handling)

 - Challenges & Solutions

Incorrect JSON from AI → Enforced strict prompt + cleaned output
Invalid user input → Added validation
API key exposure risk → Used .env file
Logic errors → Fixed program flow

  ✅Ethics



Bias: AI may generate biased questions → use neutral prompts
Privacy: No user data stored
Responsibility: Output should be reviewed for accuracy

✅Conclusion

The project demonstrates how AI and prompt engineering can automate quiz generation efficiently, saving time and improving learning experiences.

✅Future Improvements

-Web app (Streamlit)
-Score tracking & leaderboard
-Timer-based quizzes
-More question types (True/False, short answer)
