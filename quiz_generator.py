import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_quiz(topic, num_questions=3):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a quiz generator.
                Always respond in valid JSON format like this:
                {
                    "topic": "topic name",
                    "questions": [
                        {
                            "question": "question text",
                            "options": {
                                "A": "option 1",
                                "B": "option 2",
                                "C": "option 3",
                                "D": "option 4"
                            },
                            "correct": "A",
                            "explanation": "why this is correct"
                        }
                    ]
                }"""
            },
            {
                "role": "user",
                "content": f"Create a quiz about {topic} with {num_questions} questions"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # Parse JSON string → Python dict
    quiz = json.loads(response.choices[0].message.content)
    return quiz

def display_quiz(quiz):
    print(f"\n📝 Quiz: {quiz['topic']}")
    print("=" * 50)

    for i, q in enumerate(quiz['questions'], 1):
        print(f"\nQ{i}: {q['question']}")
        for option, text in q['options'].items():
            print(f"   {option}) {text}")

    print("=" * 50)

def show_answers(quiz):
    print("\n✅ Answers:")
    for i, q in enumerate(quiz['questions'], 1):
        print(f"Q{i}: {q['correct']} — {q['explanation']}")

def generate_flashcards(topic, num_cards=5):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a flashcard generator.
                Always respond in valid JSON format like this:
                {
                    "topic": "topic name",
                    "flashcards": [
                        {
                            "front": "question or concept",
                            "back": "answer or explanation",
                            "hint": "a helpful hint"
                        }
                    ]
                }"""
            },
            {
                "role": "user",
                "content": f"Create {num_cards} flashcards about {topic}"
            }
        ],
        response_format={"type": "json_object"}
    )

    flashcards = json.loads(response.choices[0].message.content)
    return flashcards


def study_flashcards(flashcards):
    cards = flashcards["flashcards"]
    total = len(cards)

    print(f"\n🃏 Studying: {flashcards['topic']}")
    print(f"Total cards: {total}")
    print("=" * 50)
    print("Press ENTER to flip | Type 'quit' to stop\n")

    for i, card in enumerate(cards, 1):
        print(f"\nCard {i}/{total}")
        print(f"{'─'*50}")
        print(f"FRONT: {card['front']}")
        print(f"💡 Hint: {card['hint']}")

        action = input("\nPress ENTER to flip...").strip()
        if action.lower() == "quit":
            break

        print(f"\nBACK: {card['back']}")
        print(f"{'─'*50}")

        input("Press ENTER for next card...")

    print("\n✅ Flashcard session complete!")

def stream_explanation(topic):
    print(f"\n📖 StudyBuddy explaining: {topic}\n")
    print("─" * 50)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are StudyBuddy — explain topics clearly with examples."
            },
            {
                "role": "user",
                "content": f"Explain {topic} in simple terms with a real world example"
            }
        ],
        stream=True    # ← enable streaming!
    )

    # Print each chunk as it arrives
    for chunk in response:
        content = chunk.choices[0].delta.content
        print(content or "", end="", flush=True)

    print("\n" + "─" * 50)


try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    topic = input("Enter a topic: ").strip()
    stream_explanation(topic)

    # Keep showing menu until user exits!
    while True:
        print("\nWhat would you like to do next?")
        print("1. Generate a quiz")
        print("2. Study flashcards")
        print("3. Exit")

        option = input("\nEnter choice (1-3): ").strip()

        if option == "1":
            quiz = generate_quiz(topic)
            display_quiz(quiz)
            answer = input("\nSee answers? (yes/no): ").strip().lower()
            if answer == "yes":
                show_answers(quiz)
            elif answer == "no":
                print("Okay, try the quiz on your own!")

        elif option == "2":
            flashcards = generate_flashcards(topic)
            study_flashcards(flashcards)

        elif option == "3":
            print("\n👋 Goodbye! Keep learning!")
            break    # ← exits the while loop!

        else:
            print("❌ Invalid choice! Enter 1, 2 or 3")

except Exception as e:
    print(f"An error occurred: {e}")