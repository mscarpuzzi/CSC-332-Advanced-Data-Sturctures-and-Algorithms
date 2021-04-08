# PA-8
# Necaise, Scarpuzzi, Williams
import tkinter as tk
from tkinter import scrolledtext

node_list = {}  # Dictionary of nodes
time = 0


class Application(tk.Frame):
    """ GUI window and widget initialization """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.node_name_label = tk.Label(self, text="\nEnter node name:")
        self.node_name_label.pack()
        self.node_name_data = tk.Entry(self)
        self.node_name_data.pack()

        self.node_adjacent_label = tk.Label(self, text="\nEnter adjacent nodes (comma separated):")
        self.node_adjacent_label.pack()
        self.node_adjacent_data = tk.Entry(self)
        self.node_adjacent_data.pack()

        self.new = tk.Button(self, text="Add Node", command=add_node)
        self.new.pack()

        self.done = tk.Button(self, text="Search", command=dfs)
        self.done.pack()

        self.output = scrolledtext.ScrolledText(self, width=80, height=30)
        self.output.pack()


class Node:
    """Node class"""

    def __init__(self, name, adjacent):
        """
        Initialize node
        argument (name) = string identifier of node
        argument (tuple) = tuple of adjacent nodes
        """
        self.name = name
        self.adjacent = adjacent
        self.color = 'w'
        self.predecessor = None
        self.first_time = None
        self.last_time = None

    def get_name(self):
        """Return node name"""
        return self.name

    def get_adjacent(self):
        """Return adjacency list"""
        return self.adjacent

    def get_color(self):
        """Return color attribute of node"""
        return self.color

    def get_predecessor(self):
        """Return predecessor node of current node"""
        return self.predecessor

    def get_first_time(self):
        """Return first_time of current node"""
        return self.first_time

    def get_last_time(self):
        """Return last_time of current node"""
        return self.last_time

    def set_color(self, color):
        """
        Set color attribute of node
        argument (string) = 'w'/'g'/'b'
        """
        self.color = color

    def set_predecessor(self, pred):
        """
        Set predecessor node of current node
        argument (node) = predecessor node
        """
        self.predecessor = pred

    def set_first_time(self, ftime):
        """
        Set first_time of current node
        argument (ftime) = first time
        """
        self.first_time = ftime

    def set_last_time(self, ltime):
        """
        Set last_time of current node
        argument (ltime) = last time
        """
        self.last_time = ltime


def print_adjacency():
    """Print adjacency list and matrix"""
    node_names = sorted(list(node_list.keys()))

    # Display adjacency list
    app.output.insert(tk.INSERT, "\nAdjacency list for graph:\n")
    for name in node_names:
        adjacent_list = node_list[name].get_adjacent()
        app.output.insert(tk.INSERT, f"{name}: ")

        for node_number in range(len(adjacent_list)):
            if node_number == 0:
                app.output.insert(tk.INSERT, f"{adjacent_list[node_number]} ")
            else:
                app.output.insert(tk.INSERT, f"-> {adjacent_list[node_number]} ")
        app.output.insert(tk.INSERT, '\n')

    # Display adjacency matrix
    app.output.insert(tk.INSERT, "\nAdjacency matrix for graph:\n")

    #app.output.insert(tk.INSERT, "\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"\t{name}")
    app.output.insert(tk.INSERT, '\n')

    for col in node_names:
        app.output.insert(tk.INSERT, f"{col}")
        for adjacent in node_names:
            if adjacent in node_list[col].get_adjacent():
                app.output.insert(tk.INSERT, '\t1')
            else:
                app.output.insert(tk.INSERT, '\t-')
        app.output.insert(tk.INSERT, '\n')
    app.output.insert(tk.INSERT, '\n')


def print_table():
    """Print tracking table """
    node_names = sorted(list(node_list.keys()))

    app.output.insert(tk.INSERT, "\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"\t{name}")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Color:\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"\t{node_list[name].get_color()}")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Predecessor:\t")
    for name in node_names:
        node_pred = node_list[name].get_predecessor()
        if node_pred:
            app.output.insert(tk.INSERT, f"\t{node_pred}")
        else:
            app.output.insert(tk.INSERT, f"\t-")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "First Time:\t")
    for name in node_names:
        node_ftime = node_list[name].get_first_time()
        if node_ftime is None:
            app.output.insert(tk.INSERT, f"\t-")
        else:
            app.output.insert(tk.INSERT, f"\t{node_ftime}")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Last Time:\t")
    for name in node_names:
        node_ltime = node_list[name].get_last_time()
        if node_ltime is None:
            app.output.insert(tk.INSERT, f"\t-")
        else:
            app.output.insert(tk.INSERT, f"\t{node_ltime}")
    app.output.insert(tk.INSERT, '\n\n\n')


def dfs_visit(node):
    """
    Depth first search
    argument (string) = string identifier of node
    """
    global time

    node.set_color('g')
    node.set_first_time(time)
    time += 1

    print_table()

    for adjacent_name in node.get_adjacent():
        adjacent_node = node_list[adjacent_name]

        if adjacent_node.get_color() == 'w':
            adjacent_node.set_predecessor(node.get_name())
            dfs_visit(adjacent_node)

    node.set_color('b')
    node.set_last_time(time)
    time += 1
    print_table()


def add_node(n_list=node_list):
    """Add node to graph"""
    name = app.node_name_data.get()
    adjacent = app.node_adjacent_data.get().split(',')

    # Create new node and add to node list
    node = Node(name, adjacent)
    n_list[name] = node

    app.node_name_data.delete(0, tk.END)
    app.node_adjacent_data.delete(0, tk.END)
    app.output.insert(tk.INSERT, f"Node {name} added to graph.\n")


def dfs():
    """Process graph via Depth First Search"""
    print_adjacency()

    node_names = list(node_list.keys())
    print_table()

    for node_name in node_names:
        node = node_list[node_name]
        if node.get_color() == 'w':
            dfs_visit(node)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PA-8 Necaise, Scarpuzzi, Williams")
    app = Application(master=root)
    app.mainloop()
