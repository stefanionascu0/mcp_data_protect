import pytest
import pandas as pd
from mcp_data_protect.database import DatabaseCache

def test_singleton_identity():
    # Ensure only one instance exists
    
    cache1 = DatabaseCache()
    cache2 = DatabaseCache()
    assert cache1 is cache2 
    
def test_data_integrity():
    cache = DatabaseCache()
    data = cache.get_records()
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    
    
