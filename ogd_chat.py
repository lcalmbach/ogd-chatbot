import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools, create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

from langchain.callbacks import StreamlitCallbackHandler

# from langchain.agents import AgentExecutor


# from langchain.chat_models import ChatOpenAI

# from langchain.agents import load_tools
# from langchain.agents import initialize_agent

context = """\nBei Fragen nach der Vornamen verwende die Tabelle vornamen. Für Fragen nach der Anzahl von Vornamen summiere die Spalte 'Anzahl'.
\nBeispiel: 'Wie viele Lukas gab es 2018? > select sum(Anzahl') from vornamen where vorname = 'Lukas' and jahr = 2018.
\nBei Fragen nach Fischen verwende die Tabelle fische.
\Antworte auf deutsch.
\Antworte mit einem kurzen Text und wiederhole die Frage im Antworttext.
"""

class OgdChat:
    def __init__(self, intent_id: int, user_question: str, train_of_thought: bool):
        self.prompt = user_question
        self.intent_id = intent_id
        self.db = SQLDatabase.from_uri("sqlite:///ogd.db")
        self.show_train_of_thought = train_of_thought

    def run(self):
        toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        agent_executor = create_sql_agent(
            llm=OpenAI(
                temperature=0, openai_api_key=st.session_state["OPENAI_API_KEY"], verbose=True
            ),
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        prompt = f'{self.prompt}{context}'
        if self.show_train_of_thought:
            st_callback = StreamlitCallbackHandler(st.container(), max_thought_containers=10, expand_new_thoughts=False)
            response = agent_executor.run(prompt, callbacks=[st_callback])
        else:
            response = agent_executor.run(prompt)
        return response
