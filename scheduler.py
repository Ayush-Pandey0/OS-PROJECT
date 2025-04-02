def fcfs_scheduling(processes):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    gantt = []
    current_time = 0

    for i in range(n):
        if processes[i]['arrival_time'] > current_time:
            gantt.append({'process': 'Idle', 'start': current_time, 'end': processes[i]['arrival_time']})
            current_time = processes[i]['arrival_time']
        
        gantt.append({
            'process': processes[i]['id'],
            'start': current_time,
            'end': current_time + processes[i]['burst_time']
        })
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
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and remaining_time[i] > 0:
                ready.append((i, remaining_time[i]))
        
        if not ready:
            next_arrival = min(p['arrival_time'] for p in processes if remaining_time[processes.index(p)] > 0)
            gantt.append({'process': 'Idle', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            continue
        
        ready.sort(key=lambda x: x[1])
        current_idx = ready[0][0]

        if preemptive:
            # Preemptive (SRTF)
            exec_time = 1
            if last_process != current_idx:
                gantt.append({
                    'process': processes[current_idx]['id'],
                    'start': current_time,
                    'end': current_time + exec_time
                })
            else:
                if gantt: gantt[-1]['end'] += exec_time
            
            remaining_time[current_idx] -= exec_time
            current_time += exec_time
            last_process = current_idx

            if remaining_time[current_idx] == 0:
                completed += 1
                completion_time[current_idx] = current_time
                turnaround_time[current_idx] = current_time - processes[current_idx]['arrival_time']
                waiting_time[current_idx] = turnaround_time[current_idx] - processes[current_idx]['burst_time']
        else:
            # Non-preemptive SJF
            start = current_time
            end = start + remaining_time[current_idx]
            gantt.append({
                'process': processes[current_idx]['id'],
                'start': start,
                'end': end
            })
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

def round_robin_scheduling(processes, time_quantum):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    remaining_time = [p['burst_time'] for p in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    gantt = []
    current_time = 0
    queue = []
    completed = 0

    # Initialize queue with processes that have arrived at time 0
    for i in range(n):
        if processes[i]['arrival_time'] <= current_time:
            queue.append(i)

    while completed < n:
        if not queue:
            next_arrival = min(p['arrival_time'] for p in processes if remaining_time[processes.index(p)] > 0)
            gantt.append({'process': 'Idle', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            for i in range(n):
                if processes[i]['arrival_time'] <= current_time and remaining_time[i] > 0 and i not in queue:
                    queue.append(i)
            continue

        current_process = queue.pop(0)
        start_time = current_time
        exec_time = min(time_quantum, remaining_time[current_process])
        end_time = start_time + exec_time
        gantt.append({
            'process': processes[current_process]['id'],
            'start': start_time,
            'end': end_time
        })

        remaining_time[current_process] -= exec_time
        current_time = end_time

        # Add newly arrived processes
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and remaining_time[i] > 0 and i not in queue and i != current_process:
                queue.append(i)

        if remaining_time[current_process] > 0:
            queue.append(current_process)
        else:
            completed += 1
            completion_time[current_process] = end_time
            turnaround_time[current_process] = end_time - processes[current_process]['arrival_time']
            waiting_time[current_process] = turnaround_time[current_process] - processes[current_process]['burst_time']
    
    return {
        'algorithm': f'Round Robin (Quantum={time_quantum})',
        'gantt_chart': gantt,
        'processes': processes,
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time,
        'completion_times': completion_time,
        'avg_waiting': sum(waiting_time)/n,
        'avg_turnaround': sum(turnaround_time)/n
    }

def priority_scheduling(processes, preemptive=False):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    remaining_time = [p['burst_time'] for p in processes]
    remaining_priority = [p['priority'] for p in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    gantt = []
    current_time = 0
    completed = 0
    last_process = None

    while completed != n:
        ready = []
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and remaining_time[i] > 0:
                ready.append((i, remaining_priority[i]))
        
        if not ready:
            next_arrival = min(p['arrival_time'] for p in processes if remaining_time[processes.index(p)] > 0)
            gantt.append({'process': 'Idle', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            continue

        ready.sort(key=lambda x: x[1])
        current_idx = ready[0][0]

        if preemptive:
            # Preemptive Priority
            exec_time = 1
            if last_process != current_idx:
                gantt.append({
                    'process': processes[current_idx]['id'],
                    'start': current_time,
                    'end': current_time + exec_time
                })
            else:
                if gantt: gantt[-1]['end'] += exec_time
            
            remaining_time[current_idx] -= exec_time
            current_time += exec_time
            last_process = current_idx

            if remaining_time[current_idx] == 0:
                completed += 1
                completion_time[current_idx] = current_time
                turnaround_time[current_idx] = current_time - processes[current_idx]['arrival_time']
                waiting_time[current_idx] = turnaround_time[current_idx] - processes[current_idx]['burst_time']
        else:
            # Non-preemptive Priority
            start = current_time
            end = start + remaining_time[current_idx]
            gantt.append({
                'process': processes[current_idx]['id'],
                'start': start,
                'end': end
            })
            remaining_time[current_idx] = 0
            current_time = end
            completed += 1
            completion_time[current_idx] = end
            turnaround_time[current_idx] = end - processes[current_idx]['arrival_time']
            waiting_time[current_idx] = turnaround_time[current_idx] - processes[current_idx]['burst_time']
    
    return {
        'algorithm': 'Priority (' + ('Preemptive' if preemptive else 'Non-Preemptive') + ')',
        'gantt_chart': gantt,
        'processes': processes,
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time,
        'completion_times': completion_time,
        'avg_waiting': sum(waiting_time)/n,
        'avg_turnaround': sum(turnaround_time)/n
    }
