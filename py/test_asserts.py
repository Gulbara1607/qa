some_word = 'authomation'
some_values = [5, 9, 2, 7]

def test_the_length():
    assert len(some_word) == 10, f"we were waiting 11, but we got {len(some_word)}" 
    
def test_the_values():
    assert max(some_values) == 9
    
def test_data():
    data = {"name": "QA", "level": 1}
    assert "name" in data