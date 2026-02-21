import pytest
from server import read_company_records

def test_audit_output(capsys):
	read_company_records()
	captured = capsys.readouterr()
	assert "_AUDIT_" in captured.out
	assert "Executing read_company_records" in captured.out
