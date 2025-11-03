# -------------------------------------------#
# inventory_data.py - MySQL Integration (Updated for Stock Quantity)
# -------------------------------------------#

import pandas as pd
from tkinter import messagebox
import mysql.connector 

# --- Database Configuration ---

DB_CONFIG = {
    'user': 'root',        
    'password': 'P@ssw0rd',  
    'host': '127.0.0.1',          
    'database': 'meta_robotics_inventory'
}


# Global variable to store the DataFrame in memory (cache)
INVENTORY_DF = pd.DataFrame() 

# --- Connection and Query Helpers ---

def get_db_connection():
    """Helper function to establish a database connection."""
    try:
        # Establish the connection using the configuration dictionary
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        # Check for specific errors like wrong password or unknown database
        messagebox.showerror("Database Connection Error", f"Failed to connect to MySQL: {err}")
        return None

def _execute_query(query, params=None, is_commit=False):
    """
    A unified function for executing SQL commands (INSERT, UPDATE, DELETE, etc.).
    Returns: True on success, False on error.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    
    try:
        # Execute the query with optional parameters
        cursor.execute(query, params or ())
        
        if is_commit:
            conn.commit()
            
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("DB Operation Error", f"SQL Error during execution: {err}")
        conn.rollback() # Rollback changes if an error occurred
        return False
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

# --- Core Data Management Functions ---

def initialize_inventory():
    """
    Loads all data from the MySQL table into the global DataFrame.
    MODIFIED to include the Quantity column.
    """
    global INVENTORY_DF
    conn = get_db_connection()
    if conn is None:
        # If connection fails, create an empty DF placeholder with all expected columns
        INVENTORY_DF = pd.DataFrame(columns=['Description', 'UnitPrice', 'Quantity', 'ImagePath'])
        INVENTORY_DF.index.name = 'PartNumber'
        return False
        
    try:
        # UPDATED: Query now selects the new 'Quantity' column
        query = "SELECT PartNumber, Description, UnitPrice, Quantity, ImagePath FROM inventory"
        
        # Read the table directly into the DataFrame, using PartNumber as index
        INVENTORY_DF = pd.read_sql(query, conn, index_col='PartNumber') 
        
        # Ensure the index (PartNumber) is treated as a string
        INVENTORY_DF.index = INVENTORY_DF.index.astype(str)
        
        # CRITICAL: Ensure Quantity column is present and is an integer type for stock calculations
        if 'Quantity' in INVENTORY_DF.columns:
            # Fill potential missing values with 0 and convert to integer
            INVENTORY_DF['Quantity'] = INVENTORY_DF['Quantity'].fillna(0).astype(int)
        else:
             # Fallback: If Quantity column is missing from the DB table (ALTER failed), initialize to 0
             messagebox.showwarning("Data Warning", "The 'Quantity' column was missing. Initializing to zero.")
             INVENTORY_DF['Quantity'] = 0
             INVENTORY_DF['Quantity'] = INVENTORY_DF['Quantity'].astype(int)
             
        # Re-format UnitPrice for display (assuming it's stored as float in DB)
        if 'UnitPrice' in INVENTORY_DF.columns:
             INVENTORY_DF['UnitPrice'] = INVENTORY_DF['UnitPrice'].apply(lambda x: f"${x:.2f}" if isinstance(x, (int, float)) else x)

        return True
    except pd.io.sql.DatabaseError as e:
        messagebox.showerror("Data Error", f"Error querying MySQL table: {e}")
        INVENTORY_DF = pd.DataFrame(columns=['Description', 'UnitPrice', 'Quantity', 'ImagePath']) # Include Quantity in placeholder
        INVENTORY_DF.index.name = 'PartNumber'
        return False
    finally:
        # Ensure the connection is closed
        if conn and conn.is_connected():
            conn.close()

def get_part_data(part_num):
    """
    Retrieves all data for a given part number from the in-memory DataFrame.
    MODIFIED to include the Quantity field.
    """
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    # We rely on the in-memory DataFrame for fast lookups
    if part_num in INVENTORY_DF.index:
        # Return the data as a dictionary (Series)
        return INVENTORY_DF.loc[part_num].to_dict()
    else:
        return None

def update_part_data(part_num, desc, price_str, image_path):
    """
    Updates the record in the DB and refreshes the in-memory DataFrame.
    Note: Does NOT update Quantity, as Quantity is only changed via Stock Received/Issued.
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
        
        # 2. Execute SQL UPDATE
        sql = """
            UPDATE inventory 
            SET Description = %s, UnitPrice = %s, ImagePath = %s
            WHERE PartNumber = %s
        """
        params = (desc, price_float, image_path, part_num)
        
        if _execute_query(sql, params, is_commit=True):
            # 3. Update the existing row in the in-memory DataFrame (cache)
            formatted_price = f"${price_float:.2f}"
            INVENTORY_DF.loc[part_num, 'Description'] = desc
            INVENTORY_DF.loc[part_num, 'UnitPrice'] = formatted_price
            INVENTORY_DF.loc[part_num, 'ImagePath'] = image_path 
            
            return "Update Successful"
        else:
            return "Error saving data. Changes were not committed to the database."
            
    except ValueError:
        return "Error: Unit Price must be a valid number (e.g., 0.20)."
    except Exception as e:
        return f"An unexpected error occurred during update: {e}"

