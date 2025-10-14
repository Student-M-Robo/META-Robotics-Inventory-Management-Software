import pandas as pd
from tkinter import messagebox
import os
import sys 

# Define the file path for your inventory data
EXCEL_FILE_PATH = "C:/Users/Student/OneDrive/Desktop/Clarence_CW_Intern/Inventory Management System - WIP/Phase1-CreatePartTest.xlsx"

# Global variable to store the DataFrame in memory
INVENTORY_DF = pd.DataFrame() 

def initialize_inventory():
    """
    Attempts to load the Excel file into the global DataFrame. 
    If the file is not found, it creates an empty DataFrame with the required columns.
    """
    global INVENTORY_DF
    try:
        # Read the first column (index 0) of the Excel file as the DataFrame index (PartNumber).
        df = pd.read_excel(EXCEL_FILE_PATH, index_col=0) 
        
        # Ensure the index (PartNumber) is treated as a string
        df.index = df.index.astype(str)
        
        # Ensure the 'ImagePath' column exists, even if empty
        if 'ImagePath' not in df.columns:
            df['ImagePath'] = ""
            
        INVENTORY_DF = df
        return True
    except FileNotFoundError:
        # If the file is missing, initialize an empty DataFrame
        messagebox.showerror("Data Error", f"Inventory Excel file not found at: {EXCEL_FILE_PATH}")
        INVENTORY_DF = pd.DataFrame(columns=['Description', 'UnitPrice', 'ImagePath'])
        INVENTORY_DF.index.name = 'PartNumber'
        return False
    except Exception as e:
        messagebox.showerror("Data Error", f"Error loading Excel file: {e}\nCheck your column names.")
        return False

def save_inventory():
    """Saves the current state of the global DataFrame back to the Excel file."""
    global INVENTORY_DF
    try:
        # Saving the DataFrame. The ImagePath column now stores the file path string.
        INVENTORY_DF.to_excel(EXCEL_FILE_PATH, sheet_name='Inventory', index=True)
        return True
    except Exception as e:
        # Log the exact Python error to the console for debugging
        print(f"ERROR: Could not save data to Excel. Error details: {e}", file=sys.stderr)
        messagebox.showerror("Save Error", "Could not save data to Excel. Check if the file is open.")
        return False

# Core Data Management Functions
def create_new_part_data(part_num, desc, price_str, image_path):
    """
    Handles validation and adds a new part record, saving the image file path string.
    """
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    if not part_num or not desc or not price_str:
        return "Error: All fields must be filled."

    if part_num in INVENTORY_DF.index:
        return "A similar Part already exist" 
    
    try:
        # 1. Price validation and formatting
        price_float = float(price_str)
        if price_float < 0:
            raise ValueError("Price cannot be negative.")
        formatted_price = f"${price_float:.2f}"
        
        # 2. Create the new row including the file path string
        new_row = pd.Series({
            'Description': desc,
            'UnitPrice': formatted_price,
            'ImagePath': image_path # This cell now stores the relative file path, e.g., 'part_images/3001.png'
        }, name=part_num)
        
        # Use pd.concat for reliable row addition
        INVENTORY_DF = pd.concat([INVENTORY_DF, new_row.to_frame().T]).copy()
        
        # 3. Attempt to save the updated data to the Excel file
        if save_inventory():
            return "Update Successful"
        else:
            # If save fails, remove the newly added row to maintain consistency
            INVENTORY_DF = INVENTORY_DF.drop(index=part_num, errors='ignore').copy()
            return "Error saving data. Part not created."
            
    except ValueError:
        return "Error: Unit Price must be a valid number (e.g., 0.20)."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Run initialization when the module is first imported
initialize_inventory()