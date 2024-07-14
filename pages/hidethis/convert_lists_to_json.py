import json
import uuid
import streamlit as st

def process_file_to_json(file_path, group_size=5):
    json_data = []

    def line_generator():
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()

    gen = line_generator()
    while True:
        group = [next(gen, None) for _ in range(group_size)]
        if group[0] is None:
            break

        group = [line for line in group if line]  # Remove empty lines
        if len(group) != 5:
            st.write(f'Skipping group due to incorrect length: {len(group)}')
            continue

        question = group[0]
        answers = group[1:]
        correct_answer = ""
        incorrect_answers = []

        for answer in answers:
            if answer.startswith("Correct!"):
                correct_answer = answer[len("Correct! "):]
            else:
                incorrect_answers.append(answer)

        json_entry = {
            "category": "Arts & Literature",
            "id": str(uuid.uuid4()),
            "correctAnswer": correct_answer,
            "incorrectAnswers": incorrect_answers,
            "question": question,
            "tags": ["arts_and_literature"],
            "type": "Multiple Choice",
            "difficulty": "easy",
            "regions": [],
            "isNiche": False
        }

        json_data.append(json_entry)

    return json_data

def write_to_json_file(data, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
root = 'pages/hidethis/'
file_path = f'{root}hum110.txt'
json_file_path = f'{root}hum110.json'

json_data = process_file_to_json(file_path)
write_to_json_file(json_data, json_file_path)

print(f"Quiz data has been written to {json_file_path}")
