import os

from dotenv import load_dotenv

load_dotenv()
def test_env():
    base_url = os.getenv("BASE_URL")
    print(f"Это секретный Base_url:{base_url}" )