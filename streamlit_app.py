import streamlit as st
import requests

# Define the Rasa server URL
RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook'

st.title('Rasa Chatbot Interface')

# Initialize a session state to hold the conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

def send_message(message):
    """Send a message to the Rasa server and get a response."""
    response = requests.post(RASA_SERVER_URL, json={'message': message})
    return response.json()

def add_to_conversation(role, text):
    """Add a message to the conversation history."""
    st.session_state.conversation.append({'role': role, 'text': text})

# Create a text input for the user to enter messages
user_input = st.text_input('You:', '')

# Create a button to send the message
if st.button('Send') and user_input:
    with st.spinner('Sending...'):
        # Add user message to the conversation
        add_to_conversation('user', user_input)
        
        # Get response from Rasa
        responses = send_message(user_input)
        
        # Add bot responses to the conversation
        for response in responses:
            if 'text' in response:
                add_to_conversation('bot', response['text'])

# Display the entire conversation history
if st.session_state.conversation:
    st.write("Conversation:")
    for message in st.session_state.conversation:
        if message['role'] == 'user':
            st.write(f"**You:** {message['text']}")
        elif message['role'] == 'bot':
            st.write(f"**Bot:** {message['text']}")
