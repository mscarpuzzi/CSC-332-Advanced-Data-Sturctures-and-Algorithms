# Team Necaise-Scarpuzzi-Williams
# PA-4

import tkinter as tk
from tkinter import messagebox
import time

way_count = 1


# Recursive stair climbing
def re_stair(stair_height, steps):
    if stair_height < 0:
        return 0
    elif stair_height == 0:
        return 1
    else:
        step_count = 0
        for step in steps:
            step_count += re_stair(stair_height - step, steps)

    return step_count


# Non-Recursive stair climbing
def dp_stair(stair_height, step_sizes):
    if stair_height < 0:
        return 0
    step_values = [0] * (stair_height + 1)
    step_values[0] = 1

    # Count combinations by summing possible ways to get to each step
    for step in range(1, stair_height + 1):
        for step_size in step_sizes:
            to_check = step - step_size

            if to_check < 0:
                add_to = 0
            else:
                add_to = step_values[to_check]

            step_values[step] += add_to

    return step_values[stair_height]


# Assign input values with error checking.
def load_and_validate():
    try:
        stair_count = int(count_input.get())
    except ValueError:
        messagebox.showerror(title="Error", message="Number of steps must be an integer value.")
        return
    if stair_count < 0:
        messagebox.showerror(title="Error", message="Number of steps must be non-negative.")
        return
    temp_list = steps_input.get().split(',')
    step_list = []
    try:
        for i in temp_list:
            step_list.append(int(i))
    except ValueError:
        messagebox.showerror(title="Error", message="Step values must be comma separated integers.")
        return
    if len(step_list) < 2:
        messagebox.showerror(title="Error", message="Step values must contain at least 2 elements")
        return
    elif len(step_list) > stair_count:
        messagebox.showerror(title="Error", message="To many steps.")
        return
    for x in step_list:
        if x < 1:
            messagebox.showerror(title="Error", message="Step values must be 1 or greater")
            return
        elif x > stair_count:
            messagebox.showerror(title="Error", message=f"Step values must be less than or equal to {stair_count}")
            return

    return stair_count, step_list


# Benchmark runtime of given function (does not save output)
def benchmark(stair_height, step_sizes, function):
    start = time.perf_counter_ns()
    function(stair_height, step_sizes)
    stop = time.perf_counter_ns()

    return stop - start


# Print all valid paths. This is ugly but it works, and I'm
# tired of banging my head on the desk
def find_path(stair_height, steps, current_step=0, path=[]):
    global way_count
    new_path = path[:]
    for step in steps:
        new_step = current_step + step
        new_path.append(step)
        if new_step == stair_height:
            result_box.insert(tk.INSERT, f"Way {way_count}: {new_path}\n")
            way_count += 1
        elif new_step < stair_height:
            find_path(stair_height, steps, new_step, new_path)
        new_path = path[:]


# Compute results
def button_click():
    # Load validated input
    stair_height, step_list = load_and_validate()
    # Benchmark functions
    re_time = benchmark(stair_height, step_list, re_stair)
    dp_time = benchmark(stair_height, step_list, dp_stair)

    # Get values. Done outside benchmark so assignment does not affect benchmark times.
    number = dp_stair(stair_height, step_list)

    # Display output
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.INSERT, f"The time elapsed in the recursive  algorithm is {re_time}ns\n")
    result_box.insert(tk.INSERT, f"The time elapsed in the non-recursive algorithm is {dp_time}ns\n\n")
    result_box.insert(tk.INSERT, f"There are {number} ways:\n")
    global way_count
    way_count = 1  # reset way_count for each submission.
    find_path(stair_height, step_list)
    return 0


# Tk GUI code
top = tk.Tk()
top.title("PA-4 Necaise, Scarpuzzi, Williams")

frame = tk.Frame(top, width=600, height=400)
frame.pack_propagate(0)
frame.pack(side=tk.TOP)

count_label = tk.Label(frame, text="Number of steps in stairs:")
count_label.pack()
count_input = tk.Entry(frame)
count_input.pack()

steps_label = tk.Label(frame, text="\n\nValue of possible Steps (comma separated):")
steps_label.pack()
steps_input = tk.Entry(frame)
steps_input.pack()

result_label = tk.Label(frame, text="\n\nResults:")
result_label.pack()
result_frame = tk.Frame(frame)
result_frame.pack()
scroll = tk.Scrollbar(result_frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_box = tk.Text(result_frame, height=10, width=70, yscrollcommand=scroll.set)
scroll.config(command=result_box.yview)
result_box.pack()

disp_button = tk.Button(frame, text="Submit", command=button_click)
disp_button.pack(side=tk.BOTTOM)

top.mainloop()
