from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from flask_session import Session
import os

# Directory for session files
session_dir = './.flask_session/'

if not os.path.exists(session_dir):
    os.makedirs(session_dir)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = session_dir
app.config['SESSION_PERMANENT'] = False
Session(app)

api_key='AIzaSyC6UDvIXqJOI0OIa7JkpxhdREg8yJZCAkQ'

def generate_response(prompt):
    model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, google_api_key=api_key)

    messages = [
        SystemMessage(content="You act as an AI chatbot and converse with the user to help them clear their doubts.Keep your answers short and to the point."),
        HumanMessage(content=prompt)
    ]
    
    responses = model(messages)
    answer = ""

    answer= responses.content

    return answer


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['conversation'].append({'role': 'user', 'text': user_input})

        if user_input.lower() in ["exit", "quit", "bye"]:
            response = "Goodbye! Have a great day!"
        else:
            response = generate_response(user_input)

        session['conversation'].append({'role': 'bot', 'text': response})
        return redirect(url_for('home'))

    return render_template('index.html', conversation=session['conversation'])

if __name__ == "__main__":
    app.run(debug=True)
