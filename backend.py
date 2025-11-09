def print_gantt_chart(order, times):
    print("\nGantt Chart:")
    print(" ", end="")
    for p in order:
        print(f"|  P{p}  ", end="")
    print("|")

    print("0", end="")
    for t in times:
        print(f"     {t}", end="")
    print("\n")


def fcfs(processes):
    processes.sort(key=lambda x: x[1])  # sort by arrival time
    start, finish, order = [], [], []
    time = 0
    for pid, at, bt in processes:
        if time < at:
            time = at
        start.append(time)
        time += bt
        finish.append(time)
        order.append(pid)
    print_gantt_chart(order, finish)
    print(f"Average Waiting Time: {sum(f - a - b for (_, a, b), f in zip(processes, finish)) / len(processes):.2f}")


def sjf(processes):
    processes.sort(key=lambda x: x[1])  # by arrival time
    n = len(processes)
    time, completed, order, finish = 0, [], [], []

    while len(completed) < n:
        available = [p for p in processes if p[1] <= time and p not in completed]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x[2])  # choose shortest burst
        time += p[2]
        completed.append(p)
        order.append(p[0])
        finish.append(time)

    print_gantt_chart(order, finish)


def priority_scheduling(processes):
    processes.sort(key=lambda x: x[1])
    n = len(processes)
    time, completed, order, finish = 0, [], [], []

    while len(completed) < n:
        available = [p for p in processes if p[1] <= time and p not in completed]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x[3])  # smallest priority
        time += p[2]
        completed.append(p)
        order.append(p[0])
        finish.append(time)

    print_gantt_chart(order, finish)


def round_robin(processes, quantum):
    n = len(processes)
    queue = []
    time = 0
    rem_bt = {p[0]: p[2] for p in processes}
    order, finish = [], []

    while processes or queue:
        # Add available processes to queue
        for p in processes[:]:
            if p[1] <= time:
                queue.append(p)
                processes.remove(p)

        if not queue:
            time += 1
            continue

        pid, at, bt = queue.pop(0)
        exec_time = min(quantum, rem_bt[pid])
        rem_bt[pid] -= exec_time
        time += exec_time
        order.append(pid)
        finish.append(time)

        if rem_bt[pid] > 0:
            for p in processes[:]:
                if p[1] <= time and p not in queue:
                    queue.append(p)
                    processes.remove(p)
            queue.append((pid, at, bt))

    print_gantt_chart(order, finish)


def main():
    print("CPU Scheduling Algorithms:")
    print("1. FCFS\n2. SJF\n3. Priority\n4. Round Robin")
    choice = int(input("Enter your choice: "))

    n = int(input("Enter number of processes: "))
    processes = []

    if choice == 3:
        print("Enter PID, Arrival Time, Burst Time, Priority:")
        for _ in range(n):
            pid, at, bt, pr = map(int, input().split())
            processes.append((pid, at, bt, pr))
    else:
        print("Enter PID, Arrival Time, Burst Time:")
        for _ in range(n):
            pid, at, bt = map(int, input().split())
            processes.append((pid, at, bt))

    if choice == 1:
        fcfs(processes)
    elif choice == 2:
        sjf(processes)
    elif choice == 3:
        priority_scheduling(processes)
    elif choice == 4:
        quantum = int(input("Enter time quantum: "))
        round_robin(processes, quantum)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
