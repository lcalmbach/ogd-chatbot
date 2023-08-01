import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI

# from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType

# from langchain.chat_models import ChatOpenAI

# from langchain.agents import load_tools
# from langchain.agents import initialize_agent


class OgdChat:
    def __init__(self, intent_id: int, user_question: str):
        self.prompt = user_question
        self.intent_id = intent_id
        self.db = SQLDatabase.from_uri("sqlite:///ogd.db")

    def run(self):
        toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        #db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, use_query_checker=True, return_intermediate_steps=True)
        agent_executor = create_sql_agent(
            llm=OpenAI(
                temperature=0, openai_api_key=st.session_state["OPENAI_API_KEY"]
            ),
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        response = agent_executor.run(self.prompt)
        return response
