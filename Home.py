import streamlit as st
import requests
import random as r
import time
from time import sleep
import json
import os
#from mods.data_processing import *

HIGH_SCORES = 'high_scores.txt'

# TODO: Quiz: Get username from login
# TODO: Quiz: Shuffle questions
# TODO: Quiz: Flipcards like quizlet
# TODO: Quiz: Save incorrect answers to a temp json file to retest.
# TODO: Quiz: Add feature: images to identify
# TODO: Quiz: Timer bonus
# TODO: Quiz: 
# TODO: Quiz: 
# TODO: Quiz: 
# TODO: Quiz: 
# TODO: Quiz: 

@st.cache_data
def get_questions(questions_file, placeholder=0) -> list:
    placeholder += 1
    with open(questions_file) as file:
        questions = json.load(file)
    return questions

def add_high_score(new_name, new_questions, new_score):
    high_scores = get_high_scores()
    high_scores.append((new_name, new_questions, new_score))
    # Sort the list of scores by the score in descending order
    high_scores.sort(key=lambda x: x[2], reverse=True)
    # # Keep only the top 10 scores
    # high_scores = high_scores[:10]
    # Rewrite the scores back to the file
    with open(HIGH_SCORES, "w") as file:
        for name, questions, score in high_scores:
            file.write(f"{name}/{questions}/{score}\n")

def get_high_scores():
    high_scores = []
    try:
        with open(HIGH_SCORES, "r") as file:
            for line in file:
                name, questions, score = line.strip().split('/')
                high_scores.append((name, int(questions), int(score)))
    except FileNotFoundError:
        # If the file doesn't exist, we assume no scores have been recorded yet
        high_scores = []
    return high_scores


def get_top_scores(file_path, top_n=10):
    scores = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split('/')
                    if len(parts) == 3:
                        name, questions, score = parts
                        add_high_score(f'\n{name}', int(questions), int(score))
    except FileNotFoundError:
        print("The score file does not exist.")
        return []
    # Sort the scores list by the score in descending order
    scores.sort(key=lambda x: x[2], reverse=True)
    # Return the top N scores
    return scores[:top_n]

def check_score():
    # Retrieve the highest score; assumes there's at least one score, otherwise returns 0
    high_scores = get_high_scores()
    current_score = st.session_state.correct
    highest_score = high_scores[0][2] if high_scores else 0

    # Check if the current session's score is higher than the highest score in the list
    if current_score > highest_score:
        try:
            hs_name = st.session_state.user_name.replace('/', '-')  # Sanitize user name to avoid file format issues
            questions_count = st.session_state.count
            # Use the add_high_score function to add the new score and update the list
            add_high_score(hs_name, questions_count, current_score)
            st.success(f'You made a new high score with {current_score}!')
        except FileNotFoundError:
            st.error('Failed to open the score file. Please check if the file exists.')


def check_answer(answer=''):
    st.session_state.count += 1
    if answer == st.session_state.correct_answer:
        msg.success(f'Correct! {answer}')
        #sleep(2)
        st.session_state.correct += 1
        st.session_state.consecutive += 1
        check_score()
    else:
        msg.error(f'Incorrect! The correct answer was {st.session_state.correct_answer}')
        sleep(2)

st.subheader('Test your Spiritual Knowledge!')

st.sidebar.success('Quiz Game!')
msg = st.empty()

# hs_name, hs_questions, hs = get_highest_score()

scores = get_high_scores()
if scores:
    st.sidebar.subheader('HIGH SCORES:')
    for score in scores:
        print(f"Name: {score[0]}, Questions Answered: {score[1]}, Score: {score[2]}")
        st.markdown(f'**{score[0]}**, with **{score[2]}** correct out of **{score[1]}** questions.')



user_name = st.text_input('What is your name?', max_chars=50, key='user_name',  value="Nonya")
if user_name:
    st.header(f'Welcome, {user_name}!')
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'consecutive' not in st.session_state:
        st.session_state.consecutive = 0
    if 'correct' not in st.session_state:
        st.session_state.correct = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = get_questions('questions.json')
        # st.session_state.questions = get_questions('final_questions.json')
        r.shuffle(st.session_state.questions)
    if st.session_state.count > 0 and st.session_state.count % len(st.session_state.questions) == 0:
        st.session_state.questions = get_questions(st.session_state.count)

    question = st.session_state.questions[st.session_state.count % len(st.session_state.questions)]

    st.session_state.correct_answer = question['correctAnswer']
    answers = question['incorrectAnswers'] + [st.session_state.correct_answer]
    r.shuffle(answers)

    st.write(question['question'])
    left_col, rt_col = st.columns(2)
    with left_col:
        st.button(answers[0], on_click=check_answer, kwargs=dict(answer=answers[0]))
        st.button(answers[1], on_click=check_answer, kwargs=dict(answer=answers[1]))
    with rt_col:
        st.button(answers[2], on_click=check_answer, kwargs=dict(answer=answers[2]))
        st.button(answers[3], on_click=check_answer, kwargs=dict(answer=answers[3]))

    st.write(f'Score: {st.session_state.correct} out of {st.session_state.count} questions.')
