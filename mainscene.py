import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd
import json
from addscene import AddWindow
from sendwindow import SendWindow
import invoice_generator

"""
Author: Aaro Karhu, aaro.karhu19@gmail.com
This is a project made for Tenaya Finland for
storage and invoice management started in 10.11.2024
this is version 1.0
"""


class PandasApp:
    """
    The main window where the storage is displayed with pandastable
    The table is updated when shoes are added to the varasto.json file
    in the add window

    TODO: make a send button and a similar window for that also
    TODO: make an automatic invoice maker in the send window
    """

    def __init__(self, master) -> None:
        # Set up main frame
        self.master = master
        self.setup_main_frame()

        # Set up inner frame and table
        self.setup_inner_frame()
        self.setup_table()

        # Set up button frame and buttons
        self.setup_button_frame()
        self.setup_buttons()

    def setup_main_frame(self):
        """Sets up the main frame with padding for rounded corner effect."""
        self.frame = tk.Frame(self.master, padx=20, pady=20, bg="light gray")  # Outer frame with padding
        self.frame.pack(fill="both", expand=True)
        self.frame.pack_propagate(False)

    def setup_inner_frame(self):
        """Sets up the inner frame to contain the table."""
        # Inner frame to mimic rounded corners around the table
        self.inner_frame = tk.Frame(self.frame, bg="white", relief="solid", bd=2)
        self.inner_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))  # Adding top and side padding

    def setup_table(self):
        """Sets up the table and loads initial data."""
        # Load initial data into DataFrame
        data = read_json()
        df = pd.DataFrame(data)

        # Create the table inside the inner frame
        self.table = Table(self.inner_frame, dataframe=df, showstatusbar=True, showtoolbar=False)
        self.table.contractColumns(30)
        self.table.rowheight = 30
        self.table.show()

    def setup_button_frame(self):
        """Sets up the frame that contains the buttons."""
        # Button frame positioned at the bottom of the outer frame
        self.button_frame = tk.Frame(self.frame, bg="light gray")
        self.button_frame.pack(side="bottom", pady=10)  # Position at the bottom with padding

    def setup_buttons(self):
        """Sets up the 'Add' and 'Send' buttons."""
        # Add "Add" button inside the button frame
        self.add_button = tk.Button(self.button_frame, text="Add", command=self.open_add_window, width=30)
        self.add_button.grid(row=0, column=0, padx=30)  # Position on the left with padding

        # Add "Send" button next to the "Add" button
        self.send_button = tk.Button(self.button_frame, text="Send", command=self.send_action, width=30)
        self.send_button.grid(row=0, column=2, padx=30)  # Position on the right with padding

        self.save_changes_button = tk.Button(self.button_frame, text="Save changes", command=self.save_table_to_json)
        self.save_changes_button.grid(row=0, column=1, padx=30) # position in the center with padding

    def save_table_to_json(self):
        """Saves the current state of the table back to the JSON file."""
        # Get the DataFrame from the table model
        updated_df = self.table.model.df

        # Ensure all numeric columns are converted to integers
        for column in updated_df.columns:
            if updated_df[column].dtype == 'O':  # Check if the column is of object type (string)
                try:
                    updated_df[column] = pd.to_numeric(updated_df[column], errors='ignore')  # Try converting
                except ValueError:
                    pass  # Skip non-numeric columns
            else:
                updated_df[column] = updated_df[column].astype('int64', errors='ignore')  # Ensure integer type

        # Convert the DataFrame to a JSON-compatible dictionary
        json_data = updated_df.to_dict(orient="records")

        # Write to the JSON file
        with open('Jsonfiles/varasto.json', 'w') as storage:
            json.dump(json_data, storage, indent=4)

        print("Table data saved to varasto.json")

    def open_add_window(self):
        """Open the 'Add' window."""
        AddWindow(self.frame, self.refresh_table)  # Create and show the AddWindow

    def refresh_table(self):
        """Reloads the data from varasto.json and refreshes the table display."""
        self.data = read_json()  # Reload the new JSON data
        self.df = pd.DataFrame(self.data)  # Update the DataFrame
        self.table.updateModel(TableModel(self.df))  # Update the table's model
        self.table.redraw()  # Redraw the table with updated data

    def send_action(self):
        """Open the 'send' window"""
        SendWindow(self.frame, self.refresh_table) # create and show this window

def read_json():
    """Reads data from the JSON file and ensures data types."""
    with open('Jsonfiles/varasto.json', 'r') as storage:
        data = json.load(storage)
    return data


def main():
    """Sets up the main application window and runs the app."""
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Tenaya Storage Management")
    app = PandasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
