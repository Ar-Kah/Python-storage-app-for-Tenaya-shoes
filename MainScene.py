import tkinter as tk
from pandastable import Table
import pandas as pd
import json

"""
Author: Aaro Karhu, aaro.karhu19@gmail.com
This is a project made for Tenaya Finland for
storage and invoice management started in 10.11.2024
this is version 1.0
"""

class PandasApp():
    def __init__(self, master) -> None:
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)  # Allow the frame to expand and fill the window
        self.frame.pack_propagate(False)  # Prevent frame from shrinking to fit table

        data = read_json()
        df = pd.DataFrame(data)

        # Create the table
        self.table = Table(self.frame, dataframe=df, showstatusbar=True, showtoolbar=True)
        self.table.rowheight = 30  # Set row height
        # TODO: make the column size smaller

        # Adjust the table to the current window size
        self.table.show()
        self.update_table_size()

        # Bind the resize event of the root window to update the table size
        master.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Adjusts the size of the table based on the window size."""
        self.update_table_size()

    def update_table_size(self):
        # Set the table size to match the frame size
        self.table.width = self.frame.winfo_width()
        self.table.height = self.frame.winfo_height()
        self.table.redraw()  # Redraw the table to apply the new size

def read_json():
    with open('Jsonfiles/varasto.json', 'r') as storage:
        data = json.load(storage)
        return data

root = tk.Tk()
root.geometry("1500x1000")
app = PandasApp(root)
root.mainloop()
