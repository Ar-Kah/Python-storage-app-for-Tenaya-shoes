import tkinter as tk
import json

"""
TODO: make the logic for invoice making and make if statements so that the storage cant go to minus.
Also dont update the json file untill the invoice is made
"""


def read_barcode_from_json(barcode):
    """
    barcode reader
    JSON format:
    {
        "shoe_name":
        {
            "size": "barcode.."
            ...
            ...
        }
    }
    """
    try:
        with open('Jsonfiles/barcodes.json', 'r') as file:
            data = json.load(file)
            # Try to find the barcode
            for shoe in data:
                for size in data[shoe]:
                    if data[shoe][size] == barcode:
                        return True, shoe, size
        # False for if logic (others are empty strings)
        return False, "", ""
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("There was an error with the json syntax")
    return False, "", ""


class SendWindow:
    def __init__(self, parent, refresh_callback):
        self.send_window = tk.Toplevel(parent)  # create new window
        self.send_window.title("Send Items")
        self.send_window.geometry("400x400")

        # Store the callback function
        self.refresh_callback = refresh_callback

        # Initialize the widgets
        self.create_widgets()

        # Ensure the focus is set to the entry field
        self.entry.focus_set()

    def create_widgets(self):
        """Initialize all widgets for the Add Window."""
        self.create_label()
        self.create_entry()
        self.create_listbox()
        self.create_buttons()

    def create_label(self):
        """Create the label that instructs the user to scan barcodes."""
        label = tk.Label(self.send_window, text="Start adding shoes by scanning barcodes")
        label.pack(pady=20)

    def create_entry(self):
        """Create the Entry widget where the barcode is scanned."""
        self.entry = tk.Entry(self.send_window)
        self.entry.pack(pady=10)

        # Bind the Entry widget to capture barcode input
        self.entry.bind("<KeyRelease>", self.read_entry)

    def create_listbox(self):
        """Create the Listbox to display scanned shoe items."""
        # List to hold the scanned items
        self.items = []
        self.list_items = tk.Variable(value=self.items)

        self.listbox = tk.Listbox(self.send_window, listvariable=self.list_items)
        self.listbox.pack(pady=10)

    def create_buttons(self):
        """Create buttons to add shoes and close the window."""
        close_button = tk.Button(self.send_window, text="Make invoice", command=self.save_and_close)
        close_button.pack(pady=10)

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

    def save_and_close(self):
        try:
            # Open varasto.json in read mode to load the data
            with open("Jsonfiles/varasto.json", 'r') as file:
                data = json.load(file)

            # Process each item in self.items
            for item in self.items:
                # Each item format is "shoe_name - size"
                shoe_name, size = item.split(" - ")

                # Search for the shoe entry in data
                for shoe_entry in data:
                    if shoe_entry["name"] == shoe_name:
                        # If the size exists within the shoe entry, increment it
                        if size in shoe_entry:
                            shoe_entry[size] -= 1
                            # Optionally, increment the total count as well
                            shoe_entry["Total"] -= 1
                            print(f"Updated {shoe_name} size {size} to {shoe_entry[size]}")
                        else:
                            print(f"Size '{size}' not found for shoe '{shoe_name}' in data.")
                        break
                else:
                    # If the shoe_name is not found in varasto.json data
                    print(f"Shoe '{shoe_name}' not found in data.")

            # Save updated data back to varasto.json
            with open("Jsonfiles/varasto.json", 'w') as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            print("The file 'Jsonfiles/varasto.json' was not found.")

        except json.JSONDecodeError:
            print(
                "Error decoding JSON from 'Jsonfiles/varasto.json'. The file may be corrupt or incorrectly formatted.")

        # Call the refresh callback after saving changes
        self.refresh_callback()

        # Close the add window
        self.send_window.destroy()
