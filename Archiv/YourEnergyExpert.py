import streamlit as st
from openai import OpenAI
from EnergyConfig import *

client = OpenAI(api_key=open("./keys.txt", "r").read().strip())
#client = OpenAI(api_key=st.secrets["DB_TOKEN"])

st.set_page_config(
    page_title="Your Travel Agent",
    #layout="wide",
    initial_sidebar_state="expanded"  # This expands the sidebar
)

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": system_prompt},
            *input_text
            ],
    )
    return chat_completion.choices[0].message.content

# Title for the app
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "user", "content": greeting}
    ]

# Sidebar for input parameters

st.sidebar.title("Your Travel Agent")

# Input fields
where = st.sidebar.text_input("Where do you want to go? Tell me as much as you think is of interest for me to plan your trip.", "")
duration = st.sidebar.text_input("How long will your trip be?", "")
who = st.sidebar.text_input("Who are you? How many? What are your interests? Tell me about yourself...", "")
why = st.sidebar.text_input("Why you do this trip? Adventure, Relaxation, ...?", "")
price = st.sidebar.text_input("How much are you willing to spend? Feel free to answer qualitatively", "")
#galvanic_isolation = st.sidebar.checkbox("Galvanically isolated?")
anything = st.sidebar.text_input("Anything else to be considered?", "")

st.session_state.messages.append({"role": "user", "content": f"Where: {where}, Who: {who}, Duration: {duration}, Why: {why}, Price: {price}, {anything}"})

if 'button_labels' not in st.session_state:
    #st.session_state.button_labels = []
    response = ""

# Button to start the analysis
if st.sidebar.button("Suggest Trip"):
    with st.spinner("Thinking..."):
        response = chat_with_openai(st.session_state.messages)

st.write(response) 