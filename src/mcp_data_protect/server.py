from mcp.server.fastmcp import FastMCP
import functools
import datetime
from mcp_data_protect.database import DatabaseCache, get_safe_employee_data, get_employee_by_name

mcp = FastMCP("SecureDataBridge")

def audit_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().isoformat()
        print(f"_AUDIT_[{timestamp}] Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"_AUDIT_[{timestamp}] Error in {func.__name__}:{e}")
            raise e
    return wrapper

@audit_log
@mcp.tool()
def read_company_records() -> str:
    """Retrieves a sanitized list of all company employees.
    
    Returns:
        str: A formatted string of IDs, Names, and Clearance Levels.
    """
    data = get_safe_employee_data()
    if data is None or data.empty:
        return "System Notification: No records available in the current data store."
    return data.to_string(index=False)

@audit_log
@mcp.tool()
def search_employee(name: str) -> str:
    """ 
    Searches for a specific employee by name and returns their details.
    
    Args:
        name (str): The name of the employee to look up.
        
    Returns: 
        str: The employee's details or a descriptive error message.
    """
    return get_employee_by_name(name.strip())
    
if __name__ == "__main__":
    DatabaseCache() # preload data on startup
    mcp.run()
    

    

    
    
