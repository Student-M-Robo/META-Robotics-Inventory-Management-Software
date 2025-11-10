# -------------------------------------------#
# stock_enquiry.py - Stock Enquiry Window
# -------------------------------------------#

import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, filedialog, ttk
from PIL import Image, ImageTk 
import os
import math 

# Import data handling functions
import inventory_data 

# Define the fixed pixel dimensions for the image preview area 
PREVIEW_W = 250
PREVIEW_H = 200

class StockEnquiryWindow:
    def __init__(self, master_root, inventory_window_instance):
        """Initializes the window with references to the main root and the inventory manager."""
        self.master_root = master_root
        # Store the instance of the InventoryManagementWindow 
        self.inventory_window_instance = inventory_window_instance 
        
        # State variables
        self.current_part_num = None
        self.preview_image_ref = None   
        
        # Entry widget reference
        self.entry_part_num = None
        
        # Label widget references for display
        self.description_label = None
        self.unit_price_label = None
        self.current_qty_label = None
        self.photo_preview_label = None
        
        # Create Toplevel window
        self.window = Toplevel(master_root)
        self.window.title("Stock Enquiry")
        self.center_window(self.window, 650, 550) # Slightly smaller window as less input is needed
        self.window.grab_set() # Modal behavior

        self._create_widgets()
        self._clear_details()

    def center_window(self, window, width, height):
        """Centers the window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """Sets up all the UI components in the window."""
        
        # --- Main Frame (Centered) ---
        main_frame = Frame(self.window, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(expand=True, fill='both')

        # --- Title ---
        title_label = Label(main_frame, text="Stock Enquiry", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#004d99")
        title_label.grid(row=0, column=0, columnspan=3, pady=15)
        
        # --- Search Bar and Part Number Input ---
        search_frame = Frame(main_frame, bg="#f0f0f0")
        search_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        Label(search_frame, text="Enter Part Number:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.entry_part_num = Entry(search_frame, width=20, font=("Arial", 12), bd=2, relief=tk.RIDGE)
        self.entry_part_num.pack(side=tk.LEFT, padx=5)
        
        search_btn = Button(search_frame, text="Search", command=self._search_part, 
                                 font=("Arial", 12, "bold"), bg="#a3d9ff", fg="black")
        search_btn.pack(side=tk.LEFT, padx=10)
        
        # --- Details Frame (Organized display of fetched data) ---
        details_frame = Frame(main_frame, padx=10, pady=10, bg="white", bd=2, relief=tk.GROOVE)
        details_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky='nsew')
        main_frame.grid_columnconfigure(0, weight=1) 

        row_index = 0
        
        # Description
        Label(details_frame, text="Description:", font=("Arial", 12, "bold"), bg="white").grid(row=row_index, column=0, sticky='w', padx=5, pady=5)
        self.description_label = Label(details_frame, text="N/A", font=("Arial", 12), bg="white", width=30, anchor='w')
        self.description_label.grid(row=row_index, column=1, sticky='w', padx=5, pady=5)
        row_index += 1

        # Unit Price
        Label(details_frame, text="Unit Price:", font=("Arial", 12, "bold"), bg="white").grid(row=row_index, column=0, sticky='w', padx=5, pady=5)
        self.unit_price_label = Label(details_frame, text="N/A", font=("Arial", 12), bg="white", anchor='w')
        self.unit_price_label.grid(row=row_index, column=1, sticky='w', padx=5, pady=5)
        row_index += 1
        
        # Current Quantity (Highlighted for enquiry)
        Label(details_frame, text="Current Stock:", font=("Arial", 12, "bold"), bg="white").grid(row=row_index, column=0, sticky='w', padx=5, pady=5)
        self.current_qty_label = Label(details_frame, text="N/A", font=("Arial", 14, "bold"), bg="white", fg="#004d99", anchor='w')
        self.current_qty_label.grid(row=row_index, column=1, sticky='w', padx=5, pady=5)
        row_index += 1
        
        # --- Image Preview (Right side) ---
        image_frame = Frame(main_frame, padx=5, pady=5, bg="#f0f0f0")
        image_frame.grid(row=2, column=2, padx=10, pady=15, sticky='n')
        
        Label(image_frame, text="Part Image", font=("Arial", 10, "italic"), bg="#f0f0f0").pack(pady=5)
        self.photo_preview_label = Label(image_frame, text="Image Preview", 
                                        bg="#cccccc", fg="black", 
                                        width=math.ceil(PREVIEW_W / 8), height=math.ceil(PREVIEW_H / 16)) 
        self.photo_preview_label.pack()
        
        # --- Footer Buttons ---
        footer_frame = Frame(self.window, bg="#e0e0e0", pady=5)
        footer_frame.pack(fill='x', side='bottom')
        
        Button(footer_frame, text="MENU", command=self._go_to_menu, 
               font=("Arial", 12, "bold"), bg="#ff8566", fg="black", padx=10).pack(side=tk.LEFT, padx=20)
        
        Button(footer_frame, text="Back Page", command=self._back_to_inventory_menu, 
               font=("Arial", 14, "bold"), bg="#ff8566", fg="black", padx=10).pack(side=tk.RIGHT, padx=20)

    def _clear_details(self):
        """Resets all detail labels and state."""
        self.description_label.config(text="N/A")
        self.unit_price_label.config(text="N/A")
        self.current_qty_label.config(text="N/A", fg="#004d99")
        
        # Reset image preview 
        self.photo_preview_label.config(text="Image Preview", image='', compound=tk.NONE, width=math.ceil(PREVIEW_W / 8), height=math.ceil(PREVIEW_H / 16))
        self.preview_image_ref = None # Clear image reference

        self.current_part_num = None

    def _display_image(self, image_path):
        """Loads, resizes, and displays an image from a given path."""
        
        if image_path and os.path.exists(image_path):
            try:
                # Open the image file
                original_img = Image.open(image_path)
                
                # Calculate ratio to fit within bounds while preserving aspect ratio
                original_width, original_height = original_img.size
                ratio = min(PREVIEW_W / original_width, PREVIEW_H / original_height)
                
                if ratio >= 1:
                    new_width, new_height = original_width, original_height
                else:
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)
                
                # Resize the image (using LANCZOS for quality)
                resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert the PIL image to a Tkinter PhotoImage
                tk_img = ImageTk.PhotoImage(resized_img)
                
                # Update the label, setting its dimensions based on the resized image
                self.photo_preview_label.config(image=tk_img, text="", compound=tk.NONE, width=new_width, height=new_height)
                
                # Store the reference to prevent garbage collection
                self.preview_image_ref = tk_img 
                
            except Exception as e:
                # Fallback if image loading/resizing fails
                self.photo_preview_label.config(text="Image Load Error", image='', compound=tk.NONE)
                self.preview_image_ref = None
                print(f"Image display error: {e}")
        else:
            # If path is empty or file doesn't exist
            self.photo_preview_label.config(text="No Image", image='', compound=tk.NONE, 
                                            width=math.ceil(PREVIEW_W / 8), height=math.ceil(PREVIEW_H / 16)) 
            self.preview_image_ref = None

    def _search_part(self):
        """Fetches and displays details for the entered part number."""
        part_num = self.entry_part_num.get().strip()
        
        self._clear_details() # Clear existing details first

        if not part_num:
            messagebox.showwarning("Input Missing", "Please enter a Part Number to search.")
            return

        # Fetch data from the database/dataframe
        part_data = inventory_data.get_part_data(part_num)
        
        if part_data and 'Description' in part_data:
            # Update detail labels
            self.description_label.config(text=part_data['Description'])
            
            # UnitPrice is stored as a float/numeric, format it for display
            try:
                 price_display = f"${float(part_data['UnitPrice']):,.2f}"
            except (ValueError, TypeError):
                 price_display = str(part_data['UnitPrice'])
                 
            self.unit_price_label.config(text=price_display)
            
            # The quantity is an integer, display it clearly
            qty = int(part_data.get('Quantity', 0))
            self.current_qty_label.config(text=f"{qty:,}", fg="green")
            
            # Display image
            image_path = part_data.get('ImagePath', '')
            self._display_image(image_path)
            
            # Set state for processing
            self.current_part_num = part_num

        else:
            messagebox.showerror("Part Not Found", f"Part Number '{part_num}' not found in inventory.")
            self._clear_details()
            self.entry_part_num.focus_set()

    def _back_to_inventory_menu(self):
        """Closes this window and returns focus to the parent Inventory Management window."""
        self.window.destroy()
        
        if self.inventory_window_instance and self.inventory_window_instance.inventory_window:
            self.inventory_window_instance.inventory_window.deiconify()

    def _go_to_menu(self):
        """Closes all sub-windows and returns to the main application menu."""
        
        # 1. Close this current window
        self.window.destroy()
        
        # 2. Call the parent InventoryManagementWindow instance's method to close itself 
        if hasattr(self.inventory_window_instance, 'return_to_main_menu'):
            self.inventory_window_instance.return_to_main_menu()
        else:
            messagebox.showerror("Error", "Could not return to main menu. Parent window navigation method missing.")
            self.master_root.deiconify()