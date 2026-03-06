import pytest
from pydantic import ValidationError
from mcp_data_protect.database import (
    get_safe_employee_data,
    get_employee_by_name,
    is_safe_name,
    Employee
)

class TestDataValidation:
    """Test Pydantic model validation for Employee"""
    
    def test_employee_model_valid_with_id(self):
        """Employee accepts 'id' field and maps to employee_id"""
        employee = Employee(
            id=1,
            name="John Doe",
            clearance_level="SECRET")
        assert employee.employee_id == 1
        assert employee.name == "John Doe"
        assert employee.clearance_level == "SECRET"

    def test_employee_model_invalid_type(self):
        """Invalid field types raise ValidationError"""
        with pytest.raises(ValidationError):
            Employee(
                id=2,
                name=123,  # should be string
                clearance_level="TOP_SECRET"
            )
    
    def test_employee_missing_required_field(self):
        """Missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            Employee(
                id=3,
                clearance_level="CONFIDENTIAL"
                # missing 'name'
            )

class TestSQLInjectionPrevention:
    """Test SQL injection prevention mechanisms"""

    def test_valid_table_name(self):
        """Valid table names pass validation"""
        assert is_safe_name("employees") is True
        assert is_safe_name("employee_data") is True
        assert is_safe_name("employee123") is True
        assert is_safe_name("employee_data_backup") is True
        assert is_safe_name("employee_data_123") is True

    def test_sql_injection_attempt_blocked(self):
        """SQL injection attempts rejected by table name validator"""
        assert is_safe_name("employees; DROP TABLE employees;") is False
        assert is_safe_name("employees; --") is False
        assert is_safe_name("employee_data; SELECT * FROM employees;") is False
        assert is_safe_name("employee_data; INSERT INTO users (username, password) VALUES ('admin', 'password');") is False
        assert is_safe_name("employee_data; UPDATE employees SET salary = 1000000 WHERE employee_id = 1;") is False

    def test_special_chars_rejected(self):
        """Special characters rejected in table names"""
        assert is_safe_name("employees.table") is False
        assert is_safe_name("employees@host") is False
        assert is_safe_name("employee_data#backup") is False

    def test_parameterized_query_injection_resistance(self):
        """Injection attempts in name search are safely parameterized"""
        # This should not raise - parameterized queries handle it safely
        result = get_employee_by_name("Bob; DROP TABLE employees;")
        # Should return error message or not found, never execute injection
        assert isinstance(result, str)
        assert "error" in result.lower() or "search error" in result.lower() or "Found" in result
    
class TestGetEmployeeData:
    """Test retrieval of employee data"""

    def test_get_safe_employee_data_returns_list(self):
        """get_safe_employee_data returns a list"""
        data = get_safe_employee_data()
        assert isinstance(data, list)

    def test_get_safe_employee_data_returns_dicts(self):
        """Returned items are dicts, not Employee objects"""
        data = get_safe_employee_data()
        if data:  # only test if records exist
            for item in data:
                assert isinstance(item, dict)

    def test_get_safe_employee_data_structure(self):
        """Dict items have required keys"""
        data = get_safe_employee_data()
        if data:  # only test if records exist
            for item in data:
                assert "employee_id" in item
                assert "name" in item
                assert "clearance_level" in item

class TestEmployeeSearch:
    """Test employee search functionality"""

    def test_get_employee_by_name_returns_string(self):
        """Search always returns a formatted string message"""
        result = get_employee_by_name("Alice")
        assert isinstance(result, str)

    def test_get_employee_by_name_not_found_returns_error(self):
        """Nonexistent employee returns error message"""
        result = get_employee_by_name("Nonexistent Employee XYZ")
        assert isinstance(result, str)
        assert "error" in result.lower() or "not found" in result.lower()

    def test_get_employee_by_name_empty_string_returns_error(self):
        """Empty string returns error message"""
        result = get_employee_by_name("")
        assert isinstance(result, str)
        assert "error" in result.lower() or "not found" in result.lower()

    def test_get_employee_by_name_whitespace_handling(self):
        """Whitespace is handled (stripped)"""
        result = get_employee_by_name("  Alice  ")
        assert isinstance(result, str)
        # Should either find Alice or return "not found", not crash

    def test_salary_intentionally_excluded(self):
        """Salary data is intentionally excluded from API for security"""
        data = get_safe_employee_data()
        if data:  # only test if records exist
            for item in data:
                assert "salary" not in item, "Salary must not be exposed in API"

