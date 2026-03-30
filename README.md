# 🤖 BlogGen: Autonomous AI Blog Orchestrator

*A scalable, multi-agent AI pipeline designed to convert keyword intent into high-ranking, GEO-optimized, and conversion-focused content.* Built for the *Prompt & Profit - Bizmark'26 Hackathon* by DTU Consulting Group.

---

## 🎯 Project Overview

In response to the Part 1: AI Blog Engine Architecture requirements, this application serves as an end-to-end content generation and SEO validation engine. It leverages a multi-agent LLM architecture to research SERP gaps, draft structured content, format semantic HTML, and calculate real-time Generative Engine Optimization (GEO) metrics.

### ✨ Core Features
* *Multi-Agent Orchestration:* Utilizes three distinct AI agent roles (Research, Drafting, and SEO Optimization) operating in a sequential pipeline to ensure high semantic richness and structural integrity.
* *Integrated GEO Validation Dashboard:* A live, interactive radar chart and scoring system that evaluates the generated text against standard metrics: Structure, Semantic, Interpretability, Conversational Tone, and Engagement.
* *Position 0 Optimization:* Automatically injects direct, 40-60 word answers after major headings to target featured snippets.
* *Headless CMS Integration:* Features an automated pipeline to push finalized HTML directly to WordPress as a draft via the WP REST API.
* *Secure Secrets Management:* Implements streamlit secrets to securely manage API keys and credentials without exposing them in the repository.

---

## 🏗️ System Architecture

1. *Frontend:* Streamlit (Python) for rapid UI deployment and interactive Plotly dashboards.
2. *Backend Engine:* Python-based orchestrator utilizing Google's gemini-2.5-flash model.
3. *Data Integration:* JSON-LD schema generation for FAQs and automated WordPress REST API syncing.

---

## 🚀 Local Setup & Installation (For Judges & Developers)

If you wish to run the AI engine locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/Inferno-0/BlogGen.git
cd BlogGen
```

### 2. Install Dependencies
Ensure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Configure API Secrets
This project uses Streamlit Secrets for environment variables.

Create a hidden folder named `.streamlit` in the root directory.

Copy the provided template:
```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and add your valid Gemini API Key and WordPress App Passwords.


### 4. Run the Application
Launch the Streamlit server:
```bash
streamlit run app.py
```

The UI will automatically open in your default web browser at http://localhost:8501.

---

## 📊 How to Use the Engine
* Enter your Target Keyword (e.g., "Autonomous AI Agents") into the sidebar.
* Click Generate Blog Post.
* The orchestrator will sequentially execute the Research, Drafting, and SEO formatting phases. (Note: Generation takes approximately 30-45 seconds as the pipeline builds comprehensive HTML).
* Review the heavily optimized content, the generated JSON-LD schema, and the interactive GEO Validation Report at the bottom of the page.
* (Optional) Use the "Push to WordPress" integration to send the draft to your CMS.

---

## 👥 Team
* **Role 1 (Technical Lead):** Core AI Architecture & Prompt Engineering.
* **Role 2 (Data & SEO Strategist):** GEO Scoring Framework & SERP Gap Analysis.
* **Role 3 (Deployment Specialist):** Cloud Hosting & WordPress Integration.
* **Role 4 (Presentation and Testing Specialist):** PPT creation and proper Testing of the Application.
