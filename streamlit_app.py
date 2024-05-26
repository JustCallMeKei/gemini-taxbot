import dotenv
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Replace the google_api_key here
 # Replace with your actual Google API key
load_dotenv()

# Replace the google_api_key here
 # Replace with your actual Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

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
    # Simulate model response for illustration (replace with actual model call)
    # Example: chatbot_response = model.generate_content(prompt).text
    chatbot_response = model.generate_content(prompt).text
    return chatbot_response if chatbot_response else "I'm sorry, I am having some trouble understanding. Could you rephrase your question?"

# Function to handle exit
def handle_exit():
    # Reset session state variables
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

# Placeholder function to calculate tax
def calculate_tax(income, deductions, filing_status):
    # Add your tax calculation logic here based on user inputs
    # For demonstration, let's assume a fixed tax rate and calculate tax
    tax_rate = 0.20  # Assume a tax rate of 20%
    tax_amount = (income - deductions) * tax_rate
    return tax_amount

# Display chat history
st.title("Tax Calculator Chatbot")
if st.session_state['chat_history']:
    st.write("### Chat History")
    for chat in st.session_state['chat_history']:
        st.write(chat)

# Step-wise user input handling
if st.session_state['step'] == 0:
    with st.form(key='start_form'):
        start = st.text_input("Hello! Do you want to calculate your tax based on Philippine tax law? (yes/no)", key="start_input")
        submit_start = st.form_submit_button(label='Submit')
        exit_start = st.form_submit_button(label='Exit')

    if submit_start:
        if start.lower() == "yes":
            st.session_state['current_prompt'].append("tax law Philippines")
            chatbot_response = generate_chatbot_response("short description of tax law Philippines")
            st.session_state['chat_history'].append(chatbot_response)
            st.session_state['step'] = 1
        else:
            current_prompt = "Alright. If you change your mind, feel free to ask!"
            chatbot_response = generate_chatbot_response("short description of tax law Philippines")
            st.session_state['chat_history'].append(chatbot_response)
        st.experimental_rerun()

    if exit_start:
        handle_exit()

elif st.session_state['step'] == 1:
    
    with st.form(key='taxpayer_type_form'):
        taxpayer_type = st.text_input("Step 1: What type of taxpayer are you? (e.g., employee, self-employed)", key="taxpayer_type_input")
        submit_taxpayer_type = st.form_submit_button(label='Submit')
        rerun_type = st.form_submit_button(label='Re-run previous step')
        exit_taxpayer_type = st.form_submit_button(label='Exit')

    if submit_taxpayer_type:
        st.session_state['taxpayer_type'] = taxpayer_type
        st.session_state['step'] = 2
        st.session_state['current_prompt'].append(taxpayer_type)
        chatbot_response = generate_chatbot_response(st.session_state['current_prompt'])
        st.session_state['chat_history'].append(chatbot_response)
        st.experimental_rerun()

    if rerun_type:
        st.session_state['step'] = 0
        st.experimental_rerun()

    if exit_taxpayer_type:
        handle_exit()
    
elif st.session_state['step'] == 2:
    with st.form(key='income_form'):
        income = st.text_input("Calculate tax?", key="income_input")
        submit_income = st.form_submit_button(label='Submit')
        exit_income = st.form_submit_button(label='Exit')
        rerun_type = st.form_submit_button(label='Re-run previous step')
    if submit_income:
        st.session_state['step'] = 3
        st.experimental_rerun()
    if rerun_type:
        st.session_state['step'] = 1
        if st.session_state['current_prompt'][1]:
            st.session_state['current_prompt'].pop()
        st.experimental_rerun()
    if exit_income:
        handle_exit()


elif st.session_state['step'] == 3:
    with st.form(key='filing_status_form'):
        income = st.text_input("Enter Income", key="filing_status_input")
        submit_income = st.form_submit_button(label='Submit')
        exit_income= st.form_submit_button(label='Exit')
        rerun_type = st.form_submit_button(label='Re-run previous step')
    if submit_income:
        st.session_state['income'] = income
        st.session_state['step'] = 4
        st.session_state['current_prompt'].append(f"get tax with this {income}")
        chatbot_response = generate_chatbot_response(st.session_state['current_prompt'])
        st.session_state['chat_history'].append(chatbot_response)
        st.experimental_rerun()
    if rerun_type:
        st.session_state['step'] = 2
        if st.session_state['current_prompt'][2]:
            st.session_state['current_prompt'].pop()
        st.experimental_rerun()

    if exit_income:
        handle_exit()

# Display final summary
elif st.session_state['step'] == 4:
    print(st.session_state['current_prompt'])
    st.write(f"### Summary of your inputs:")
    st.write(f"- Taxpayer Type: {st.session_state['taxpayer_type']}")
    st.write(f"- Income: {st.session_state['income']}")
    if st.button("Exit", key="exit_summary"):
        handle_exit()
        st.rerun()