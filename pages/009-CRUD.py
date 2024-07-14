from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from bson import ObjectId 
from mods.data_processing import *

PAGE_HEADER = 'Home'
PAGE_SUBHEADER = 'CRUD for HUM-110 QUIZ Game'
SITE_TITLE = f'HUM-110 | {PAGE_HEADER}'

MENU_ITEMS = {
       'Get Help': '/',
       'Report a bug': '/report_bug',
       'About': '# Add text here.'
}

### SESSION VARIABLES ###
# TODO: if logged in, show logout button
if st.sidebar.button("Logout", key='logout_btn'):
    logout()

if not 'consecutive_count' in st.session_state:
    st.session_state.consecutive_count = 0
        
st.session_state.show_popover = False

### CONSTANT VARIABLES ###
ADMIN = load_dbs(CLIENT, 'admin')
HUM110_DB = load_dbs(CLIENT, 'hum110')
print(f' \n\n CLIENT:  {CLIENT} \n\n ')
print(f' \n\n ADMIN:  {ADMIN} \n\n ')

### COLLECTIONS ###
HUM110_USERS = load_coll(HUM110_DB, 'users')
HUM110_CATEGORIES = load_coll(HUM110_DB, 'categories')
HUM110_QUESTIONS = load_coll(HUM110_DB, 'questions')
### CURSORS ###
ALL_HUM110_QUESTIONS = load_cursor(HUM110_QUESTIONS, {}, 'timestamp', st.session_state.srt_order)
ALL_HUM110_CATEGORIES = load_cursor(HUM110_CATEGORIES, {}, 'timestamp', st.session_state.srt_order)

# # Use current_op command
# current_operations = ADMIN.command('currentOp')

# # Print the current operations
# for operation in current_operations.get('inprog', []):
#     # Only print operations that have a 'ns' field (namespace)
#     if 'ns' in operation:
#         print(f"Operation ID: {operation.get('opid')}, Database: {operation.get('ns').split('.')[0]}")

# Alternatively, to get a list of all databases:
databases = CLIENT.list_database_names()
print("Databases available:", databases)



# Pydantic model for Category
class Category(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="id")
    category: str

# CRUD operations for Category
class CategoryCRUD:
    def __init__(self, category):
        self.category = category

    def to_dict(self):
        return {
            "category": self.category
        }
    
    @staticmethod
    def create(category: Category) -> str:
        category_dict = category.dict(exclude={"id"})
        result = category.insert_one(category_dict)
        return str(result.inserted_id)

    @staticmethod
    def read() -> list[Category]:
        categories = HUM110_CATEGORIES.find()
        return [Category(**category) for category in categories]

    @staticmethod
    def update(category_id: str, category: Category) -> int:
        category_dict = category.dict(exclude={"id"})
        result = HUM110_CATEGORIES.update_one({"_id": ObjectId(category_id)}, {"$set": category_dict})
        return result.modified_count

    @staticmethod
    def delete(category_id: str) -> int:
        result = HUM110_CATEGORIES.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count
    
