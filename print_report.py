# -------------------------------------------#
# print_report.py - View Inventory Report Window (Fixed Data Presentation)
# -------------------------------------------#

import tkinter as tk
from tkinter import Toplevel, Label, Button, Frame, messagebox, ttk
import pandas as pd
# Removed: from PIL import Image, ImageTk 
import os
import re 
import inventory_data 

THUMBNAIL_H = 55 # Retain row height for large text if needed

class PrintReportWindow:
    def __init__(self, master_root, inventory_window_instance):
        self.master_root = master_root
        self.inventory_window_instance = inventory_window_instance 
        
        # No more image references needed
        
        self.window = Toplevel(master_root)
        self.window.title("Full Inventory Stock Report")
        self.center_window(self.window, 900, 650) 

        self.window.protocol("WM_DELETE_WINDOW", self._back_to_inventory_menu)
        self.window.focus_set()
        self.window.grab_set()
        
        self._configure_styles() 
        self._create_widgets()
        self.load_inventory_data()

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.resizable(True, True)
    
    def _configure_styles(self):
        style = ttk.Style()
        # Row height for spacing, even without images
        style.configure('Treeview', rowheight=THUMBNAIL_H) 

    def _create_widgets(self):
        main_container = Frame(self.window, padx=10, pady=10)
        main_container.pack(fill='both', expand=True)

        Label(main_container, text="Full Inventory Stock Report", font=("Arial", 16, "bold"), fg="#004d99").pack(pady=(0, 10))
        
        # Navigation Buttons Frame (Layout confirmed working)
        nav_frame = Frame(main_container)
        nav_frame.pack(side=tk.BOTTOM, fill='x', pady=(10, 0)) 
        
        Button(nav_frame, text="Back", command=self._back_to_inventory_menu).pack(side=tk.LEFT, padx=20, pady=10)
        Button(nav_frame, text="MENU", command=self._go_to_menu).pack(side=tk.RIGHT, padx=20, pady=10)

        # Table Frame 
        table_frame = Frame(main_container)
        table_frame.pack(fill='both', expand=True) 
        
        columns = ('PartNumber', 'Description', 'UnitPrice', 'Quantity')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        self.tree.heading('#0', text='Image', anchor=tk.CENTER)
        self.tree.heading('PartNumber', text='Part Number', anchor=tk.W)
        self.tree.heading('Description', text='Description', anchor=tk.W)
        self.tree.heading('UnitPrice', text='Unit Price', anchor=tk.E)
        self.tree.heading('Quantity', text='Quantity', anchor=tk.E)
        
        # 3. Set Column Properties (Aggressive fixed sizing for better control)
        # All columns except Description are fixed to force Description to handle remaining space.
        self.tree.column('#0', width=70, minwidth=70, stretch=tk.NO, anchor=tk.CENTER)
        self.tree.column('PartNumber', width=100, minwidth=100, stretch=tk.NO)
        
        # --- AGGRESSIVE COLUMN WIDTH ADJUSTMENT ---
        # Fixed minwidth of 200, stretch to fill the rest of the window.
        self.tree.column('Description', width=100, minwidth=100, stretch=tk.YES)
        # -------------------------------
        
        self.tree.column('UnitPrice', width=100, minwidth=100, stretch=tk.NO, anchor=tk.E)
        self.tree.column('Quantity', width=80, minwidth=80, stretch=tk.NO, anchor=tk.E)
        
        self.tree.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_inventory_data(self):
        """Fetches data from the global INVENTORY_DF and populates the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Image rendering is now skipped
        
        df = inventory_data.INVENTORY_DF.copy() 
        
        if df.empty:
            messagebox.showwarning("No Data", "The inventory data cache is empty. Please ensure data is loaded.")
            return

        # Data Cleaning
        if 'UnitPrice' in df.columns:
            df['UnitPrice'] = df['UnitPrice'].astype(str).apply(lambda x: re.sub(r'[$,£,]', '', x.strip()))
            df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
        if 'Quantity' in df.columns:
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

        for part_num, row in df.iterrows():
            
            # image_path = row.get('ImagePath', '') # Image path is now unused
            
            description = row.get('Description', 'N/A')
            unit_price_raw = row['UnitPrice']
            quantity_raw = row['Quantity']
            
            unit_price = f"${unit_price_raw:,.2f}" if pd.notna(unit_price_raw) else "$0.00"
            quantity = f"{int(quantity_raw):,}" if pd.notna(quantity_raw) and quantity_raw == quantity_raw else "0"
            
            # Explicitly display "No Image" text
            display_text = "No Image"

            self.tree.insert('', tk.END, 
                             text=display_text, 
                             image='', # Explicitly empty image
                             values=(part_num, description, unit_price, quantity)
                             )

    def _back_to_inventory_menu(self):
        self.window.destroy()
        if self.inventory_window_instance and self.inventory_window_instance.inventory_window:
            self.inventory_window_instance.inventory_window.deiconify()

    def _go_to_menu(self):
        self.window.destroy()
        if hasattr(self.inventory_window_instance, 'return_to_main_menu'):
            self.inventory_window_instance.return_to_main_menu()
        else:
            messagebox.showerror("Error", "Could not return to main menu.")