def delete_part_data(part_num):
    """Deletes a part record from the database and the in-memory DataFrame."""
    global INVENTORY_DF
    part_num = str(part_num).strip()
    
    if part_num not in INVENTORY_DF.index:
        return "Error: Part Number not found for deletion."
    
    try:
        # 1. Execute SQL DELETE
        sql = "DELETE FROM inventory WHERE PartNumber = %s"
        params = (part_num,)
        
        if _execute_query(sql, params, is_commit=True):
            # 2. Delete the row from the in-memory DataFrame (cache)
            INVENTORY_DF = INVENTORY_DF.drop(index=part_num, errors='ignore').copy()
            return "Deletion Successful"
        else:
            return "Error saving data. Part could not be deleted from the database."
            
    except Exception as e:
        return f"An unexpected error occurred during deletion: {e}"


def create_new_part_data(part_num, desc, price_str, image_path):
    """
    Adds a new part record to the DB and refreshes the in-memory DataFrame.
    MODIFIED to initialize Quantity to 0.
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
        
        # 2. Execute SQL INSERT (Updated to include Quantity)
        sql = """
            INSERT INTO inventory (PartNumber, Description, UnitPrice, Quantity, ImagePath)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Parameters for the query. Quantity is initialized to 0.
        params = (part_num, desc, price_float, 0, image_path) 

        if _execute_query(sql, params, is_commit=True):
            # 3. Add to the in-memory DataFrame (cache) (Updated to include Quantity)
            formatted_price = f"${price_float:.2f}"
            new_row = pd.Series({
                'Description': desc,
                'UnitPrice': formatted_price,
                'Quantity': 0, # Initialize to 0
                'ImagePath': image_path 
            }, name=part_num)
            
            # Use pd.concat for reliable row addition
            INVENTORY_DF = pd.concat([INVENTORY_DF, new_row.to_frame().T]).copy()
            # Ensure the new Quantity column is treated as integer type for math operations
            INVENTORY_DF['Quantity'] = INVENTORY_DF['Quantity'].astype(int)
            
            return "Update Successful"
        else:
            return "Error saving data. Part not created in the database."
            
    except ValueError:
        return "Error: Unit Price must be a valid number (e.g., 0.20)."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- NEW STOCK MANAGEMENT FUNCTION ---

def update_stock_quantity(part_num, quantity_received):
    """
    Increments the Quantity for a given PartNumber in DB and DataFrame.
    """
    global INVENTORY_DF

    part_num = part_num.strip()

    # 1. Validation
    if part_num not in INVENTORY_DF.index:
        return "Error: Part Number not found."
    try:
        qty_change = int(quantity_received)
        if qty_change <= 0:
            return "Error: Quantity received must be a positive whole number."
    except ValueError:
        return "Error: Quantity must be a valid whole number."

    # Current quantity from the in-memory cache
    current_qty = INVENTORY_DF.loc[part_num, 'Quantity']
    new_qty = int(current_qty) + qty_change
    
    # 2. Update the database using the new total quantity
    sql = "UPDATE inventory SET Quantity = %s WHERE PartNumber = %s"
    params = (new_qty, part_num)
    
    if _execute_query(sql, params, is_commit=True):
        # 3. Update the in-memory DataFrame (cache)
        INVENTORY_DF.loc[part_num, 'Quantity'] = new_qty
        return f"Stock updated successfully. New Quantity: {new_qty}"
    else:
        # If DB update fails, the cache remains untouched for consistency
        return "Error: Database update failed."
    

def issue_stock_quantity(part_num, quantity_issued):
    """
    Decrements the Quantity for a given PartNumber in DB and DataFrame,
    checking for sufficient stock.
    """
    global INVENTORY_DF

    part_num = part_num.strip()

    # 1. Validation
    if part_num not in INVENTORY_DF.index:
        return "Error: Part Number not found."
    try:
        qty_change = int(quantity_issued)
        # Quantity issued must be a positive whole number
        if qty_change <= 0:
            return "Error: Quantity issued must be a positive whole number."
    except ValueError:
        return "Error: Quantity must be a valid whole number."

    # Current quantity from the in-memory cache
    current_qty = INVENTORY_DF.loc[part_num, 'Quantity']
    
    # CRITICAL: Check for sufficient stock before issuing
    if qty_change > int(current_qty):
        return f"Error: Insufficient stock. Available: {current_qty}, Requested: {qty_change}"

    # Calculate new quantity (SUBTRACTION)
    new_qty = int(current_qty) - qty_change
    
    # 2. Update the database using the new total quantity
    sql = "UPDATE inventory SET Quantity = %s WHERE PartNumber = %s"
    params = (new_qty, part_num)
    
    if _execute_query(sql, params, is_commit=True):
        # 3. Update the in-memory DataFrame (cache)
        INVENTORY_DF.loc[part_num, 'Quantity'] = new_qty
        return f"Stock issued successfully. New Quantity: {new_qty}"
    else:
        # If DB update fails, the cache remains untouched for consistency
        return "Error: Database update failed."

# Run initialization when the module is first imported
initialize_inventory()