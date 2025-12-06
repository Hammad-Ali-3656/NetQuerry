# NetQuerry - Comprehensive Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File-by-File Documentation](#file-by-file-documentation)
4. [Data Flow](#data-flow)
5. [Technical Stack](#technical-stack)
6. [Setup and Installation](#setup-and-installation)
7. [Usage Guide](#usage-guide)
8. [Troubleshooting](#troubleshooting)

---

## Project Overview

**NetQuerry** is an AI-powered Retrieval-Augmented Generation (RAG) chatbot specifically designed for answering questions about computer networking concepts. It provides a local, privacy-first solution that ensures no data leaves your machine while delivering accurate, context-based responses from provided PDF documents.

### Key Features
- **100% Local & Private**: All processing happens on your machine using Ollama
- **Context-Aware Responses**: Only answers from provided documentation
- **Multi-Topic Support**: Dynamic topic selection with automatic database management
- **Dual-Theme UI**: Professional dark/light themes with cybersecurity aesthetics
- **Intelligent Citations**: Automatic page and chunk referencing
- **Interaction Logging**: Complete chat history with performance metrics
- **No Hallucination**: Strict prompting prevents made-up information

### Technologies Used
- **LLM**: Gemma3 4B (via Ollama)
- **Embeddings**: nomic-embed-text (via Ollama)
- **Vector Database**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
- **PDF Processing**: PyPDF

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface (app.py)                │
│                    Streamlit Web Application                 │
│              Dark/Light Theme | Topic Selection              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─► Query Input
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Query Processing (query_data.py)               │
│   • Embedding Generation • Vector Search • LLM Inference    │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼──────┐    ┌──────▼───────────────────────────────┐
│  Vector DB   │    │  Database Management (db_utils.py)   │
│  (ChromaDB)  │◄───┤  • Dynamic DB Creation per Topic     │
│              │    │  • Document Processing                │
└──────────────┘    └──────────────────────────────────────┘
        ▲
        │
┌───────┴──────────────────────────────────────────────────┐
│       Document Processing (populate_database.py)         │
│  • PDF Loading • Text Splitting • Chunk ID Assignment   │
└──────────────────────────────────────────────────────────┘
        ▲
        │
┌───────┴──────────────────────────────────────────────────┐
│              Embedding Function (get_embedding_function.py)│
│              Ollama Nomic-Embed-Text Model                │
└──────────────────────────────────────────────────────────┘
        ▲
        │
┌───────┴──────────────────────────────────────────────────┐
│              Data Sources (data/)                         │
│  Cisco/ | Computer Networks/ | [Other Topics]            │
└──────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
1. User asks question → 2. Query embedding generated → 3. Vector similarity search
                                                              ↓
6. Response logged ← 5. LLM generates answer ← 4. Top 3 chunks retrieved
```

---

## File-by-File Documentation

### 1. **app.py** - Main Application Interface

**Purpose**: The primary Streamlit web application that serves as the user interface for NetQuerry.

**Key Responsibilities**:
- Rendering the dual-theme (dark/light) UI with cybersecurity aesthetics
- Managing user session state (theme, answers, sources)
- Handling topic selection from available data folders
- Processing user queries and displaying responses
- Managing source citations display
- Coordinating with backend modules for query processing

**Key Components**:

#### Theme Management
```python
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
```
- Maintains theme state across sessions
- Provides `get_theme_styles()` function returning CSS for dark/light themes
- Dark theme: Matrix-inspired with neon green (#00ff41) accents
- Light theme: Professional with purple gradient (#667eea, #764ba2)

#### UI Elements
- **Header**: Animated logo with glowing effects
- **Topic Selector**: Dropdown menu populated from `data/` folder structure
- **Query Input**: Text input with placeholder examples
- **Response Display**: Formatted answer box with optional source citations
- **Theme Toggle**: Floating button to switch between dark/light modes

#### Workflow
1. Initialize session state and theme
2. Load available topics from `data/` directory using `get_data_folders()`
3. Display topic selector and query input
4. On query submission:
   - Call `get_or_build_bot_db_path()` from `db_utils.py`
   - Execute `query_rag()` from `query_data.py`
   - Log interaction using `log_interaction()` from `log.py`
   - Parse and display answer with optional sources
5. Provide toggle for viewing source citations

**Dependencies**:
- `streamlit`: UI framework
- `db_utils.get_or_build_bot_db_path`: Database management
- `query_data.query_rag`: Query processing
- `log.log_interaction`: Logging functionality

**Notable Features**:
- Automatic database creation for new topics
- Real-time query processing with spinner feedback
- Response time tracking
- Source extraction and formatting
- Responsive design with custom CSS

---

### 2. **query_data.py** - RAG Query Engine

**Purpose**: Core query processing module implementing the Retrieval-Augmented Generation (RAG) pipeline.

**Key Responsibilities**:
- Embedding user queries
- Performing vector similarity search
- Constructing context-aware prompts
- Invoking the LLM for answer generation
- Post-processing responses (removing think blocks, adding citations)
- Generating intelligent source references

**Key Components**:

#### PROMPT_TEMPLATE
```python
PROMPT_TEMPLATE = """
You are a helpful assistant.
You must follow these rules strictly:

1. ONLY answer based on the information provided in the context below
2. If the context does not contain information to answer the question, say "This information is not available in the provided context"
3. Do NOT make up, assume, or infer information that is not explicitly stated in the context
4. Be concise and direct in your answers
5. Do NOT add extra information or explanations beyond what is asked
...
"""
```
- Strict rules prevent hallucination
- Ensures context-only responses
- Guides LLM behavior for accurate answers

#### query_rag() Function
**Parameters**:
- `query_text`: User's question
- `db_path`: Path to topic-specific ChromaDB

**Process**:
1. **Retrieval Phase**:
   - Loads ChromaDB with embedding function
   - Performs similarity search with `k=3` (top 3 chunks)
   - Concatenates retrieved chunks into context

2. **Prompt Construction**:
   - Formats prompt template with context and question
   - Creates structured input for LLM

3. **Generation Phase**:
   - Invokes Ollama Gemma3 4B model
   - Generates response based on context

4. **Post-Processing**:
   - Removes `<think>` blocks using regex
   - Cleans up formatting artifacts
   - Extracts sentences for citation

5. **Citation Generation**:
   - Analyzes first 3 sentences of answer
   - Performs additional similarity search per sentence
   - Extracts source metadata (file, page, chunk)
   - Assigns reference numbers [1], [2], etc.
   - Filters out low-confidence matches (score > 0.8)
   - Excludes metadata pages (prologue, table of contents, index)
   - Appends formatted sources section

**Reference Format**:
```
Answer text here [1]. More information [2].

Sources:
[1] page 42, chunk 2
[2] page 89, chunk 1
```

**Helper Functions**:
- `remove_think_blocks()`: Regex-based removal of LLM reasoning text
- Sentence splitting: `re.split(r"(?<=[.!?])\s+", text)`
- Page number conversion: Adjusts from 0-indexed to 1-indexed

**Dependencies**:
- `langchain_chroma.Chroma`: Vector database
- `langchain_ollama.OllamaLLM`: LLM interface
- `get_embedding_function`: Embedding model

**Command-Line Usage**:
```bash
python query_data.py "What is TCP/IP?"
```

---

### 3. **db_utils.py** - Dynamic Database Management

**Purpose**: Manages vector database creation and retrieval for different topics dynamically.

**Key Responsibilities**:
- Checking if topic-specific database exists
- Building new databases on-demand
- Reusing existing databases for performance
- Coordinating document processing pipeline

**Key Functions**:

#### get_or_build_bot_db_path(folder_name: str)
**Purpose**: Returns database path, creating it if necessary.

**Parameters**:
- `folder_name`: Topic name (e.g., "Cisco", "Computer Networks")

**Logic**:
1. Constructs database directory name: `chroma_{folder_name}`
2. Checks if database exists using `os.path.exists()`
3. If not exists:
   - Constructs data path: `data/{folder_name}`
   - Loads PDFs using `PyPDFDirectoryLoader`
   - Splits documents into chunks
   - Adds chunks to new ChromaDB
4. Returns database directory path

**Example**:
```python
# User selects "Cisco" topic
db_path = get_or_build_bot_db_path("Cisco")
# Returns: "chroma_Cisco"
# Creates database if first time, reuses if exists
```

#### add_to_chroma(chunks, persist_directory)
**Purpose**: Adds document chunks to ChromaDB, avoiding duplicates.

**Process**:
1. Initializes or loads existing ChromaDB
2. Retrieves existing document IDs
3. Filters out chunks that already exist
4. Adds only new chunks with their IDs

**Duplicate Prevention**:
```python
existing_ids = set(existing_items["ids"])
new_chunks = [chunk for chunk in chunks_with_ids 
              if chunk.metadata["id"] not in existing_ids]
```

**Dependencies**:
- `populate_database`: Document processing functions
- `langchain_community.document_loaders.PyPDFDirectoryLoader`: PDF loading
- `langchain_chroma.Chroma`: Vector database

**Benefits**:
- **On-Demand Creation**: Databases created only when needed
- **Reusability**: Existing databases loaded instantly
- **Scalability**: Easy to add new topics by adding folders
- **No Duplication**: Incremental updates without re-indexing

---

### 4. **populate_database.py** - Document Processing Pipeline

**Purpose**: Handles the complete pipeline for loading, processing, and indexing PDF documents into ChromaDB.

**Key Responsibilities**:
- Loading PDFs from directories
- Splitting documents into manageable chunks
- Generating unique chunk IDs
- Populating vector database
- Database reset functionality

**Key Functions**:

#### main()
**Purpose**: Command-line interface for database population.

**Usage**:
```bash
python populate_database.py           # Normal mode: add new documents
python populate_database.py --reset   # Reset mode: clear and rebuild
```

**Process**:
1. Parses command-line arguments
2. Clears database if `--reset` flag present
3. Loads documents from `DATA_PATH`
4. Splits into chunks
5. Adds to ChromaDB at `CHROMA_PATH`

#### load_documents()
**Purpose**: Loads all PDFs from data directory.

**Returns**: List of `Document` objects with:
- `page_content`: Extracted text
- `metadata`: Source file path, page number

**Implementation**:
```python
document_loader = PyPDFDirectoryLoader(DATA_PATH)
return document_loader.load()
```

#### split_documents(documents: list[Document])
**Purpose**: Splits documents into smaller, overlapping chunks for better retrieval.

**Configuration**:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,        # 1500 characters per chunk
    chunk_overlap=200,      # 200 character overlap between chunks
    length_function=len,    # Use character count
    is_separator_regex=False
)
```

**Why These Settings?**:
- **1500 characters**: Optimal balance between context and precision
- **200 overlap**: Ensures continuous context isn't broken at boundaries
- **Recursive splitting**: Preserves semantic structure (paragraphs, sentences)

**Returns**: List of smaller `Document` chunks

#### calculate_chunk_ids(chunks)
**Purpose**: Assigns unique, deterministic IDs to each chunk for duplicate detection.

**ID Format**: `{source_file}:{page_number}:{chunk_index}`

**Example**:
```
data/Cisco/CCNA_Guide.pdf:42:0
data/Cisco/CCNA_Guide.pdf:42:1
data/Cisco/CCNA_Guide.pdf:43:0
```

**Logic**:
```python
last_page_id = None
current_chunk_index = 0

for chunk in chunks:
    source = chunk.metadata.get("source")
    page = chunk.metadata.get("page")
    current_page_id = f"{source}:{page}"
    
    if current_page_id == last_page_id:
        current_chunk_index += 1  # Same page, increment chunk
    else:
        current_chunk_index = 0    # New page, reset counter
    
    chunk_id = f"{current_page_id}:{current_chunk_index}"
    chunk.metadata["id"] = chunk_id
```

**Benefits**:
- **Uniqueness**: No ID collisions
- **Determinism**: Same document always generates same IDs
- **Traceability**: IDs encode source location
- **Incremental Updates**: New documents don't affect existing IDs

#### add_to_chroma(chunks: list[Document])
**Purpose**: Adds chunks to vector database, avoiding duplicates.

**Process**:
1. Loads or creates ChromaDB at `CHROMA_PATH`
2. Calculates chunk IDs using `calculate_chunk_ids()`
3. Retrieves existing IDs from database
4. Filters chunks to only new ones
5. Adds new chunks with their IDs

**Duplicate Prevention**:
```python
existing_ids = set(existing_items["ids"])
new_chunks = [chunk for chunk in chunks_with_ids 
              if chunk.metadata["id"] not in existing_ids]

if len(new_chunks):
    print(f"Adding new documents: {len(new_chunks)}")
    db.add_documents(new_chunks, ids=new_chunk_ids)
else:
    print("No new documents to add")
```

#### clear_database()
**Purpose**: Completely removes the database directory for fresh start.

**Implementation**:
```python
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)
```

**Constants**:
- `CHROMA_PATH = "chroma"`: Default database location
- `DATA_PATH = "data"`: Source PDF directory

**Dependencies**:
- `langchain_community.document_loaders.PyPDFDirectoryLoader`: PDF loading
- `langchain_text_splitters.RecursiveCharacterTextSplitter`: Text chunking
- `langchain_chroma.Chroma`: Vector database
- `get_embedding_function`: Embedding model

---

### 5. **get_embedding_function.py** - Embedding Configuration

**Purpose**: Provides a centralized configuration for the embedding model used throughout the application.

**Key Responsibilities**:
- Configuring Ollama embedding model
- Providing consistent embedding function to all modules
- Abstracting embedding implementation details

**Implementation**:
```python
from langchain_ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings
```

**Embedding Model Details**:
- **Model**: `nomic-embed-text`
- **Provider**: Ollama (local)
- **Dimension**: 768 (typical for nomic-embed-text)
- **Purpose**: Convert text to vector representations for similarity search

**Why nomic-embed-text?**:
1. **Optimized for RAG**: Specifically designed for retrieval tasks
2. **Local Execution**: Runs entirely on your machine via Ollama
3. **High Quality**: Competitive with OpenAI embeddings
4. **Fast**: Efficient inference for real-time queries
5. **Free**: No API costs

**Usage Pattern**:
```python
# In query_data.py
embedding_function = get_embedding_function()
db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

# In populate_database.py
db = Chroma(persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function())
```

**Centralization Benefits**:
- **Consistency**: Same embeddings used for indexing and retrieval
- **Easy Updates**: Change model in one place
- **Testability**: Easy to mock for testing
- **Configuration**: Single point for model parameters

**Requirements**:
- Ollama must be installed and running
- Model must be pulled: `ollama pull nomic-embed-text`

---

### 6. **log.py** - Interaction Logging System

**Purpose**: Tracks all user interactions with the chatbot for analytics, debugging, and performance monitoring.

**Key Responsibilities**:
- Creating and managing SQLite database
- Logging questions, responses, and metadata
- Initializing database schema on first run
- Providing persistent storage for chat history

**Database Schema**:
```sql
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    question TEXT NOT NULL,
    response TEXT NOT NULL,
    time_taken REAL NOT NULL
)
```

**Fields**:
- `id`: Auto-incrementing unique identifier
- `timestamp`: When the interaction occurred (YYYY-MM-DD HH:MM:SS format)
- `question`: User's query text
- `response`: AI-generated answer (including sources)
- `time_taken`: Query processing time in seconds

**Key Functions**:

#### initialize_db()
**Purpose**: Creates the database and logs table if they don't exist.

**Execution**: Called automatically when module is imported:
```python
initialize_db()  # At module level
```

**Implementation**:
```python
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            time_taken REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
```

#### log_interaction(question: str, response: str, time_taken: float)
**Purpose**: Inserts a new interaction record into the database.

**Parameters**:
- `question`: User's query
- `response`: AI's complete response (with sources)
- `time_taken`: Processing time in seconds

**Usage in app.py**:
```python
start_time = time.time()
answer = query_rag(user_input, db_path)
end_time = time.time()
time_taken = round(end_time - start_time, 3)
log_interaction(user_input, answer, time_taken)
```

**Implementation**:
```python
def log_interaction(question: str, response: str, time_taken: float):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, question, response, time_taken)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, question, response, time_taken))
    conn.commit()
    conn.close()
```

**Database Location**:
- `DB_PATH = "chat_logs.db"` (root directory)

**Benefits**:
- **Performance Tracking**: Monitor query response times
- **Quality Assurance**: Review answer accuracy
- **Usage Analytics**: Understand common queries
- **Debugging**: Trace issues through interaction history
- **Compliance**: Maintain audit trail

**Data Access**:
- View via `show.py` script
- Export via `chat_logs_output.csv`
- Direct SQL queries to `chat_logs.db`

---

### 7. **show.py** - Log Viewer and Export Utility

**Purpose**: Provides functionality to view, format, and export chat interaction logs from the SQLite database.

**Key Responsibilities**:
- Connecting to the chat logs database
- Querying and displaying interaction history
- Exporting logs to CSV format
- Pretty-printing tables (with optional tabulate library)

**Workflow**:
1. Connect to `chat_logs.db`
2. List all tables in database
3. Query the `logs` table
4. Display data using pandas DataFrame
5. Optionally format with tabulate for terminal viewing
6. Export to `chat_logs_output.csv`

**Implementation**:
```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('chat_logs.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Load data into DataFrame
df = pd.read_sql_query("SELECT * FROM logs", conn)

# Display
print(df)

# Pretty print (optional)
try:
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='psql'))
except ImportError:
    print("Install tabulate for pretty table: pip install tabulate")

# Export to CSV
df.to_csv('chat_logs_output.csv', index=False)
print("Data saved to chat_logs_output.csv")

# Clean up
conn.close()
```

**Output Format (CSV)**:
```csv
id,timestamp,question,response,time_taken
1,2025-12-04 14:32:11,What is TCP/IP?,TCP/IP is a protocol suite...,2.451
2,2025-12-04 14:33:45,Explain OSI model,The OSI model has 7 layers...,1.872
```

**Usage**:
```bash
python show.py
```

**Output Includes**:
- All logged interactions in tabular format
- Export confirmation message
- Optional pretty-printed table (if tabulate installed)

**Dependencies**:
- `sqlite3`: Database connectivity (standard library)
- `pandas`: Data manipulation and CSV export
- `tabulate`: Pretty table formatting (optional)

**Benefits**:
- **Easy Access**: View logs without SQL knowledge
- **Export Capability**: CSV format for analysis in Excel, etc.
- **Formatted Display**: Human-readable table output
- **Analytics Ready**: DataFrame format for data analysis

---

### 8. **requirements.txt** - Python Dependencies

**Purpose**: Specifies all Python packages and their versions required to run NetQuerry.

**Dependencies Breakdown**:

#### Core RAG Framework
```
langchain>=0.0.95
langchain-community>=0.0.10
```
- **LangChain**: Framework for building LLM applications
- **LangChain Community**: Community-contributed integrations

#### Vector Database
```
chromadb>=0.4.24
```
- **ChromaDB**: Embedded vector database for similarity search
- Stores document embeddings and performs fast retrieval

#### LLM & Embeddings (via Ollama)
```
# Note: Ollama integration comes through langchain-community
# Requires external Ollama installation
```

#### PDF Processing
```
pypdf>=4.2.0
```
- **PyPDF**: Extract text from PDF documents
- Handles multi-page PDFs, metadata extraction

#### Web Interface
```
streamlit>=1.13.0
```
- **Streamlit**: Web application framework
- Provides UI components, session state, custom CSS

#### ML & NLP
```
transformers>=4.21.0
torch>=2.0.0
sentencepiece>=0.1.96
```
- **Transformers**: Hugging Face model library (if needed for fallback)
- **PyTorch**: Deep learning framework
- **SentencePiece**: Tokenization library

#### Data Processing
```
numpy>=1.23.0
pandas>=1.4.3
```
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and CSV handling

#### Utilities
```
python-dotenv>=0.19.0
tiktoken>=0.3.3
```
- **python-dotenv**: Environment variable management
- **tiktoken**: Token counting for OpenAI models (optional)

**Installation**:
```bash
pip install -r requirements.txt
```

**Version Specifications**:
- `>=`: Minimum version required
- Ensures compatibility while allowing updates

---

### 9. **README.md** - Project Documentation

**Purpose**: Provides comprehensive user-facing documentation for setup, usage, and troubleshooting.

**Sections**:

1. **Features**: Lists key capabilities
2. **Quickstart**: Step-by-step setup guide
3. **Prerequisites**: Required software (Python, Ollama, models)
4. **Installation**: Dependency installation instructions
5. **Data Preparation**: How to organize PDF documents
6. **Usage**: How to run and interact with the application
7. **Project Structure**: Directory and file layout
8. **Technical Details**: Model specifications, settings
9. **Troubleshooting**: Common issues and solutions
10. **Credits**: Attribution and technologies used

**Key Information**:

#### Models Required
```bash
ollama pull gemma3:4b          # Text generation
ollama pull nomic-embed-text   # Embeddings
```

#### Directory Structure
```
data/
├── Cisco/                     # Topic-specific PDFs
├── Computer Networks/
└── [Add more topics]/
```

#### Running the Application
```bash
streamlit run app.py
```

#### Manual Database Population
```bash
python populate_database.py --reset
```

**Target Audience**: End users, developers, maintainers

---

### 10. **Data Directory Structure**

**Purpose**: Organizes PDF source documents by topic for multi-domain support.

**Current Structure**:
```
data/
├── Cisco/
│   └── CCNA_Certification_Guide_2024_V8 final.pdf
└── Computer Networks/
    └── Kurose-7.pdf
```

**Topics**:

#### Cisco
- **Content**: Cisco networking certification materials
- **File**: CCNA Certification Guide 2024 V8
- **Database**: `chroma_Cisco/`

#### Computer Networks
- **Content**: General computer networking concepts
- **File**: Kurose and Ross - Computer Networking (7th Edition)
- **Database**: `chroma_Computer Networks/`

**Adding New Topics**:
1. Create new folder in `data/`: `data/New_Topic/`
2. Add PDF files to the folder
3. Application auto-detects and lists in dropdown
4. Database auto-created on first query

**Best Practices**:
- Use descriptive folder names
- Avoid spaces (use underscores): `Network_Security` not `Network Security`
- Group related PDFs in same folder
- Keep PDFs focused on specific topics

---

### 11. **Chroma Database Directories**

**Purpose**: Persistent storage for vector embeddings, organized by topic.

**Structure**:
```
chroma/                          # Default database (if populated manually)
├── chroma.sqlite3              # SQLite storage
└── {collection_id}/            # Vector data

chroma_Cisco/                   # Cisco topic database
├── chroma.sqlite3
└── e152807f-.../

chroma_Computer Networks/       # Networks topic database
├── chroma.sqlite3
└── 6b1284db-.../
```

**Contents**:
- **chroma.sqlite3**: Metadata, IDs, mappings
- **Collection directories**: Vector embeddings, indexes

**Characteristics**:
- **Persistent**: Data survives application restarts
- **Incremental**: Can add documents without rebuilding
- **Fast**: Optimized for similarity search
- **Isolated**: Each topic has independent database

**Size Considerations**:
- Proportional to document corpus size
- Typical: 10-100 MB per topic
- Includes embeddings for all chunks

**Management**:
- Auto-created by `db_utils.py`
- Can be deleted to force rebuild
- Portable (can be copied/shared)

---

## Data Flow

### Complete Query Processing Flow

```
1. USER ACTION
   └─► User enters question in Streamlit UI (app.py)

2. TOPIC SELECTION
   └─► User selects topic from dropdown (e.g., "Cisco")
   
3. DATABASE CHECK
   └─► app.py calls get_or_build_bot_db_path("Cisco") [db_utils.py]
       └─► Checks if chroma_Cisco/ exists
           ├─► YES: Return "chroma_Cisco"
           └─► NO: Build database
               ├─► Load PDFs from data/Cisco/ [PyPDFDirectoryLoader]
               ├─► Split into chunks [populate_database.split_documents]
               │   └─► 1500 char chunks, 200 char overlap
               ├─► Calculate chunk IDs [populate_database.calculate_chunk_ids]
               │   └─► Format: source:page:chunk_index
               ├─► Generate embeddings [get_embedding_function]
               │   └─► Using nomic-embed-text via Ollama
               ├─► Store in ChromaDB [db_utils.add_to_chroma]
               └─► Return "chroma_Cisco"

4. QUERY EMBEDDING
   └─► app.py calls query_rag(question, "chroma_Cisco") [query_data.py]
       └─► Generate embedding for user question
           └─► Using nomic-embed-text via Ollama

5. VECTOR SEARCH
   └─► Search ChromaDB for similar chunks
       └─► db.similarity_search_with_score(query, k=3)
           └─► Returns top 3 most similar chunks with scores

6. CONTEXT ASSEMBLY
   └─► Concatenate retrieved chunks
       └─► Format: "chunk1\n\n---\n\nchunk2\n\n---\n\nchunk3"

7. PROMPT CONSTRUCTION
   └─► Insert context and question into PROMPT_TEMPLATE
       └─► Includes strict rules against hallucination

8. LLM INFERENCE
   └─► Send prompt to Ollama Gemma3 4B
       └─► model.invoke(prompt)
           └─► Returns text response

9. POST-PROCESSING
   └─► Remove <think> blocks (LLM reasoning)
   └─► Clean formatting artifacts
   └─► Split into sentences

10. CITATION GENERATION
    └─► For each sentence (first 3):
        ├─► Search ChromaDB for matching chunks
        ├─► Extract metadata (source, page, chunk)
        ├─► Filter low-confidence matches (score > 0.8)
        ├─► Assign reference number [1], [2], etc.
        └─► Append to sentence

11. SOURCE FORMATTING
    └─► Append "Sources:" section
        └─► List all references with page/chunk info

12. LOGGING
    └─► app.py logs interaction [log.py]
        ├─► Question
        ├─► Response (with sources)
        ├─► Time taken
        └─► Store in chat_logs.db

13. UI DISPLAY
    └─► app.py renders response in styled box
        ├─► Main answer displayed
        └─► "View Sources" button shown (if sources exist)

14. USER INTERACTION
    └─► User can toggle source visibility
        └─► Sources displayed in collapsible section
```

### Document Indexing Flow (One-Time per Topic)

```
1. PDF FILES
   └─► Placed in data/{topic}/ directory

2. LOADING
   └─► PyPDFDirectoryLoader reads all PDFs
       └─► Extracts text and metadata per page

3. SPLITTING
   └─► RecursiveCharacterTextSplitter
       ├─► 1500 char chunks
       ├─► 200 char overlap
       └─► Preserves semantic boundaries

4. ID ASSIGNMENT
   └─► calculate_chunk_ids()
       └─► Format: source:page:chunk_index
       └─► Example: data/Cisco/CCNA.pdf:42:0

5. EMBEDDING GENERATION
   └─► For each chunk:
       └─► Generate 768-dim vector via nomic-embed-text

6. STORAGE
   └─► ChromaDB stores:
       ├─► Chunk text
       ├─► Embeddings
       ├─► Metadata (source, page, ID)
       └─► Index structures for fast search

7. PERSISTENCE
   └─► Database saved to chroma_{topic}/
       └─► Ready for queries
```

---

## Technical Stack

### Backend Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Gemma3 4B (Ollama) | Text generation, answer synthesis |
| **Embeddings** | nomic-embed-text (Ollama) | Convert text to vector representations |
| **Vector DB** | ChromaDB | Store and search document embeddings |
| **Framework** | LangChain | RAG pipeline orchestration |
| **PDF Processing** | PyPDF | Extract text from PDF documents |
| **Database** | SQLite | Store chat interaction logs |

### Frontend Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI Framework** | Streamlit | Web application interface |
| **Styling** | Custom CSS | Dark/light themes, cybersecurity aesthetics |
| **State Management** | Streamlit Session State | Persist theme, answers across interactions |

### Development Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.10+ | Core development language |
| **Package Manager** | pip | Dependency management |
| **Data Analysis** | Pandas | Log viewing and CSV export |
| **Environment** | python-dotenv | Configuration management |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Execution** | Local machine | 100% local processing |
| **LLM Runtime** | Ollama | Local LLM inference |
| **Storage** | File system | ChromaDB and SQLite persistence |

---

## Setup and Installation

### Prerequisites

1. **Python 3.10 or higher**
   ```bash
   python --version
   ```

2. **Ollama**
   - Download from [ollama.com](https://ollama.com/)
   - Install for your platform (Windows/Mac/Linux)
   - Start Ollama service:
     ```bash
     ollama serve
     ```

3. **Required Ollama Models**
   ```bash
   ollama pull gemma3:4b          # LLM for text generation
   ollama pull nomic-embed-text   # Embedding model
   ```

### Installation Steps

1. **Clone or Download Project**
   ```bash
   cd NetQuerry
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Data**
   - Create topic folders in `data/` directory
   - Add PDF files to respective topic folders
   - Example:
     ```
     data/
     ├── Cisco/
     │   └── CCNA_Guide.pdf
     ├── Computer Networks/
     │   └── Kurose_Ross_7ed.pdf
     └── Network_Security/
         └── Security_Fundamentals.pdf
     ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

6. **Access Interface**
   - Open browser to: http://localhost:8501
   - Select topic from dropdown
   - Start asking questions!

### Optional: Pre-populate Default Database

```bash
python populate_database.py
```
This creates the default `chroma/` database. Topic-specific databases are auto-created on first query.

---

## Usage Guide

### Basic Usage

1. **Start Application**
   ```bash
   streamlit run app.py
   ```

2. **Select Topic**
   - Choose from dropdown menu (e.g., "Cisco", "Computer Networks")
   - Database auto-builds on first selection (may take 1-2 minutes)

3. **Ask Questions**
   - Type question in text input
   - Examples:
     - "What is TCP/IP protocol?"
     - "Explain the OSI model layers"
     - "How does DNS resolution work?"
     - "What is VLAN tagging in Cisco?"

4. **View Answers**
   - Answer displays in styled box
   - Processing time shown
   - Sources available via "View Sources" button

5. **Toggle Theme**
   - Click moon icon for dark theme
   - Click sun icon for light theme

### Advanced Features

#### View Interaction Logs
```bash
python show.py
```
- Displays all logged interactions
- Exports to `chat_logs_output.csv`

#### Reset Database
```bash
python populate_database.py --reset
```
- Clears and rebuilds default database
- Use if documents updated or database corrupted

#### Query from Command Line
```bash
python query_data.py "What is TCP handshake?"
```
- Uses default `chroma/` database
- Outputs answer to terminal

#### Add New Topic
1. Create folder: `data/New_Topic/`
2. Add PDF files to folder
3. Restart app (or refresh if already running)
4. New topic appears in dropdown automatically

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Ollama not found" or "Model not available"

**Problem**: Ollama service not running or models not pulled

**Solution**:
```bash
# Check if Ollama is running
ollama list

# Start Ollama service (if not running)
ollama serve

# Pull required models
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

#### 2. "No topics available" / Empty dropdown

**Problem**: No folders in `data/` directory or folders are empty

**Solution**:
- Create topic folders in `data/`
- Add PDF files to each folder
- Ensure folder names don't contain special characters
- Restart Streamlit application

#### 3. "Database error" or "ChromaDB connection failed"

**Problem**: Corrupted database or permission issues

**Solution**:
```bash
# Delete corrupted database
rm -rf chroma_TopicName/

# Or delete all databases
rm -rf chroma*/

# Restart app - databases will rebuild automatically
```

#### 4. Slow first query / "Building knowledge base..." takes long

**Problem**: Database being created for first time (normal behavior)

**Solution**:
- Wait for initial build (1-5 minutes depending on PDF size)
- Subsequent queries will be fast (1-3 seconds)
- Pre-build databases manually:
  ```bash
  python populate_database.py
  ```

#### 5. "Unable to answer" or "Information not available"

**Problem**: Question not covered in provided documents

**Solution**:
- Rephrase question to match document terminology
- Add more relevant PDFs to topic folder
- Ensure PDFs contain text (not scanned images)
- Check if correct topic selected

#### 6. Answers missing source citations

**Problem**: Low similarity scores or metadata filtering

**Solution**:
- Check PDF quality (text-based, not scanned)
- Verify PDFs have proper page numbers
- Ensure `query_data.py` similarity threshold not too strict (current: 0.8)

#### 7. "Module not found" errors

**Problem**: Dependencies not installed or virtual environment not activated

**Solution**:
```bash
# Activate virtual environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 8. Chat logs not appearing

**Problem**: Database not initialized or permission issues

**Solution**:
```bash
# Check if database exists
ls chat_logs.db

# View logs
python show.py

# If empty, ensure you've submitted queries through UI
```

#### 9. Theme not changing

**Problem**: Browser cache or session state issue

**Solution**:
- Click theme toggle button again
- Refresh browser page (F5)
- Clear browser cache
- Restart Streamlit app

#### 10. Out of memory errors

**Problem**: Large PDFs or many documents

**Solution**:
- Reduce `chunk_size` in `populate_database.py` (from 1500 to 1000)
- Process PDFs in smaller batches
- Increase system RAM
- Use smaller PDF files

---

## Performance Optimization

### Query Response Time

**Typical Performance**:
- First query (new topic): 30-120 seconds (database building)
- Subsequent queries: 1-3 seconds
- Command-line queries: < 2 seconds

**Optimization Tips**:
1. **Pre-build databases**: Run `populate_database.py` before first use
2. **Reduce k value**: Change `k=3` to `k=2` in `query_data.py` for faster retrieval
3. **Smaller chunks**: Reduce `chunk_size` in `populate_database.py` (trade-off: less context)
4. **Limit PDFs**: Keep topic-specific folders focused

### Memory Usage

**Typical Memory**:
- Base application: ~500 MB
- Per database: ~50-200 MB (depends on corpus size)
- Ollama models: ~3 GB (loaded in separate process)

**Optimization**:
- Close unused applications
- Limit number of topics loaded simultaneously
- Use smaller PDF files when possible

---

## Security and Privacy

### Data Privacy
- **100% Local Processing**: No data sent to external servers
- **No Internet Required**: All models run via Ollama locally
- **No Telemetry**: No usage tracking or analytics
- **Private Documents**: Your PDFs never leave your machine

### Best Practices
- Keep NetQuerry in trusted environment
- Don't expose Streamlit port (8501) to public internet
- Regularly backup `chroma*/` databases if important
- Clear `chat_logs.db` if contains sensitive queries

---

## Future Enhancements

### Potential Features
1. **Multi-language Support**: Non-English PDFs
2. **Chat History UI**: View past interactions in app
3. **Advanced Filtering**: Date ranges, page ranges
4. **Document Upload**: UI-based PDF upload (no manual folder management)
5. **Export Answers**: Save specific answers to file
6. **Batch Queries**: Process multiple questions at once
7. **Feedback System**: Rate answer quality
8. **Custom Prompts**: User-configurable prompt templates
9. **Image Support**: Extract and reference diagrams from PDFs
10. **API Mode**: RESTful API for integration with other tools

---

## Contributing

### Development Setup
1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly (all topics, edge cases)
5. Submit pull request

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to functions
- Comment complex logic
- Update documentation for new features

### Testing Checklist
- [ ] Test with multiple topics
- [ ] Verify database auto-creation
- [ ] Check source citations accuracy
- [ ] Test both dark and light themes
- [ ] Validate logging functionality
- [ ] Test with various PDF types and sizes
- [ ] Verify error handling

---

## Credits and Acknowledgments

### Development Team
- **Project**: Semester 7 Capstone Project
- **Course**: Theory of Automata (TOAT)
- **Institution**: National University of Sciences & Technology (NUST)

### Technologies
- **LangChain**: RAG framework - [langchain.com](https://www.langchain.com/)
- **Ollama**: Local LLM runtime - [ollama.com](https://ollama.com/)
- **Streamlit**: Web UI framework - [streamlit.io](https://streamlit.io/)
- **ChromaDB**: Vector database - [trychroma.com](https://www.trychroma.com/)
- **Gemma3**: LLM by Google - [ai.google.dev/gemma](https://ai.google.dev/gemma)
- **PyPDF**: PDF processing - [pypdf.readthedocs.io](https://pypdf.readthedocs.io/)

### Inspiration
- ChatGPT interface design
- Cybersecurity/Matrix aesthetic themes
- Modern RAG best practices

---

## License

Educational project for academic purposes.

---

## Contact and Support

For issues, questions, or contributions, please refer to the course instructor or project team.

**Version**: 1.0  
**Last Updated**: December 2025  
**Status**: Active Development

---

## Appendix

### A. Chunk Size Analysis

**Why 1500 characters?**
- **Too Small (< 500)**: Loses context, requires more chunks for same answer
- **Optimal (1000-2000)**: Balances context and precision
- **Too Large (> 3000)**: Retrieves irrelevant information, slower processing

**Current Setting**: 1500 characters with 200 overlap

### B. Similarity Score Thresholds

**ChromaDB Scores** (lower = more similar):
- **< 0.5**: Highly similar (exact matches, paraphrases)
- **0.5 - 0.8**: Moderately similar (related concepts)
- **> 0.8**: Weakly similar (filtered out in citation)

**Current Threshold**: 0.8 (citations only for strong matches)

### C. Prompt Engineering Notes

**Key Prompt Elements**:
1. **Role Definition**: "You are a helpful assistant"
2. **Strict Rules**: Numbered constraints (1-5)
3. **Context Injection**: `{context}` placeholder
4. **Question Injection**: `{question}` placeholder
5. **Output Guidance**: "Answer (based only on the context above):"

**Anti-Hallucination Measures**:
- Rule #2: Explicit instruction to decline when info unavailable
- Rule #3: Prohibition on inferring/assuming
- Rule #4: Conciseness requirement (reduces speculation)
- Rule #5: No extra information (stays grounded)

### D. Database Schema Details

**ChromaDB Collections**:
```python
{
    "ids": ["doc1:0:0", "doc1:0:1", ...],
    "embeddings": [[0.1, 0.2, ...], ...],
    "metadatas": [
        {"source": "data/Cisco/CCNA.pdf", "page": 42, "id": "..."},
        ...
    ],
    "documents": ["chunk text 1", "chunk text 2", ...]
}
```

**SQLite Logs Schema**:
```sql
logs (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,      -- "2025-12-04 14:32:11"
    question TEXT,       -- User query
    response TEXT,       -- AI answer with sources
    time_taken REAL      -- Seconds (e.g., 2.451)
)
```

### E. File Dependencies Graph

```
app.py
├─► db_utils.py
│   ├─► populate_database.py
│   │   ├─► get_embedding_function.py
│   │   └─► langchain_community (PyPDFDirectoryLoader)
│   └─► get_embedding_function.py
├─► query_data.py
│   └─► get_embedding_function.py
└─► log.py

populate_database.py (standalone)
└─► get_embedding_function.py

show.py (standalone)
```

### F. Environment Variables (Optional)

Create `.env` file for configuration:
```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_NUM_PARALLEL=1

# Database Paths
CHROMA_PATH=chroma
DATA_PATH=data

# Model Settings
LLM_MODEL=gemma3:4b
EMBEDDING_MODEL=nomic-embed-text

# Chunk Settings
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# Retrieval Settings
TOP_K=3
SIMILARITY_THRESHOLD=0.8
```

**Note**: Current implementation uses hardcoded values. Environment variables can be added for flexibility.

---

**End of Documentation**
