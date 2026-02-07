import sys
import os
import pandas as pd

# Setup path
sys.path.append(os.path.join(os.getcwd(), 'Backend'))

from Backend.agents.menu_agent import MenuAgent
from Backend.main import load_db

def test_local():
    print("--- Loading DB ---")
    db = load_db()
    if not db:
        print("DB Load Failed")
        return
        
    print(f"Menu Count: {len(db['menu'])}")
    if 'Is_Active' in db['menu'].columns:
        print(f"Raw Is_Active values: {db['menu']['Is_Active'].unique()}")
    else:
        print("Is_Active column missing!")

    print("--- Initializing Agent ---")
    worker = MenuAgent(db['menu'], db['orders'], db['items'])
    
    print("--- Getting Smart Menu ---")
    res = worker.get_smart_menu(email="test@debug.com")
    
    sections = res.get('menu_sections', {})
    print(f"Sections Returned: {list(sections.keys())}")
    for k, v in sections.items():
        print(f"Section '{k}': {len(v)} items")
        if len(v) > 0:
            print(f"SAMPLE ITEM KEYS in '{k}': {list(v[0].keys())}")
            print(f"SAMPLE ITEM in '{k}': {v[0]}")

if __name__ == "__main__":
    test_local()
