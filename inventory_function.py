# -------------------------------------------#
# inventory_function.py - UI and Application Logic
# This module defines the main Inventory Management Window and its sub-windows.
# -------------------------------------------#

import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, filedialog 
from PIL import Image, ImageTk 
import os 
import shutil 

import inventory_data

from edit_part import EditPartWindow 
from stock_received import StockReceivedWindow
from stock_issued import StockIssuedWindow
from stock_enquiry import StockEnquiryWindow



# Global reference for images to prevent garbage collection
new_part_image_ref = None

# Define a stable directory to store all part images
IMAGE_DIR = "part_images" 

# Define the fixed pixel dimensions for the image preview area 
PREVIEW_W = 250
PREVIEW_H = 200

class InventoryManagementWindow:
    def __init__(self, master_root):
        """Initializes the window with a reference to the main root."""
        self.master_root = master_root
        # Store references to entry widgets for later data retrieval
        self.entry_part_num = None
        self.entry_description = None
        self.entry_unit_price = None
        
        # Image-related attributes pretty 
        self.selected_photo_path = None # Stores the absolute path of the selected image
        self.photo_preview_label = None 
        self.preview_image_ref = None   
        self.inventory_window = None # Initialize the main inventory window reference
        
        # Ensure the image directory exists on startup 
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

    # Helper Method
    def return_to_main_menu(self):
        """Closes the inventory window and re-opens the main menu."""
        if self.inventory_window:
            self.inventory_window.destroy()
        self.master_root.deiconify()

    # Helper Method
    def center_window(self, window, width, height):
        """Centers a given Tkinter window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Helper Method
    def return_to_inventory_menu(self, current_window):
        """Closes the current sub-window and re-opens the inventory menu window."""
        current_window.destroy()
        if self.inventory_window:
            self.inventory_window.deiconify()
        
    # Helper Method
    def return_to_main_menu_from_sub(self, current_window):
        """Closes the current sub-window and returns to the main application menu."""
        current_window.destroy()
        self.master_root.deiconify()

    # UI: Inventory Management Menu
    def open_window(self):
        """Creates and displays the main Inventory Management menu window."""
        
        # Make sure the main root is withdrawn if it's visible, for cleaner flow
        self.master_root.withdraw() 
        
        self.inventory_window = Toplevel(self.master_root)
        self.inventory_window.title("Inventory Management")
        
        WINDOW_WIDTH = 500
        WINDOW_HEIGHT = 600
        self.center_window(self.inventory_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.inventory_window.config(bg="white")
        
        # Grid Configuration for main buttons
        self.inventory_window.columnconfigure(0, weight=1)
        self.inventory_window.columnconfigure(1, weight=5) # Center column for content
        self.inventory_window.columnconfigure(2, weight=1)
        
        # Header
        header_label = Label(self.inventory_window, text="Inventory Management",
                             font=("Arial", 20, "bold"), bg="white", fg="#004d99")
        header_label.grid(row=0, column=1, pady=(20, 0), sticky="s") 

        # List of buttons and their commands
        buttons = [
            ("Create New Part", self.open_create_new_part),
            ("Edit Part Information", self.open_edit_part_information),
            ("Stock Received", self.open_stock_received), # UPDATED: Call the new method
            ("Stocks Issued", self.open_stock_issued_window),     
            ("Stock Enquiry", self.open_stock_enquiry),     
            ("Print Report", lambda: messagebox.showinfo("WIP", "Generating Print Report")),     
        ]

        # Dynamically create buttons
        row_num = 1
        for text, command in buttons:
            btn = Button(self.inventory_window, text=text, command=command,
                         bg="#cccccc", fg="black", font=("Arial", 14), width=25, height=2)
            btn.grid(row=row_num, column=1, padx=40, pady=10, sticky="ew")
            row_num += 1

        # Navigation Buttons
        nav_frame = Frame(self.inventory_window, bg="white")
        nav_frame.grid(row=row_num, column=1, pady=(10, 20), sticky="e")
        
        # Back Page button
        back_btn = Button(nav_frame, text="Back Page", command=self.return_to_main_menu,
                          bg="#cccccc", font=("Arial", 10))
        back_btn.pack(side="right", padx=10)
        
        # MENU button
        menu_btn = Button(nav_frame, text="MENU", command=self.return_to_main_menu,
                          bg="#cccccc", font=("Arial", 10))
        menu_btn.pack(side="right", padx=10)
        
        # Handle window close
        self.inventory_window.protocol("WM_DELETE_WINDOW", self.return_to_main_menu)

    def open_stock_received(self):
        """Initializes and opens the Stock Received window."""
        self.inventory_window.withdraw()
        stock_manager = StockReceivedWindow(self.master_root, self)
    
        
    def open_edit_part_information(self):
        """Initializes and opens the Edit Part Information window."""
        self.inventory_window.withdraw()
        
        edit_manager = EditPartWindow(self.master_root, self)
        edit_manager.open_window()
    

    def open_create_new_part(self):
        """Creates and displays the Create New Part sub-window."""
        self.inventory_window.withdraw()
        
        self.create_window = Toplevel(self.master_root)
        self.create_window.title("Create New Part")
        
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 600
        self.center_window(self.create_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.create_window.config(bg="white")
        
        # Grid Configuration 
        self.create_window.columnconfigure(0, weight=1) 
        self.create_window.columnconfigure(1, weight=5) # Central content column
        self.create_window.columnconfigure(2, weight=1) 
        for i in range(10):
            self.create_window.rowconfigure(i, weight=1)

        # Header
        header = Label(self.create_window, text="Create New Part", 
                            font=("Arial", 20, "bold"), bg="white", fg="#004d99")
        header.grid(row=0, column=1, pady=10, sticky="n")

        input_frame = Frame(self.create_window, bg="white")
        input_frame.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=30, pady=10)
        input_frame.columnconfigure(0, weight=1) # Label column
        input_frame.columnconfigure(1, weight=3) # Entry column
        for i in range(5):
            input_frame.rowconfigure(i, weight=1)
        
        # 1. Part Number
        Label(input_frame, text="Enter New Part Number:", font=("Arial", 12), bg="white").grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )
        self.entry_part_num = Entry(input_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_part_num.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # 2. Description
        Label(input_frame, text="Enter Part Description:", font=("Arial", 12), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=5
        )
        self.entry_description = Entry(input_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_description.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # 3. Unit Price
        Label(input_frame, text="Enter Part Unit Price:", font=("Arial", 12), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=5
        )
        self.entry_unit_price = Entry(input_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_unit_price.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # 4. Image Section
        Label(input_frame, text="Upload Part Image Here:", font=("Arial", 12), bg="white").grid(
            row=3, column=0, sticky="ne", padx=10, pady=5
        )
        image_upload_frame = Frame(input_frame, bg="white")
        image_upload_frame.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        image_upload_frame.columnconfigure(0, weight=1)
        image_upload_frame.columnconfigure(1, weight=1)
        
        # The Preview Label (Default: fixed size based on text units)
        self.photo_preview_label = Label(image_upload_frame, text="No image selected", 
                                             font=("Arial", 10), bg="#f0f0f0", height=3, width=25, relief="solid")
        self.photo_preview_label.grid(row=0, column=1, sticky="ew", padx=10)
        
        # UPLOAD button
        upload_btn = Button(image_upload_frame, text="UPLOAD", font=("Arial", 12), bg="#d9d9d9", 
                             command=self.select_photo_file) 
        upload_btn.grid(row=0, column=0, sticky="w", padx=10)
        
        # Control Buttons
        control_frame = Frame(self.create_window, bg="white")
        control_frame.grid(row=6, column=1, sticky="e", padx=30, pady=10)
        
        update_btn = Button(control_frame, text="UPDATE", font=("Arial", 14, "bold"), 
                                     bg="#4CAF50", fg="white", 
                                     command=self.handle_create_part)
        update_btn.pack(side="right", padx=10)
        
        # Navigation Buttons
        nav_frame = Frame(self.create_window, bg="white")
        nav_frame.grid(row=7, column=1, pady=(0, 10))
        
        back_btn = Button(nav_frame, text="Back Page", 
                              command=lambda: self.return_to_inventory_menu(self.create_window),
                              bg="#cccccc", font=("Arial", 10))
        back_btn.pack(side="right", padx=10)
        
        menu_btn = Button(nav_frame, text="MENU", 
                              command=lambda: self.return_to_main_menu_from_sub(self.create_window),
                              bg="#cccccc", font=("Arial", 10))
        menu_btn.pack(side="right", padx=10)

        # Handle window close (X button)
        self.create_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_inventory_menu(self.create_window))
        
    def select_photo_file(self):
        """Opens a file dialog for selecting an image and displays a preview."""
        file_path = filedialog.askopenfilename(
            title="Select Part Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_photo_path = file_path # Store the absolute path
            
            try:
                # Use a global reference to prevent garbage collection
                global new_part_image_ref 
                
                img = Image.open(file_path)
                
                # Define a reasonable max size for the preview (in pixels)
                MAX_PREVIEW_WIDTH = PREVIEW_W
                MAX_PREVIEW_HEIGHT = PREVIEW_H
                
                original_width, original_height = img.size
                
                # Calculate ratio to fit within bounds while preserving aspect ratio
                ratio = min(MAX_PREVIEW_WIDTH / original_width, MAX_PREVIEW_HEIGHT / original_height)
                
                if ratio >= 1:
                    new_width, new_height = original_width, original_height
                else:
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)
                
                # Resize the image (replaces the img.thumbnail line)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Store the reference in the global variable
                new_part_image_ref = ImageTk.PhotoImage(img)
                self.preview_image_ref = new_part_image_ref # Also store a local class reference
                
                self.photo_preview_label.config(
                    image=self.preview_image_ref, 
                    text="",             
                    compound=tk.NONE,    
                    padx=0,              
                    width=new_width,
                    height=new_height
                )
                
            except Exception as e:
                messagebox.showerror("Image Error", f"Could not load or display image: {e}")
                self.photo_preview_label.config(text="Image Load Error", image='', compound=tk.NONE)
                self.preview_image_ref = None
                self.selected_photo_path = None 

    def handle_create_part(self):
        """Gathers data, saves the image, and calls the data module to create a new part."""
        
        part_num = self.entry_part_num.get().strip()
        desc = self.entry_description.get().strip()
        price_str = self.entry_unit_price.get().strip()
        
        if not part_num or not desc or not price_str:
            messagebox.showerror("Error", "Part Number, Description, and Price must be filled.")
            return

        # 1. Image Copying Logic
        saved_image_path = "" # Default to empty path
        
        if self.selected_photo_path and os.path.exists(self.selected_photo_path):
            try:
                # Create filename based on part number and original extension
                file_ext = os.path.splitext(self.selected_photo_path)[1]
                new_filename = f"{part_num}{file_ext}"
                target_path = os.path.join(IMAGE_DIR, new_filename)
                
                # Copy the file to the project's 'part_images' directory
                shutil.copy2(self.selected_photo_path, target_path)
                
                # The path saved to the Excel file is the path within the project directory
                saved_image_path = target_path
                
            except Exception as e:
                messagebox.showwarning("File Error", f"Failed to save image file: {e}. Data will be saved without an image reference.")
                # If copy fails, saved_image_path remains ""

        
        # 2. Call the function from your data module
        result_message = inventory_data.create_new_part_data(part_num, desc, price_str, saved_image_path)
        
        # 3. Display the result and clear fields
        if result_message.startswith("Error"):
            messagebox.showerror("Update Error", result_message)
        elif result_message.startswith("Update Successful"):
            messagebox.showinfo("Update Status", result_message)
            
            # Clear fields after successful update
            self.entry_part_num.delete(0, 'end')
            self.entry_part_num.insert(0, '')
            
            self.entry_description.delete(0, 'end')
            self.entry_description.insert(0, '')
            
            self.entry_unit_price.delete(0, 'end')
            self.entry_unit_price.insert(0, '')
            
            # Clear image preview 
            self.selected_photo_path = None
            # IMPORTANT: Revert label config back to its default text-unit size (width=25, height=3) and compound=tk.NONE
            self.photo_preview_label.config(text="No image selected", image='', compound=tk.NONE, width=25, height=3) 
            self.preview_image_ref = None 
        else:
            messagebox.showwarning("Status", result_message)

    def open_stock_issued_window(self):
        self.inventory_window.withdraw()
        StockIssuedWindow(self.master_root, self)

    def open_stock_enquiry(self): # Or whatever you named the method
        """
        Creates and opens the StockEnquiryWindow.
        """
        # 1. Hide the current window (the Inventory Management Toplevel)
        if self.inventory_window:
            self.inventory_window.withdraw() 
        
        # 2. Instantiate and open the new window.
        # FIX APPLIED HERE: Changed self.root to self.master_root
        self.stock_enquiry_window = StockEnquiryWindow(self.master_root, self)
