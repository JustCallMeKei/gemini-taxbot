import dotenv
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")  # I used Gemini since it's free
chat = model.start_chat(history=[])

# Declaring session state variables
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
# Track the current step in the process
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'current_prompt' not in st.session_state:
    st.session_state['current_prompt'] = []
if 're_run_button_clicked' not in st.session_state:
    st.session_state['re_run_button_clicked'] = False

# Function to generate chatbot response
def generate_chatbot_response(prompt):
    """Generates chatbot response using the model and the current prompt"""
    conversation_history = '\n'.join(st.session_state['chat_history'] + [prompt])
    chatbot_response = model.generate_content(conversation_history).text
    return chatbot_response if chatbot_response else "I'm sorry, I am having some trouble understanding. Could you rephrase your question?"

# Function to handle exit button
def handle_exit():
    # Empty session state variables
    st.session_state['step'] = 0
    st.session_state['taxpayer_type'] = ""
    st.session_state['income'] = ""
    st.session_state['deductions'] = ""
    st.session_state['filing_status'] = ""
    st.session_state['chat_history'].append("Thank you for using the Tax Calculator Chatbot. Goodbye!")
    st.session_state['current_prompt'] = []
    # JavaScript to reload the page
    st.write('<script>location.reload()</script>', unsafe_allow_html=True)

# Display chat history
st.title("Tax Calculator Chatbot")
if st.session_state['chat_history']:
    st.write("### Chat History")
    for chat in st.session_state['chat_history']:
        st.write(chat)

# Step-wise input handling
# Most code of each step are similar with only differences in content
if st.session_state['step'] == 0:
    with st.form(key='start_form'):
        start = st.text_input("Hello! Do you want to calculate your tax based on Philippine tax law? (yes/no)", key="start_input")
        #Forms were used to avoid the webpage from returning to the very top everytime a user clicks a button.
        submit_start = st.form_submit_button(label='Submit')
        exit_start = st.form_submit_button(label='Exit')

    if submit_start:  # If the answer is yes, the program continues to step 2, but it will display first a short description of tax laws in the Philippines as a guide for the next step
        if start.lower() == "yes":
            st.session_state['current_prompt'].append("tax law Philippines")
            chatbot_response = generate_chatbot_response("short description of tax law and its taxpayers Philippines")
            st.session_state['chat_history'].append(f"You: {start}")
            st.session_state['chat_history'].append(f"Bot: {chatbot_response}")
            st.session_state['step'] = 1
            st.rerun()
        else:  # Any other answer than yes will rerun the same step
            st.write(f"You: {start}")
            st.write("Bot: Alright. If you change your mind, feel free to ask!")
    if exit_start:
        handle_exit()

elif st.session_state['step'] == 1:  # Step 1 asks what type of taxpayer they are in the Philippines
    with st.form(key='taxpayer_type_form'):
        taxpayer_type = st.text_input("Step 1: What type of taxpayer are you? (e.g., employee, self-employed)", key="taxpayer_type_input")
        submit_taxpayer_type = st.form_submit_button(label='Submit')
        rerun_type = st.form_submit_button(label='Re-run previous step')
        exit_taxpayer_type = st.form_submit_button(label='Exit')

    if submit_taxpayer_type:
        st.session_state['taxpayer_type'] = taxpayer_type
        st.session_state['step'] = 2
        st.session_state['current_prompt'].append(taxpayer_type)
        chatbot_response = generate_chatbot_response(f"You are a {taxpayer_type}.")
        st.session_state['chat_history'].append(f"You: {taxpayer_type}")
        st.session_state['chat_history'].append(f"Bot: {chatbot_response}")
        st.rerun()

    if rerun_type:  # If rerun step button is clicked, return to step 0 and remove all responses from the previous step
        if st.session_state['current_prompt']:
            st.session_state['current_prompt'].pop()
        if st.session_state.get('taxpayer_type'):
            del st.session_state['taxpayer_type']
        st.session_state['step'] = 0
        st.rerun()

    if exit_taxpayer_type:  # If exit is clicked, return to step 0 as well but emptying all session state
        handle_exit()

elif st.session_state['step'] == 2:  # Step 2 asks if they want to calculate their tax
    with st.form(key='income_form'):
        income = st.text_input("Step 2: Enter income to calculate tax", key="income_input")
        submit_income = st.form_submit_button(label='Submit')
        rerun_type = st.form_submit_button(label='Re-run previous step')
        exit_income = st.form_submit_button(label='Exit')

    if submit_income:  # Then we move to step 3 if they clicked yes
        st.session_state['income'] = income
        st.session_state['step'] = 3
        st.session_state['current_prompt'].append(income)
        chatbot_response = generate_chatbot_response(f"Let's calculate the tax for an income of {income}.")
        st.session_state['chat_history'].append(f"You: {income}")
        st.session_state['chat_history'].append(f"Bot: {chatbot_response}")
        st.rerun()

    if rerun_type:
        if st.session_state['current_prompt']:
            st.session_state['current_prompt'].pop()
        if st.session_state.get('income'):
            del st.session_state['income']
        st.session_state['step'] = 1
        st.rerun()

    if exit_income:
        handle_exit()

elif st.session_state['step'] == 3:  # Step 3 handles the filing status of the user, are they single or are they married. 
    # Tax laws in the Philippines take into consideration whether both spouses combine their income or file separate taxes
    with st.form(key='filing_status_form'):
        filing_status = st.text_input("Step 3: Enter Filing Status", key="filing_status_input")
        submit_filing_status = st.form_submit_button(label='Submit')
        exit_filing_status = st.form_submit_button(label='Exit')
        rerun_type = st.form_submit_button(label='Re-run previous step')

    if submit_filing_status: 
        st.session_state['filing_status'] = filing_status
        st.session_state['step'] = 4
        st.session_state['current_prompt'].append(filing_status)
        chatbot_response = generate_chatbot_response(f"Income: {st.session_state['income']}, Filing Status: {filing_status}")
        st.session_state['chat_history'].append(f"You: {filing_status}")
        st.session_state['chat_history'].append(f"Bot: {chatbot_response}")
        st.rerun()

    if rerun_type:
        if st.session_state['current_prompt']:
            st.session_state['current_prompt'].pop()
        if st.session_state.get('filing_status'):
            del st.session_state['filing_status']
        st.session_state['step'] = 2
        st.rerun()

    if exit_filing_status:
        handle_exit()

# Last step of the process
elif st.session_state['step'] == 4:
    st.write(f"Thank you for chatting with me. Please exit if you want to start from step 1")
    prompt = st.text_input("Ask me!")

    if st.button("Submit"):
        st.session_state['current_prompt'].append(prompt)
        chatbot_response = generate_chatbot_response(prompt)
        st.session_state['chat_history'].append(f"You: {prompt}")
        st.session_state['chat_history'].append(f"Bot: {chatbot_response}")
        st.rerun()

    if st.button("Exit", key="exit_summary"):
        handle_exit()
        st.rerun()
