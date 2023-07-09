import socket
import os
import openai
import streamlit as st

from const import INTENT_PROMPT, THEME_PROMPT, LANG_LIST
from ogd_chat import OgdChat
from helper import refresh_lang, init_lang_options, set_lang_list

LOCAL_HOST = "liestal"
__version__ = "0.0.4"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-7-09"
APP_NAME = "OGD-ChatBot"
GIT_REPO = "https://github.com/lcalmbach/ogd-chatbot"
DEFAULT_LANG = "en"

if "lang" not in st.session_state:
    st.set_page_config(page_title=APP_NAME, page_icon="🤖")
    refresh_lang(__file__, DEFAULT_LANG)
    # find lang list which is needed for the init_lang_options routine
    set_lang_list(__file__)
    # set the option dict to fill the lang selection list
    st.session_state["lang_options"] = init_lang_options()
    # st.experimental_rerun()


def get_app_info():
    created_by = st.session_state["lang_dict"]["app_created_by"]
    powered_by = st.session_state["lang_dict"]["powered_by"]
    version = st.session_state["lang_dict"]["version"]

    info = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>{created_by} <a href="mailto:{__author_email__}">{__author__}</a><br>
    {version}: {__version__} ({VERSION_DATE})<br>
    {powered_by} <a href="https://streamlit.io/">Streamlit</a>, 
    <a href="https://platform.openai.com/">OpenAI API</a> 
    and<br><a href="https://github.com/hwchase17/langchain">🦜LangChain</a><br>
    <a href="{GIT_REPO}">git-repo</a>
    """
    return info


def display_language_selection():
    index = list(st.session_state["lang_options"].keys()).index(
        st.session_state["lang"]
    )
    x = st.sidebar.selectbox(
        label=f'🌐{st.session_state["lang_dict"]["language"]}',
        options=st.session_state["lang_options"].keys(),
        format_func=lambda x: st.session_state["lang_options"][x],
        index=index,
    )
    if x != st.session_state["lang"]:
        refresh_lang(__file__, x)
        st.experimental_rerun()


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


def get_first_prompt():
    intent_expression = ", ".join(st.session_state["lang_dict"]["intents"])
    first_prompt = st.session_state["lang_dict"]["first_prompt"].format(
        intent_expression
    )
    return first_prompt


def get_intent(prompt: str):
    prompt = [{"role": "assistant", "content": INTENT_PROMPT.format(prompt)}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
    return int(response.choices[0].message.content)


def main():
    st.title("💬 OpenData-ChatBot")
    display_language_selection()

    if "messages" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] = get_var("OPENAI_API_KEY")
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": get_first_prompt(),
            }
        ]

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
            st.chat_message("assistant").write(msg["content"])
        elif intent == 3:
            msg = {"role": "assistant", "content": THEME_PROMPT}
            st.session_state["messages"] = [msg]
            st.session_state.messages.append(msg)
            st.chat_message("assistant").write(msg["content"])
        else:
            chat = OgdChat(intent, prompt)
            msg = chat.run()
            msg = {"role": "assistant", "content": msg}
            st.session_state.messages.append(msg)
            st.chat_message("assistant").write(msg["content"])
    st.sidebar.markdown(get_app_info(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
