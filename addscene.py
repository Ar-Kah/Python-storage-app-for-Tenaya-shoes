import tkinter as tk
from tkinter import messagebox
from Utility import utils
import json


class AddWindow:
    def __init__(self, parent, refresh_callback):
        self.add_window = tk.Toplevel(parent)
        self.add_window.title("Add Items")
        self.add_window.geometry("400x500")
        self.add_window.wm_minsize(400, 500)

        self.refresh_callback = refresh_callback

        # Lists to manage items and counts
        self.items = []
        self.shoe_counts = {}

        # Tkinter variables
        self.list_items = tk.Variable(value=self.items)
        self.count_items = tk.Variable(value=[])

        self.create_widgets()
        self.create_context_menu()
        self.entry.focus_set()

    def create_widgets(self):
        """Create all widgets for the layout."""
        # Header Label
        label = tk.Label(self.add_window, text="Start adding shoes by scanning barcodes")
        label.pack(pady=20)

        # Barcode Entry
        self.entry = tk.Entry(self.add_window)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.read_entry)

        # Frame to contain both Listboxes
        main_frame = tk.Frame(self.add_window)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- First Listbox with Scrollbar ---
        listbox1_frame = tk.LabelFrame(main_frame, text="Scanned Shoes", padx=10, pady=10)
        listbox1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.listbox = tk.Listbox(
            listbox1_frame, listvariable=self.list_items,
            selectbackground="darkgray", selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar1 = tk.Scrollbar(listbox1_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar1.set)

        # --- Second Listbox with Scrollbar ---
        listbox2_frame = tk.LabelFrame(main_frame, text="Shoe Counts", padx=10, pady=10)
        listbox2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.listbox2 = tk.Listbox(
            listbox2_frame, listvariable=self.count_items,
            selectbackground="darkgray", selectmode=tk.SINGLE
        )
        self.listbox2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar2 = tk.Scrollbar(listbox2_frame, orient=tk.VERTICAL, command=self.listbox2.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox2.config(yscrollcommand=scrollbar2.set)

        self.total = 0
        self.totalLable = tk.Label(self.add_window, text=f"Total amount: {self.total}", font=8)
        self.totalLable.pack(fill=tk.BOTH, expand=True, pady=2)

        # Add Shoes Button
        close_button = tk.Button(self.add_window, text="Add Shoes", command=self.save_and_close)
        close_button.pack(pady=10)

    def create_context_menu(self):
        """Create context menu for deleting items from the listboxes."""
        self.context_menu = tk.Menu(self.add_window, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_item)

        # Bind context menu to both listboxes
        self.listbox.bind("<Button-3>", self.show_context_menu)

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
            else:
                messagebox.showerror("Error", "Barcode not recognized.")
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
        """Save scanned shoes into the storage file."""
        try:
            with open("Jsonfiles/varasto.json", 'r') as file:
                data = json.load(file)

            for item in self.items:
                shoe_name, size = item.split(" - ")
                for shoe in data:
                    if shoe["name"] == shoe_name:
                        if size in shoe:
                            shoe[size] += 1
                            shoe["Total"] += 1
                            break
                else:
                    print(f"Shoe '{shoe_name}' not found.")

            with open("Jsonfiles/varasto.json", 'w') as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            print("The file 'Jsonfiles/varasto.json' was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

        self.refresh_callback()
        self.add_window.destroy()
