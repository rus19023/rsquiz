import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase
cred = credentials.Certificate('firebase_creds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_quiz(file_path, quiz_name):
    # Read the JSON file
    with open(file_path, 'r') as file:
        quiz_data = json.load(file)
    
    # Create a new document in the 'quizzes' collection with the quiz name
    quiz_ref = db.collection('quizzes').document(quiz_name)
    
    # Set the data for the quiz
    quiz_ref.set({
        'questions': quiz_data
    })
    
    print(f"Quiz '{quiz_name}' has been successfully uploaded.")
    
    st.write(f"Quiz '{quiz_name}' has been successfully uploaded.")


# Example usage
#upload_quiz('GodsIntentIsToBringYouHome.json', 'GodsIntentIsToBringYouHome')
#upload_quiz('RejoiceInTheGiftOfPriesthoodKeys.json', 'RejoiceInTheGiftOfPriesthoodKeys')
#upload_quiz('CovenantConfidenceWithJesusChrist.json', 'CovenantConfidenceWithJesusChrist')

# TODO: automate getting talk, creating questions, saving as file, make a dropdown list to choose which file to upload, 

#upload_quiz('filename.json', 'filename')
#upload_quiz('filename.json', 'filename')
#upload_quiz('filename.json', 'filename')
#upload_quiz('filename.json', 'filename')