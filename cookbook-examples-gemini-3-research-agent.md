# Building a Web-Powered AI Research Agent

This walkthrough will guide you through the process of building a powerful, web-enabled AI research agent using Python. This project is a fantastic addition to a portfolio for any developer interested in AI, as it demonstrates a practical application of large language models (LLMs) and agent-based systems.

## Project Overview

The goal of this project is to create an AI agent that can answer complex questions by actively searching the web for the most current information. Unlike a standard chatbot, this "Research Agent" is designed to provide well-researched, factual responses, complete with source citations. It's a perfect example of how to augment an LLM's knowledge with real-time data from the internet.

## Why This Project Belongs in Your Portfolio

*   **Demonstrates Modern AI Skills:** You'll be working with Google's Gemini Pro model, showcasing your ability to integrate cutting-edge AI into applications.
*   **Highlights Agentic AI Concepts:** This project moves beyond simple Q&A bots. You're building an "agent" that has a specific role, instructions, and tools (in this case, web search).
*   **Practical Application:** A research agent is a genuinely useful tool, demonstrating that you can build AI solutions that solve real-world problems.
*   **Shows Best Practices:** The use of a structured agent framework (`agno`), environment variables for API keys (`dotenv`), and clear, instructive prompting are all hallmarks of a well-engineered AI application.

## Technical Deep Dive: Code Walkthrough

Let's break down the `cookbook-examples-gemini-3-research-agent.py` script step by step.

```python
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from db import demo_db

from dotenv import load_dotenv
load_dotenv()

research_agent = Agent(
    name="Research Agent",
    model=Gemini(
        id="gemini-3-pro-preview",
        search=True,
    ),
    description="You are a research agent with access to the web. You can search the web and provide well-researched responses.",
    instructions=dedent("""
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


if __name__ == "__main__":
    research_agent.print_response(
        "What are the latest breakthroughs in quantum computing this year?",
        stream=True,
    )
```

### 1. Imports and Setup

*   `from agno.agent import Agent`: This imports the core `Agent` class from the `agno` library, which provides a framework for creating AI agents.
*   `from agno.models.google import Gemini`: This imports the `Gemini` model wrapper from `agno`, allowing for easy integration with Google's Gemini models.
*   `from dotenv import load_dotenv`: This is a standard practice for managing sensitive information like API keys. It loads variables from a `.env` file into the environment.

### 2. The `Agent` Configuration

The `Agent` class is the heart of our application. We instantiate it with several key parameters:

*   `name`: A simple, descriptive name for our agent.
*   `model`: Here, we specify the `Gemini` model.
    *   `id="gemini-3-pro-preview"`: This selects the specific version of the Gemini model we want to use.
    *   `search=True`: This is the magic ingredient! By setting this to `True`, we are enabling the model's built-in web search capability.
*   `description`: A high-level description of the agent's purpose.
*   `instructions`: This is the detailed prompt that governs the agent's behavior. It's a multi-step set of rules that forces the agent to:
    *   Cite its sources.
    *   Distinguish between facts and opinions.
    *   Flag potentially outdated information.
    *   Structure its responses for clarity (concise answer first, then details).
*   `db=demo_db`: The agent is configured to use a database to persist conversation history. This allows it to remember past interactions.
*   `add_datetime_to_context`: This injects the current date and time into the model's context, which is useful for time-sensitive questions.
*   `add_history_to_context` & `num_history_runs`: These parameters control the conversation history feature, allowing the agent to have contextually aware follow-up conversations.
*   `markdown=True`: This tells the agent to format its output using Markdown for better readability.

### 3. Running the Agent

The `if __name__ == "__main__":` block is the entry point of the script.
*   `research_agent.print_response(...)`: This is the method that sends a prompt to the agent and prints its response.
*   `stream=True`: This streams the response as it's being generated, providing a more interactive and real-time experience for the user.

## How to Run the Project

1.  **Install Dependencies:**
    Make sure you have Python installed. Then, create a virtual environment and install the required packages:

    ```bash
    pip install "agno>=2.3.8" "google-genai>=1.54.0" "python-dotenv"
    ```

2.  **Set Up Your API Key:**
    *   Create a file named `.env` in the same directory as the script.
    *   Add your Google API key to this file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

3.  **Run the script:**
    ```bash
    python cookbook-examples-gemini-3-research-agent.py
    ```
    You should see the agent start to stream a well-researched answer to the question about quantum computing.

## Customization and Extension Ideas

This agent is a great starting point. Here are some ideas to make it your own:

*   **Build a Web Interface:** Wrap the agent in a simple web framework like Flask or FastAPI to create a web-based research tool.
*   **Add More Tools:** The `agno` framework allows for adding custom tools. You could give the agent the ability to run code, access databases, or interact with other APIs.
*   **Specialize the Agent:** Change the `instructions` to create agents for different roles, such as a "Financial Analyst Agent" or a "Creative Writing Assistant."
*   **Persistent Memory:** The `demo_db` is likely an in-memory database. Swap it out for a persistent database like SQLite or PostgreSQL to give your agent a long-term memory.
*   **Interactive Chat:** Modify the `if __name__ == "__main__":` block to create a loop that allows you to have an interactive chat session with the agent.
