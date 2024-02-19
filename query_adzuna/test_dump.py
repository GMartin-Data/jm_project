import json
from datetime import datetime
import os

test_json = {'item1': 1,
             'item2': 2}

ts = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
current_wd = os.getcwd()
dump_path = current_wd + f'/api_dump/test_{ts}.json'


#dump_path = f'api_dump/test_{ts}.json'
with open(dump_path, 'w', encoding='utf-8') as dump_file:
    json.dump(test_json, dump_file, indent=4, ensure_ascii=False) 
