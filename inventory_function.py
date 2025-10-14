import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, filedialog # Added filedialog
from PIL import Image, ImageTk # Keep PIL imports
import os # Keep os for file path handling
import shutil # Keep shutil for file copying

import inventory_data # Import the data handling module

# Global reference for images to prevent garbage collection
new_part_image_ref = None

# Define a stable directory to store all part images
IMAGE_DIR = "part_images" 

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

        # Ensure the image directory exists on startup 
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

    # Helper Method
    def return_to_main_menu(self):
        """Closes the inventory window and re-opens the main menu."""
        self.inventory_window.destroy()
        self.master_root.deiconify()

    def return_to_inventory_menu(self, current_window):
        """Closes the current sub-window and returns to the Inventory Management menu."""
        current_window.destroy()
        self.inventory_window.deiconify()
        # Reset image state when returning (Added for cleanup)
        self.selected_photo_path = None
        self.preview_image_ref = None

    def return_to_main_menu_from_sub(self, current_window):
        """Closes the current sub-window and returns to the Main Menu."""
        current_window.destroy()
        self.inventory_window.destroy() 
        self.master_root.deiconify()

    # Helper function to calculate window center position
    def center_window(self, window, width, height):
        """Calculates and sets the geometry string to center the window on the screen."""
        window.update_idletasks() # Ensure dimensions are updated
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        center_x = int((screen_width / 2) - (width / 2))
        center_y = int((screen_height / 2) - (height / 2))
        
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")

    # UI: Inventory Management Menu
    def open_window(self):
        """Creates and displays the Inventory Management sub-window, centered on screen."""
        self.master_root.withdraw()
        self.inventory_window = Toplevel(self.master_root)
        self.inventory_window.title("Inventory Management") 
        
        # Centering Logic
        WINDOW_WIDTH = 600
        WINDOW_HEIGHT = 600
        self.center_window(self.inventory_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        

        self.inventory_window.config(bg="white")
        
        # Grid setup
        self.inventory_window.columnconfigure(0, weight=1) 
        self.inventory_window.columnconfigure(1, weight=3)
        self.inventory_window.columnconfigure(2, weight=1)
        for i in range(10):
            self.inventory_window.rowconfigure(i, weight=1) 

        header_label = Label(self.inventory_window, text="Inventory Management",
                                 font=("Arial", 20, "bold"), bg="white", fg="#004d99")
        header_label.grid(row=0, column=1, pady=(20, 0), sticky="s") 

        # List of buttons - Connect Create New Part here
        buttons = [
            ("Create New Part", self.open_create_new_part),
            ("Edit Part Information", lambda: messagebox.showinfo("WIP", "Opening Edit Part Information")), 
            ("Stock Received", lambda: messagebox.showinfo("WIP", "Opening Stock Received")), 
            ("Stocks Issued", lambda: messagebox.showinfo("WIP", "Opening Stocks Issued")),       
            ("Stock Enquiry", lambda: messagebox.showinfo("WIP", "Opening Stock Enquiry")),      
            ("Print Report", lambda: messagebox.showinfo("WIP", "Generating Print Report")),      
        ]

        start_row = 1
        for text, command in buttons:
            btn = Button(self.inventory_window, text=text, command=command,
                             bg="#e0e0e0", fg="black", font=("Arial", 14))
            btn.grid(row=start_row, column=1, padx=40, pady=5, sticky="nsew") 
            start_row += 1

        back_btn = Button(self.inventory_window, text="MENU",
                              command=self.return_to_main_menu,
                              bg="#f0f0f0", fg="black", font=("Arial", 12, "bold"))
        back_btn.grid(row=start_row, column=1, pady=20, sticky="n") 
        
    # UI: Create New Part
    def open_create_new_part(self):
        """Creates the window for 'Create New Part', centered on screen."""
        self.inventory_window.withdraw() 
        
        # Reset photo state when opening the form
        self.selected_photo_path = None
        self.preview_image_ref = None
        
        create_part_window = Toplevel(self.inventory_window)
        create_part_window.title("Create New Part")
        
        # Centering Logic for Create New Part Window (700x500)
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 500
        self.center_window(create_part_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        
        create_part_window.config(bg="white")
        
        # Grid Configuration (Added uniform weight to all rows for stability)
        for i in range(7):
            create_part_window.rowconfigure(i, weight=1)
        create_part_window.columnconfigure(0, weight=1) 
        create_part_window.columnconfigure(1, weight=2) 
        create_part_window.columnconfigure(2, weight=4) 
        create_part_window.columnconfigure(3, weight=1) 

        # Header (Fixed sticky to "n" to anchor it to the top of its row space)
        header = Label(create_part_window, text="Create New Part", 
                         font=("Arial", 20, "bold"), bg="white", fg="#004d99")
        header.grid(row=0, column=1, columnspan=2, pady=10, sticky="n") # <-- FIX: sticky="n"

        # Helper to create label/entry pair
        def add_input_row(parent, row, label_text):
            Label(parent, text=label_text, font=("Arial", 12), bg="white").grid(
                row=row, column=1, sticky="e", padx=10, pady=5
            )
            entry = Entry(parent, font=("Arial", 12), bd=1, relief="solid")
            entry.grid(row=row, column=2, sticky="ew", padx=(0, 20), pady=5)
            return entry

        # Input Fields
        self.entry_part_num = add_input_row(create_part_window, 1, "Enter New Part Number:")
        self.entry_description = add_input_row(create_part_window, 2, "Enter Part Description:")
        self.entry_unit_price = add_input_row(create_part_window, 3, "Enter Part Unit Price:")

        # Upload Part Image Section
        Label(create_part_window, text="Upload Part Image Here:", font=("Arial", 12), bg="white").grid(
            row=4, column=1, sticky="e", padx=10, pady=5
        )
        upload_frame = Frame(create_part_window, bg="white")
        upload_frame.grid(row=4, column=2, sticky="ew", padx=(0, 20), pady=5)
        upload_frame.columnconfigure(0, weight=1)
        upload_frame.columnconfigure(1, weight=1)
        
        # The Preview Label 
        self.photo_preview_label = Label(upload_frame, text="No image selected", 
                                          font=("Arial", 10), bg="#f0f0f0", height=3, width=25, relief="solid")
        self.photo_preview_label.grid(row=0, column=1, sticky="ew", padx=10)
        
        # UPLOAD button
        upload_btn = Button(upload_frame, text="UPLOAD", font=("Arial", 12), bg="#d9d9d9", 
                            command=self.select_photo_file) # <-- Command restored
        upload_btn.grid(row=0, column=0, sticky="w", padx=10)

        # Update Button - Connects to the data module
        update_btn = Button(create_part_window, text="UPDATE", font=("Arial", 14, "bold"), 
                            bg="#4CAF50", fg="white", 
                            command=self.handle_create_part_update)
        update_btn.grid(row=5, column=2, sticky="e", padx=20, pady=10)

        # Navigation Buttons
        nav_frame = Frame(create_part_window, bg="white")
        nav_frame.grid(row=6, column=1, columnspan=2, pady=(0, 10))
        
        back_btn = Button(nav_frame, text="Back Page", 
                            command=lambda: self.return_to_inventory_menu(create_part_window),
                            bg="#cccccc", font=("Arial", 10))
        back_btn.pack(side="right", padx=10)
        
        menu_btn = Button(nav_frame, text="MENU", 
                            command=lambda: self.return_to_main_menu_from_sub(create_part_window),
                            bg="#cccccc", font=("Arial", 10))
        menu_btn.pack(side="right", padx=10)

        create_part_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_inventory_menu(create_part_window))

    def select_photo_file(self):
        """
        Opens a file dialog, allows the user to select an image,
        stores the path, and displays a preview in the label. (Restored)
        """
        file_path = filedialog.askopenfilename(
            title="Select Part Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_photo_path = file_path
            self._display_photo_preview(file_path)
        else:
            self.selected_photo_path = None
            self.photo_preview_label.config(text="No image selected", image='', compound=tk.NONE)
            self.preview_image_ref = None

    def _display_photo_preview(self, file_path):
        """Displays a small thumbnail of the selected photo using PIL. (Restored)"""
        try:
            # Open and resize the image for a thumbnail preview (e.g., 50x50 pixels)
            img = Image.open(file_path)
            target_size = (50, 50)
            img.thumbnail(target_size, Image.Resampling.LANCZOS) 
            
            # Convert to PhotoImage and store the reference to prevent garbage collection
            self.preview_image_ref = ImageTk.PhotoImage(img)
            
            # Update the label to show the image and the filename
            filename = os.path.basename(file_path)
            self.photo_preview_label.config(
                image=self.preview_image_ref, 
                text=f"Selected:\n{filename}", 
                compound=tk.LEFT, # Places text to the left of the image
                padx=5, 
                width=180
            )
            
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load or display image: {e}")
            self.photo_preview_label.config(text="Image Load Error", image='', compound=tk.NONE)
            self.preview_image_ref = None

    def handle_create_part_update(self):
        """Retrieves user input, handles image copying, and calls the data module to save the new part."""
        
        part_num = self.entry_part_num.get()
        desc = self.entry_description.get()
        price_str = self.entry_unit_price.get()
        
        if not part_num or not desc or not price_str:
            messagebox.showerror("Error", "Part Number, Description, and Price must be filled.")
            return
            
        # 1. Handle Image Copying if an image was selected (Restored)
        saved_image_path = ""
        original_image_path = self.selected_photo_path

        if original_image_path and os.path.exists(original_image_path):
            try:
                # Create a unique filename using the part number and original extension
                file_ext = os.path.splitext(original_image_path)[1]
                new_filename = f"{part_num}{file_ext}"
                target_path = os.path.join(IMAGE_DIR, new_filename)
                
                # Copy the file to the stable image directory
                shutil.copy2(original_image_path, target_path)
                
                # We save the relative path to keep the Excel data portable
                saved_image_path = os.path.join(IMAGE_DIR, new_filename)
                
            except Exception as e:
                messagebox.showwarning("File Error", f"Failed to save image file: {e}. Data will be saved without an image reference.")
                saved_image_path = ""
        else:
            # If no image was selected, ensure the path is saved as empty string/placeholder
            saved_image_path = "" # Or whatever placeholder your data system expects

        
        # 2. Call the function from your data module
        result_message = inventory_data.create_new_part_data(part_num, desc, price_str, saved_image_path)
        
        # 3. Display the result and clear fields
        if result_message.startswith("Error"):
            messagebox.showerror("Update Error", result_message)
        elif result_message.startswith("Update Successful"):
            messagebox.showinfo("Update Status", result_message)
            
            # Clear fields after successful update
            # FIX: Use delete() + insert('') trick for stability
            self.entry_part_num.delete(0, 'end')
            self.entry_part_num.insert(0, '')
            
            self.entry_description.delete(0, 'end')
            self.entry_description.insert(0, '')
            
            self.entry_unit_price.delete(0, 'end')
            self.entry_unit_price.insert(0, '')
            
            # Clear image preview (Restored)
            self.selected_photo_path = None
            # Update the label to the 'No image selected' state
            self.photo_preview_label.config(text="No image selected", image='', compound=tk.NONE, width=25)
            self.preview_image_ref = None # Clear the reference to free the image
        else:
            messagebox.showwarning("Status", result_message)
