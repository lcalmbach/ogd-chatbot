import socket
import os
import openai
import streamlit as st
from const import FIRST_PROMPT, INTENT_PROMPT
from ogd_chat import OgdChat

LOCAL_HOST = "liestal"
__version__ = "0.0.1"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-7-01"
my_name = "OGD-ChatBot"
GIT_REPO = "https://github.com/lcalmbach/ogd-chatbot"
APP_INFO = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>App created by <a href="mailto:{__author_email__}">{__author__}</a><br>
    version: {__version__} ({VERSION_DATE})<br>
    app powered by <a href="https://streamlit.io/">Streamlit</a>, 
    <a href="https://platform.openai.com/">OpenAI API</a> 
    and <a href="https://github.com/hwchase17/langchain">🦜LangChain</a><br>
    <a href="{GIT_REPO}">git-repo</a>
    """


def get_var(varname: str) -> str:
    """
    Retrieves the value of a given environment variable or secret from the
    Streamlit configuration.

    If the current host is the local machine (according to the hostname), the
    environment variable is looked up in the system's environment variables.
    Otherwise, the secret value is fetched from Streamlit's secrets dictionary.

    Args:
        varname (str): The name of the environment variable or secret to
        retrieve.

    Returns:
        The value of the environment variable or secret, as a string.

    Raises:
        KeyError: If the environment variable or secret is not defined.
    """
    if socket.gethostname().lower() == LOCAL_HOST:
        return os.environ[varname]
    else:
        return st.secrets[varname]


def get_intent(prompt: str):
    prompt = [{"role": "assistant", "content": INTENT_PROMPT.format(prompt)}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
    return int(response.choices[0].message.content)


def main():
    st.title("💬 OpenData-ChatBot")
    if "messages" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] = get_var("OPENAI_API_KEY")
        st.session_state["messages"] = [{"role": "assistant", "content": FIRST_PROMPT}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        openai.api_key = st.session_state["OPENAI_API_KEY"]
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        intent = get_intent(prompt)
        if intent == -99:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state.messages
            )
            msg = response.choices[0].message
            st.session_state.messages.append(msg)
            st.chat_message("assistant").write(msg.content)
        else:
            chat = OgdChat(intent, prompt)
            msg = chat.run()
            st.session_state.messages.append({"role": "assistant", "content": prompt})
            st.chat_message("assistant").write(msg)
    st.sidebar.markdown(APP_INFO, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
