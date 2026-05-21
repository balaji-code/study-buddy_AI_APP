languages = ["Python", "JavaScript", "Java"]

for i, lang in enumerate(languages,1):
    print(f"{i}. {lang}")

students = [
    {"name": "Balaji", "score": 90},
    {"name": "Ravi",   "score": 85}
]

for i,student in enumerate(students,1):
    print(f"{i}. {student['name']} - Score : {student['score']}")

questions = [
    {
        "question": "What is RAG?",
        "options": {
            "A": "Random Access Generation",
            "B": "Retrieval Augmented Generation",
            "C": "Recursive AI Generation"
        }
    }
]

for i,q in enumerate(questions,1):
    print(f"Q{i}: {q['question']}")
    for option, text in q['options'].items():
        print(f"   {option}) {text}")       
    