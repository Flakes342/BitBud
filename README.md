# BitBud

<p align="center">
  <img width="600" height="500" src="https://github.com/user-attachments/assets/84724850-bf67-4fac-85c5-0d4cfed4f648"
 />
</p>



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

## Technology Stack

| Component          | Technologies                              |
|--------------------|-------------------------------------------|
| Frontend           | React, Tailwind CSS, GSAP                 |
| AI Engine          | Python, Gemma3:4b, LangGraph              |
| Retrieval & Memory | ChromaDB, LangChain                       |
| Backend            | Flask, WebSockets                         |
| Automation         | Custom Python and shell scripts           |
| Platform           | Linux Desktop                             |

---

## Setup Instructions

```bash
git clone https://github.com/Flakes342/BitBud.git
cd BitBud

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py


