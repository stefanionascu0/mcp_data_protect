from mcp.server.fastmcp import FastMCP
from database import get_safe_employee_data, get_employee_by_name

mcp = FastMCP("SecureDataBridge")

@mcp.tool()
def read_company_records() -> str:
    """Retrieves a sanitized list of all company employees.
    
    Returns:
        str: A formatted string of IDs, Names, and Clearance Levels.
    """
    data = get_safe_employee_data()
    return data.to_string(index=False)
    
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
    mcp.run()
    

    

    
    
