import streamlit as st
import os
import time
from log import log_interaction

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def get_theme_styles(theme):
    if theme == "dark":
        return """
<style>
    /* App background with cybersecurity theme - dark matrix-like pattern */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d1117 100%);
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        color: #e0e0e0;
        font-family: 'Consolas', 'Monaco', monospace;
        position: relative;
        overflow: hidden;
    }

    /* Ensure content appears above animated background */
    .stApp > div {
        position: relative;
        z-index: 1;
    }

    /* Title bar with cyber security glow effect */
    h1 {
        background: linear-gradient(135deg, #00ff41 0%, #00d4aa 50%, #0088ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 0.8rem 1rem;
        text-align: center;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        font-weight: 800;
        border: 2px solid #00ff41;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3), inset 0 0 10px rgba(0, 255, 65, 0.1);
    }

    /* Logo container styling with neon glow */
    img {
        background-color: rgba(0, 20, 40, 0.8);
        padding: 0.6rem;
        border-radius: 50%;
        border: 2px solid #00ff41;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6), 0 0 40px rgba(0, 255, 65, 0.3);
    }

    /* Buttons with cyber theme */
    .stButton>button {
        background: linear-gradient(135deg, #00ff41 0%, #00d4aa 100%);
        color: #0a0e27;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        border: 2px solid #00ff41;
        transition: 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #00d4aa 0%, #0088ff 100%);
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.8);
    }

    /* Dropdowns and input text with cyber styling */
    label, .stSelectbox label, .stTextInput label {
        color: #00ff41 !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #00ff41;
        border-radius: 8px;
        background-color: rgba(10, 14, 39, 0.95);
        color: #e0e0e0;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }

    .stTextInput input {
        background-color: rgba(10, 14, 39, 0.95);
        color: #e0e0e0;
        border: 2px solid #00ff41;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }

    .stTextInput input:focus {
        border-color: #00d4aa;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.5);
    }

    /* Answer box styling with terminal-like appearance */
    .answer-box {
        background: rgba(10, 14, 39, 0.95);
        border-left: 5px solid #00ff41;
        border: 2px solid #00ff41;
        padding: 1.2rem;
        color: #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.4), inset 0 0 15px rgba(0, 255, 65, 0.1);
        font-size: 1rem;
        line-height: 1.7;
        font-family: 'Consolas', 'Monaco', monospace;
        margin-bottom: 1.5em;
    }

    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #00ff41 !important;
    }

    /* Footer text with cyber theme */
    footer, .footer {
        color: #00ff41;
        font-size: 0.95rem;
        margin-top: 2em;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }

    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
    }
</style>
"""
    else:  # light theme
        return """
<style>
    /* Light theme - clean professional look */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Title bar for light theme */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 0.8rem 1rem;
        text-align: center;
        letter-spacing: 2px;
        font-weight: 800;
        border: 2px solid #667eea;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
    }

    /* Logo container for light theme */
    img {
        background-color: #ffffff;
        padding: 0.6rem;
        border-radius: 50%;
        border: 2px solid #667eea;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Buttons with light theme */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        border: none;
        transition: 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }

    /* Dropdowns and input text with light styling */
    label, .stSelectbox label, .stTextInput label {
        color: #667eea !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #667eea;
        border-radius: 8px;
        background-color: #ffffff;
        color: #667eea;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        color: #667eea;
    }

    .stTextInput input {
        background-color: #ffffff;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
    }

    .stTextInput input:focus {
        border-color: #764ba2;
        box-shadow: 0 4px 8px rgba(118, 75, 162, 0.3);
    }
    
    .stTextInput input::placeholder {
        color: #a0a8d4;
    }

    /* Answer box styling for light theme */
    .answer-box {
        background: #ffffff;
        border-left: 5px solid #667eea;
        border: 2px solid #667eea;
        padding: 1.2rem;
        color: #2c3e50;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 1rem;
        line-height: 1.7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 1.5em;
    }

    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Footer text with light theme */
    footer, .footer {
        color: #667eea;
        font-size: 0.95rem;
        margin-top: 2em;
    }

    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
    }
</style>
"""


st.markdown(get_theme_styles(st.session_state.theme), unsafe_allow_html=True)


def get_data_folders(path="data"):
    try:
        return [
            name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
        ]
    except Exception:
        return []


