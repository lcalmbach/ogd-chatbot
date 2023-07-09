import streamlit as st
import iso639
import json
from io import BytesIO
import os
import socket


def init_lang_options():
    """
    Filter a dictionary of all available languages and their corresponding codes
    based on a given list of used language codes.

    Parameters:
    used_langs_list (list): A list of used language codes.

    Returns:
    lang_dict (dict): A dictionary containing only the key-value pairs that correspond
                     to the languages in the used_langs_list.
    """
    all_langs = get_all_language_dict()
    result = {}
    for lang in st.session_state["lang_list"]:
        if lang in all_langs:
            result[lang] = all_langs[lang]
    return result


def get_lang_file(module_name: str):
    """Generates a list of languages keys from the first language file read

    Args:
        module_name (str): _description_

    Returns:
        _type_: _description_
    """
    lang_file = f"./lang/{os.path.splitext(os.path.basename(module_name))[0]}.json"
    return lang_file


def set_lang_list(module_name):
    """Generates a list of languages keys from the first language file read
    and sets the st.session_state["lang_list"] so it can be used everywhere
    in the app
    """
    lang_file = get_lang_file(module_name)
    with open(lang_file, "r") as file:
        lang_all_dict = json.load(file)
    st.session_state["lang_list"] = list(lang_all_dict.keys())


def refresh_lang(module_name, lang):
    lang_file = get_lang_file(module_name)
    with open(lang_file, "r") as file:
        lang_all_dict = json.load(file)
    st.session_state["lang"] = lang
    st.session_state["lang_dict"] = lang_all_dict[lang]
    if "messages" in st.session_state:
        del st.session_state["messages"]


def get_all_language_dict():
    keys = [lang["iso639_1"] for lang in iso639.data if lang["iso639_1"] != ""]
    values = [lang["name"] for lang in iso639.data if lang["iso639_1"] != ""]
    language_dict = dict(zip(keys, values))
    return language_dict


def get_used_languages():
    language_dict = get_all_language_dict()
    used_languages = list(lang_dict_complete.keys())
    extracted_dict = {
        key: language_dict[key] for key in used_languages if key in language_dict
    }
    return extracted_dict


def download_button(data, download_filename, button_text):
    """
    Function to create a download button for a given object.

    Parameters:
    - object_to_download: The object to be downloaded.
    - download_filename: The name of the file to be downloaded.
    - button_text: The text to be displayed on the download button.
    """
    # Create a BytesIO buffer
    json_bytes = json.dumps(data).encode("utf-8")
    buffer = BytesIO(json_bytes)

    # Set the appropriate headers for the browser to recognize the download
    st.set_option("deprecation.showfileUploaderEncoding", False)
    st.download_button(
        label=button_text,
        data=buffer,
        file_name=download_filename,
        mime="application/json",
    )


def get_var(varname: str):
    if socket.gethostname().lower() == LOCAL_HOST:
        return os.environ[varname]
    else:
        return st.secrets[varname]


LOCAL_HOST = "liestal"
# list of all iso639 languages
# lang_dict_complete = get_lang_dict_complete()
