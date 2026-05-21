from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

STUDY_BUDDY_PROMPT = """
You are StudyBuddy — an expert AI tutor.

Your personality:
→ Friendly and encouraging
→ Patient with confused students
→ Use simple language and real examples
→ Break complex topics into small pieces

Your rules:
→ Always explain with a real world analogy
→ Give one example after every explanation
→ End with "What would you like to explore next?"
→ Never make the student feel stupid
→ If asked to create a quiz — make 3 questions

Your expertise:
→ Programming and technology
→ Science and mathematics
→ History and general knowledge
→ Any topic the student needs help with
"""

def chat(conversation, user_input):
    # Step 1 — add user message
    conversation.append({"role": "user", "content": user_input})

    # Step 2 — call API with full history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Step 3 — store and return AI reply
    ai_reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": ai_reply})
    return ai_reply

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    conversation = [{"role": "system", "content": STUDY_BUDDY_PROMPT}]

    print("🧠 Welcome to StudyBuddy!")
    print("=" * 50)
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("👋 Goodbye! Keep learning!")
            break

        if not user_input:          # handle empty input
            print("Please type something!")
            continue

        print("\nStudyBuddy: ", end="")
        print(chat(conversation, user_input))
        print(f"\n[Messages in history: {len(conversation)}]")

except Exception as e:
    print(f"An error occurred: {e}")