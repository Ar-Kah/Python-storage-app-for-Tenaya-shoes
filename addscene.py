import tkinter as tk
import json


def read_barcode_from_json(barcode):
    try:
        with open('Jsonfiles/barcodes.json', 'r') as file:
            data = json.load(file)
            # Try to find the barcode
            for shoe in data:
                for size in data[shoe]:
                    if data[shoe][size] == barcode:
                        return True, shoe, size

        return False, "", ""
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("There was an error with the json syntax")


class AddWindow:
    def __init__(self, parent):
        self.add_window = tk.Toplevel(parent)  # Create a new window
        self.add_window.title("Add Item")
        self.add_window.geometry("400x300")

        # Add content to the new window
        label = tk.Label(self.add_window, text="Start adding shoes by scanning barcodes")
        label.pack(pady=20)

        # Create the Entry widget
        self.entry = tk.Entry(self.add_window)
        self.entry.pack(pady=10)

        # Bind the Entry widget to capture barcode input
        self.entry.bind("<KeyRelease>", self.read_entry)

        # List to hold the scanned items
        self.items = []
        self.list_items = tk.Variable(value=self.items)

        # Create the Listbox and display the items
        self.listbox = tk.Listbox(self.add_window, listvariable=self.list_items)
        self.listbox.pack(pady=10)

        # Add a button to close the 'Add' window
        close_button = tk.Button(self.add_window, text="Close", command=self.add_window.destroy)
        close_button.pack(pady=10)

        # Ensure the focus is set to the entry field
        self.entry.focus_set()

    def read_entry(self, event):
        """
        This method is called whenever a key is released in the Entry widget.
        It checks if the barcode (entry text) has reached the desired length.
        """
        barcode = self.entry.get()

        # Check if the length of the barcode is 13 (for example)
        if len(barcode) == 13:
            self.entry.delete(0, tk.END)  # Clear the entry field after reading the barcode
            if_found, shoe_name, size = read_barcode_from_json(barcode)
            if if_found:
                # Add shoe name and size to the list
                self.items.append(f"{shoe_name} - {size}")
                # Update the list variable to refresh the Listbox
                self.list_items.set(self.items)

        elif len(barcode) > 13:
            self.entry.delete(0, tk.END)  # Clear the entry if barcode is too long
