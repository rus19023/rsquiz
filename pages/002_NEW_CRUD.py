import streamlit as st
from pymongo import MongoClient
import random
import time

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client.quiz_app
questions_collection = db.questions
categories_collection = db.categories

# Initialize session state for quiz metrics
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'consecutive_correct' not in st.session_state:
    st.session_state.consecutive_correct = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# Helper function to fetch a random question
def get_random_question():
    questions = list(questions_collection.find())
    return random.choice(questions) if questions else None

# Sidebar for adding new category
st.sidebar.subheader("Add New Category")
with st.sidebar.form(key='add_category_form'):
    category_name = st.text_input('Category Name')
    if st.form_submit_button('Add Category'):
        categories_collection.insert_one({"category": category_name})
        st.sidebar.success('Category added successfully')

# Sidebar for adding new question
st.sidebar.subheader("Add New Question")
with st.sidebar.form(key='add_question_form'):
    question_text = st.text_input('Question Text')
    categories = list(categories_collection.find())
    category_options = {category['category']: category['_id'] for category in categories}
    category_id = st.selectbox('Category', list(category_options.keys()))
    correct_answer = st.text_input('Correct Answer')
    incorrect_answers = st.text_area('Incorrect Answers (comma separated)').split(',')
    if st.form_submit_button('Add Question'):
        question_data = {
            "question_text": question_text,
            "category_id": category_options[category_id],
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answers
        }
        questions_collection.insert_one(question_data)
        st.sidebar.success('Question added successfully')

# Display a question with answer buttons
def display_question(question):
    st.write(f"Category: {categories_collection.find_one({'_id': question['category_id']})['category']}")
    st.write(f"Question: {question['question_text']}")
    answers = [question['correct_answer']] + question['incorrect_answers']
    random.shuffle(answers)
    for answer in answers:
        if st.button(answer):
            if answer == question['correct_answer']:
                st.session_state.correct_answers += 1
                st.session_state.consecutive_correct += 1
                st.success('Correct!')
            else:
                st.session_state.consecutive_correct = 0
                st.error('Incorrect!')
            st.session_state.current_question = None

# Main app display
st.title("Quiz Application")

# Dashboard
st.subheader("Dashboard")
st.write(f"Correct Answers: {st.session_state.correct_answers}")
st.write(f"Consecutive Correct Answers: {st.session_state.consecutive_correct}")
elapsed_time = time.time() - st.session_state.start_time
st.write(f"Time Elapsed: {elapsed_time:.2f} seconds")

# Management buttons
if st.button('Start New Quiz'):
    st.session_state.correct_answers = 0
    st.session_state.start_time = time.time()
    st.session_state.consecutive_correct = 0
    st.session_state.current_question = get_random_question()

# Display random question
if st.session_state.current_question is None:
    if st.button('Get Random Question'):
        st.session_state.current_question = get_random_question()
        if st.session_state.current_question is None:
            st.warning('No questions available. Please add some questions.')
else:
    display_question(st.session_state.current_question)
