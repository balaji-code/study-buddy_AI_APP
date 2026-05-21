🧠 StudyBuddy — AI Powered Study Assistant
An AI-powered study companion built with Python and OpenAI that explains any topic, generates quizzes, and creates interactive flashcards.

🚀 Features

📖 Streaming Explanations — AI explains any topic word by word in real time
📝 Quiz Generation — Auto-generates multiple choice quizzes with explanations
🃏 Flashcard Study — Interactive flashcard sessions with hints
🔄 Menu Loop — Keep studying until you're ready to exit
🎯 Any Topic — Python, RAG, History, Science — anything!


🛠️ Built With

Python 3.9
OpenAI API — GPT-3.5-turbo
Streaming — Real time word by word responses
Structured Outputs — JSON forced responses for quizzes and flashcards
python-dotenv — Secure API key management


⚙️ Setup & Run
1. Clone the repo
bashgit clone https://github.com/balaji-code/study-buddy.git
cd study-buddy
2. Create virtual environment
bashpython3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Create .env file
OPENAI_API_KEY=your-key-here
MODEL=gpt-3.5-turbo
APP_NAME=StudyBuddy
5. Run the app
bashpython study_buddy.py

📸 Sample Usage
Enter a topic: RAG Systems

📖 StudyBuddy explaining: RAG Systems
──────────────────────────────────────
RAG stands for Retrieval Augmented Generation.
Think of it like giving an AI a textbook to
read before answering your questions...
(streams word by word!)
──────────────────────────────────────

What would you like to do next?
1. Generate a quiz
2. Study flashcards
3. Exit
→ 1

📝 Quiz: RAG Systems
==================================================
Q1: What does RAG stand for?
   A) Random Access Generation
   B) Retrieval Augmented Generation
   C) Recursive AI Generation
   D) Rapid Answer Generation
==================================================

See answers? (yes/no): yes

✅ Answers:
Q1: B — RAG stands for Retrieval Augmented Generation

What would you like to do next?
1. Generate a quiz
2. Study flashcards
3. Exit
→ 2

🃏 Studying: RAG Systems
Total cards: 5
──────────────────────────────────────
Card 1/5
FRONT: What does RAG stand for?
💡 Hint: Think about what it retrieves...

Press ENTER to flip...

BACK: Retrieval Augmented Generation

📚 Concepts Practised

OpenAI API integration
Streaming responses with stream=True
Structured JSON outputs with response_format
System prompts for AI personality
Conversation history management
Interactive CLI application design
Error handling for API calls
Environment variables for API keys


👨‍💻 Author
Balaji — AI Engineer in training
Building towards a full AI-powered study platform with RAG, vector databases, and web interface.