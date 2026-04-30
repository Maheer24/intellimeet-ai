import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def post(endpoint, data=None, files=None):
    try:
        if files:
            res = requests.post(f"{BASE_URL}{endpoint}", files=files)
        else:
            res = requests.post(f"{BASE_URL}{endpoint}", json=data)

        res.raise_for_status()
        return res.json()

    except Exception as e:
        return {"error": str(e)}
    
def get(endpoint):
    try:
        return requests.get(f"{BASE_URL}{endpoint}").json()
    except Exception as e:
        return {"error": str(e)} 

def delete(endpoint):
    try:
        return requests.delete(f"{BASE_URL}{endpoint}").json()
    except Exception as e:
        return {"error": str(e)}

def patch(endpoint, data=None):
    try:
        return requests.patch(f"{BASE_URL}{endpoint}", json=data).json()
    except Exception as e:
        return {"error": str(e)}