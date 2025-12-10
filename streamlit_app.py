# streamlit_app.py

import os
import re
from datetime import datetime
from textwrap import dedent

import streamlit as st
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini
from db import demo_db

# -------------------------------------------------------------------
#  ENV + CONSTANTS
# -------------------------------------------------------------------
load_dotenv()

LOG_DIR = "research_notes"
os.makedirs(LOG_DIR, exist_ok=True)

# -------------------------------------------------------------------
#  HELPER FUNCTIONS FOR SAVING / LISTING NOTES
# -------------------------------------------------------------------
def slugify(text: str, max_words: int = 6) -> str:
    """Create a short, meaningful slug from the first few words of a question."""
    text = " ".join(text.strip().split())
    words = text.split(" ")[:max_words]
    short = " ".join(words)
    slug = re.sub(r"[^a-z0-9]+", "-", short.lower()).strip("-")
    return slug or "research-note"

def save_markdown_note(question: str, answer_md: str) -> str:
    """Save research result as a Markdown file and return the filepath."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = slugify(question)
    filename = f"{ts}-{slug}.md"
    path = os.path.join(LOG_DIR, filename)

    content = f"""# Research Note: {question}

- **Saved at:** {datetime.now().isoformat(timespec='seconds')}
- **File:** {filename}

---

{answer_md}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def list_markdown_notes():
    """Return list of (label, path) for saved notes, most recent first."""
    files = sorted(
        [os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith(".md")],
        reverse=True,
    )

    notes = []
    for fpath in files:
        fname = os.path.basename(fpath)
        # remove timestamp and extension for label
        if "-" in fname:
            _, rest = fname.split("-", 1)
        else:
            rest = fname
        label = rest.replace(".md", "").replace("-", " ").title()
        notes.append((label, fpath))
    return notes

# -------------------------------------------------------------------
#  AGENT CONFIG (same logic as CLI)
# -------------------------------------------------------------------
research_agent = Agent(
    name="Research Agent",
    model=Gemini(
        id="gemini-3-pro-preview",
        search=True,  # Enable web search
    ),
    description=(
        "You are a research agent with access to the web. "
        "You can search the web and provide well-researched responses."
    ),
    instructions=dedent(
        """
        1. Search the web and provide well-researched responses.

        2. With every response, you must: 
            - Include source citations with URLs when available.
            - Distinguish facts from opinions.
            - Note if information may be outdated.

        3. Start with a concise answer, then provide supporting details.

        4. Keep responses focused and scannable with clear headings.
        """
    ),
    db=demo_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# -------------------------------------------------------------------
#  STREAMLIT UI
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Web-Powered AI Research Agent",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Web-Powered AI Research Agent")

st.markdown(
    """
This app uses **Gemini 3 Pro + Agno** to build a real-time **Research Agent**.

- 🌐 Searches the web  
- 📚 Gives citation-backed answers  
- 🧐 Separates facts vs opinions  
- 🕰 Notes outdated or uncertain info  

This is a **100% FREE project** using a **free Gemini API key**, and we run it using **uv** instead of pip.
"""
)

# -------------------------------------------------------
#  SIDEBAR: Saved Research Notes
# -------------------------------------------------------
with st.sidebar:
    st.header("📁 Saved Research Notes")

    notes = list_markdown_notes()
    if notes:
        labels = [lbl for (lbl, _) in notes]
        selected_label = st.selectbox(
            "Open a previous research note:", labels, index=0
        )
        load_btn = st.button("📂 Load Selected Note")

        if load_btn:
            path_map = {lbl: p for lbl, p in notes}
            selected_path = path_map[selected_label]
            with open(selected_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.session_state["loaded_note_md"] = content
            st.session_state["show_loaded_note"] = True
    else:
        st.caption("No notes yet. Run research to create your first note.")

    st.markdown("---")
    st.subheader("Run with uv")
    st.code("uv run streamlit run streamlit_app.py", language="bash")

# -------------------------------------------------------
#  MAIN INPUT AREA
# -------------------------------------------------------
st.markdown("### ❓ Ask your research question")

question = st.text_area(
    "Enter your query:",
    value="What are the latest breakthroughs in quantum computing this year?",
    height=120,
)

col1, col2 = st.columns([1, 4])
with col1:
    run_button = st.button("🔍 Run Research", type="primary")
with col2:
    clear_button = st.button("🧹 Clear")

if clear_button:
    st.session_state.pop("loaded_note_md", None)
    st.session_state.pop("show_loaded_note", None)
    st.rerun()

response_container = st.container()

# -------------------------------------------------------
#  RUN AGENT & SAVE RESULT AS MD
# -------------------------------------------------------
if run_button:
    st.session_state["show_loaded_note"] = False  # we are showing fresh result now
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Researching the web…"):
            try:
                result = research_agent.run(question)
            except Exception as e:
                st.error(f"❌ Error while running agent: {e}")
                result = None

        if result:
            # Extract markdown content
            if hasattr(result, "content") and result.content:
                answer_md = result.content
            else:
                answer_md = str(result)

            # Show on screen
            with response_container:
                st.markdown("### ✅ Answer")
                st.markdown(answer_md)

            # Save as markdown file
            filepath = save_markdown_note(question, answer_md)
            st.success(f"Saved this research as: `{os.path.basename(filepath)}`")

# -------------------------------------------------------
#  SHOW LOADED NOTE (IF ANY)
# -------------------------------------------------------
if st.session_state.get("show_loaded_note") and st.session_state.get("loaded_note_md"):
    st.markdown("### 📂 Loaded Research Note")
    st.markdown(st.session_state["loaded_note_md"])

# -------------------------------------------------------
#  SAMPLE TERMINAL OUTPUT (NO WRAP)
# -------------------------------------------------------
with st.expander("📄 Sample Terminal Output (from notes.txt)"):
    st.caption("This shows how the CLI version behaved before converting to Streamlit.")
    try:
        with open("notes.txt", "r", encoding="utf-8") as fh:
            raw_text = fh.read()

        # st.code uses <pre> with horizontal scroll and no wrapping
        st.code(raw_text, language="text")
    except FileNotFoundError:
        st.info("notes.txt not found. Add it to your project folder to display here.")
