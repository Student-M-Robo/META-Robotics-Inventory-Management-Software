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
        # Saving the DataFrame.
        INVENTORY_DF.to_excel(EXCEL_FILE_PATH, sheet_name='Inventory', index=True)
        return True
    except Exception as e:
        # Log the exact Python error to the console for debugging
        print(f"ERROR: Could not save data to Excel. Error details: {e}", file=sys.stderr)
        messagebox.showerror("Save Error", "Could not save data to Excel. Check if the file is open.")
        return False

# --- New Functions for Edit/Delete ---

def get_part_data(part_num):
    """Retrieves all data for a given part number."""
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    if part_num in INVENTORY_DF.index:
        # Return the data as a dictionary (Series)
        return INVENTORY_DF.loc[part_num].to_dict()
    else:
        return None

def update_part_data(part_num, desc, price_str, image_path):
    """
    Validates and updates the record for an existing part.
    """
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    if part_num not in INVENTORY_DF.index:
        return "Error: Part Number not found for update."
        
    try:
        # 1. Price validation and formatting
        price_float = float(price_str.replace('$', '').replace(',', '').strip())
        if price_float < 0:
            raise ValueError("Price cannot be negative.")
        formatted_price = f"${price_float:.2f}"
        
        # 2. Update the existing row
        INVENTORY_DF.loc[part_num, 'Description'] = desc
        INVENTORY_DF.loc[part_num, 'UnitPrice'] = formatted_price
        INVENTORY_DF.loc[part_num, 'ImagePath'] = image_path 
        
        # 3. Attempt to save the updated data to the Excel file
        if save_inventory():
            return "Update Successful"
        else:
            # Note: Reversing changes is complex. If save fails, we rely on the
            # user re-initializing the app or manual correction.
            return "Error saving data. Changes were made in memory but could not be saved to file."
            
    except ValueError:
        return "Error: Unit Price must be a valid number (e.g., 0.20)."
    except Exception as e:
        return f"An unexpected error occurred during update: {e}"

def delete_part_data(part_num):
    """Deletes a part record from the DataFrame."""
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    if part_num not in INVENTORY_DF.index:
        return "Error: Part Number not found for deletion."
    
    try:
        # Delete the row
        INVENTORY_DF = INVENTORY_DF.drop(index=part_num, errors='ignore').copy()
        
        # Attempt to save the updated data to the Excel file
        if save_inventory():
            return "Deletion Successful"
        else:
            # If save fails, re-add the row (if possible) or warn user
            # Since dropping is fast, we prioritize warning the user to check file status.
            return "Error saving data. Part was deleted in memory but could not be saved to file."
            
    except Exception as e:
        return f"An unexpected error occurred during deletion: {e}"


# --- Existing create_new_part_data function (kept for reference) ---
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