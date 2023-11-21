"""
    created on 18/11/2023 17:27
    @author: lnasri

"""

import logging
import re
from bs4 import BeautifulSoup
import requests
from requests import get
from pathlib import Path
from pprint import pprint


#Parent folder
#specify the full path to the current python file  
BASE_DIR = Path(__file__).resolve().parent
#We use the basic configuration, the first logger level which is DEBUG
#to create file.log
logging.basicConfig(filename=BASE_DIR/'file.log', level= logging.DEBUG,
                    filemode="a",
                    format='%(asctime)s : %(levelname)s : %(message)s')

class Constant(object):
    """In this clsse we use HTML attributes as constants


    Args:
        object (_type_): HTML attribute

    Raises:
        Exception: return the exception whenever someone tries to\
            assign a new value to the class attribute
    """
    
    CLASS_1= {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'}
    CLASS_2= {'class' : 'tw-mb-3 tw-flex'}
    CLASS_3= {'class' : 'tw-tag-contract-s tw-readonly'}
    CLASS_4= {'class' : 'tw-flex tw-gap-3 tw-flex-wrap tw-mb-3 tw-whitespace-nowrap'}
    CLASS_6= {'class': 'tw-typo-long-m tw-mb-12 sm:tw-mb-14 tw-break-words'}
    CLASS_5= {'class': 'tw-flex tw-flex-col sm:tw-flex-row tw-mb-8 sm:tw-items-center'}
    HEADERS= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


    def __setattr__(self, *_):
        raise Exception("Tried to change the value of a constant")


def get_request(url):
    """

    Args:
        url (str): Link to Hellowork's page

    Returns:
        str: result of the request
    """
    #
    CONST= Constant()
    result = requests.get(url, headers=CONST.HEADERS)
    if result.status_code == 200:
        return result.text

    else: return logging.info(result.status_code)
    

def hellowork_scrap(url, Id):
    """ This function extracts information from the 
        hellowork web page using the BeautifulSoup library.

    Args:
        url (str): Link to Hellowork's page
        Id (str): adzuna's page id

    Returns:
        dict: job information in Hellowork page
    """

    CONST= Constant()
    #HTML page output
    page_html= BeautifulSoup(get_request(url), 'html.parser')
    #initialise all variable defined in dictionary to srting 
    salary_min= salary_max= salary= education= experience= contract= location= remote=\
            duration= description= salary_min_e= salary_med_e= salary_max_e= ""
    
    #check if the page exists  
    if page_html.find('span', {'class' : 'warning'}) is  None: 
        #check if the tag exists 
        if page_html.find('ul', CONST.CLASS_1) is not None:
            #Extract education and experience informations
            text_1= page_html.find('ul', CONST.CLASS_1).text
            experience= re.findall(r"- 1 an|[0-9] à [0-9] ans|\+ [0-9]+ ans", text_1)
            education= re.findall(r"Bac \+[0-9]|Bac", text_1)

        #check if the tag exists 
        if page_html.find('ul', CONST.CLASS_2) is not None:
            #Extract salaries communicated by the recruiter
            list_2= page_html.find('ul', CONST.CLASS_2).text.replace('\u202f', '').\
                replace('EUR', '€').split()
            
            if ('an' or 'mois'or 'jour' or 'heure' in list_2) and (len(list_2)!=0):
                if "-" in list_2:
                    indx= list_2.index("-")
                    salary_min= " ".join(list_2[:indx])+ f" € par {list_2[-1]}"
                    salary_max= " ".join(list_2[indx+1:])     
                else:
                    salary= " ".join(list_2[:])

        #Check if the tag exists 
        if page_html.findAll('li', CONST.CLASS_3) is not None:
            #Extract contract and location informations
            list_3= page_html.findAll('li', CONST.CLASS_3)
            if len(list_3)> 1:
                contract= list_3[1].text.strip().replace('\u202f', '')
                location= list_3[0].text.strip().replace('\u202f', '')

        #check if the tag exists 
        if page_html.find('ul', CONST.CLASS_4) is not None:
            #Extract remote and duration informations
            text_4= page_html.find('ul', CONST.CLASS_4).text
            remote= re.findall(r"Télétravail complet|Télétravail partiel|Télétravail occasionnel", text_4)
            duration= re.findall(r"[0-9]+ mois|[0-9] an|[0-9]+ ans|[0-9] jour|[0-9]+ jours", text_4)
        
        #check if the tag exists 
        if page_html.find('div', CONST.CLASS_5) is not None:
            #Extract Estimated HelloWork salary
            text_5= page_html.find('div', CONST.CLASS_5).text.replace('\u202f', '')
            list_5= text_5.split()
            
            #Regex to create a dictionary value list
            value_list = re.findall(r"[0-9]+,[0-9]+|[0-9]+", text_5)
            #Regex to create a dictionary key list
            key_list= re.findall(r"basse|brut|haute", text_5)
            #Create dictionary with the two lists
            dict_from_list= dict(zip(key_list, [f"{i} € {list_5[-1]}" if ('mois'or 'an' or 'jour' or 'heure'\
                                                in list_5) else f"{i} €" for i in value_list])) 

            for key, value in dict_from_list.items():
                if key == "basse":
                    salary_min_e = value
                if key == "brut":
                    salary_med_e= value
                if key == "haute":
                    salary_max_e= value

        #check if the tag exists 
        if page_html.findAll('p', CONST.CLASS_6) is not None:
            #Extract all paragraphs 
            bs_elem= page_html.findAll('p', CONST.CLASS_6)
            description= [elem.text.strip().replace('\u202f', '') for elem in bs_elem[0:]]


        return {"id" : Id,
                "hellowork_url": url,
                "location": location,
                "contract": contract,
                "education": education,
                "duration": duration,
                "remote": remote,
                "experience":experience,
                "salary_min":salary_min,
                "salary_max":salary_max,
                "salary":salary,
                "salary_min_e" : salary_min_e,
                "salary_med_e": salary_med_e,
                "salary_max_e" : salary_max_e,
                "description": description}
    
    else: return logging.info(f"hellowork_urll: {url}, Id: {Id}. Cette offre d'emploi a été pourvue")

if __name__ == "__main__":
    pprint(hellowork_scrap("https://www.hellowork.com/fr-fr/emplois/42551684.html", "544545454"))

