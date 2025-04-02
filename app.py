from flask import Flask, render_template, request, jsonify
from scheduler import (fcfs_scheduling, sjf_scheduling, 
                      round_robin_scheduling, priority_scheduling)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    
    algorithm = data['algorithm']
    processes = data['processes']
    time_quantum = data.get('time_quantum', 2)
    
    results = {}
    
    if algorithm == 'fcfs':
        results = fcfs_scheduling(processes)
    elif algorithm == 'sjf':
        results = sjf_scheduling(processes, preemptive=False)
    elif algorithm == 'srtf':
        results = sjf_scheduling(processes, preemptive=True)
    elif algorithm == 'rr':
        results = round_robin_scheduling(processes, time_quantum)
    elif algorithm == 'priority':
        results = priority_scheduling(processes, preemptive=False)
    elif algorithm == 'priority_p':
        results = priority_scheduling(processes, preemptive=True)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
