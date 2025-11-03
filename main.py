# -------------------------------------------#
# Main Python File
# -------------------------------------------#

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import warnings
# Suppress all UserWarnings globally.
warnings.filterwarnings("ignore", category=UserWarning)

from inventory_function import InventoryManagementWindow 

logo_image_ref = None 

# Functions Main Menu Operations

def open_inventory_management():
    """Opens the Inventory Management sub-window by calling the class method."""
    global inventory_manager_instance
    inventory_manager_instance.open_window() 

def open_order_placement():
    """Creates a placeholder for the Order Placement sub-menu (Page 1)."""
    messagebox.showinfo("Order Placement", "Placeholder for Order Placement")
    
def close_app():
    """Closes the entire application (Page 1) and confirms exit."""
    if messagebox.askyesno("Exit Application", "Are you sure you want to close?"):
        root.quit()

# Main Window Setup

root = tk.Tk()
root.title("Meta Robotics Inventory Management System")

# 1. Define the desired window size
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 600

# 2. Get the screen size
root.update_idletasks() 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center position
position_right = int(screen_width/2 - WINDOW_WIDTH/2)
position_down = int(screen_height/2 - WINDOW_HEIGHT/2)

# Set the window size and position
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_down}')

# Configure the grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3) # Center column for content
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1) # Last row for closing button/padding

# Set background to white
root.config(bg="white")

# 3. Load and Display Logo (or placeholder)

# Placeholder image loading - CHANGE THIS PATH TO YOUR ACTUAL LOGO FILE
LOGO_PATH = "Meta Robotics Logo.png" 
LOGO_SIZE = (400, 150)

try:
    original_image = Image.open(LOGO_PATH)
    resized_image = original_image.resize(LOGO_SIZE, Image.LANCZOS)
    logo_image_ref = ImageTk.PhotoImage(resized_image) # Must store reference
    
    # Display the logo
    tk.Label(root, image=logo_image_ref, bg="white").grid(
        row=0, column=1, pady=10, sticky="s"
    )
    
except FileNotFoundError:
    # Display placeholder if logo is missing
    tk.Label(root, text="[LOGO MISSING]", font=("Arial", 16, "bold"), bg="white", fg="red").grid(
        row=0, column=1, pady=10, sticky="s"
    )
    tk.Label(root, text="**Update LOGO_PATH in main.py**", font=("Arial", 8), bg="white", fg="red").grid(
        row=1, column=1
    )
    
# 4. Determine Title Row based on image loading success
if logo_image_ref:
    title_row = 1
else:
    title_row = 2
    
# Main System Title
main_title = tk.Label(root, text="Meta Robotics\n Inventory Management System", font=("Arial", 24, "bold"), bg="white", fg="#004d99")

main_title.grid(
    row=title_row, column=1, pady=20, sticky="s"
)

# 5. Inventory Management Button
inventory_btn = tk.Button(root, text="Inventory Management", command=open_inventory_management,
                         bg="#a3d9ff", fg="black", font=("Arial", 20, "bold"))
inventory_btn.grid(
    row=title_row + 1, column=1, padx=100, pady=40, sticky="nsew" 
)

# 6. Order Placement Button
order_btn = tk.Button(root, text="Order Placement", command=open_order_placement,
                      bg="#a3d9ff", fg="black", font=("Arial", 20, "bold"))
order_btn.grid(
    row=title_row + 2, column=1, padx=100, pady=10, sticky="nsew"
)

# 7. Close App Button
close_btn = tk.Button(root, text="Close", command=close_app,
                      bg="#ff9999", fg="black", font=("Arial", 18, "bold"))
close_btn.grid(
    row=title_row + 4, column=1, padx=40, pady=20, sticky="s"
)

# Create an instance of the InventoryManagementWindow class
# This makes it available for the 'open_inventory_management' function
inventory_manager_instance = InventoryManagementWindow(root)

# Start the application main loop
root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()