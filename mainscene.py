import tkinter as tk
from pandastable import Table
import pandas as pd
import json
from addscene import AddWindow

"""
Author: Aaro Karhu, aaro.karhu19@gmail.com
This is a project made for Tenaya Finland for
storage and invoice management started in 10.11.2024
this is version 1.0
"""

class PandasApp():
    def __init__(self, master) -> None:
        self.frame = tk.Frame(master)
        self.frame.pack(fill='x', side='top')

        data = read_json()
        df = pd.DataFrame(data)

        # Create the table
        self.table = Table(self.frame, dataframe=df, showstatusbar=True, showtoolbar=True)
        self.table.rowheight = 30


        # Adjust the table to the current window size
        self.table.show()

    def open_add_window(self):
        """Open the 'Add' window."""
        AddWindow(self.frame)  # Create and show the AddWindow

def read_json():
    with open('Jsonfiles/varasto.json', 'r') as storage:
        data = json.load(storage)
        return data

root = tk.Tk()
root.geometry("1500x1000")
app = PandasApp(root)
root.mainloop()
