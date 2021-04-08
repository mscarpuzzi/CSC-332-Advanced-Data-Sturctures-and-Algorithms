# Team Necaise, Scarpuzzi, Williams
# PA-2
import math
import random
import time
from tkinter import *


# Merge two sorted lists
def merge(left, right):
    # Initialize variables
    merged = []
    ptr_left = 0
    ptr_right = 0

    # Loop while both lists have elements
    while ptr_left < len(left) and ptr_right < len(right):
        if left[ptr_left] < right[ptr_right]:
            merged.append(left[ptr_left])
            ptr_left += 1
        else:
            merged.append(right[ptr_right])
            ptr_right += 1

    # Dump remainder of list into new list
    if ptr_left < len(left):
        merged.extend(left[ptr_left:])
    if ptr_right < len(right):
        merged.extend(right[ptr_right:])

    return merged


# Sort by divide and conquer
def merge_sort(to_sort):
    if len(to_sort) == 1:
        # A 1 element list is sorted
        return to_sort
    else:
        # Split list and recurse
        mid = len(to_sort) // 2
        left = merge_sort(to_sort[:mid])
        right = merge_sort(to_sort[mid:])

        return merge(left, right)


# On button click
def button_clicked():
    # Get selected array (First/only item of returned tuple)
    array = array_select.curselection()[0]

    # Clear output text boxes
    left_array.delete(1.0, END)
    right_array.delete(1.0, END)

    # Fill output text boxes
    for x in range(0, len(unsorted_array[array])):
        left_array.insert(INSERT, f"{unsorted_array[array][x]}\n")
        right_array.insert(INSERT, f"{sorted_array[array][x]}\n")


# Seed random, set constants and initialize array
random.seed(42)
array_count = 9
size_base = 1000
max_size = 10000000
unsorted_array = [[] for rows in range(array_count)]
sorted_array = [[] for rows in range(array_count)]

# Open and prep output
fout = open("Mergesort_Time.csv", 'w')
fout.write("Input Size n for Array_i, Value of n*Log(n), Time Spent (Nanoseconds), Value of [n*log(n)]/time\n")

# Populate arrays
for i in range(array_count):
    # Arrays are internally numbered 0-8, add 1 to multiplier to fix
    for j in range(0, size_base * (i + 1)):
        unsorted_array[i].append(random.randrange(max_size))

# Time and output
for i in range(array_count):
    # Time execution
    start = time.perf_counter_ns()
    sorted_array[i] = merge_sort(unsorted_array[i])
    stop = time.perf_counter_ns()

    # Statistics
    n = len(unsorted_array[i])
    nlogn = n * math.log(n)
    elapsed = stop - start
    time_divide = "{:.0e}".format(nlogn / elapsed)

    # Write to file
    fout.write(f"{n}, {nlogn}, {elapsed}, {time_divide}\n")

fout.close()

# Build GUI using Tk
root = Tk()
root.title("PA-2 - Team Necaise, Scarpuzzi, Williams")

# Frame containing array selection and button
left_frame = Frame(root)
left_frame.pack(side=LEFT)

# Array select
array_select = Listbox(left_frame, height=9, selectmode="SINGLE")
for i in range(array_count):
    array_select.insert(i, f"{i + 1}")
array_select.pack()

# Button
select_button = Button(left_frame, pady=5, text="Select Array", command=button_clicked)
select_button.pack()

# Frame containing array displays
right_frame = Frame(root)
right_frame.pack(side=RIGHT)

# Unsorted array display
left_label = LabelFrame(right_frame, text="Unsorted Array", width=35)
left_label.pack(side=LEFT)
left_scroll = Scrollbar(left_label)
left_scroll.pack(side=RIGHT, fill=Y)
left_array = Text(left_label, pady=5, padx=5, width=30, height=30, yscrollcommand=left_scroll.set)
left_array.pack(side=LEFT, fill=BOTH)
left_scroll.config(command=left_array.yview)
left_array.insert(INSERT, "Unsorted Array Will Appear\nHere Upon Selection")

# Sorted array display
right_label = LabelFrame(right_frame, text="Sorted Array", width=35)
right_label.pack(side=RIGHT)
right_scroll = Scrollbar(right_label)
right_scroll.pack(side=RIGHT, fill=Y)
right_array = Text(right_label, pady=5, padx=5, width=30, height=30, yscrollcommand=right_scroll.set)
right_array.pack(side=RIGHT, fill=BOTH)
right_scroll.config(command=right_array.yview)
right_array.insert(INSERT, "Sorted Array Will Appear\nHere Upon Selection")

root.mainloop()