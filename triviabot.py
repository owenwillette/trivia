import requests

url = "https://raw.githubusercontent.com/owenwillette/trivia/refs/heads/main/triviaquestions.json"
response = requests.get(url)
trivia_questions = response.json()

for q in trivia_questions:
    print(q["question"])
    for i, option in enumerate(q["options"], start=1):
        print(f"{i}. {option}")
