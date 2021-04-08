# PA-5 Necaise, Scarpuzzi, Williams

import time
tasks = [(0, 0, 0)]


# Recursive value max
def re_max(task):
    global tasks
    path = [[0]]
    if task == 0:
        return 0, [0]
    else:
        pre_value, pre_path = re_max(get_prev(task))
        current_value = tasks[task][2] + pre_value
        last_value, last_path = re_max(task - 1)
        if current_value >= last_value:
            new_path = pre_path[-1:]
            new_path.append(task)
            pre_path.append(new_path)
            path = pre_path.copy()
            value = current_value
        else:
            path = last_path.copy()
            value = last_value

    return value, path


# Non-recursive value max
def nr_max():
    global tasks
    # Hold values and path as lists
    values = [0]
    path = [[0]]

    # Iterate until list is complete
    for i in range(1, len(tasks)):
        prev_task = get_prev(i)
        current_value = tasks[i][2] + values[prev_task]
        prev_value = values[i - 1]
        if current_value >= prev_value:
            new_path = path[prev_task].copy()
            new_path.append(i)
            path.append(new_path)
            values.append(current_value)
        else:
            path.append(path[i - 1])
            values.append(prev_value)
    # return last element in values and path
    return values[-1:][0], path[-1:][0][1:]


# Brute force value max
def bf_max(task):
    global tasks
    return


# Maximize tasks completed instead of value
def task_max(task):
    global tasks
    return


# Get most recent ending task
def get_prev(task):
    global tasks
    i = task - 1
    while tasks[i][0] > tasks[task][1]:
        i -= 1
    return i


# Display output
def disp_tasks():
    print("\n\n")
    for i in range(1, len(tasks)):
        start = tasks[i][1]
        stop = tasks[i][0]
        value = tasks[i][2]
        print(f"{i}  |", "    " * (start), "****" * (stop - start),f"\t<--- {value}", sep='')

    print("---| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25|\n")

    start_t = time.perf_counter_ns()
    re_max(len(tasks) - 1)
    stop_t = time.perf_counter_ns()
    print(f"The time for the recursive DP algorithm is: {stop_t - start_t}ns.")

    start_t = time.perf_counter_ns()
    max, steps = nr_max()
    stop_t = time.perf_counter_ns()
    print(f"The time for the non-recursive DP algorithm is: {stop_t - start_t}ns.")

    for step in steps:
        print(f"{step}-> ", end='')
    print(f", with a total earnings of {max}.")



def main():
    print("****************************************************************")
    print("* PA-5 Necaise, Scarpuzzi, Williams                            *")
    print("****************************************************************")
    job_count = int(input("\nNumber of jobs to enter: "))

    for i in range(0, job_count):
        start = int(input("\nStarting time: "))
        stop = int(input("Stoping time: "))
        value = int(input("Value: "))

        tasks.append((stop, start, value))

    tasks.sort()
    disp_tasks()


if __name__ == "__main__":
    main()
