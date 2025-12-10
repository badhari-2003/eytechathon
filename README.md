# eytechathon
🚗 AutoSense – Agentic Predictive Maintenance System
EY Techathon 6.0 – Round 2 Prototype

A unified Agentic AI system for predictive vehicle maintenance, autonomous scheduling, and RCA/CAPA-based manufacturing insights.

📌 Overview

AutoSense is an AI-powered, agentic predictive maintenance platform designed for automotive OEMs and service networks.
It continuously analyzes telematics data, predicts upcoming failures, engages customers using an AI voice agent, schedules service slots automatically, and sends RCA/CAPA feedback to manufacturing.

This repository contains:

✅ Streamlit Web Dashboard (frontend)

✅ Agentic Multi-Agent System (backend)

✅ Fully working integrated prototype

✅ Ready for EY Techathon demonstration

🧠 Features
✔ Agentic Multi-Agent Architecture

Master Agent (orchestrator)

Data Analysis Agent (sensor anomaly detection)

Diagnosis Agent (failure prediction)

Customer Voice Agent (AI-generated messages)

Scheduling Agent (auto-booking slots)

Manufacturing Insights Agent (RCA/CAPA feedback)

✔ Streamlit Dashboard

Fleet risk overview

Real-time simulated telematics charts

Agentic prediction flow per vehicle

Manual booking section

RCA/CAPA insights visualization

✔ Integrated Prototype

The UI directly calls the Master Agent and displays all outputs:

Risk score

Diagnosis

Voice agent message

Recommended slot

RCA/CAPA report

| Component       | Technology                   |
| --------------- | ---------------------------- |
| Frontend        | Streamlit                    |
| Backend Logic   | Python                       |
| ML / Risk Model | Rule-based (demo)            |
| Agents          | Pure Python (OOP)            |
| Data            | Synthetic telematics dataset |
| Charts          | Streamlit + Pandas           |
| Deployment      | Local (Streamlit run)        |


📂 Project Structure

├── app.py                 # Main Streamlit (UI + Agentic model integrated)
├── README.md              # Documentation
└── assets/                # (Optional) Screenshots, architecture diagrams


🚀 Running the Project
1️⃣ Install dependencies
pip install streamlit pandas numpy

2️⃣ Run the unified app
streamlit run app.py


Your browser will open automatically at:

http://localhost:8501

🧪 How the Agentic Model Works

▶ Step 1: Data Analysis

Reads temperature, vibration, and service history → generates a risk score.

▶ Step 2: Diagnosis

Classifies risk as High / Medium / Low.

▶ Step 3: Customer Engagement

Creates a voice-style message based on the diagnosis.

▶ Step 4: Autonomous Scheduling

If High/Medium risk → recommends a nearest service slot.

▶ Step 5: RCA/CAPA

Generates feedback for OEM manufacturing teams.

▶ Step 6: Display in Dashboard

All outputs shown in Streamlit UI instantly.
