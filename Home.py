import streamlit as st

# Page config
st.set_page_config(
    page_title="NetQuerry - AI Network Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def get_theme_styles(theme):
    if theme == "dark":
        return """
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d1117 100%);
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        color: #e0e0e0;
        font-family: 'Consolas', 'Monaco', monospace;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00ff41 0%, #00d4aa 50%, #0088ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
    }
    
    .subtitle {
        font-size: 1.4rem;
        text-align: center;
        color: #00d4aa;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    .feature-card {
        background: rgba(10, 14, 39, 0.95);
        border: 2px solid #00ff41;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
    }
    
    .feature-title {
        color: #00ff41;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #e0e0e0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(0, 255, 65, 0.2);
        border: 1px solid #00ff41;
        color: #00ff41;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .video-container {
        border: 3px solid #00ff41;
        border-radius: 12px;
        padding: 1rem;
        background: rgba(10, 14, 39, 0.95);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
        margin: 2rem 0;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #00ff41 0%, #00d4aa 100%);
        color: #0a0e27;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border: 2px solid #00ff41;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        transition: 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.8);
    }
    
    .section-title {
        color: #00ff41;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }
    
    /* Style the Streamlit video iframe */
    iframe[title*="video"] {
        border: 3px solid #00ff41 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4) !important;
    }
</style>
"""
    else:  # light theme
        return """
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }
    
    .subtitle {
        font-size: 1.4rem;
        text-align: center;
        color: #764ba2;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    .feature-card {
        background: #ffffff;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .feature-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #2c3e50;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid #667eea;
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .video-container {
        border: 3px solid #667eea;
        border-radius: 12px;
        padding: 1rem;
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        margin: 2rem 0;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        transition: 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    .section-title {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    /* Style the Streamlit video iframe */
    iframe[title*="video"] {
        border: 3px solid #667eea !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
</style>
"""


st.markdown(get_theme_styles(st.session_state.theme), unsafe_allow_html=True)

# Theme toggle in sidebar
with st.sidebar:
    st.markdown("### Settings")
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    if st.button(f"{theme_icon} Toggle Theme", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# Hero Section
st.markdown('<h1 class="hero-title">NetQuerry</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">AI-Powered Assistant for Computer Networks</p>',
    unsafe_allow_html=True,
)

# Logo
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    shadow_color = (
        "rgba(0, 255, 65, 0.8)"
        if st.session_state.theme == "dark"
        else "rgba(102, 126, 234, 0.6)"
    )
    st.markdown(
        f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 5rem; text-shadow: 0 0 30px {shadow_color};'>🌐</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Introduction
st.markdown(
    """
<div style='text-align: center; font-size: 1.1rem; line-height: 1.8; margin: 2rem auto; max-width: 800px;'>
NetQuerry is a local, privacy-first RAG (Retrieval-Augmented Generation) chatbot designed specifically for 
answering questions about computer networking concepts. Powered by Gemma3 4B and vector database technology, 
it provides accurate, context-based answers from your networking documentation without sending any data to external servers.
</div>
""",
    unsafe_allow_html=True,
)

# Video Section
st.markdown('<h2 class="section-title">Project Demo</h2>', unsafe_allow_html=True)

# YouTube video embed
st.video("https://www.youtube.com/watch?v=AVUL9Q5Vigg")

# Key Features Section
st.markdown('<h2 class="section-title">Key Features</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">🔒 100% Local & Private</div>
        <div class="feature-text">
            All processing happens on your machine. No data leaves your computer, ensuring complete privacy for your documents and queries.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">🎯 Context-Aware Responses</div>
        <div class="feature-text">
            Only answers based on provided documentation. No hallucinations or made-up information - strict context-based responses.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">🌐 Multi-Topic Support</div>
        <div class="feature-text">
            Dynamic topic selection with automatic database management. Supports multiple networking domains like Cisco, general networks, and more.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">📚 Intelligent Citations</div>
        <div class="feature-text">
            Automatic page and chunk referencing from source PDFs. Know exactly where each piece of information comes from.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">🎨 Dual-Theme UI</div>
        <div class="feature-text">
            Professional dark/light themes with cybersecurity aesthetics. Switch between themes for comfortable viewing in any environment.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">📊 Interaction Logging</div>
        <div class="feature-text">
            Complete chat history with performance metrics. Track queries, responses, and response times for analysis.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Tech Stack Section
st.markdown('<h2 class="section-title">Technology Stack</h2>', unsafe_allow_html=True)

st.markdown(
    """
<div style='text-align: center; margin: 2rem 0;'>
    <span class="tech-badge">Gemma3 4B</span>
    <span class="tech-badge">Ollama</span>
    <span class="tech-badge">LangChain</span>
    <span class="tech-badge">ChromaDB</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Python</span>
    <span class="tech-badge">PyPDF</span>
    <span class="tech-badge">nomic-embed-text</span>
</div>
""",
    unsafe_allow_html=True,
)

# How It Works Section
st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">1️⃣ Document Processing</div>
        <div class="feature-text">
            Your PDF documents are split into chunks and converted to vector embeddings using nomic-embed-text model via Ollama.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">2️⃣ Intelligent Retrieval</div>
        <div class="feature-text">
            When you ask a question, the system finds the most relevant chunks from your documents using vector similarity search.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-title">3️⃣ AI Response</div>
        <div class="feature-text">
            Gemma3 4B generates accurate answers based only on the retrieved context, with automatic source citations.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Getting Started Section
st.markdown('<h2 class="section-title">Getting Started</h2>', unsafe_allow_html=True)

st.markdown(
    """
<div style='max-width: 800px; margin: 0 auto;'>
    <div class="feature-card">
        <div class="feature-title">Quick Setup</div>
        <div class="feature-text" style='line-height: 2;'>
            <strong>1. Install Prerequisites:</strong><br/>
            • Python 3.10+ <br/>
            • Ollama (<code>ollama pull gemma3:4b</code> and <code>ollama pull nomic-embed-text</code>)<br/><br/>
            <strong>2. Install Dependencies:</strong><br/>
            <code>pip install -r requirements.txt</code><br/><br/>
            <strong>3. Add Your PDFs:</strong><br/>
            Place networking PDFs in topic folders under <code>data/</code><br/><br/>
            <strong>4. Run the Application:</strong><br/>
            <code>streamlit run Home.py</code>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Footer
st.markdown("<br/><br/>", unsafe_allow_html=True)
footer_color = "#00ff41" if st.session_state.theme == "dark" else "#667eea"
st.markdown(
    f"""
<div style='text-align: center; font-size: 1rem; margin-top: 3rem; color: {footer_color};'>
    <b>NetQuerry v1.0</b> | Semester 7 Capstone Project<br/>
    <span style='font-size:0.9rem;'>Theory of Automata (TOAT) - NUST</span><br/>
    <span style='font-size:0.85rem;'>Powered by Gemma3 4B & Vector Database Technology</span>
</div>
""",
    unsafe_allow_html=True,
)
