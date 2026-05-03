# IntelliMeet AI: AI-Powered Meeting Assistant ⚆_⚆

An AI-powered meeting assistant that summarizes transcripts, extracts action items, sends personalized emails, and enables context-aware querying using a RAG chatbot.

## 🦀 Problem

Meetings generate unstructured information that is difficult to track. Teams often struggle with:
- remembering key decisions
- tracking assigned tasks
- managing follow-ups

This leads to inefficiency and missed deadlines.

## 🌟 Solution

IntelliMeet AI automates post-meeting workflows by:
- generating concise summaries
- extracting structured action items
- sending personalized emails to participants
- enabling a chatbot to query meeting data using natural language
  
## ❄️ Architecture

The system follows a modular service-based architecture:

- FastAPI backend for APIs and orchestration
- Streamlit frontend for UI
- Pinecone for vector storage (RAG)
- Supabase for relational data
- Groq API (LLaMA) for LLM tasks
- Docker and AWS EC2 for Deployment

## 🦋 Workflow

- User uploads transcript
- LLM generates summary
- LLM extracts structured tasks
- Data stored in Supabase
- User sends emails
- Transcript chunked and embedded
- Embeddings stored in Pinecone
- User queries chatbot
- Relevant chunks retrieved
- LLM generates contextual response
    
## ⚡Deployment

Deployed on AWS EC2 using Docker and docker-compose.

Steps:
- Launch Ubuntu EC2 instance
- Install Docker & docker-compose
- Clone repo
- Configure environment variables
- Run: docker compose up -d

Access via:
- http://\<ec2-ip\>:8501

## Installation (Local Setup) (✿◡‿◡)

1. Clone repository:
   git clone https://github.com/Maheer24/intellimeet-ai.git

2. Navigate:
   cd intellimeet-ai

3. Add .env files (backend & frontend)

4. Run using Docker:
   docker compose up --build

5. Access:
   Frontend → http://localhost:8501  
   Backend → http://localhost:8000/docs
