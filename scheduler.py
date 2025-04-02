def fcfs_scheduling(processes):
    # Sort processes by arrival time (First Come First Serve Scheduling)
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    gantt = []
    current_time = 0

    for i in range(n):
        # If CPU is idle, insert an idle time slot in Gantt chart
        if processes[i]['arrival_time'] > current_time:
            gantt.append({'process': 'Idle', 'start': current_time, 'end': processes[i]['arrival_time']})
            current_time = processes[i]['arrival_time']
        
        # Schedule the process
        gantt.append({
            'process': processes[i]['id'],
            'start': current_time,
            'end': current_time + processes[i]['burst_time']
        })
        
        # Calculate completion, turnaround, and waiting times
        completion_time[i] = current_time + processes[i]['burst_time']
        turnaround_time[i] = completion_time[i] - processes[i]['arrival_time']
        waiting_time[i] = turnaround_time[i] - processes[i]['burst_time']
        current_time = completion_time[i]
    
    return {
        'algorithm': 'FCFS',
        'gantt_chart': gantt,
        'processes': processes,
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time,
        'completion_times': completion_time,
        'avg_waiting': sum(waiting_time)/n,
        'avg_turnaround': sum(turnaround_time)/n
    }


def sjf_scheduling(processes, preemptive=False):
    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    remaining_time = [p['burst_time'] for p in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    gantt = []
    current_time = 0
    completed = 0
    last_process = None

    while completed != n:
        ready = []
        # Select processes that have arrived and are not yet completed
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and remaining_time[i] > 0:
                ready.append((i, remaining_time[i]))
        
        # If no process is ready, CPU stays idle
        if not ready:
            next_arrival = min(p['arrival_time'] for p in processes if remaining_time[processes.index(p)] > 0)
            gantt.append({'process': 'Idle', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            continue
        
        # Sort processes by shortest remaining time (for preemptive) or burst time (for non-preemptive)
        ready.sort(key=lambda x: x[1])
        current_idx = ready[0][0]

        if preemptive:
            # Preemptive SJF (Shortest Remaining Time First)
            exec_time = 1
            if last_process != current_idx:
                gantt.append({'process': processes[current_idx]['id'], 'start': current_time, 'end': current_time + exec_time})
            else:
                if gantt: gantt[-1]['end'] += exec_time
            
            remaining_time[current_idx] -= exec_time
            current_time += exec_time
            last_process = current_idx

            # If process completes execution
            if remaining_time[current_idx] == 0:
                completed += 1
                completion_time[current_idx] = current_time
                turnaround_time[current_idx] = current_time - processes[current_idx]['arrival_time']
                waiting_time[current_idx] = turnaround_time[current_idx] - processes[current_idx]['burst_time']
        else:
            # Non-preemptive SJF
            start = current_time
            end = start + remaining_time[current_idx]
            gantt.append({'process': processes[current_idx]['id'], 'start': start, 'end': end})
            remaining_time[current_idx] = 0
            current_time = end
            completed += 1
            completion_time[current_idx] = end
            turnaround_time[current_idx] = end - processes[current_idx]['arrival_time']
            waiting_time[current_idx] = turnaround_time[current_idx] - processes[current_idx]['burst_time']
    
    return {
        'algorithm': 'SJF (' + ('Preemptive' if preemptive else 'Non-Preemptive') + ')',
        'gantt_chart': gantt,
        'processes': processes,
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time,
        'completion_times': completion_time,
        'avg_waiting': sum(waiting_time)/n,
        'avg_turnaround': sum(turnaround_time)/n
    }
