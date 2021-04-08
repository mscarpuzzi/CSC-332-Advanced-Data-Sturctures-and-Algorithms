# Team Necaise, Scarpuzzi, Williams
# PA-3

import time
import tkinter as tk


# Recursive Fibonacci
def re_fib(n):
    if 1 >= n >= 0:
        return n

    return re_fib(n - 1) + re_fib(n - 2)


# Dynamic Programming Fibonacci
def dp_fib(n):
    temp = 0
    a = 1
    b = 1

    if 1 >= n >= 0:
        return n

    for i in range(2, n):
        temp = a
        a = b
        b = a + temp

    return b


# Benchmark
def benchmark():
    fout = open("Fibonacci_Time.csv", "w")
    fout.write("n, "
               "F(n), "
               "T1: Time spent on the recursive algorithm (nanoseconds), "
               "T1: Time spent on the DP algorith (nanoseconds), "
               "Value of (2^n)/n, "
               "Value of T1/T2\n")

    sizes = [10, 12, 15, 20, 23, 25, 30]

    for x in sizes:
        # Result of re_fib() is not used but it still assigned to be consistent with timing for dp_fib()
        start = time.perf_counter_ns()
        result = re_fib(x)
        stop = time.perf_counter_ns()
        re_time = stop - start

        start = time.perf_counter_ns()
        result = dp_fib(x)
        stop = time.perf_counter_ns()
        dp_time = stop - start

        theo_ratio = "{:.0e}".format((2 ** x) / x)
        real_ratio = "{:.0e}".format(re_time / dp_time)

        fout.write(f"{x}, {result}, {re_time}, {dp_time}, {theo_ratio}, {real_ratio}\n")

    fout.close()


# Display results
def button_click():
    n = int(var_value.get())
    # Display Fibonacci number if algorithm selected, else display Error
    try:
        alg = alg_select.curselection()[0]
        if alg == 0:
            fib = re_fib(n)
        elif alg == 1:
            fib = dp_fib(n)
        else:
            fib = "An error that should never happen."
    except IndexError:
        fib = "Select Algorithm"

    val_text.delete(1.0, tk.END)
    val_text.insert(tk.INSERT, fib)


# Tk GUI setup code
top = tk.Tk()
top.title("PA-3 Necaise, Scarpuzzi, Williams")

menu_bar = tk.Menu(top)
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Generate Benchmarks", command=benchmark)
file_menu.add_command(label="Exit", command=top.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
top.config(menu=menu_bar)

frame = tk.Frame(top, width=400, height=400)
frame.pack_propagate(0)
frame.pack(side=tk.TOP)

var_label = tk.Label(frame, text="\n\nInput Number: ")
var_label.pack()
var_value = tk.Spinbox(frame, width=10, from_=0, to=10000000)
var_value.pack()

alg_label = tk.Label(frame, text="\nSelect Algorithm: ")
alg_label.pack()
alg_select = tk.Listbox(frame, height=2, selectmode=tk.SINGLE)
alg_select.insert(0, "Recursive")
alg_select.insert(1, "Dynamic")
alg_select.activate(0)
alg_select.pack()

val_label = tk.Label(frame, text="\n\n\nResult: ")
val_label.pack()
val_text = tk.Text(frame, height=1, width=20)
val_text.pack()
disp_button = tk.Button(frame, text="Generate Number", command=button_click)
disp_button.pack()

top.mainloop()
