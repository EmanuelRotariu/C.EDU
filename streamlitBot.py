from openai import OpenAI
import streamlit as st
#streamlit run streamlitBot.py
st.title("C.EDU")
#st.markdown("<h1 style='text-align: center; color: red;'>C.EDU</h1>", unsafe_allow_html=True) centreaza titlul
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Interacționează cu C.EDU"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
           #max_tokens=150  aceasta variabila o pot folosi pentru a determina marimea raspunsului dat de bot
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})