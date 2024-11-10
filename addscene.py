import tkinter as tk

class AddWindow:
    def __init__(self, parent):
        self.add_window = tk.Toplevel(parent)  # Create a new top-level window
        self.add_window.title("Add Item")
        self.add_window.geometry("400x300")

        # Add content to the new window
        label = tk.Label(self.add_window, text="This is the 'Add' window.")
        label.pack(pady=20)

        # You can add more widgets here (like entry fields, labels, etc.)
        add_label = tk.Label(self.add_window, text="Enter details:")
        add_label.pack(pady=10)

        # Example of adding an entry field
        self.entry = tk.Entry(self.add_window)
        self.entry.pack(pady=10)

        # Add a button to close the 'Add' window
        close_button = tk.Button(self.add_window, text="Close", command=self.add_window.destroy)
        close_button.pack(pady=10)
