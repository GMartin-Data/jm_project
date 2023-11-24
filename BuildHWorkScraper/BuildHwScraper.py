"""
    created on 18/11/2023 17:27
    @author: lnasri
    @code-reviewer: Greg 
"""

import logging
from pathlib import Path
import re
from bs4 import BeautifulSoup
from rich import print  
import requests 
from urllib.parse import urlparse
from DataModel import OnlyId, HelloWorkAd

# Specify the full path of the current python file's parent folder  
BASE_DIR = Path(__file__).resolve().parent
# Creating a logger with DEBUG level, outputting a file.log file
logging.basicConfig(filename=BASE_DIR/'file.log', level=logging.DEBUG,
                    filemode="a",
                    format='%(asctime)s : %(levelname)s : %(message)s')


class Constant(object):
    """In this class, we use HTML attributes as constants
    Args:
        object: HTML attribute
    Raises:
        Exception: return the exception whenever someone tries to\
            assign a new value to the class attribute
    """
    
    CLASS_EDU_EXP = {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'}
    CLASS_SAL_COM = {'class' : 'tw-mb-3 tw-flex'}
    CLASS_CON_LOC = {'class' : 'tw-tag-contract-s tw-readonly'}
    CLASS_REM_DUR = {'class' : 'tw-flex tw-gap-3 tw-flex-wrap tw-mb-3 tw-whitespace-nowrap'}
    CLASS_SAL_EST = {'class': 'tw-flex tw-flex-col sm:tw-flex-row tw-mb-8 sm:tw-items-center'}
    CLASS_DESC = {'class': 'tw-typo-long-m tw-mb-12 sm:tw-mb-14 tw-break-words'}
    
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __setattr__(self, *_):
        raise Exception("Tried to change the value of a constant")


class IsValidHwUrl:
    """Validating hellowork url"""
    def __init__(self, url):
        parts = urlparse(url)
        self.parts = parts
    
    def eq_netloc(self) -> bool:
        return self.parts.netloc == 'www.hellowork.com' 


def get_request(url) -> str:
    """
    Args:
        url (str): Link to Hellowork's page
    Returns:
        str: result of the request
    """
    CONST= Constant()  
    try:
        response = requests.get(url, headers=CONST.HEADERS)
        response.raise_for_status()
        return response.text
    # - separate logins according to errors,
    # - return None in case of error 
    except requests.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        logging.error(f'Non HTTP error occured: {err}')  
    return None
    

def build_hw_scraper(url: str, Id: str):
    """ This function extracts information from the 
        hellowork web page using the BeautifulSoup library.
    Args:
        url (str): Link to Hellowork's page
        Id (str): adzuna's page id
    Returns:
         HelloWorkAd Class
    """

    CONST = Constant()  
    # check if hellowork url is valid
    if IsValidHwUrl(url).eq_netloc() is False:
        logging.info(f"hellowork_url: {url}, Id: {Id} Invalid url")
        return  OnlyId(id = Id)

    # HTML page output
    page_html = BeautifulSoup(get_request(url), 'html.parser')

    # Initialize all fields - This has to fit with HelloWorkAd type hinting
    location = contract = ''
    description = ['']
    education = duration = remote = experience = salary_min = salary_max = \
        salary = salary_min_e = salary_med_e = salary_max_e = None
   
    # Check if the page exist
    if page_html is None: 
        return None  
    
    # Check if the page isn't outdated
    if page_html.find('span', {'class' : 'warning'}) is None:
        # Check if the tag exists 
        if page_html.find('ul', CONST.CLASS_EDU_EXP) is not None:
            # Extract Education and Experience informations
            text_edu_exp = page_html.find('ul', CONST.CLASS_EDU_EXP).text
            experience = re.findall(r"- 1 an|[0-9] à [0-9] ans|\+ [0-9]+ ans", text_edu_exp)
            if not experience:
                experience = None  
            education = re.findall(r"Bac \+[0-9]|Bac", text_edu_exp)
            if not education:
                education = None  

        # Check if the tag exists 
        if page_html.find('ul', CONST.CLASS_SAL_COM) is not None:
            # Extract Salaries communicated by the recruiter
            list_sal_com = (page_html
                            .find('ul', CONST.CLASS_SAL_COM).text
                            .replace('\u202f', '').replace('EUR', '€')
                            .split()
                            )
            
            if (len(list_sal_com)!=0) and ('an' or 'mois' or 'jour' or 'heure' in list_sal_com):
                if "-" in list_sal_com:
                    indx = list_sal_com.index("-")
                    salary_min = " ".join(list_sal_com[:indx])+ f" € par {list_sal_com[-1]}"
                    salary_max = " ".join(list_sal_com[indx+1:])     
                else:
                    salary = " ".join(list_sal_com)  

        # Check if the tag exists 
        if page_html.find_all('li', CONST.CLASS_CON_LOC) is not None:
            # Extract contract and location informations
            list_con_loc = page_html.find_all('li', CONST.CLASS_CON_LOC)
            if len(list_con_loc)> 1:
                contract = list_con_loc[1].text.strip().replace('\u202f', '')
                location = list_con_loc[0].text.strip().replace('\u202f', '')

        # Check if the tag exists 
        if page_html.find('ul', CONST.CLASS_REM_DUR) is not None:
            # Extract Remote and Duration informations
            text_rem_dur = page_html.find('ul', CONST.CLASS_REM_DUR).text

            remote = re.findall(
                r"Télétravail complet|Télétravail partiel|Télétravail occasionnel", text_rem_dur)
            if not remote: 
                remote = None 

            duration = re.findall(
                r"[0-9]+ mois|[0-9] an|[0-9]+ ans|[0-9] jour|[0-9]+ jours", text_rem_dur)
            if not duration: 
                duration = None 
        
        # Check if the tag exists 
        if page_html.find('div', CONST.CLASS_SAL_EST) is not None:
            # Extract Salary information, estimated by HelloWork
            text_sal_est = page_html.find('div', CONST.CLASS_SAL_EST).text.replace('\u202f', '')
            list_sal_est = text_sal_est.split()
            
            # Regex to create a dictionary value list
            value_list = re.findall(r"[0-9]+,[0-9]+|[0-9]+", text_sal_est)
            # Regex to create a dictionary key list
            key_list = re.findall(r"basse|brut|haute", text_sal_est)
            # Create dictionary with the two lists
            dict_from_list= dict(
                zip(
                    key_list,
                    [f"{i} € {list_sal_est[-1]}"
                     if ('mois'or 'an' or 'jour' or 'heure' in list_sal_est) else f"{i} €"
                     for i in value_list]
                    )
                ) 

            for key, value in dict_from_list.items():
                if key == "basse":
                    salary_min_e = value
                if key == "brut":
                    salary_med_e= value
                if key == "haute":
                    salary_max_e= value

        #check if the tag exists 
        if page_html.find_all('p', CONST.CLASS_DESC) is not None:
            #Extract all paragraphs 
            bs_elem = page_html.find_all('p', CONST.CLASS_DESC)
            description = [elem.text.strip().replace('\u202f', '') for elem in bs_elem[0:]]
            

        return HelloWorkAd(
            id = Id,
            url = url,
            location = location,
            contract = contract,
            education = education,
            duration = duration,
            remote = remote,
            experience = experience,
            salary_min = salary_min,
            salary_max = salary_max,
            salary = salary,
            salary_min_e = salary_min_e,
            salary_med_e = salary_med_e,
            salary_max_e = salary_max_e,
            description = description
        )
    
    else:
        logging.info(f"hellowork_url: {url}, Id: {Id}. Cette offre d'emploi a été pourvue")
        return None


if __name__ == "__main__":
    print(build_hw_scraper("https://www.hellowork.com/fr-fr/emplois/32898119.html" , "544545454"))
    
    
    
