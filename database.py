import pandas as pd 
from typing import Final
from pydantic import BaseModel, Field, ValidationError

# Configuration: Constant for the data source
DATA_SOURCE: Final[str] = "company_data.csv"

class Employee(BaseModel):
    employee_id: int = Field(alias="id")
    name: str
    clearance_level: str

def get_safe_employee_data() -> pd.DataFrame:
    """
    Fetches the employee dataset and filters for non-sensitive columns.
    
    Returns:
        pd.DataFrame: A DataFrame containing only safe employee information.
    """
    try:
        df = pd.read_csv(DATA_SOURCE)
        # Make sure salary is never included
        return df[['id', 'name', 'clearance_level']]
    except FileNotFoundError:
            # Return an empty DataFrame with expected columns to maintain consistency
            return pd.DataFrame(columns=['id', 'name', 'clearance_level'])
    
def get_employee_by_name(name: str) -> str:
    """
    Queries the data store for a specific employee.
    
    Args:
        name: The target employee name to search for.
        
    Returns:
        A formatted string results or a descriptive error message.
    """
    try:
        df = pd.read_csv(DATA_SOURCE)
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
    

