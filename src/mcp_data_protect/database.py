import os, re
from typing import Final, Optional, List, Dict
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()
DB_URL = "sqlite:///./mcp_protected.db"
DB_TABLE_NAME: str = os.getenv("MCP_DB_TABLE", 'employees')
engine = create_engine(DB_URL, connect_args={"check_same_thread": False}) 

class Employee(BaseModel): # Pydantic model for data validation
    employee_id: int = Field(alias="id")
    name: str
    clearance_level: str
    

def is_safe_name(name: str) -> bool:
    # Prevent SQL injection in table/column names
    return bool(re.match(r"^[a-zA-Z0-9_]+$", name))

# prevents crashes for first-time users with no table
Base.metadata.create_all(bind=engine)
    
def get_safe_employee_data() -> List[dict]:
    """
    Fetches from SQL db the whole data.
    """
    
    if not is_safe_name(DB_TABLE_NAME):
        print(f"SECURITY ALERT: Invalid table name attempted: {DB_TABLE_NAME}")
        return []
    try:    
        with engine.connect() as conn:
            query = text(f"SELECT id, name, clearance_level FROM {DB_TABLE_NAME}")
            
            # TODO: implement generator or pagination for really long db
            result = conn.execute(query).mappings().all()
            return [Employee(**row).model_dump() for row in result]
    except Exception as e:
        print(f"Database Read Error: {e}") 
        return []
        
def get_employee_by_name(name: str) -> str:
    """
    Safe data fetcher per employee name
    """

    
    if not is_safe_name(DB_TABLE_NAME):
        return "System Error: Security violation in table configuration."
        
    try:
        with engine.connect() as conn:
            query = text(f"SELECT id, name, clearance_level FROM {DB_TABLE_NAME} WHERE LOWER(name) = LOWER(:n)") # prevents sql injection with placeholder
            result = conn.execute(query, {"n": name.strip()}).mappings().first()
            
            if not result:
                return f"Search error: No record found for employee '{name}'."
                
            validated = Employee(**dict(result))
            return f"Found: {validated.name} (ID: {validated.employee_id} - Level: {validated.clearance_level})"
    
    except Exception as e:
        return f"System Error: {str(e)}"
 
            
    
            
    
    

    
    

    


