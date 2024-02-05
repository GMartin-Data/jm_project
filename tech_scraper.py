"""
This module contains logic to scrape data from tech reference sites,
in order to create dumps summing up currently used tools and technologies.
"""


from datetime import datetime
import json
from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import requests


# URLS ⚠️ To insert here as CONSTANTS or to import from external file (.env?)
DB_ENGINES_URL = 'https://db-engines.com/en/ranking'
GITHUB_SURVEY_URL = 'https://insights.stackoverflow.com/survey/2021#technology-most-popular-technologies'
TIOBE_URL = 'https://www.tiobe.com/tiobe-index/'
# USER-AGENT - Maybe import it too
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/116.0.0.0 Safari/537.36'


def get_db_engines_ranking(export: str) -> List[str]:
    """
    Get db engines ranking for database usage.
    Params
    ------
        `export`: str
            'csv' or 'json' to set the export type,
            the file will be saved in the config_data folder.
    Returns
    -------
        A list of strings of databases' names.
    """
    # Loading all tables from the page
    tables = pd.read_html(DB_ENGINES_URL)
    # Preprocessing
    ranking = (tables[3]
               .rename(columns={3: 'DataBase'})
               .loc[3:, 'DataBase']
               .str.replace(' Detailed vendor-provided information available', '')
               .reset_index(drop=True)
              )
    ranking_list = ranking.to_list()

    # Export
    if export not in {'json', 'csv'}:
        print("NO EXPORT")
        print(f"Expected 'csv' or 'json' as output format, got {export}")
        return ranking_list
        
    ts = datetime.now().strftime('%Y-%m')
    path = '../config_data/db_engines_ranking'
    
    if export == 'csv':
        ranking.to_csv(f'{path}_{ts}.csv')
    else:
        with open(f'{path}_{ts}.json', 'w', encoding='utf-8') as dump_file:
            # `ensure_ascii` to force display of non-ascii characters
            json.dump(ranking_list, dump_file, indent=4, ensure_ascii=False)
        
    return ranking_list


def get_github_frameworks(web: bool = True, export: bool = True) -> List[str]:
    """
    Get names of web most popular frameworks from GitHub survey.
    Params
    ------
        `web`: bool (default: True)
            specify if you want web frameworks or not.
        `export`: bool (default: True)
            specifiy if a dump is required or not,
            it will be saved in the config_data folder.
    Returns
    -------
        A list of strings with the frameworks' names.
    """
    resp = requests.get(GITHUB_SURVEY_URL, headers={'User-Agent': USER_AGENT})
    # Manage requests issues
    if resp.status_code != 200:
        print(f"AN ERROR OCCURED: {resp.reason}")
        return []
        
    # Scraping
    html = BeautifulSoup(resp.text, 'html.parser')
    fw_type = 'webframe' if web else 'misc-tech'
    tags = (html
            .find('figure', {'id': f'most-popular-technologies-{fw_type}'})
            .find('table', {'id': fw_type})
            .find_all('td', {'class': 'label'})
    )
    fws = [tag.text.strip() for tag in tags]

    # Split records containing '/'
    cleaned_fws = []
    for fw in fws:
        if '/' in fw:
            fw_list = [item.strip() for item in fw.split('/')]
            cleaned_fws.extend(fw_list)
        else:
            cleaned_fws.append(fw)
            
    # Dump
    if export:
        ts = datetime.now().strftime("%Y-%m")
        path = '../config_data/github_web_fws' if web else '../config_data/github_misc_fws'
        json_path = f'{path}_{ts}.json'
        with open(json_path, 'w', encoding='utf-8') as dump_file:
            # `ensure_ascii` to force display of non-ascii characters
            json.dump(fws, dump_file, indent=4, ensure_ascii=False)
            
    return cleaned_fws


def get_tiobe_top50(export: str) -> List[str]:
    """
    Get Tiobe's monthly ranking for programming languages.
    Params
    ------
        `export`: str
            'csv' or 'json' to set the export type,
            the file will be saved in the config_data folder.
    Returns
    -------
        A list of strings of languages' names.
    """
    # Scrape tables
    tiobe_tables = pd.read_html(TIOBE_URL)
    # Get top 20 then 21-50
    tiobe_top20 = (tiobe_tables[0]
               .rename(columns={'Programming Language.1': 'Language'})
               ['Language']
              )
    tiobe_21_50 = (tiobe_tables[1]
               .rename(columns={'Programming Language': 'Language'})
               ['Language']
              )
    # Merging and preprocessing for next text searches
    tiobe_top50 = (pd
                   .concat([tiobe_top20, tiobe_21_50])
                   .reset_index(drop=True)
                   .str.replace('+', '\+')  # To properly preprocess C++
                   .apply(lambda s: r'\b' + s + r'\b')  # Add word boundaries
                  )
    tiobe_top50_list = tiobe_top50.to_list()

    # Export
    if export not in {'json', 'csv'}:
        print("NO EXPORT")
        print(f"Expected 'csv' or 'json' as output format, got {export}")
        return tiobe_top50_list
        
    ts = datetime.now().strftime('%Y-%m')
    path = '../config_data/tiobe_ranking'
    
    if export == 'csv':
        tiobe_top50.to_csv(f'{path}_{ts}.csv')
    else:
        with open(f'{path}_{ts}.json', 'w', encoding='utf-8') as dump_file:
            # `ensure_ascii` to force display of non-ascii characters
            json.dump(tiobe_top50_list, dump_file, indent=4, ensure_ascii=False)

    return tiobe_top50_list 
