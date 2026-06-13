# 🔬 ResearchMind – Multi-Agent AI Research System

ResearchMind is a multi-agent AI research assistant that autonomously performs web research, content extraction, report generation, and quality evaluation.

The system combines specialized AI agents with web search and scraping tools to transform a simple research query into a structured, professional research report with automated critique and feedback.

---

## 🚀 Features

### 🌐 Search Agent

* Searches the web using Tavily Search API.
* Retrieves relevant and up-to-date information.
* Collects titles, URLs, and content snippets.

### 📖 Reader Agent

* Selects the most relevant source.
* Scrapes webpage content using BeautifulSoup.
* Extracts clean textual information for deeper analysis.

### ✍️ Writer Agent

* Synthesizes gathered information.
* Generates structured research reports.
* Produces professional, well-organized outputs.

### 🧠 Critic Agent

* Evaluates report quality.
* Identifies strengths and weaknesses.
* Provides a score and actionable feedback.

### 🎨 Streamlit Frontend

* Modern research dashboard.
* Real-time visualization of the research workflow.
* Interactive report generation experience.

---

## 🏗️ Architecture

```text
User Query
    │
    ▼
┌─────────────────┐
│  Search Agent   │
│ (Tavily Search) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reader Agent   │
│ (Web Scraping)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Agent   │
│ (Report Draft)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic Agent   │
│ (Evaluation)    │
└────────┬────────┘
         │
         ▼
 Final Research Report
```

---

## 🛠️ Tech Stack

### AI & Agent Framework
- LangChain
- LangChain GroQ

### LLM
- Llama 3 (via GroQ API)

### Search & Retrieval
- Tavily Search API

### Web Scraping
- BeautifulSoup4
- Requests
- lxml

### Frontend
- Streamlit

### Environment Management
- Python Dotenv

---

## 📂 Project Structure

```text
multi-agent-research-system/
│
├── agents.py
│   ├── Search Agent
│   ├── Reader Agent
│   ├── Writer Chain
│   └── Critic Chain
│
├── tools.py
│   ├── Tavily Search Tool
│   └── URL Scraping Tool
│
├── pipeline.py
│   └── Research Workflow Orchestration
│
├── app.py
│   └── Streamlit User Interface
│
├── requirements.txt
├── .gitignore
└── .env
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/multi-agent-research-system.git
cd multi-agent-research-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Running the CLI Pipeline

Run the research workflow directly from the terminal:

```bash
python pipeline.py
```

Example:

```text
Enter a research topic:
Impact of AI Agents on Software Engineering Jobs
```

The pipeline will execute:

1. Search Agent
2. Reader Agent
3. Writer Agent
4. Critic Agent

and generate a final report with evaluation.

---

## 🖥️ Running the Streamlit Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

in your browser.

---

## 🧪 Example Research Topics

* Future of AI Agents in Software Engineering
* Impact of Generative AI on Healthcare
* RAG vs Fine-Tuning for Enterprise Applications
* Autonomous Agents in Business Automation
* Smart Cities and AI-driven Urban Planning
* Cybersecurity Challenges in the Age of AI

---


## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

* Multi-Agent AI Systems
* Agent Orchestration
* Tool-Augmented LLMs
* Search-Augmented Generation
* Prompt Engineering
* Autonomous Research Pipelines
* Web Scraping Integration
* Streamlit Application Development
* LangChain Agent Development

---

## 🔮 Future Enhancements

* PDF Report Export
* Citation Management
* Multi-Source Reading Agent
* Memory-Enabled Agents
* LangGraph Workflow Integration
* Multi-LLM Support (Claude, Gemini, OpenAI)
* Vector Database Integration
* Research History & Persistence

---

### Skills Demonstrated

* Python
* LangChain
* OpenAI APIs
* Streamlit
* Web Scraping
* Multi-Agent Systems
* Prompt Engineering

---

## 📄 License

This project is released for educational and portfolio purposes.
