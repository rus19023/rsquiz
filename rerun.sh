#!/bin/bash

# Check for updates
outdated=$(poetry show --outdated)

# If updates are available, run the update command
if [ ! -z "$outdated" ]; then
    poetry update
fi

source /Users/drushlopez/Library/Caches/pypoetry/virtualenvs/my-reddit-9QrHQESL-py3.11/bin/activate

streamlit run /Users/drushlopez/000000-git/000000-python/000-STREAMLIT-APPS/streamlit-quiz/Home.py
