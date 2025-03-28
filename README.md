CPU Scheduling Algorithm Simulator
cpu-scheduler/ ├── app.py # Flask application ├── scheduler.py # Scheduling algorithms ├── templates/ │ ├── home.html # Landing page │ └── simulator.html # Simulation interface └── static/ ├── style.css # Stylesheets └── script.js # Frontend logic

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

Team information Ayush Pandey (12313405) - Backend Developer

Nitin kumar(1232412) - Frontend Developer

Aniket (1232412) - Algorithm Specialist
