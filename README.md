CPU Scheduling Algorithm Simulator
cpu-scheduler/
├── app.py                 # Flask application entry point
├── scheduler.py           # Core scheduling algorithms
├── templates/
│   ├── home.html          # Landing page (new)
│   └── simulator.html     # Main simulator page (formerly index.html)
└── static/
    ├── style.css          # Styles for simulator page
    └── script.js          # JavaScript for simulator functionality

An interactive web application that visualizes various CPU scheduling algorithms with real-time performance metrics.

Features

6 Scheduling Algorithms :

First-Come-First-Serve (FCFS)
Shortest Job First (Non-Preemptive)
Shortest Remaining Time First (Preemptive)
Round Robin (RR)
Priority Scheduling (Non-Preemptive)
Priority Scheduling (Preemptive)
Interactive Visualization :

Dynamic Gantt charts
Process timeline visualization
Performance metrics comparison
User-Friendly Interface :

Add/remove processes easily
Customize arrival times, burst times, and priorities
Responsive design works on all devices
Installation

Clone the repository:
git clone https://github.com/yourusername/cpu-scheduler.git
cd cpu-schedulerInstall dependencies:
bash pip install flask Run the application:

bash python app.py Access the simulator in your browser: http://localhost:5000

Usage Landing Page:

Overview of features

Team information =>
Ayush Pandey (12313405) 
Nitin kumar(1232412)
Aniket (1232412)
