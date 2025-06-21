# Mitchi AI

<p align="center">
  <img width="300" height="300" src="https://github.com/user-attachments/assets/f257c518-1803-4d70-9abb-c86e54da88cf"
 />
</p>



**Your Local AI Productivity Agent**  
An desktop agent that learns your habits, helps automate tasks, and enhances your Linux environment, all running locally on your machine.
It observes you just like Mitchi does..


---

## Overview

Mitchi AI is a local-first AI assistant designed for Linux desktops. It monitors your behavior, understands your preferences, and proactively assists with daily tasks using local large language models (LLMs), retrieval-augmented generation (RAG), and AI agent workflows.

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
```

## Application Flow

<p align="center">
  <img width="300" height="800" src="https://github.com/user-attachments/assets/ed1a7c54-cbc7-4faf-8608-0bde1de6d1c1"
 />
</p>

