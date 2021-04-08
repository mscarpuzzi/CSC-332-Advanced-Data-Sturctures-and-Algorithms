# Group Necaise, Scarpuzzi, Williams
# PA-6

import tkinter as tk
from tkinter import scrolledtext

full_path = []
FT_ARROW = '\u2193'
FL_ARROW = '\u2192'
FD_ARROW = '\u2198'


# GUI window and widget initialization
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.seq_one_label = tk.Label(self, text="\nEnter sequence one:")
        self.seq_one_label.pack()
        self.seq_one_data = tk.Entry(self)
        self.seq_one_data.pack()

        self.seq_two_label = tk.Label(self, text="\nEnter sequence two:")
        self.seq_two_label.pack()
        self.seq_two_data = tk.Entry(self)
        self.seq_two_data.pack()

        self.match_value_label = tk.Label(self, text="\n\nMatch value:")
        self.match_value_label.pack()
        self.match_value_data = tk.Entry(self)
        self.match_value_data.pack()

        self.miss_value_label = tk.Label(self, text="\nMiss value (Negative if penalty):")
        self.miss_value_label.pack()
        self.miss_value_data = tk.Entry(self)
        self.miss_value_data.pack()

        self.gap_value_label = tk.Label(self, text="\nGap value (Negative if penalty):")
        self.gap_value_label.pack()
        self.gap_value_data = tk.Entry(self)
        self.gap_value_data.pack()

        self.submit = tk.Button(self, text="Submit", command=submit)
        self.submit.pack()

        self.output = scrolledtext.ScrolledText(self, width=80, height=30)
        self.output.pack()


# Define parent cells. Used as bitwise value.
def get_parents(top, left, diag):
    if top == left == diag:
        parents = 7
    elif top == left and top > diag:
        parents = 6
    elif top == diag and top > left:
        parents = 5
    elif top > max(left, diag):
        parents = 4
    elif left == diag:
        parents = 3
    elif left > diag:
        parents = 2
    else:
        parents = 1

    return parents


# Find path back to origin and insert arrows
def backtrack(table, full_table, x, y, path, seq_one, seq_two):
    parents = table[y][x][1]
    if parents & 4:  # Top is possible path
        if y > 0:
            full_table[y * 2][(x * 2) + 1] = f'  {FT_ARROW}'
        new_path = path.copy()
        new_path.insert(0, (' ', seq_two[y - 1]))
        backtrack(table, full_table, x, y - 1, new_path, seq_one, seq_two)
    if parents & 2:  # Left is possible path
        if x > 0:
            full_table[(y * 2) + 1][x * 2] = f'{FL_ARROW}'
        new_path = path.copy()
        new_path.insert(0, (seq_one[x - 1], ' '))
        backtrack(table, full_table, x - 1, y, new_path, seq_one, seq_two)
    if parents & 1:  # Diagonal is possible path
        if x > 0 and y > 0:
            full_table[y * 2][x * 2] = f'{FD_ARROW}'
        new_path = path.copy()
        new_path.insert(0, (seq_one[x - 1], seq_two[y - 1]))
        backtrack(table, full_table, x - 1, y - 1, new_path, seq_one, seq_two)
    if not parents:  # No parents means origin
        full_path.append(path)


# Print table with pathing arrows
def print_table(table):
    for row in table:
        line = ''
        for cell in row:
            line += cell
        line += '\n'
        app.output.insert(tk.INSERT, line)
    app.output.insert(tk.INSERT, '\n\n')


# Print out sequence groupings
def print_groupings(paths):
    s1_line = ''
    s2_line = ''
    for x, y in paths:
        s1_line += x
        s2_line += y

    s1_line += '\n'
    s2_line += '\n\n'

    app.output.insert(tk.INSERT, s1_line)
    app.output.insert(tk.INSERT, s2_line)


# Build the path table
def build_temp_table(seq_one, seq_two, match, miss, gap):
    # Table size
    w = len(seq_one) + 1
    h = len(seq_two) + 1

    # Prep top row and left column
    table = [[None] * w for i in range(h)]
    table[0][0] = (0, 0)
    for i in range(1, w):
        table[0][i] = (table[0][i - 1][0] + gap, 2)
    for i in range(1, h):
        table[i][0] = (table[i - 1][0][0] + gap, 4)

    # Build table
    for y in range(1, h):
        for x in range(1, w):
            from_top = table[y - 1][x][0] + gap
            from_left = table[y][x - 1][0] + gap
            if seq_one[x - 1] == seq_two[y - 1]:
                from_diag = table[y - 1][x - 1][0] + match
            else:
                from_diag = table[y - 1][x - 1][0] + miss

            parents = get_parents(from_top, from_left, from_diag)

            if parents in (4, 5, 6, 7):
                table[y][x] = (from_top, parents)
            elif parents in (2, 3):
                table[y][x] = (from_left, parents)
            else:
                table[y][x] = (from_diag, parents)

    return table


# Build table with pathing arrows
def build_full_table(table, seq_one, seq_two):
    w = (len(seq_one) + 1)
    h = (len(seq_two) + 1) * 2

    full_table = [[] for i in range(h)]

    full_table[0] = [' ', '   ']
    for x in seq_one:
        full_table[0].append(' ')
        full_table[0].append(f'  {x}')

    for y in range(1, h):
        if y % 2:
            for x in range(w):
                if x == 0:
                    if y == 1:
                        full_table[y].append(' ')
                        full_table[y].append('%3d' % table[y // 2][x][0])
                    else:
                        full_table[y].append(f'{seq_two[(y // 2) - 1]}')
                        full_table[y].append('%3d' % table[y // 2][x][0])
                else:
                    full_table[y].append(' ')
                    full_table[y].append('%3d' % table[y // 2][x][0])
        else:
            for x in range(w):
                full_table[y].append(' ')
                full_table[y].append('   ')

    return full_table


# Begin processing input
def submit():
    # Reset globals and output
    global full_path
    full_path = []
    path = []
    app.output.delete(1.0, tk.END)

    # Get sequence and split into char list
    seq_one = [char for char in app.seq_one_data.get()]
    seq_two = [char for char in app.seq_two_data.get()]

    # Get values and penalties
    match = int(app.match_value_data.get())
    miss = int(app.miss_value_data.get())
    gap = int(app.gap_value_data.get())

    x = len(seq_one)
    y = len(seq_two)

    table = build_temp_table(seq_one, seq_two, match, miss, gap)
    full_table = build_full_table(table, seq_one, seq_two)
    backtrack(table, full_table, x, y, path, seq_one, seq_two)

    print_table(full_table)

    max_score = table[y][x][0]
    
    app.output.insert(tk.INSERT, f"Max sequence score: {max_score}\n\n")

    if len(full_path) == 1:
        app.output.insert(tk.INSERT, "Sequence grouping found:\n")
        print_groupings(full_path[0])
    else:
        for i in range(len(full_path)):
            app.output.insert(tk.INSERT, f"Sequence grouping {i + 1}:\n")
            print_groupings(full_path[i])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PA-6 Necaise, Scarpuzzi, Williams")
    app = Application(master=root)
    app.mainloop()
