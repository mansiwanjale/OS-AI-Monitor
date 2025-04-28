# OS-AI-Monitor _Zerolag_

This project is a **System Utility Dashboard** that integrates four core functionalities:

1. **Chatbot** – An intelligent assistant to help diagnose and provide system suggestions.
2. **Cleanup** – Automatically detects and cleans up unnecessary files or data on your system.
3. **System Health Score** – Displays real-time system health metrics such as CPU, memory, disk usage, and network status.
4. **Task Manager Easy UI** – A simple user interface to manage running tasks and processes on your system.

---

## Table of Contents

1. [Installation](#installation)
2. [Features](#features)
3. [How to Use](#how-to-use)
4. [Technologies Used](#technologies-used)
5. [Contributors](#contributors)

---

## Installation

### Backend (Python)

1. Clone this repository:

   ```bash
   git clone https://github.com/mansiwanjale/OS-AI-Monitor.git
   cd system-utility-dashboard

2. Set up a virtual environment:
   python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate

3.Install the required Python dependencies:
  pip install -r backend/requirements.txt

4.Start the backend server:
  python backend/app.py

5. Navigate to frontend and start 
  cd frontend
  npm start

Features
1. Chatbot
The Chatbot serves as an interactive assistant to help diagnose issues and suggest system improvements.

It uses NLP (Natural Language Processing) to understand user queries and provides relevant suggestions.

Main features:

Ability to recognize commands like "Check CPU usage," "System slow," etc.

Provides helpful suggestions based on system status.

2. Cleanup
The Cleanup page helps optimize the system by removing unnecessary files.

It scans for temporary files, cached data, and other potential disk clutter.

Main features:

Option to scan and clean up unused files automatically.

Provides feedback on how much space was saved during cleanup.

3. System Health Score
The System Health Score is a metric that gives an overall status of your system's health.

It calculates a health score based on CPU, memory, disk usage, and network usage.

Main features:

Real-time health score updates displayed in a circular graph.

CPU, memory, disk, and network usage in percentage.

Daily health scores are stored and displayed in a calendar format.

4. Task Manager Easy UI
A simple user interface to monitor and manage running processes.

Displays active processes and allows users to end tasks or view detailed system information.

