from flask import Flask, render_template, request, jsonify
import nltk
import random
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Healthcare-focused intents for training the chatbot
intents = {
    "greetings": {
        "patterns": ["hello", "hi", "hey", "howdy", "good day"],
        "responses": ["Hello! How can I assist you with your health today?", "Hi! How are you feeling today?"]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you later"],
        "responses": ["Goodbye! Take care of your health.", "See you later! Stay healthy!"]
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "that's helpful"],
        "responses": ["You're welcome! Stay well!", "Happy to help!", "No problem, take care!"]
    },
    "symptoms": {
        "patterns": ["headache", "dizzy", "fever"],
        "responses": ["For headaches, try resting and staying hydrated. If it persists, consult a doctor.",
                      "Dizziness can be a sign of dehydration or low blood pressure. Try drinking water and resting.",
                      "For a fever, keep yourself hydrated and rest. If it’s severe, see a healthcare professional."]
    },
    "conditions": {
        "patterns": ["diabetes", "hypertension", "asthma"],
        "responses": ["Diabetes is a chronic condition where the body struggles to manage blood sugar levels.",
                      "Hypertension is high blood pressure, a condition that can lead to heart issues.",
                      "Asthma is a condition where your airways narrow, making it hard to breathe."]
    },
    "advice": {
        "patterns": ["improve health", "healthy habits", "better sleep"],
        "responses": ["Eat a balanced diet, exercise regularly, and get plenty of rest.",
                      "Healthy habits include regular physical activity, proper sleep, and a balanced diet.",
                      "For better sleep, maintain a regular schedule, avoid caffeine before bed, and create a relaxing environment."]
    }
}


# Function to process and lemmatize text
def process_input(input_text):
    tokens = nltk.word_tokenize(input_text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)


# Prepare data for pattern matching
patterns = []
responses = []

for intent, data in intents.items():
    for pattern in data['patterns']:
        patterns.append(process_input(pattern))
        responses.append(data['responses'])

# Vectorize patterns using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)


# Function to get a response based on user input
def get_response(user_input):
    user_input_processed = process_input(user_input)
    user_input_vector = vectorizer.transform([user_input_processed])

    # Compute similarity between user input and patterns
    similarities = cosine_similarity(user_input_vector, X)
    highest_similarity_idx = similarities.argmax()

    # Check if similarity is above a threshold
    if similarities[0, highest_similarity_idx] > 0.2:  # Adjust threshold as needed
        return random.choice(responses[highest_similarity_idx])
    else:
        return "I'm sorry, I don't understand. Please consult a healthcare professional."


# Home route
@app.route('/')
def chatbot():
    return render_template('index.html')


# Route to handle chatbot responses
@app.route('/get_response', methods=['POST'])
def chatbot_response():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
