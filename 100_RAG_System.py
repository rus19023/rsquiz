import streamlit as st
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import requests
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data for sentence tokenization
nltk.download('punkt', quiet=True)

# Load pre-trained models
@st.cache_resource
def load_models():
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    qa_tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    qa_model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
    return embedding_model, qa_tokenizer, qa_model

embedding_model, qa_tokenizer, qa_model = load_models()

@st.cache_data
def load_corpus(url):
    response = requests.get(url)
    text = response.text
    sentences = sent_tokenize(text)
    return sentences[:1000]  # Limit to first 1000 sentences for this example

# Load a larger corpus (e.g., a public domain book)
corpus = load_corpus("https://www.gutenberg.org/files/1342/1342-0.txt")  # Pride and Prejudice

# Create embeddings for the corpus
@st.cache_resource
def create_embeddings_and_index(corpus):
    corpus_embeddings = embedding_model.encode(corpus)
    dimension = corpus_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(corpus_embeddings.astype('float32'))
    return index, corpus_embeddings

index, corpus_embeddings = create_embeddings_and_index(corpus)

def search_similar_sentences(query, top_k=5):
    query_vector = embedding_model.encode([query])
    distances, indices = index.search(query_vector.astype('float32'), top_k)
    return [corpus[i] for i in indices[0]], distances[0]

def answer_question(question, context):
    inputs = qa_tokenizer(question, context, return_tensors="pt")
    with torch.no_grad():
        outputs = qa_model(**inputs)
    
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = qa_tokenizer.convert_tokens_to_string(qa_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
    
    return answer

st.title("Enhanced RAG Q&A App")

user_question = st.text_input("Ask a question about Pride and Prejudice:")

if user_question:
    similar_sentences, distances = search_similar_sentences(user_question)
    context = " ".join(similar_sentences)

    answer = answer_question(user_question, context)

    st.write("Retrieved context (with relevance scores):")
    for sentence, distance in zip(similar_sentences, distances):
        relevance_score = 1 / (1 + distance)  # Convert distance to a relevance score
        st.write(f"- ({relevance_score:.2f}) {sentence}")

    st.write("\nAnswer:")
    st.write(answer)

    st.write("\nConfidence Analysis:")
    answer_embedding = embedding_model.encode([answer])[0]
    question_embedding = embedding_model.encode([user_question])[0]
    confidence_score = np.dot(answer_embedding, question_embedding) / (np.linalg.norm(answer_embedding) * np.linalg.norm(question_embedding))
    st.write(f"Confidence Score: {confidence_score:.2f}")

st.sidebar.header("About")
st.sidebar.write("This is an enhanced RAG (Retrieval-Augmented Generation) app built with Streamlit. It uses advanced sentence embeddings for retrieval and a sophisticated question-answering model to generate answers from Pride and Prejudice.")