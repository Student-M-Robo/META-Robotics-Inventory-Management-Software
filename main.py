# -------------------------------------------#
# Main Python File
# -------------------------------------------#

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 


# Assuming these modules/files exist in your project
import inventory_data
from inventory_function import InventoryManagementWindow 

logo_image_ref = None 

# Functions Main Menu Operations

def open_inventory_management():
    """Opens the Inventory Management sub-window by calling the class method."""
    global inventory_manager_instance
    # Ensure the main window is withdrawn before opening the new one for better focus management
    # root.withdraw() # Optional: hide the main window
    inventory_manager_instance.open_window() 

def open_order_placement():
    """Creates a placeholder for the Order Placement sub-menu (Page 1)."""
    messagebox.showinfo("Order Placement", "Placeholder for Order Placement")
def close_app():
    """Closes the entire application (Page 1) and confirms exit."""
    # Ensure data is saved before closing the app
    inventory_data.save_inventory()
    if messagebox.askyesno("Exit Application", "Are you sure you want to close?"):
        root.quit()

# Main Window Setup

root = tk.Tk()
root.title("Meta Robotic Inventory Management System")

# 1. Define the desired window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# 2. Get the screen size
root.update_idletasks() 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 3. Calculate the central position (x and y)
# Formula: (Screen Dimension / 2) - (Window Dimension / 2)
center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

# 4. Set the geometry to the calculated position
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")


root.config(bg="white")

# Initialize the Inventory Management class instance globally
inventory_manager_instance = InventoryManagementWindow(root)

# 1. Configure Grid Weights for Resizing
root.columnconfigure(0, weight=1) 
root.columnconfigure(1, weight=3) 
root.columnconfigure(2, weight=1) 

root.rowconfigure(0, weight=1) 
root.rowconfigure(1, weight=1) 
root.rowconfigure(2, weight=2) 
root.rowconfigure(3, weight=2) 
root.rowconfigure(4, weight=1) 

IMAGE_PATH = "C:/Users/Student/OneDrive/Desktop/Clarence_CW_Intern/Inventory Management System - WIP/Meta Robotics Logo.png"

try:
    original_image = Image.open(IMAGE_PATH)
    height_ratio = 100 / original_image.size[1]
    new_width = int(original_image.size[0] * height_ratio)
    resized_image = original_image.resize((new_width, 100), Image.Resampling.LANCZOS)
    logo_image_ref = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=logo_image_ref, bg="white")
    image_label.grid(row=0, column=1, pady=10, sticky="s") 

except FileNotFoundError:
    # Fallback to text if the image isn't found
    tk.Label(root, text="[LOGO MISSING]", font=("Arial", 16, "bold"), bg="white", fg="red").grid(
        row=0, column=1, pady=10, sticky="s"
    )
    tk.Label(root, text="**Update IMAGE_PATH in main_app.py**", font=("Arial", 8), bg="white", fg="red").grid(
        row=1, column=1
    )
    
# 3. Determine Title Row based on image loading success
if logo_image_ref:
    title_row = 1
else:
    title_row = 2
    
# Main System Title
main_title = tk.Label(root, text="Meta Robotic Management System", font=("Arial", 24, "bold"), bg="white", fg="#004d99")

main_title.grid(
    row=title_row, column=1, pady=20, sticky="s"
)

# 4. Inventory Management Button
inventory_btn = tk.Button(root, text="Inventory Management", command=open_inventory_management,
                         bg="#a3d9ff", fg="black", font=("Arial", 16, "bold"))
inventory_btn.grid(
    row=title_row + 1, column=1, padx=40, pady=10, sticky="nsew" 
)

# 5. Order Placement Button
order_btn = tk.Button(root, text="Order Placement", command=open_order_placement,
                      bg="#a3d9ff", fg="black", font=("Arial", 16, "bold"))
order_btn.grid(
    row=title_row + 2, column=1, padx=40, pady=10, sticky="nsew"
)

# 6. CLOSE Button
close_btn = tk.Button(root, text="CLOSE", command=close_app,
                      width=10, bg="#ff6666", fg="white", font=("Arial", 12, "bold"))
close_btn.grid(
    row=title_row + 3, column=1, pady=20, sticky="n"
)

# 7. Start the Tkinter event loop
root.mainloop()