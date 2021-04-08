import tkinter as tk
from tkinter import scrolledtext
import queue

node_list = {}  # Dictionary of nodes


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

        self.source_node_label = tk.Label(self, text="\nSource node:")
        self.source_node_label.pack()
        self.source_node_data = tk.Entry(self)
        self.source_node_data.pack()

        self.done = tk.Button(self, text="Search", command=submit)
        self.done.pack()

        self.output = scrolledtext.ScrolledText(self, width=80, height=30)
        self.output.pack()


class Node:
    """Node class"""

    def __init__(self, name, adjacent):
        """
        Initialize node
        argument (tuple) = tuple of adjacent nodes
        """
        self.name = name
        self.adjacent = adjacent
        self.color = 'w'
        self.predecessor = None
        self.distance = -1

    def get_name(self):
        """Return node name"""
        return self.name

    def get_adjacent(self):
        """Return adjacency list"""
        return self.adjacent

    def set_color(self, color):
        """
        Set color attribute of node
        argument (string) = 'w'/'g'/'b'
        """
        self.color = color

    def get_color(self):
        """Return color attribute of node"""
        return self.color

    def set_predecessor(self, pred):
        """
        Set predecessor node or current node
        argument (node) = predecessor node
        """
        self.predecessor = pred

    def get_predecessor(self):
        """Return predecessor node of current node"""
        return self.predecessor

    def set_distance(self, dist):
        """
        Set distance to starting node
        argument (int) = distance from starting node
        """
        self.distance = dist

    def get_distance(self):
        """Return distance to starting node"""
        return self.distance


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

    # Display adjacency list
    app.output.insert(tk.INSERT, "\nAdjacency matrix for graph:\n")

    app.output.insert(tk.INSERT, "\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"{name}\t")
    app.output.insert(tk.INSERT, '\n')

    for col in node_names:
        app.output.insert(tk.INSERT, f"{col}\t")
        for adjacent in node_names:
            if adjacent in node_list[col].get_adjacent():
                app.output.insert(tk.INSERT, '1\t')
            else:
                app.output.insert(tk.INSERT, '-\t')
        app.output.insert(tk.INSERT, '\n')


def print_table():
    """Print tracking table """
    node_names = sorted(list(node_list.keys()))

    app.output.insert(tk.INSERT, "\t\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"{name}\t")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Color:\t\t")
    for name in node_names:
        app.output.insert(tk.INSERT, f"{node_list[name].get_color()}\t")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Distance:\t\t")
    for name in node_names:
        node_dist = node_list[name].get_distance()
        if node_dist == -1:
            app.output.insert(tk.INSERT, "Inf\t")
        else:
            app.output.insert(tk.INSERT, f"{node_dist}\t")
    app.output.insert(tk.INSERT, '\n')

    app.output.insert(tk.INSERT, "Predecessor:\t\t")
    for name in node_names:
        node_pred = node_list[name].get_predecessor()
        if node_pred == None:
            app.output.insert(tk.INSERT, f"-\t")
        else:
            app.output.insert(tk.INSERT, f"{node_pred}\t")
    app.output.insert(tk.INSERT, '\n\n')


def bfs(source_node):
    """
    Breath first search
    argument (string) = string identifier of node
    """
    # Print initial tracking table
    app.output.insert(tk.INSERT, "\nTracking tables:\n")
    print_table()

    node_queue = queue.Queue()
    node = node_list[source_node]
    node.set_color('g')
    node.set_distance(0)
    node_queue.put(source_node)

    # Print tracking table after source insert
    print_table()

    # Loop through queue
    while not node_queue.empty():
        node = node_list[node_queue.get()]

        # Check adjacent nodes
        for adjacent_name in node.get_adjacent():
            adjacent_node = node_list[adjacent_name]

            # If adjacent node has not been visited
            if adjacent_node.get_color() == 'w':
                adjacent_node.set_color('g')
                adjacent_node.set_distance(node.get_distance() + 1)
                adjacent_node.set_predecessor(node.get_name())
                node_queue.put(adjacent_name)

            # Print tracking table after adjacency inserts
            print_table()

        node.set_color('b')

    # Print final tracking table
    print_table()


def add_node(node_list=node_list):
    """Add node to graph"""
    name = app.node_name_data.get()
    adjacent = app.node_adjacent_data.get().split(',')

    # Create new node and add to node list
    node = Node(name, adjacent)
    node_list[name] = node

    app.node_name_data.delete(0, tk.END)
    app.node_adjacent_data.delete(0, tk.END)
    app.output.insert(tk.INSERT, f"Node {name} added to graph.\n")


def submit():
    """Process graph with given values and start node"""
    start_node = app.source_node_data.get()
    print_adjacency()
    bfs(start_node)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PA-7 Necaise, Scarpuzzi, Williams")
    app = Application(master=root)
    app.mainloop()
