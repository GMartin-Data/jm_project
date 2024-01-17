# import module
from datetime import datetime
import json
import os
from json import JSONEncoder
from rich import print

# subclass JSONEncoder
""" class AdzunaJobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__ """

def json_Dump(adzuna_jobs, env):

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    fileName = f'jobs_{ts}.json'
    dump_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', env['jsonExport.output_folder'] , fileName))
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        # `ensure_ascii=False` to force display of non-ascii characters in JSON
        json.dump(adzuna_jobs, dump_file, indent=4, ensure_ascii=False) 
    print(f'\t[cyan]{dump_path} dumped![/cyan]')