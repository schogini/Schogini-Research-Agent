import streamlit as st
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from db import demo_db
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Research Agent", page_icon="🔍", layout="wide")

st.title("🔍 Research Agent")
st.markdown("Ask me anything! I can search the web and provide well-researched responses.")

@st.cache_resource
def get_research_agent():
    return Agent(
        name="Research Agent",
        model=Gemini(
            id="gemini-3-pro-preview",
            search=True,
        ),
        description="You are a research agent with access to the web. You can search the web and provide well-researched responses.",
        instructions=dedent("""\
        1. Search the web and provide well-researched responses.

        2. With every response, you must: 
            - Include source citations with URLs when available.
            - Distinguish facts from opinions.  
            - Note if information may be outdated.

        3. Start with a concise answer, then provide supporting details.

        4. Keep responses focused and scannable with clear headings.
        """),
        db=demo_db,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=3,
        markdown=True,
    )

research_agent = get_research_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to research?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Create a generator for the response
        response_generator = research_agent.run(prompt, stream=True)
        
        for chunk in response_generator:
            if chunk.content:
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
