import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

# from langchain.agents import load_tools
# from langchain.agents import initialize_agent
from const import INTENT_DICT


class OgdChat:
    def __init__(self, intent_id: int, prompt: str):
        self.prompt = prompt
        self.db = SQLDatabase.from_uri("sqlite:///ogd.db")
        self.intent = INTENT_DICT[intent_id]

    def run(self):
        toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        agent_executor = create_sql_agent(
            llm=OpenAI(
                temperature=0, openai_api_key=st.session_state["openai_api_key"]
            ),
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        # self.prompt = self.intent.format(self.prompt)
        response = agent_executor.run(self.prompt)
        return response
