import json
import time
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APITimeoutError, BadRequestError
import os
from dotenv import load_dotenv

load_dotenv()



def generate_quiz(topic, num_questions=3):
    is_valid, message = validate_input(topic)
    if not is_valid:
        print(f"❌ {message}")
        return None
    try:
        model = "gpt-3.5-turbo"
        messages = [
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
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        quiz = json.loads(response.choices[0].message.content)
        return quiz

    except AuthenticationError:
        print("❌ Invalid API key!")
        print("→ Check your OPENAI_API_KEY in .env file")
        return None

    except RateLimitError:
        print("⏳ Rate limit hit! Waiting 10 seconds...")
        time.sleep(10)
        print("→ Retrying now...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            print("❌ Still failing — try again later!")
            return None

    except APITimeoutError:
        print("❌ Request timed out!")
        print("→ OpenAI is slow right now — try again")
        return None

    except APIConnectionError:
        print("❌ No internet connection!")
        print("→ Check your network and try again")
        return None

    except BadRequestError as e:
        print(f"❌ Bad request: {e}")
        print("→ Check your messages format")
        return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

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
    is_valid, message = validate_input(topic)
    if not is_valid:
        print(f"❌ {message}")
        return None
    try:
        model = "gpt-3.5-turbo"
        messages = [
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
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"}
        )

        flashcards = json.loads(response.choices[0].message.content)
        return flashcards

    except AuthenticationError:
        print("❌ Invalid API key!")
        print("→ Check your OPENAI_API_KEY in .env file")
        return None

    except RateLimitError:
        print("⏳ Rate limit hit! Waiting 10 seconds...")
        time.sleep(10)
        print("→ Retrying now...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            print("❌ Still failing — try again later!")
            return None

    except APITimeoutError:
        print("❌ Request timed out!")
        print("→ OpenAI is slow right now — try again")
        return None

    except APIConnectionError:
        print("❌ No internet connection!")
        print("→ Check your network and try again")
        return None

    except BadRequestError as e:
        print(f"❌ Bad request: {e}")
        print("→ Check your messages format")
        return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


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
    is_valid, message = validate_input(topic)
    if not is_valid:
        print(f"❌ {message}")
        return

    print(f"\n📖 StudyBuddy explaining: {topic}\n")
    print("─" * 50)

    try:
        model = "gpt-3.5-turbo"
        messages = [
            {
                "role": "system",
                "content": "You are StudyBuddy — explain topics clearly with examples."
            },
            {
                "role": "user",
                "content": f"Explain {topic} in simple terms with a real world example"
            }
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        # Print each chunk as it arrives
        for chunk in response:
            content = chunk.choices[0].delta.content
            print(content or "", end="", flush=True)

        print("\n" + "─" * 50)

    except AuthenticationError:
        print("❌ Invalid API key!")
        print("→ Check your OPENAI_API_KEY in .env file")

    except RateLimitError:
        print("⏳ Rate limit hit! Waiting 10 seconds...")
        time.sleep(10)
        print("→ Retrying now...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                print(content or "", end="", flush=True)
            print("\n" + "─" * 50)
        except Exception:
            print("❌ Still failing — try again later!")

    except APITimeoutError:
        print("❌ Request timed out!")
        print("→ OpenAI is slow right now — try again")

    except APIConnectionError:
        print("❌ No internet connection!")
        print("→ Check your network and try again")

    except BadRequestError as e:
        print(f"❌ Bad request: {e}")
        print("→ Check your messages format")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def validate_setup():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env!")

    if not api_key.startswith("sk-"):
        raise ValueError("Invalid API key format!")

    print("✅ API key found!")
    return True


def validate_input(user_input):
    # Check length
    if len(user_input) > 500:
        return False, "Input too long! Keep it under 500 characters."

    # Check for injection patterns
    injection_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "forget your instructions",
        "you are now",
        "new instructions:",
        "override:",
        "system prompt:"
    ]

    user_lower = user_input.lower()
    for pattern in injection_patterns:
        if pattern in user_lower:
            return False, "⚠️ Invalid input detected!"

    return True, "valid"

try:

    validate_setup()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    topic = input("Enter a topic: ").strip()
    is_valid, message = validate_input(topic)
    if not is_valid:
        print(f"❌ {message}")
        exit(1)
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
