from utils import is_even

def test_is_even():
    assert is_even(4)
    print("\nfour is even number - true")
    
    try:
        assert is_even(7)
    except AssertionError:
        print("seven isn't even number bro")
    
    assert is_even(0)
    print("0 is even number - true")
 
# если вы это чекаете, я короче чутка заморочилась и чтоб проверить мой тест можете ввести плиз эту команду  
# "pytest -v -s test_utils.py" бикос вы увидете все мои принты в терминале, ильхом кеб кетти красиво сделать 