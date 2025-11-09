# CPU Scheduling Algorithms with Gantt Chart
# FCFS, SJF (NP), SJF (P), Priority (NP), Priority (P), Round Robin

def print_gantt_chart(order, times):
    print("\nGantt Chart:")
    print("-" * (len(order) * 6))
    for p in order:
        print(f"| {p:^3} ", end="")
    print("|")
    print("-" * (len(order) * 6))
    for t in times:
        print(f"{t:<6}", end="")
    print("\n")

def fcfs(processes):
    print("\n--- FCFS Scheduling ---")
    processes.sort(key=lambda x: x[1])
    t = 0
    order, times = [], [0]
    for p in processes:
        t = max(t, p[1]) + p[2]
        order.append(p[0])
        times.append(t)
    print_gantt_chart(order, times)

def sjf_non_preemptive(processes):
    print("\n--- SJF (Non-Preemptive) ---")
    processes.sort(key=lambda x: x[1])
    n = len(processes)
    t = processes[0][1]
    completed = []
    order, times = [], [t]
    while len(completed) < n:
        ready = [p for p in processes if p[1] <= t and p not in completed]
        if ready:
            p = min(ready, key=lambda x: x[2])
            t += p[2]
            completed.append(p)
            order.append(p[0])
            times.append(t)
        else:
            t += 1
    print_gantt_chart(order, times)

def sjf_preemptive(processes):
    print("\n--- SJF (Preemptive) ---")
    n = len(processes)
    remaining = {p[0]: p[2] for p in processes}
    t = 0
    order, times = [], [0]
    completed = 0
    while completed < n:
        ready = [p for p in processes if p[1] <= t and remaining[p[0]] > 0]
        if ready:
            p = min(ready, key=lambda x: remaining[x[0]])
            remaining[p[0]] -= 1
            if not order or order[-1] != p[0]:
                order.append(p[0])
                times.append(t)
            t += 1
            if remaining[p[0]] == 0:
                completed += 1
        else:
            t += 1
    times.append(t)
    print_gantt_chart(order, times)

def priority_non_preemptive(processes):
    print("\n--- Priority (Non-Preemptive) ---")
    processes.sort(key=lambda x: x[1])
    t = 0
    completed = []
    order, times = [], [0]
    while len(completed) < len(processes):
        ready = [p for p in processes if p[1] <= t and p not in completed]
        if ready:
            p = min(ready, key=lambda x: x[3])
            t += p[2]
            completed.append(p)
            order.append(p[0])
            times.append(t)
        else:
            t += 1
    print_gantt_chart(order, times)

def priority_preemptive(processes):
    print("\n--- Priority (Preemptive) ---")
    remaining = {p[0]: p[2] for p in processes}
    t = 0
    order, times = [], [0]
    completed = 0
    while completed < len(processes):
        ready = [p for p in processes if p[1] <= t and remaining[p[0]] > 0]
        if ready:
            p = min(ready, key=lambda x: x[3])
            remaining[p[0]] -= 1
            if not order or order[-1] != p[0]:
                order.append(p[0])
                times.append(t)
            t += 1
            if remaining[p[0]] == 0:
                completed += 1
        else:
            t += 1
    times.append(t)
    print_gantt_chart(order, times)

def round_robin(processes, quantum=2):
    print("\n--- Round Robin ---")
    queue = []
    t = 0
    order, times = [], [0]
    remaining = {p[0]: p[2] for p in processes}
    processes.sort(key=lambda x: x[1])
    i = 0
    while i < len(processes) or queue:
        while i < len(processes) and processes[i][1] <= t:
            queue.append(processes[i])
            i += 1
        if queue:
            p = queue.pop(0)
            exec_time = min(quantum, remaining[p[0]])
            if not order or order[-1] != p[0]:
                order.append(p[0])
                times.append(t)
            t += exec_time
            remaining[p[0]] -= exec_time
            if remaining[p[0]] > 0:
                while i < len(processes) and processes[i][1] <= t:
                    queue.append(processes[i])
                    i += 1
                queue.append(p)
        else:
            t += 1
    times.append(t)
    print_gantt_chart(order, times)

# Example Input Format: (ProcessID, ArrivalTime, BurstTime, Priority)
processes = [
    ('P1', 0, 5, 2),
    ('P2', 1, 3, 1),
    ('P3', 2, 8, 4),
    ('P4', 3, 6, 3)
]

fcfs(processes[:])
sjf_non_preemptive(processes[:])
sjf_preemptive(processes[:])
priority_non_preemptive(processes[:])
priority_preemptive(processes[:])
round_robin(processes[:], quantum=2)
