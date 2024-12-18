import tkinter as tk
from tkinter import filedialog, ttk
import json
from invoice_generator import InvoiceGenerator
from Utility import utils


def update_invoice_path(path):
    ''' Update the invoice number'''
    str_list = path.split("/")
    str_list.pop(len(str_list) -1)
    file = open("Text files/invoice_number.txt", "r")
    number = file.readline()
    file.close()

    str_list.append("lasku " + number + ".pdf")

    result = '/'.join(str_list)
    pathfile = open("Text files/path.txt", "w")
    pathfile.write(result)
    pathfile.close()

    return result


class SendWindow:
    def __init__(self, parent, refresh_callback):
        self.send_window = tk.Toplevel(parent)
        self.send_window.title("Send Items")
        self.send_window.geometry("400x550")
        self.send_window.wm_minsize(400, 550)

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
                    new_path = update_invoice_path(saved_path)
                    self.save_location_var.set(new_path)
                    self.invoice_save_path = new_path  # Set the path immediately

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
        self.create_listboxes()
        # Button to trigger file save location selection
        select_save_location_button = tk.Button(self.send_window, text="Select Save Location",
                                                command=self.select_save_location)
        select_save_location_button.pack(pady=5)

        self.create_save_location_entry()
        self.create_combobox()

        # Button to finalize and create the invoice
        close_button = tk.Button(self.send_window, text="Make Invoice", command=self.save_and_close)
        close_button.pack(pady=10)

    def create_combobox(self):
        values = [
            "Varuste.net",
            "Salmisaari",
            "Ristikko",
            "Kalasatama",
            "Oulun Kiipelykeskus",
            "Bolderpaja",
            "Tampereen kiipelyksekus"
        ]
        self.combobox = ttk.Combobox(self.send_window, values=values)
        self.combobox.set("Select customer")
        self.combobox.pack(pady=10)

    def create_label(self):
        self.label = tk.Label(self.send_window, text="Start adding shoes by scanning barcodes")
        self.label.pack(pady=20)

    def create_entry(self):
        self.entry = tk.Entry(self.send_window)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.read_entry)

    def create_listboxes(self):
        self.items = []
        self.shoe_counts = {}
        self.list_items = tk.Variable(value=self.items)

        # Frame to hold the LabelFrames
        main_frame = tk.Frame(self.send_window)
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        first_listbox_frame = tk.LabelFrame(main_frame, text="Scanned Items", padx=10, pady=10)
        first_listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.listbox = tk.Listbox(
            first_listbox_frame, listvariable=self.list_items,
            selectbackground="darkgray", selectmode=tk.SINGLE
        )
        self.create_context_menu()
        self.listbox.bind("<Button-3>", self.show_context_menu)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar1 = tk.Scrollbar(first_listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar1.set)

        # --- Second Listbox with LabelFrame and Scrollbar ---
        self.count_items = tk.Variable(value=[])

        second_listbox_frame = tk.LabelFrame(main_frame, text="Shoe Counts", padx=10, pady=10)
        second_listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.listbox1 = tk.Listbox(
            second_listbox_frame, listvariable=self.count_items,
            selectbackground="darkgray", selectmode=tk.SINGLE
        )
        self.listbox1.bind("<Button-3>", self.show_context_menu)
        self.listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar2 = tk.Scrollbar(second_listbox_frame, orient=tk.VERTICAL, command=self.listbox1.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox1.config(yscrollcommand=scrollbar2.set)

        self.totalLable = tk.Label(self.send_window, text=f"Total amount: 0", font=8)
        self.totalLable.pack(fill=tk.BOTH, expand=True, pady=2)

    def show_context_menu(self, event):
        """
        Show the context menu and select the item under the cursor on right-click.
        """
        try:
            # Identify the listbox widget
            widget = event.widget

            # Find the index of the item under the cursor
            index = widget.nearest(event.y)
            widget.selection_clear(0, tk.END)
            widget.selection_set(index)
            widget.activate(index)

            # Show the context menu at the cursor position
            self.context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error: {e}")

    def create_context_menu(self):
        # Create a context menu (dropdown menu)
        self.context_menu = tk.Menu(self.listbox, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_item)


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

        self.send_window.focus_force()

    def read_entry(self, event):
        """Read barcode input and add shoes to the lists."""
        barcode = self.entry.get()

        if len(barcode) == 13:
            self.entry.delete(0, tk.END)
            found, shoe_name, size = utils.read_barcode_from_json(barcode)

            if found:
                # Add to scanned items
                item = f"{shoe_name} - {size}"
                self.items.append(item)
                self.list_items.set(self.items)

                # Update counts
                if shoe_name not in self.shoe_counts:
                    self.shoe_counts[shoe_name] = 1
                else:
                    self.shoe_counts[shoe_name] += 1
                self.update_counts()

        elif len(barcode) > 13:
            self.entry.delete(0, tk.END)

    def update_counts(self):
        """Update the second listbox with shoe counts and calculate the total number of items."""
        # Format the counts for the listbox
        formatted_counts = [f"{shoe}: {count}" for shoe, count in self.shoe_counts.items()]

        # Calculate the total number of items by summing the counts
        total = sum(self.shoe_counts.values())

        # Update the total label with the total amount of items
        formatted_total = f"Total amount of items: {total}"
        self.totalLable.config(text=formatted_total)  # Update label text

        # Update the listbox with formatted counts
        self.count_items.set(formatted_counts)

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

                file.close()

            with open("Jsonfiles/varasto.json", 'w') as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            print("The file 'Jsonfiles/varasto.json' was not found.")
        except json.JSONDecodeError:
            print(
                "Error decoding JSON from 'Jsonfiles/varasto.json'. The file may be corrupt or incorrectly formatted.")

        # Example data
        items = [
            {"tuotekuvaus": "Tenaya Oasi kiipeilykenkä", "määrä": 7, "yksikko": "kpl", "hinta": 84.93},
            {"tuotekuvaus": "Tenaya Masai kiipeilykenkä", "määrä": 3, "yksikko": "kpl", "hinta": 72.55},
            # Add more items as needed
        ]
        self.reformat_data()
        customer = self.combobox.get()
        if customer == "Select customer":
            self.label.config(text="Please select a customer", fg="red", font="15")
            return

        invoice = InvoiceGenerator(self.reformat, customer, output_file=self.invoice_save_path)
        invoice.generate()
        print(f"Invoice saved to {self.invoice_save_path}")
        self.send_window.destroy()


    def delete_selected_item(self):
        """Delete the selected item from the appropriate listbox."""
        try:
            # Delete from the first listbox (scanned shoes)
            selected_index = self.listbox.curselection()
            if selected_index:
                item = self.items.pop(selected_index[0])
                self.list_items.set(self.items)

                # Update the second listbox (counts)
                shoe_name = item.split(" - ")[0]
                if shoe_name in self.shoe_counts:
                    self.shoe_counts[shoe_name] -= 1
                    if self.shoe_counts[shoe_name] == 0:
                        del self.shoe_counts[shoe_name]

                self.update_counts()
                return

        except Exception as e:
            print(f"Error: {e}")


    def reformat_data(self):
        '''
        Reformat the items from the self.items list to a different data format before
        generating an invoice.
        :return:
        '''
        self.reformat = []
        try:
            with open("Jsonfiles/kenka_tiedot.json", 'r') as file:
                data = json.load(file)

            # Process each item in self.items
            for item in self.items:
                shoe_name, size = item.split(" - ")

                # Check if the shoe exists in the JSON data
                if shoe_name in data:
                    details_of_shoe = data[shoe_name]

                    # Check if the shoe is already in self.reformat
                    for added in self.reformat:
                        if added.get('description') == details_of_shoe.get('description'):
                            # Increment the 'quantity' field if a duplicate is found
                            added['quantity'] = added.get('quantity', 0) + 1
                            break
                    else:
                        # Add the shoe to the reformat list if it's not already there
                        self.reformat.append(details_of_shoe.copy())


            print(str(self.reformat))

        except FileNotFoundError:
            print("Could not find file")
        except json.JSONDecodeError:
            print("JSON syntax error")