# Pydantic model for question
class Question(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    #timestamp: datetime = datetime.now()
    category_id: str
    question_text: str
    correct_answer: str
    incorrect_answers: list[str]
    #is_done: bool = False
    #duedate: datetime
    #is_repeat: bool

# CRUD operations for Question
class Question_CRUD:
    @staticmethod
    def create(question: Question) -> str:
        question_dict = question.dict(exclude={"id"})
        result = HUM110_QUESTIONS.insert_one(question_dict)
        return str(result.inserted_id)

    @staticmethod
    def read() -> list[Question]:
        questions = HUM110_QUESTIONS.find()
        return [Question(**question) for question in questions]

    @staticmethod
    def update(question_id: str, question: Question) -> int:
        question_dict = question.dict(exclude={"id"})
        result = HUM110_QUESTIONS.update_one({"_id": ObjectId(question_id)}, {"$set": question_dict})
        return result.modified_count

    @staticmethod
    def delete(question_id: str) -> int:
        result = HUM110_QUESTIONS.delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count

# Streamlit UI
st.title("HUM-110 EXAMS STUDY")
st.subheader("Quiz Game")

col_question, col_cat = st.columns(2)
with col_cat:
    # Add category (modal form)
    with st.popover('\+ Category'):
        with st.form("Add New Category"):
            new_category_name = st.text_input("Category Name")
            if st.form_submit_button("Save"):
                if new_category_name:
                    new_category = CategoryCRUD(category=new_category_name)
                    new_category_id = new_category.create(new_category)
                    st.success(f"Category '{new_category.category}' added with ID: {new_category_id}")
                    # Close modal                
                    st.session_state.show_popover = not st.session_state.show_popover
                else:
                    st.warning("Please enter a category name")
with col_question:            
    with st.popover('\+ Question'):            
        # Create form
        with st.form('add_question'):
            question_task = st.text_input("Question")
            correct = st.text_input("Correct answer")
            incorrect1 = st.text_input("Incorrect answer #1")
            incorrect2 = st.text_input("Incorrect answer #2")
            incorrect3 = st.text_input("Incorrect answer #3")
            #duedate = st.date_input("Due Date")
            #is_repeat = st.checkbox("Repeat?")
            # Get list of categories from db for dropdown
            categories = HUM110_CATEGORIES.find({}, {'_id': 1, 'category': 1})
            #print(categories)
            # for document in categories:
            #     print(f'category: {document}')
                #print(f' \n\n category name: {category.catname} \n\n ')
            # st.sidebar.error(f' \n\n categories: {categories} \n\n ')
            # category_names = [category.name for category in categories]
            # Create dropdown of categories
            #categories = HUM110_CATEGORIES.find()
            #for key, value in categories.items():
                #st.sidebar.success(f'category: {key}, {value}')
            st.sidebar.success(f'categories: {categories}')
            for doc in categories:
                st.sidebar.success(f'category: {doc}')
            category_options = [(str(doc['_id']), doc['category']) for doc in categories]
            selected_category = st.selectbox("Select Category", category_options, format_func=lambda option: option[1])
            if selected_category:
                st.sidebar.success("Selected category ID:", selected_category[0])
                st.sidebar.success("Selected category name:", selected_category[1])
                st.sidebar.error(f'selected_category: {selected_category}')
                if st.form_submit_button("Add Question"):
                    new_question = Goal(timestamp=datetime.now(), question_task=question_task, is_done=False, duedate=duedate, is_repeat=is_repeat, category_id=selected_category)
                    question_id = GoalCRUD.create(new_question)
                    st.success(f"Question added with ID: {question_id}")
                    # Close modal                
                    st.session_state.show_popover = not st.session_state.show_popover
            else:
                st.warning("No categories found. Please create categories first.")

# Display Question
st.subheader("Quiz Questions")
for question in ALL_HUM110_QUESTIONS:
    st.sidebar.error(f'question: {question} \n\n')
    category = HUM110_CATEGORIES.find_one({"_id": question.category_id})
    if category:
        category_name = HUM110_CATEGORIES["category"]
    else:
        category_name = "General"
    st.sidebar.success(f"Category: {category_name}")
    st.sidebar.success(f"Question: {question.question_task}")
    st.sidebar.success(f"correct: {correct}")
    st.sidebar.success(f"incorrect: {category}")
    st.sidebar.success(f"Category: {category}")
    #st.write(f"Is Done?: {question.is_done}")
    #st.write(f"Due Date: {question.duedate}")
    #st.write(f"Repeat?: {question.is_repeat}")
    # Edit and Delete buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"Edit {question._id}", key=f"edit_{question.id}"):
            # Implement edit functionality
            pass
    with col2:
        if st.button(f"Delete {question.id}", key=f"delete_{question.id}"):
            # Implement delete functionality
            pass


# # TODO:
# add search
# add filters
# add sort asc/desc 
# add date done when marked done everytime
# how/when to check for various bonuses 
# add +10 points to current_points variable on completion of tasks, include check for bonuses
# save high scores to users document
# add personal dashboard with leaderboard scores
# high scores: daily, weekly, monthly, year-to-date, total, daily average, d-w-m-y-t on-time 
# add time bonus-tier of times before duedate
# add time penalty-if after duedate, deduct x points
# add consecutive on-time bonus tiers
# add no reminders bonus (a/k/a without being asked)
# add on-time time left bonus
# add all opted in users leaderboard, same high scores in a nice table
# add cheat resistance        