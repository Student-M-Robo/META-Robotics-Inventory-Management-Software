# Meta Robotics Inventory Management

Desktop inventory manager built with Tkinter and MySQL. The app provides a simple GUI for creating and editing parts, tracking received/issued stock, viewing stock levels, and printing basic reports. Data is persisted in a MySQL/TiDB table and cached in memory with pandas. Part images are stored locally.

## Main Components
- `main.py` – Entry point; renders the main menu and logo, wires buttons to inventory management.
- `inventory_function.py` – Main inventory window with navigation to sub-windows.
- `inventory_data.py` – Database layer using `mysql-connector-python`; loads/caches the `inventory` table (columns: PartNumber, Description, UnitPrice, Quantity, ImagePath) into a pandas DataFrame and exposes helpers for CRUD + quantity updates. Uses `isrgrootx1.pem` for SSL CA.
- `stock_received.py` – Receive stock: search part, view details/image, add quantity.
- `stock_issued.py` – Issue stock: validate available quantity before decrementing.
- `stock_enquiry.py` – Look up parts and view details.
- `edit_part.py` – Edit existing part info and image.
- `print_report.py` – Generate a simple report view.
- `part_images/` – Local storage for uploaded part photos.

## Requirements
- Python 3.13 with Tk support.
- MySQL/TiDB instance reachable with credentials configured in `inventory_data.py`.
- Installed Python packages (`requirements.txt`): `mysql-connector-python`, `pandas`, `Pillow`, `requests`.

## Setup
```bash
cd /path/to/META-Robotics-Inventory-Management-Software
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Configure DB access in `inventory_data.py` (`DB_CONFIG`). The `ssl_ca` path defaults to `isrgrootx1.pem` in the repo root; adjust if your DB requires a different CA or no SSL.

## Running the App
```bash
source .venv/bin/activate
python main.py
```

## How Data Flows
1) `inventory_data.initialize_inventory()` runs on import, loading the `inventory` table into a global DataFrame cache for fast lookups.
2) UI actions call helpers in `inventory_data` to read/update DB and keep the cache in sync.
3) Part images selected via file dialogs are copied into `part_images/` and stored by path in the DB.

## Notes & Tips
- If MySQL credentials/host change, update `DB_CONFIG`. Avoid committing secrets.
- Ensure your MySQL user has rights to SELECT/INSERT/UPDATE/DELETE on the `inventory` table.
- If you see pandas warnings about SQLAlchemy, they’re informational; `mysql-connector-python` is used directly.
- Tkinter requires a Python build with Tk; if `import tkinter` fails, install a Tk-enabled Python (python.org installer is easiest).
