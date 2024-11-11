import tkinter as tk
from tkinter import ttk
import json
from invoice_generator import InvoiceGenerator

def read_barcode_from_json(barcode):
    try:
        with open('Jsonfiles/barcodes.json', 'r') as file:
            data = json.load(file)
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
        self.send_window.geometry("500x500")

        # Add padding around the main window
        self.send_window.grid_rowconfigure(0, weight=1)
        self.send_window.grid_columnconfigure(0, weight=1)
        self.refresh_callback = refresh_callback
        self.create_widgets()
        self.entry.focus_set()

    def create_widgets(self):
        # Creating each widget with padding
        self.create_label()
        self.create_entry()
        self.create_listbox()
        self.create_lower_section()
        self.create_buttons()

    def create_label(self):
        self.label = tk.Label(self.send_window, text="Start adding shoes by scanning barcodes")
        self.label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="ew")

    def create_entry(self):
        self.entry = tk.Entry(self.send_window)
        self.entry.grid(row=1, column=0, columnspan=2, pady=(5, 10), padx=20, sticky="ew")
        self.entry.bind("<KeyRelease>", self.read_entry)

    def create_listbox(self):
        self.items = []
        self.list_items = tk.Variable(value=self.items)
        self.listbox = tk.Listbox(self.send_window, listvariable=self.list_items, height=15)
        self.listbox.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=20, sticky="nsew")

    def create_lower_section(self):
        # Label for size selection
        self.text_label = tk.Label(self.send_window, text="Select the recipient")
        self.text_label.grid(row=3, column=0, sticky="ew", padx=(20, 5), pady=(10, 10))

        # Combobox for location selection
        locations = ["Nekala", "Salmisaari", "Lielahti"]
        self.combobox = ttk.Combobox(self.send_window)
        self.combobox['values'] = locations
        self.combobox.grid(row=3, column=1, sticky="ew", padx=(5, 20), pady=(10, 10))

    def create_buttons(self):
        self.close_button = tk.Button(self.send_window, text="Make invoice", command=self.save_and_close)
        self.close_button.grid(row=4, column=0, columnspan=2, pady=(20, 20), padx=20)

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
            print(
                "Error decoding JSON from 'Jsonfiles/varasto.json'. The file may be corrupt or incorrectly formatted.")

        # dummy data
        items = [
            {"quantity": 1, "description": "Front and rear brake cables", "unit_price": 100.00},
            {"quantity": 2, "description": "New set of pedal arms", "unit_price": 15.00},
            {"quantity": 3, "description": "Labor 3hrs", "unit_price": 5.00},
        ]
        recipient = {
            "name": "John Smith",
            "address": "2 Court Square",
            "city": "New York, NY 12210",
        }

        invoice = InvoiceGenerator(items, recipient, output_file="sample_invoice.pdf")
        invoice.generate()