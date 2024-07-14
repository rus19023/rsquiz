#########################
#*  MONGODB Utilities  *#
#########################

import streamlit as st
import pymongo
from pymongo import MongoClient
# from pymongo import bson

# from pymongo.server_api import ServerApi
import os
import shutil
import tempfile
from datetime import datetime, timedelta
import zipfile
import pydantic
from pydantic_settings import BaseSettings
#import streamlit_pydantic as sp



st.set_page_config(
    page_title='Test your knowledge quiz!',initial_sidebar_state='expanded', page_icon='random',
    menu_items={
        'Get Help': 'mailto:danioshi@gmail.com',
        'Report a bug': "mailto:danioshi@gmail.com",
        'About': "# Made by Daniel Osorio. This app uses *The Trivia API*."
    }
)


def backup_collection(db_name, collection_name):
    # Create a temporary directory to store the backup files
    backup_dir = '/backups/' # tempfile.mkdtemp()
    # Backup MongoDB collection
    st.sidebar.error(f'db_name: {db_name}, collection_name: {collection_name}')
    backup_filepath = os.path.join(backup_dir, f"{db_name}-{collection_name}_backup_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.system(f"mongodump --db your_database --collection {collection_name} --out {backup_filepath}.bson")
    # Create a ZIP file containing the backup files
    zip_file = os.path.join(backup_dir, f"{backup_filepath}.zip")
    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, _, filenames in os.walk(backup_dir):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.relpath(filePath, backup_dir))
    return zip_file    

# st.write("Initializing search_term...")
if not 'search_term' in st.session_state:
    # st.write("search_term not found in session_state. Initializing...")
    st.session_state.search_term = ''    
    # st.write("Current search_term: ", st.session_state.search_term)
# else:    
    # st.write("Current search_term: ", st.session_state.search_term)

if not 'filter_option' in st.session_state:
    st.session_state.filter_option = {} 

if not 'sort' in st.session_state:
    st.session_state.sort = 'timestamp' 
    
if not 'srt_order' in st.session_state:
    st.session_state.srt_order = -1 

# TODO: remove hard-coded search term

# Set up db connection
@st.cache_resource
def setup_conn(conn_string):
    client = MongoClient(conn_string)
    return client

# CONN_STRING = os.environ["CONN_STRING"]
# SERVER_API = os.environ["SERVER_API"]

st.sidebar = st.empty()
SBAR_CONTAINER = st.empty()

# Set up db connection
@st.cache_resource
def setup_conn(conn_string):
    client = MongoClient(conn_string, PORT)
    return client

# Set up db   
@st.cache_resource
def load_dbs(_client, db):
    return _client.db

# Set up collections
@st.cache_resource
def load_coll(_db, coll):   
    return _db.coll

# Set up cursors
@st.cache_resource
def load_cursor(_coll, _filter, _sort, _srt_order):
    cursor = _coll.find(_filter)    
    sorted = cursor.sort(_sort, _srt_order)
    return sorted
  
def change_sort_order():
    st.session_state.srt_order = st.session_state.srt_order * -1

# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())

def add_new_document(_coll, data):
    try:
        st.write('add_new_document() invoked')
        # Attempt to insert the document
        new_id = _coll.insert_one(data)
        # Display success message
        st.sidebar.success(f'Document added successfully with id: {new_id.inserted_id}')
        return new_id
        st.rerun()  # Refresh the goal journal
    except Exception as e:
        # Handle any exceptions that occur during the insertion process
        st.sidebar.warning(f'Failed to save document: {e}')
        return None

def edit_document_by_id(coll, document_id, new_data):
    try:
        # Attempt to update the document
        update_result = coll.update_one({"_id": document_id}, {"$set": new_data})        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Document updated successfully
            st.sidebar.success(f"Document with ID {document_id} updated successfully.")
            st.rerun()  # Refresh the goal journal
            return True
        else:
            # Document not updated (no matching document found)
            st.sidebar.warning(f"No document found with ID {document_id}.")
            return False
    except Exception as e:
        # Handle any exceptions that occur during the update process
        st.sidebar.error(f"Failed to update document with ID {document_id}: {e}")
        sleep(3)
        return False

def delete_document_by_id(coll, document_id):
    try:
        # Attempt to delete the document
        delete_result = coll.delete_one({"_id": document_id})
        if delete_result.deleted_count == 1:
            st.rerun()       
            st.sidebar.success(f"Document with ID {document_id} deleted successfully.")
        else:        
            st.sidebar.warning(f"No document found with ID {document_id}.")
    except Exception as e:
        # Handle any exceptions that occur during the deletion process
        st.sidebar.error(f"Failed to delete document with ID {document_id}: {e}")
        sleep(3)

def delete_all_documents(coll):
    delete_all_result = coll.delete_many({})
    # Update the content of the container with your message
    st.sidebar.success(f"Deleted {delete_all_result.deleted_count} documents from the collection.")
    
def update_specific_string_many(coll, filter, update):
    update_result = coll.update_many(filter, update)
    st.sidebar.success(f"Updated {update_result.modified_count} documents in the collection.")
    
    query['$text'] = {'$search': search_term} 

# Function to list documents in a collection
def list_documents(db_name, coll_name):
    db = CLIENT[db_name]
    coll = db[coll_name]
    doc = coll.find()
    return doc

def check_existing_doc(coll, new_data):    
    # Check if the new data already exists in the collection
    existing_data = coll.find_one(new_data)
    if existing_data:
        st.sidebar.warning("Data already exists in the collection, not saved.")
    else:
        st.sidebar.success("Data does not exist in the collection. Data saved!")
       
def toggle_bool(coll, document_id, bool_field):
    # Retrieve the current document
    current_document = coll.find_one({"_id": document_id})
    if current_document:
        # Toggle the value of the "is_done" field
        new_value = not current_document.get(bool_field, False)
        # Update the document in the collection
        coll.update_one({"_id": document_id}, {"$set": {bool_field: new_value}})
        return new_value  # Return the new value of bool_field
    else:
        return None  # Document not found

# QUIZ_DB = load_dbs(CLIENT, 'quiz')

#SERVER_API = st.secrets.mongo.server
#PORT = st.secrets.mongo.port

if os.path.exists("/.dockerenv"):
    print("\n\n Running in Docker container \n\n")
    HOST = st.secrets.mongo.host
else:
    print("\n\n Not running in Docker container (assuming it's development environment) \n\n")
    HOST = st.secrets.mongo.host_dev

CONN_STRING = f'mongodb://{HOST}:{PORT}'# , {SERVER_API}'
# st.write(f'CONN_STRING: {CONN_STRING}')
CLIENT = setup_conn(CONN_STRING)

# st.sidebar.success(f'CLIENT: {CLIENT}')