# BitBud

![image](https://github.com/user-attachments/assets/4e90b666-9cfb-487d-8c99-e8f2090f2c5f)

**Your Local AI Productivity Sidekick**  
An 8-bit desktop agent that learns your habits, helps automate tasks, and enhances your Linux environment — all running locally on your machine.

---

## Overview

BitBud is a voice-enabled, local-first AI assistant designed for Linux desktops. It monitors your behavior, understands your preferences, and proactively assists with daily tasks using local large language models (LLMs), retrieval-augmented generation (RAG), and AI agent workflows.

This project demonstrates a sophisticated desktop co-pilot built with privacy and efficiency in mind.

---

## Features

- 8-bit floating desktop avatar inspired by classic desktop pets  
- Optional voice-enabled interaction  
- Chat interface accessible on hover or click for seamless communication  
- Integration with local LLMs (via [Ollama](https://ollama.ai)) to ensure offline use  
- Website observer for logging and summarizing visited content (optional)  
- Automation of common apps such as Spotify, YouTube, Netflix, and VS Code  
- Personalized learning to adapt to user preferences over time  
- Fully private and offline with all data stored locally  

---

How It Works

BitBud operates by continuously learning from user interactions and system context. It combines local LLMs with retrieval-augmented generation to provide relevant responses and automates system tasks through AI agents. Interaction is possible via voice or text, facilitated by an engaging 8-bit avatar.
Privacy and Security

BitBud is designed with privacy as a core principle. All user data and interactions are processed and stored locally, with no external telemetry or cloud dependency.
Future Development Plans

    Implement a context timeline with editable memory

    Develop a comprehensive automation dashboard

    Add voice-to-action scripting capabilities

    Create a plugin system for custom task extensions



## Technology Stack

|--------------------|-------------------------------------------|
| Component          | Technologies                              |
|--------------------|-------------------------------------------|
| Frontend           | React, Tailwind CSS, GSAP                 |
| AI Engine          | Python, Ollama (Mistral model), LangGraph |
| Retrieval & Memory | ChromaDB, LangChain                       |
| Backend            | Flask, WebSockets                         |
| Automation         | Custom Python and shell scripts           |
| Platform           | Linux Desktop                             |
|--------------------|-------------------------------------------|

---

## Setup Instructions

### Clone the repository

```bash
git clone https://github.com/Flakes342/BitBud.git
cd BitBud

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

ollama run <your_desired_model>

python backend/app.py

cd frontend
npm install
npm run dev
