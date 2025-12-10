# Building an AI Product Comparison Agent

This guide provides a walkthrough for creating a sophisticated AI agent that can compare products by analyzing web pages and searching for reviews. This project is an excellent portfolio piece for developers looking to showcase their skills in building practical, tool-using AI applications.

## Project Overview

The project's goal is to build an AI agent that takes product names (or URLs) and generates a detailed, structured comparison. This "Product Comparison Agent" uses the web to gather information, ensuring its comparisons are based on current data, and then presents the findings in a clear, easy-to-digest format.

## Why This Project Belongs in Your Portfolio

*   **Advanced Tool Use:** This agent doesn't just search the web; it can also be given specific URLs to analyze. This demonstrates your ability to build AI that integrates multiple tools (`search` and `url_context`).
*   **Structured Output:** You're programming the agent to follow a strict output format (verdict, table, pros/cons). This is a key skill in making AI outputs reliable and useful for downstream applications.
*   **Real-World Utility:** A product comparison tool is immediately recognizable and useful, making it a compelling demonstration of your ability to apply AI to solve common problems.
*   **Focus on Prompt Engineering:** The detailed `instructions` highlight your skills in prompt engineering, which is crucial for controlling and directing the behavior of LLMs.

## Technical Deep Dive: Code Walkthrough

Let's dissect the `cookbook-examples-gemini-3-product-comparison-agent.py` script.

```python
from dotenv import load_dotenv
load_dotenv()
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from db import demo_db

product_comparison_agent = Agent(
    name="Product Comparison Agent",
    model=Gemini(
        id="gemini-3-pro-preview",
        url_context=True,
        search=True,
    ),
    description="You are a product comparison agent that analyzes URLs and searches for reviews to provide comprehensive comparisons.",
    instructions=dedent("""
1. Analyze URLs and search for reviews to provide comprehensive comparisons.

2. Your output format must be:
    - **Quick Verdict** - One sentence recommendation
    - **Comparison Table** - Key specs side by side
    - **Pros & Cons** - For each option
    - **Best For** - Who should choose which option

3. Be decisive and provide a coherent chain of thought for your recommendations.

4. Keep your responses concise and to the point.
        """),
    db=demo_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)


if __name__ == "__main__":
    product_comparison_agent.print_response(
        "Compare the Iphone 15 and Samsung Galaxy S25",
        stream=True,
    )
```

### 1. Imports and Setup

The script begins by importing necessary libraries: `Agent` and `Gemini` from the `agno` framework, and `load_dotenv` for managing API keys from a `.env` file.

### 2. The `Agent` Configuration

The `Agent` is configured with a specific persona and toolset:

*   `name`: "Product Comparison Agent".
*   `model`: We are again using the `Gemini` model, but with a different configuration.
    *   `id="gemini-3-pro-preview"`: Selects the powerful Gemini Pro model.
    *   `url_context=True`: This is a key feature. It gives the agent the ability to read and analyze the content of URLs provided in the prompt.
    *   `search=True`: This enables the agent's general web search capability, allowing it to find reviews, articles, and product pages on its own.
*   `description`: A concise summary of the agent's function.
*   `instructions`: This is a masterclass in prompt engineering for structured output. The instructions are very explicit, telling the agent *exactly* how to format its response. This includes:
    *   A **Quick Verdict**.
    *   A **Comparison Table**.
    *   A **Pros & Cons** list.
    *   A recommendation for who each product is **Best For**.
    This level of instruction is vital for creating reliable and predictable AI agents.
*   `db`, `add_datetime_to_context`, `add_history_to_context`: These parameters provide the agent with memory and temporal awareness, just like in the research agent.
*   `markdown=True`: Ensures the output is formatted with Markdown, which is perfect for rendering tables and lists.

### 3. Running the Agent

The `if __name__ == "__main__":` block demonstrates how to use the agent.
*   `product_comparison_agent.print_response(...)`: The prompt "Compare the Iphone 15 and Samsung Galaxy S25" is sent to the agent. Because `search=True`, the agent will go online to find information about these two phones to formulate its comparison.
*   `stream=True`: The response is streamed to the console for a real-time feel.

## How to Run the Project

1.  **Install Dependencies:**
    If you haven't already, set up a Python virtual environment and install the necessary packages.

    ```bash
    pip install "agno>=2.3.8" "google-genai>=1.54.0" "python-dotenv"
    ```

2.  **Set Up Your API Key:**
    *   Ensure you have a `.env` file in your project directory.
    *   Add your Google API key to this file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

3.  **Run the script:**
    ```bash
    python cookbook-examples-gemini-3-product-comparison-agent.py
    ```
    The agent will now perform a web search and stream back a detailed comparison of the two smartphones.

## Customization and Extension Ideas

*   **URL-based Comparison:** Modify the main script to pass URLs to the `print_response` method. For example: `agent.print_response("Compare the products at these URLs: [URL1] and [URL2]")`.
*   **Interactive CLI:** Create a command-line interface (CLI) that prompts the user for products to compare, allowing for an interactive session.
*   **Price Tracking:** Add a tool that allows the agent to check for the latest prices from specific e-commerce sites.
*   **Sentiment Analysis:** Extend the agent to perform sentiment analysis on the reviews it finds to provide a summary of public opinion.
*   **Web Frontend:** Build a simple Flask or FastAPI web application that allows users to enter products or URLs and see the formatted comparison in their browser.

```