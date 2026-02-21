import pandas as pd 
import threading
from typing import Final, Optional
from pydantic import BaseModel, Field, ValidationError

DATA_SOURCE: Final[str] = "company_data.csv"

class Employee(BaseModel):
    employee_id: int = Field(alias="id")
    name: str
    clearance_level: str

class DatabaseCache:  # thread safe for RAM caching
    _instance: Optional["DatabaseCache"] = None
    _data: Optional[pd.DataFrame] = None
    _lock = threading.Lock() # only one process to build the cache at a time
    
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._load_data()
        return cls._instance
            
    def _load_data(self):
        try:
            self._data = pd.read_csv(DATA_SOURCE)
        except FileNotFoundError:
            self._data = pd.DataFrame(columns=['id', 'name', 'clearance_level']) # empty fallback
        
    def get_records(self) -> pd.DataFrame:
        with self._lock:
            return self._data
    
    
    
def get_safe_employee_data() -> pd.DataFrame:
    """
    Fetches the employee dataset and filters for non-sensitive columns.
    
    Returns:
        pd.DataFrame: A DataFrame containing only safe employee information.
    """
    
    cache = DatabaseCache()
    df= cache.get_records()
    
    return df [['id', 'name', 'clearance_level']] # filter for safety, ignore salary
    
def get_employee_by_name(name: str) -> str:
    """
    Queries the data store for a specific employee.
    
    Args:
        name: The target employee name to search for.
        
    Returns:
        A formatted string results or a descriptive error message.
    """
    try:
        df = get_safe_employee_data() # get cached records
        normalized_name = name.strip().lower()
        mask = df['name'].str.strip().str.lower() == normalized_name
        result = df.loc[mask, ['id', 'name', 'clearance_level']]
        
        if result.empty:
            return f"Search error: No record found for employee '{name}'."
        
        user_dict = result.iloc[0].to_dict()
        validated_user = Employee(**user_dict)
        
        return f"Found: {validated_user.name} (ID: {validated_user.employee_id} - Level: {validated_user.clearance_level})"
        
    except ValidationError as e:
        return f"Data Integrity Error: {str(e)}"
    
    except FileNotFoundError:
        return f"System Error: Critical data file '{DATA_SOURCE}' not found."
        
    except Exception as e:
        return f"System error: An unexpected failure occurred: {str(e)}"
    

