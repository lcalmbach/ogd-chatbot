import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.agents import AgentType, create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler


class OgdChat:
    def __init__(self, intent_id: int, user_question: str, train_of_thought: bool):
        self.prompt = user_question
        self.intent_id = intent_id
        self.db = SQLDatabase.from_uri("sqlite:///ogd.db")
        self.show_train_of_thought = train_of_thought

    def run(self):
        toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        #db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, use_query_checker=True, return_intermediate_steps=True)
        agent_executor = create_sql_agent(
            llm=OpenAI(
                temperature=0, openai_api_key=st.session_state["OPENAI_API_KEY"], verbose=True
            ),
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        if self.show_train_of_thought:
            st_callback = StreamlitCallbackHandler(st.container(), max_thought_containers=10, expand_new_thoughts=False)
            response = agent_executor.run(self.prompt, callbacks=[st_callback])
        else:
            response = agent_executor.run(self.prompt)
        return response
