import json
import uuid
import streamlit as st

def read_file_in_groups(file_path, group_size=5):
    grouped_lines = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), group_size):
        group = lines[i:i + group_size]
        grouped_lines.append([line.strip() for line in group])

    return grouped_lines

def process_groups_to_json(grouped_lines):
    json_data = []

    for group in grouped_lines:
        if len(group) == 5:
            print(f'length of group: {len(group)}')
            question = group[0]
            answers = group[1:]
            correct_answer = ""
            incorrect_answers = []
            st.write(f'group[0]: {group[0]}')
            st.write(f'question: {question}')
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

def read_file_in_groups(file_path, group_size=5):
    grouped_lines = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), group_size):
        group = lines[i:i + group_size]
        grouped_lines.append([line.strip() for line in group])

    return grouped_lines

# Example usage
file_path = 'quiztest.txt'
file_path = 'quiz.txt'
grouped_lines = read_file_in_groups(file_path)

# for group in grouped_lines:
#     print(group)


def write_groups_to_python_file(groups, python_file_path):
    with open(python_file_path, 'w') as python_file:
        python_file.write("grouped_lines = [\n")
        for group in groups:
            python_file.write(f"    {group},\n")
        python_file.write("]\n")

# Example usage
#file_path = 'rs_quiztext.txt'
python_file_path = 'rs_converted.py'

grouped_lines = read_file_in_groups(file_path)
write_groups_to_python_file(grouped_lines, python_file_path)

print(f"Grouped lines have been written to {python_file_path}")


# Example usage
file_path = 'pages/hidethis/rs_quiztext.txt'
grouped_lines = read_file_in_groups(file_path)
json_data = process_groups_to_json(grouped_lines)
json_file_path = 'rs_quiz.json'
write_to_json_file(json_data, json_file_path)

print(f"Quiz data has been written to {json_file_path}")
