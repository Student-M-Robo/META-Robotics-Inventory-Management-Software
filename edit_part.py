import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, filedialog, ttk
from PIL import Image, ImageTk 
import os
import shutil

# Import data handling functions and constants
import inventory_data 

# Define a stable directory to store all part images
IMAGE_DIR = "part_images" 

class EditPartWindow:
    def __init__(self, master_root, inventory_window_instance):
        """Initializes the window with references to the main root and the inventory manager."""
        self.master_root = master_root
        # Store the instance of the InventoryManagementWindow to use its helper methods
        self.inventory_window_instance = inventory_window_instance 
        
        # State variables
        self.current_part_num = None
        self.selected_photo_path = None 
        self.preview_image_ref = None   
        
        # Entry widget references
        self.entry_part_num_search = None
        self.entry_description = None
        self.entry_unit_price = None
        self.photo_preview_label = None 
        self.delete_btn = None
        self.update_btn = None
        
        # List of widgets to enable/disable easily
        self.editable_widgets = []
        
        # Ensure image directory exists
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

    def center_window(self, window, width, height):
        """Calculates and sets the geometry string to center the window on the screen."""
        self.inventory_window_instance.center_window(window, width, height)

    def open_window(self):
        """Creates and displays the Edit Part Information sub-window."""
        
        # Reset state when opening
        self.current_part_num = None
        self.selected_photo_path = None
        self.preview_image_ref = None
        
        self.edit_part_window = Toplevel(self.master_root)
        self.edit_part_window.title("Edit Part Information")
        
        # Centering Logic for Edit Part Window (700x600)
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 600
        self.center_window(self.edit_part_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.edit_part_window.config(bg="white")
        
        # Grid Configuration 
        self.edit_part_window.columnconfigure(0, weight=1) 
        self.edit_part_window.columnconfigure(1, weight=5) # Central content column
        self.edit_part_window.columnconfigure(2, weight=1) 
        for i in range(10):
            self.edit_part_window.rowconfigure(i, weight=1)

        # Header
        header = Label(self.edit_part_window, text="Edit Part Information", 
                              font=("Arial", 20, "bold"), bg="white", fg="#004d99")
        header.grid(row=0, column=1, pady=10, sticky="n")

        # Search Frame
        search_frame = Frame(self.edit_part_window, bg="#f0f0f0", bd=2, relief="groove")
        search_frame.grid(row=1, column=1, sticky="ew", padx=30, pady=10)
        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=3)
        search_frame.columnconfigure(2, weight=1)

        Label(search_frame, text="Enter Part Number:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )
        self.entry_part_num_search = Entry(search_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_part_num_search.grid(row=0, column=1, sticky="ew", pady=10)
        
        search_btn = Button(search_frame, text="SEARCH", font=("Arial", 12, "bold"), 
                            bg="#004d99", fg="white", 
                            command=self.handle_search_part)
        search_btn.grid(row=0, column=2, sticky="w", padx=10, pady=10)


        # Part Information Frame (Initially Empty/Disabled)
        info_frame = Frame(self.edit_part_window, bg="white")
        info_frame.grid(row=2, column=1, rowspan=4, sticky="nsew", padx=30, pady=10)
        info_frame.columnconfigure(0, weight=1) # Label column
        info_frame.columnconfigure(1, weight=3) # Entry column
        for i in range(5):
            info_frame.rowconfigure(i, weight=1)
        
        # 1. Part Number Display
        Label(info_frame, text="Part Number:", font=("Arial", 12, "bold"), bg="white").grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )
        self.part_num_display = Label(info_frame, text="N/A", font=("Arial", 12), bg="white", fg="blue")
        self.part_num_display.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # 2. Description Entry
        Label(info_frame, text="Part Description:", font=("Arial", 12), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=5
        )
        self.entry_description = Entry(info_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_description.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # 3. Unit Price Entry
        Label(info_frame, text="Unit Price:", font=("Arial", 12), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=5
        )
        self.entry_unit_price = Entry(info_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_unit_price.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # 4. Image Section
        Label(info_frame, text="Part Image:", font=("Arial", 12), bg="white").grid(
            row=3, column=0, sticky="ne", padx=10, pady=5
        )
        image_edit_frame = Frame(info_frame, bg="white")
        image_edit_frame.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        image_edit_frame.columnconfigure(0, weight=1)
        image_edit_frame.columnconfigure(1, weight=1)
        
        # The Preview Label (Default size based on fixed text/character units)
        self.photo_preview_label = Label(image_edit_frame, text="No image loaded", 
                                             font=("Arial", 10), bg="#f0f0f0", height=3, width=25, relief="solid")
        self.photo_preview_label.grid(row=0, column=1, sticky="ew", padx=10)
        
        # UPLOAD button
        upload_btn = Button(image_edit_frame, text="CHANGE PHOTO", font=("Arial", 12), bg="#d9d9d9", 
                            command=self.select_photo_file) 
        upload_btn.grid(row=0, column=0, sticky="w", padx=10)

        # Store editable widgets (including the button for mass enable/disable)
        self.editable_widgets = [
            self.entry_description, self.entry_unit_price, upload_btn
        ]

        # Control Buttons
        control_frame = Frame(self.edit_part_window, bg="white")
        control_frame.grid(row=6, column=1, sticky="e", padx=30, pady=10)
        
        self.delete_btn = Button(control_frame, text="DELETE", font=("Arial", 14, "bold"), 
                                     bg="#ff6666", fg="white", 
                                     command=self.handle_delete_part, state=tk.DISABLED)
        self.delete_btn.pack(side="left", padx=10)
        
        self.update_btn = Button(control_frame, text="UPDATE", font=("Arial", 14, "bold"), 
                                     bg="#4CAF50", fg="white", 
                                     command=self.handle_update_part, state=tk.DISABLED)
        self.update_btn.pack(side="right", padx=10)
        
        # Navigation Buttons
        nav_frame = Frame(self.edit_part_window, bg="white")
        nav_frame.grid(row=7, column=1, pady=(0, 10))
        
        back_btn = Button(nav_frame, text="Back Page", 
                            command=lambda: self.inventory_window_instance.return_to_inventory_menu(self.edit_part_window),
                            bg="#cccccc", font=("Arial", 10))
        back_btn.pack(side="right", padx=10)
        
        menu_btn = Button(nav_frame, text="MENU", 
                            command=lambda: self.inventory_window_instance.return_to_main_menu_from_sub(self.edit_part_window),
                            bg="#cccccc", font=("Arial", 10))
        menu_btn.pack(side="right", padx=10)

        # Initial state setup
        self._set_form_state(tk.DISABLED)
        self.edit_part_window.protocol("WM_DELETE_WINDOW", lambda: self.inventory_window_instance.return_to_inventory_menu(self.edit_part_window))

    def _set_form_state(self, state):
        """Enables or disables the editable input fields and control buttons."""
        for widget in self.editable_widgets:
            widget.config(state=state)
        self.update_btn.config(state=state)
        self.delete_btn.config(state=state)

    def _clear_form(self):
        """Clears all input fields and resets internal state/display."""
        self.current_part_num = None
        
        self.part_num_display.config(text="N/A")
        
        self.entry_description.delete(0, 'end')
        self.entry_description.insert(0, '')
        
        self.entry_unit_price.delete(0, 'end')
        self.entry_unit_price.insert(0, '')
        
        self.selected_photo_path = None
        # Revert label to default text-based size when clearing
        self.photo_preview_label.config(text="No image loaded", image='', compound=tk.NONE, width=25, height=3, padx=0)
        self.preview_image_ref = None

    def handle_search_part(self):
        """Searches for the part number and loads the data into the form."""
        search_num = self.entry_part_num_search.get().strip()
        
        if not search_num:
            messagebox.showwarning("Search", "Please enter a Part Number to search.")
            return

        # Clear previous state
        self._clear_form()
        self._set_form_state(tk.DISABLED)

        # Call the data module to get the part data
        part_data = inventory_data.get_part_data(search_num)

        if part_data is None:
            messagebox.showerror("Search Error", f"Part Number '{search_num}' not found.")
            return

        # Store the current part number
        self.current_part_num = search_num
        
        # Enable the form and buttons
        self._set_form_state(tk.NORMAL)
        
        # Display static part number
        self.part_num_display.config(text=self.current_part_num)

        # Load data into fields (Description, Price)
        self.entry_description.insert(0, part_data['Description'])
        # Clean price by removing '$' for easier editing
        price_clean = str(part_data['UnitPrice']).replace('$', '').replace(',', '')
        self.entry_unit_price.insert(0, price_clean)
        
        # Load Image
        image_path_saved = part_data['ImagePath']
        if image_path_saved:
            # Check if the file exists in the relative path
            full_path = image_path_saved
            if os.path.exists(full_path):
                self.selected_photo_path = full_path # Temporarily use the saved path as the 'selected' path
                self._display_photo_preview(full_path)
            else:
                messagebox.showwarning("Image Warning", f"Image file not found at saved path: {full_path}")
                self.selected_photo_path = "" # Clear the path if the file is missing
        else:
            self.selected_photo_path = ""
        
        # Ensure focus is on the description field after a successful search
        self.entry_description.focus_set()


    def select_photo_file(self):
        """Opens a file dialog for selecting a new image."""
        file_path = filedialog.askopenfilename(
            title="Select New Part Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_photo_path = file_path # Store the new absolute path
            self._display_photo_preview(file_path)


    def _display_photo_preview(self, file_path):
        """Displays a small thumbnail of the selected photo using PIL."""
        try:
            img = Image.open(file_path)
            target_size = (100, 100)
            img.thumbnail(target_size, Image.Resampling.LANCZOS) 
            
            self.preview_image_ref = ImageTk.PhotoImage(img)

            self.photo_preview_label.config(
                image=self.preview_image_ref, 
                text="",          
                compound=tk.NONE, 
                padx=0,           
                width=50,         
                height=50         
            )
            
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load or display image: {e}")
            self.photo_preview_label.config(text="Image Load Error", image='', compound=tk.NONE)
            # Safe way to handle missing part_num index
            try:
                self.selected_photo_path = inventory_data.INVENTORY_DF.loc[self.current_part_num, 'ImagePath'] 
            except Exception:
                self.selected_photo_path = None
            self.preview_image_ref = None


    def handle_update_part(self):
        """Handles data validation, image copy, and calls the data module to update the part."""
        
        if not self.current_part_num:
            messagebox.showerror("Error", "No part loaded for update.")
            return

        part_num = self.current_part_num
        desc = self.entry_description.get()
        price_str = self.entry_unit_price.get()
        
        if not desc or not price_str:
            messagebox.showerror("Error", "Description and Price must be filled.")
            return

        # 1. Handle Image Copying/Update Logic
        # Get the currently saved image path from the DataFrame
        saved_image_path = inventory_data.INVENTORY_DF.loc[part_num, 'ImagePath'] 
        original_image_path_selected = self.selected_photo_path 
        image_path_to_save = saved_image_path

        # Check if a new file was selected (i.e., the path is NOT the one currently saved)
        if original_image_path_selected and original_image_path_selected != saved_image_path:
            # Check if the path selected is outside the part_images directory (i.e., a new file upload)
            if not original_image_path_selected.startswith(os.path.abspath(IMAGE_DIR)):
                try:
                    # 1a. Remove old image file if it exists and a new image is being uploaded
                    if saved_image_path and os.path.exists(saved_image_path):
                        os.remove(saved_image_path)
                    
                    # 1b. Create new filename using the part number and original extension
                    file_ext = os.path.splitext(original_image_path_selected)[1]
                    new_filename = f"{part_num}{file_ext}"
                    target_path = os.path.join(IMAGE_DIR, new_filename)
                    
                    # 1c. Copy the new file
                    shutil.copy2(original_image_path_selected, target_path)
                    
                    # Update the path to be saved in the Excel file (relative path)
                    image_path_to_save = target_path
                    
                except Exception as e:
                    messagebox.showwarning("File Error", f"Failed to save new image file: {e}. Data will be updated without an image reference.")
                    image_path_to_save = ""
            # Else: The user selected the *same* image that was already saved. image_path_to_save remains saved_image_path
        
        
        # 2. Call the data module to update the data
        result_message = inventory_data.update_part_data(part_num, desc, price_str, image_path_to_save)
        
        # 3. Display the result
        if result_message.startswith("Error"):
            messagebox.showerror("Update Error", result_message)
        elif result_message.startswith("Update Successful"):
            messagebox.showinfo("Update Status", result_message)
            self._clear_form()
            self.entry_part_num_search.delete(0, 'end')
            self._set_form_state(tk.DISABLED)
        else:
            messagebox.showwarning("Status", result_message)

    def handle_delete_part(self):
        """Prompts for confirmation and calls the data module to delete the part."""
        
        if not self.current_part_num:
            messagebox.showerror("Error", "No part loaded for deletion.")
            return

        part_num = self.current_part_num
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete Part Number {part_num}?"):
            # 1. Get the image path for cleanup BEFORE deletion from DF
            image_path_to_delete = inventory_data.INVENTORY_DF.loc[part_num, 'ImagePath']
            
            # 2. Call the data module to delete the data
            result_message = inventory_data.delete_part_data(part_num)
            
            # 3. Handle result and cleanup
            if result_message.startswith("Error"):
                messagebox.showerror("Deletion Error", result_message)
            elif result_message.startswith("Deletion Successful"):
                
                # 4. Attempt to delete the associated image file
                if image_path_to_delete and os.path.exists(image_path_to_delete):
                    try:
                        os.remove(image_path_to_delete)
                    except Exception as e:
                        messagebox.showwarning("Cleanup Warning", f"Could not delete associated image file: {e}")

                messagebox.showinfo("Deletion Status", result_message)
                self._clear_form()
                self.entry_part_num_search.delete(0, 'end')
                self._set_form_state(tk.DISABLED)
            else:
                messagebox.showwarning("Status", result_message)