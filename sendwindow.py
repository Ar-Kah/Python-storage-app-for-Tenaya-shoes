import tkinter as tk
from tkinter import filedialog
import json
from invoice_generator import InvoiceGenerator


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
    return False, "", ""


class SendWindow:
    def __init__(self, parent, refresh_callback):
        self.send_window = tk.Toplevel(parent)
        self.send_window.title("Send Items")
        self.send_window.geometry("400x400")

        # Store the callback function
        self.refresh_callback = refresh_callback
        self.invoice_save_path = ""  # Path where the invoice will be saved
        self.save_location_var = tk.StringVar(value="")

        # Try to read the saved path from 'path.txt'
        try:
            with open("Text files/path.txt", 'r') as path_file:
                saved_path = path_file.readline().strip()

                # Check if saved_path is empty; if so, open dialog for a new path
                if not saved_path:
                    self.save_location_var.set("No location selected")
                else:
                    self.save_location_var.set(saved_path)
                    self.invoice_save_path = saved_path  # Set the path immediately

        except FileNotFoundError:
            # If the file doesn't exist, open dialog to get the path
            print("File 'path.txt' not found.")
            self.select_save_location()  # Prompt for the save location right away

        # Initialize the widgets
        self.create_widgets()
        self.entry.focus_set()

    def create_widgets(self):
        self.create_label()
        self.create_entry()
        self.create_listbox()
        self.create_buttons()
        self.create_save_location_entry()

    def create_label(self):
        label = tk.Label(self.send_window, text="Start adding shoes by scanning barcodes")
        label.pack(pady=20)

    def create_entry(self):
        self.entry = tk.Entry(self.send_window)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.read_entry)

    def create_listbox(self):
        self.items = []
        self.list_items = tk.Variable(value=self.items)
        self.listbox = tk.Listbox(self.send_window, listvariable=self.list_items)
        self.listbox.pack(pady=10)

    def create_buttons(self):
        # Button to trigger file save location selection
        select_save_location_button = tk.Button(self.send_window, text="Select Save Location",
                                                command=self.select_save_location)
        select_save_location_button.pack(pady=5)

        # Button to finalize and create the invoice
        close_button = tk.Button(self.send_window, text="Make Invoice", command=self.save_and_close)
        close_button.pack(pady=10)

    def create_save_location_entry(self):
        save_location_label = tk.Label(self.send_window, text="Invoice Save Location:")
        save_location_label.pack(pady=5)

        self.save_location_entry = tk.Entry(self.send_window, textvariable=self.save_location_var, state="readonly",
                                            width=50)
        self.save_location_entry.pack(pady=5)

    def select_save_location(self):
        # Try to read the saved path from 'path.txt'
        try:
            with open("Text files/path.txt", 'r') as path_file:
                saved_path = path_file.readline().strip()  # Read and remove any extra newline/whitespace

            # Check if saved_path is empty; if so, open dialog for a new path
            if not saved_path:
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            else:
                # Use saved path as initial directory in dialog, allowing user to change if needed
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=saved_path,
                                                         filetypes=[("PDF files", "*.pdf")])

        except FileNotFoundError:
            # If the file doesn't exist, open dialog to get the path
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        # If a file_path was chosen, update the entry and save the path
        if file_path:
            self.invoice_save_path = file_path
            self.save_location_var.set(file_path)

            # Save the chosen path back to 'path.txt' for next time
            with open("Text files/path.txt", 'w') as path_file:
                path_file.write(file_path)

    def read_entry(self, event):
        barcode = self.entry.get()
        if len(barcode) == 13:
            self.entry.delete(0, tk.END)
            if_found, shoe_name, size = read_barcode_from_json(barcode)
            if if_found:
                self.items.append(f"{shoe_name} - {size}")
                self.list_items.set(self.items)
        elif len(barcode) > 13:
            self.entry.delete(0, tk.END)

    def save_and_close(self):
        if not self.invoice_save_path:
            # Show a message if no save location is selected
            print("Please select a save location for the invoice.")
            return

        try:
            with open("Jsonfiles/varasto.json", 'r') as file:
                data = json.load(file)

            for item in self.items:
                shoe_name, size = item.split(" - ")
                for shoe_entry in data:
                    if shoe_entry["name"] == shoe_name:
                        if size in shoe_entry:
                            shoe_entry[size] -= 1
                            shoe_entry["Total"] -= 1
                            print(f"Updated {shoe_name} size {size} to {shoe_entry[size]}")
                        else:
                            print(f"Size '{size}' not found for shoe '{shoe_name}' in data.")
                        break
                    else:
                        print(f"Shoe '{shoe_name}' not found in data.")

            with open("Jsonfiles/varasto.json", 'w') as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            print("The file 'Jsonfiles/varasto.json' was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from 'Jsonfiles/varasto.json'. The file may be corrupt or incorrectly formatted.")

        # Generate the invoice using the selected save path
        items = [
            {"quantity": 10, "unit": "kg", "description": "Mansikkaa", "unit_price": 10.00},
            {"quantity": 20, "unit": "l", "description": "Mustikkaa", "unit_price": 5.59},
            {"quantity": 1, "unit": "kpl", "description": "Toimitusmaksu", "unit_price": 15.00},
        ]

        invoice = InvoiceGenerator(items, output_file=self.invoice_save_path)
        invoice.generate()
        print(f"Invoice saved to {self.invoice_save_path}")
        self.send_window.destroy()
