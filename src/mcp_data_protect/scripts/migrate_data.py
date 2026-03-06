import csv, sys, os
import pandas as pd
from sqlalchemy import inspect
from mcp_data_protect.database import engine


def run_cli_migration():
    """
    Reades any CSV and creates matching SQL table.
    Asks user for input to confirm.
    """
    print("--- MCP Data Protect: Enterprise Migrator ---")
    
    csv_path= input("Enter the path to your CSV(e.g., company_data.csv): ").strip()
    if not os.path.exists(csv_path):
        print(f"ERROR: File '{csv_path}' not found.")
    
    table_name = input("Enter target SQL db table name (default: employees): ").strip() or "employees"
    
    inspector = inspect(engine) #to look at the db
    if table_name in inspector.get_table_names():
        print(f"WARNING: Table '{table_name}' already exists in the database.")
        choice = input(f"Do you want to OVERWRITE all data in '{table_name}'? (y/N): ").lower()
        
        if choice != 'y':
            print("Migration aborted by user.")
            sys.exit(0)
            
        mode = 'replace' #overwrite
        print(f"Proceeding with OVERWRITE on '{table_name}'...")
        
    else:
        mode = 'fail' #failed to find table, need to create it
        print(f"Table '{table_name}' not found. Creating new table now...")
    
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists=mode, index=False)
        print(f"SUCCESS: Migrated {len(df)} rows from '{csv_path}' to table '{table_name}'.") 
    except Exception as e:
        print(f"FATAL ERROR during migration: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    run_cli_migration()
        
    
    
    
    
    

  
        
        
