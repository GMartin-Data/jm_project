
import re
from bs4 import BeautifulSoup
from warnings import warn
import requests
from requests import get



  

def get_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        return result.text
    else :
        return warn('Status code: {}'.format(result.status_code))
 

    
def getSoup(url):
    page_html = BeautifulSoup(get_request(url), 'html.parser')
    return page_html



def expe_level_items(url):
    """extracte experience level data"""
    
    page_result = getSoup(url).find('ul', {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'})

    if page_result is not None:
        text_data = getSoup(url).find('ul', {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'}).text
        e_level = re.findall(r"- 1 an|[0-9] à [0-9] ans|\+ [0-9] ans", text_data)
        
        return e_level    

    else : return warn("L’offre recherchée est expirée.")

    

def salary(url): 
    """extracte salary data"""
    
    page_result = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex'})
    if page_result is not None:
        list_data = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex'}).text.replace('\u202f', '')\
                                                                        .replace('EUR', '€').split()
        
        value ='-'
        
        if  len(list_data)!=0:
            
            if 'an' in list_data: 
                if value in list_data:
                    indx = list_data.index("-")
                    return [" ".join(list_data[:indx])+f" € par an", " ".join(list_data[indx+1:])]
                else : [" ".join(list_data[:])]
 
            if 'mois' in list_data :
                if value in list_data:
                    indx = list_data.index("-")
                    return [" ".join(list_data[:indx])+f" € par mois", " ".join(list_data[indx+1:])]
                else : [" ".join(list_data[:])]
                    
            if ' jour' in list_data :
                if value in list_data:
                    indx = list_data.index("-")
                    return [" ".join(list_data[:indx])+f" € par jour", " ".join(list_data[indx+1:])] 
                else :  [" ".join(list_data[:])]
        
        
    else : return warn("L’offre recherchée est expirée.")

    
    
def contract_type_items(url):
    """extracte contract_type data"""

    page_result = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'})

    if page_result is not None:
        text_data = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'}).text
        c_type = re.findall(r"Indépendant/Freelance|CD\w|Intérim|Alternance", text_data)
        
        if len(c_type) !=0:
            return  c_type[0]
        
    else : return warn("L’offre recherchée est expirée.")

    
    
def departement(url):
    """extracte dep data"""

    page_result = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'})

    if page_result is not None:
        list_data = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'}).text.split()

        for string in list_data:
            if string.isdigit():
                return string
        
    else : return warn("L’offre recherchée est expirée.")

    
    
def city(url):
    """extracte city data"""

    page_result = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'})

    if page_result is not None:
        list_data = getSoup(url).find('ul', {'class' : 'tw-mb-3 tw-flex tw-gap-3 tw-flex-wrap'}).text.split()
        
        for string in list_data:
            if len(string) >= 3:
                return string 
        
    else : return warn("L’offre recherchée est expirée.")

    
    
def study_level_items(url):
    """extracte study_level data"""
    
    page_result = getSoup(url).find('ul', {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'})

    if page_result is not None:
        text_data = getSoup(url).find('ul', {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'}).text
        s_level = re.findall(r"Bac \+[0-9]|Bac", text_data)  
        
        return  s_level
    
    else : return warn("L’offre recherchée est expirée.")

    
    

        