st.set_page_config(
    page_title="NetQuery - AI-Powered Network Assistant",
    page_icon="🌐",
    layout="centered",
)

# Theme toggle button in top right
col_theme1, col_theme2 = st.columns([9, 1])
with col_theme2:
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Toggle Dark/Light Theme"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    shadow_color = (
        "rgba(0, 255, 65, 0.8)"
        if st.session_state.theme == "dark"
        else "rgba(102, 126, 234, 0.6)"
    )
    st.markdown(
        f"""
    <div style='text-align: center; margin-top: -50px;'>
        <div style='font-size: 4rem; text-shadow: 0 0 20px {shadow_color};'>🌐</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)

# Dynamic header based on theme
if st.session_state.theme == "dark":
    header_html = """
    <div style='border: 2px solid #00ff41; border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0, 255, 65, 0.3), inset 0 0 10px rgba(0, 255, 65, 0.1); margin-bottom: 1.5rem; text-align: center; background: rgba(10, 14, 39, 0.95);'>
        <div style='font-size: 2.8rem; font-weight: 800; letter-spacing: 3px; margin: 0; color: #00ff41; text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);'>NetQuery</div>
        <p style='color: #00d4aa; font-size: 1.1rem; margin: 0.5rem 0 0 0; letter-spacing: 1px;'>An AI-Powered Assistant for Computer Networks</p>
    </div>
    """
    topic_label_color = "#00ff41"
else:
    header_html = """
    <div style='border: 2px solid #667eea; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2); margin-bottom: 1.5rem; text-align: center; background: #ffffff;'>
        <div style='font-size: 2.8rem; font-weight: 800; letter-spacing: 3px; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>NetQuery</div>
        <p style='color: #764ba2; font-size: 1.1rem; margin: 0.5rem 0 0 0; letter-spacing: 1px;'>An AI-Powered Assistant for Computer Networks</p>
    </div>
    """
    topic_label_color = "#667eea"

st.markdown(header_html, unsafe_allow_html=True)

if st.session_state.theme == "dark":
    st.markdown(
        "<div style='font-size: 1.1rem; margin-bottom: 0.3em; padding: 0.8rem; background: rgba(10, 14, 39, 0.95); border: 2px solid #00ff41; border-radius: 8px; color: #00ff41; text-align: center; box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);'>🌐 Select Network Topic:</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='font-size: 1.1rem; margin-bottom: 0.3em; padding: 0.8rem; background: #ffffff; border: 2px solid #667eea; border-radius: 8px; color: #667eea; text-align: center; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);'>🌐 Select Network Topic:</div>",
        unsafe_allow_html=True,
    )
data_folders = get_data_folders("data")


def to_option(name):
    return name.replace("_", " ").replace("-", " ").title()


options = [to_option(name) for name in data_folders]

# Add inline CSS for selectbox
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background-color: rgba(10, 14, 39, 0.95) !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: rgba(10, 14, 39, 0.95) !important;
            color: #e0e0e0 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background-color: #ffffff !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #667eea !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

selected_bot = st.selectbox(
    "Select Topic",
    options,
    label_visibility="collapsed",
    key="bot_select",
    help="Choose a computer networking topic",
)


from db_utils import get_or_build_bot_db_path
from query_data import query_rag

if "answer" not in st.session_state:
    st.session_state["answer"] = ""
if "sources" not in st.session_state:
    st.session_state["sources"] = ""

if st.session_state.theme == "dark":
    st.markdown(
        "<div style='font-size: 1.1rem; margin-bottom: 0.3em; margin-top: 1em; padding: 0.8rem; background: rgba(10, 14, 39, 0.95); border: 2px solid #00ff41; border-radius: 8px; color: #00ff41; text-align: center; box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);'>💬 Type Your Networking Question:</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='font-size: 1.1rem; margin-bottom: 0.3em; margin-top: 1em; padding: 0.8rem; background: #ffffff; border: 2px solid #667eea; border-radius: 8px; color: #667eea; text-align: center; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);'>💬 Type Your Networking Question:</div>",
        unsafe_allow_html=True,
    )

# Add inline CSS for text input
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] input {
            background-color: rgba(10, 14, 39, 0.95) !important;
            color: #e0e0e0 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            color: #667eea !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

user_input = st.text_input(
    "Question Input",
    placeholder="e.g., Explain TCP/IP, What is OSI model, How does DNS work...",
    key="input",
    label_visibility="collapsed",
    on_change=None,
)
send_clicked = st.button("🚀 SEND QUERY", key="send_btn", use_container_width=False)

# Process query on button click OR when Enter is pressed (text input change with non-empty value)
if (send_clicked or user_input) and user_input.strip():
    # Reset sources visibility when new query is submitted
    st.session_state["show_sources"] = False

    folder_map = {to_option(name): name for name in data_folders}
    folder_name = folder_map.get(selected_bot)
    if folder_name:
        with st.spinner("Checking/Building knowledge base for selected topic..."):
            db_path = get_or_build_bot_db_path(folder_name)
        with st.spinner("Analyzing your query..."):
            start_time = time.time()
            answer = query_rag(user_input, db_path)
            end_time = time.time()
            time_taken = round(end_time - start_time, 3)
            log_interaction(user_input, answer, time_taken)

        # Extract sources from the answer
        if "\n\nReferences:\n" in answer:
            parts = answer.split("\n\nReferences:\n", 1)
            main_answer = parts[0].strip()
            sources = "Sources:\n" + parts[1].strip()
            st.session_state["answer"] = main_answer
            st.session_state["sources"] = sources
        elif "\n\nSources:\n" in answer:
            parts = answer.split("\n\nSources:\n", 1)
            main_answer = parts[0].strip()
            sources = "Sources:\n" + parts[1].strip()
            st.session_state["answer"] = main_answer
            st.session_state["sources"] = sources
        else:
            st.session_state["answer"] = answer
            st.session_state["sources"] = ""
    else:
        st.session_state["answer"] = "Could not find selected topic's folder."
        st.session_state["sources"] = ""

if st.session_state["answer"]:
    st.markdown(
        f"<div class='answer-box'>{st.session_state['answer']}</div>",
        unsafe_allow_html=True,
    )

    # View Sources button
    if st.session_state["sources"]:
        if st.button(
            "📚 View Sources",
            key="sources_btn",
            use_container_width=False,
            type="secondary",
        ):
            if "show_sources" not in st.session_state:
                st.session_state["show_sources"] = True
            else:
                st.session_state["show_sources"] = not st.session_state["show_sources"]

    # Display sources in an expander if button was clicked
    if st.session_state.get("show_sources", False):
        if st.session_state.theme == "dark":
            st.markdown(
                f"""<div style='background: rgba(10, 14, 39, 0.95); border: 2px solid #00d4aa; border-radius: 8px; padding: 1rem; margin-top: 1rem; color: #e0e0e0; box-shadow: 0 0 15px rgba(0, 212, 170, 0.3);'>
                    <div style='font-weight: 700; color: #00d4aa; margin-bottom: 0.5rem; font-size: 1.1rem;'>📚 Sources</div>
                    <div style='font-family: "Consolas", "Monaco", monospace; white-space: pre-wrap;'>{st.session_state['sources'].replace('Sources:', '').strip()}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""<div style='background: #ffffff; border: 2px solid #667eea; border-radius: 8px; padding: 1rem; margin-top: 1rem; color: #2c3e50; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);'>
                    <div style='font-weight: 700; color: #667eea; margin-bottom: 0.5rem; font-size: 1.1rem;'>📚 Sources</div>
                    <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; white-space: pre-wrap;'>{st.session_state['sources'].replace('Sources:', '').strip()}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

st.markdown("<br>", unsafe_allow_html=True)

# Dynamic footer based on theme
if st.session_state.theme == "dark":
    footer_html = """
<div style='text-align: center; font-size: 1rem; margin-top: 2em; color: #00ff41;'>
    🌐 <b>NetQuery v1.0</b> | Developed as Semester Capstone project</b><br>
    <span style='font-size:0.85rem; color: #00d4aa;'>Powered by Gemma3 4B & Vector Database Technology</span>
</div>
"""
else:
    footer_html = """
<div style='text-align: center; font-size: 1rem; margin-top: 2em; color: #667eea;'>
    🌐 <b>NetQuery v1.0</b> | Developed as Semester Capstone project</b><br>
    <span style='font-size:0.85rem; color: #764ba2;'>Powered by Gemma3 4B & Vector Database Technology</span>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
