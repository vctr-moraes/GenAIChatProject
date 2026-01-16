import streamlit as st
import time
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

openai = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    max_tokens=2000)

# Streamed response emulator
def response_generator(model_response):
    for word in model_response.split():
        yield word + " "
        time.sleep(0.05)

def template_generator(question, context):
    template = '''
    # Você é um assistente útil que ajuda os usuários a responder perguntas com base nas informações fornecidas.
    # Pergunta: {question}
    # Responda de forma clara.
    '''
    prompt_template = PromptTemplate.from_template(template=template)
    
    return prompt_template.format(question=question, context=context)

st.title("GenAI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if question := st.chat_input("Pergunte..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    print("messages")
    print(st.session_state.messages)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Montar o prompt com template
        prompt = template_generator(question, st.session_state.messages)

        print("prompt: " + prompt)

        # Consultar o LLM aqui
        model_response = openai.invoke(prompt)

        response = st.write_stream(response_generator(model_response.content))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
