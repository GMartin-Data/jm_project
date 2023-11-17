"""
This module contains logic to scrape data from HelloWork ad pages,
the output being a devoted Pydantic class.

IMPORTANT:
For the moment, this is a module, not a script.
It means that you have to import, at least,
the final function `scrape_hw` to implement it into your workflow.
"""


from typing import List, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel
import requests
from rich import print


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/116.0.0.0 Safari/537.36'
URL = '<Enter your URL here>'


# Classes, by order of appearance in the code
class HelloWorkSumUp(BaseModel):
    """Output class from `get_hw_sum_up`function"""
    location: str
    contract: str
    duration: Optional[str]
    remote: Optional[str]
    education: Optional[List[str]]
    experience: Optional[List[str]]
    sectors: Optional[List[str]]


class HelloWorkSalary(BaseModel):
    """Output class from `get_hw_salary` function"""
    salary_min: Optional[str]
    salary_med: Optional[str]
    salary_max: Optional[str]
    

class HelloWorkAd(BaseModel):
    """Output class for a HelloWord scraped ad"""
    id: str   # Given by adzuna_url's output
    url: str 
    location: str
    contract: str
    duration: Optional[str]  
    remote: Optional[str]       
    education: Optional[List[str]]
    experience: Optional[List[str]]
    sectors: Optional[List[str]]
    description: str
    salary_min: Optional[str]
    salary_med: Optional[str]
    salary_max: Optional[str]
    

# Function, by order of appearance in the code
def load_and_parse(url: str) -> BeautifulSoup:
    """Load (requests) and parse (BeautifulSoup)"""
    resp = requests.get(url, headers={'User-Agent': USER_AGENT})
    if resp.status_code != 200:
        print(f"{resp.reason = }")
        
    return BeautifulSoup(resp.text, 'html.parser')


def is_ad_outdated(html: BeautifulSoup) -> bool:
    """
    Check if there's a `span` tag with class `warning`.
    Its text is generally: "Cette offre d'emploi a été pourvue"
    """
    return html.find("span", {'class': 'warning'})


def get_hw_sum_up(html: BeautifulSoup) -> Optional[HelloWorkSumUp]:
    """Get information contained in HelloWork's page sum-up"""
    sum_up = html.find_all('section')[-1]  # Sum-up is always the last section
    
    # Mandatory two first tags with: `location` and `contract` fields
    two_first_tags = sum_up.find_all('li', {'class': 'tw-tag-contract-s'})    
    location = two_first_tags[0].text.strip()
    contract = two_first_tags[1].text.strip()
    
    # Other tags with remaining fields
    other_tags = sum_up.find_all('li', {'class': 'tw-tag-primary-s'})
    other_fields = set(tag.text.strip() for tag in other_tags)
    # duration
    duration = None
    for field in other_fields:
        if field.startswith('\U0001F551'):
            duration = field[2:]
            other_fields.remove(field)
            break
    # remote
    remote = None  # Default value
    for field in other_fields:
        if field.startswith(u'\U0001F3E0'):
            remote = field[2:]
            other_fields.remove(field)
            break
    # education
    education = [field for field in other_fields
                 if field.startswith('Bac')]
    for level in education:
        other_fields.remove(level)
    # experience
    experience = [field for field in other_fields
                  if field.startswith('Exp.')]
    for level in experience:
        other_fields.remove(level)
    # sectors (remaining items if everything is ok)
    sectors = sorted(list(other_fields))

    return HelloWorkSumUp(
        location=location,
        contract=contract,
        duration=duration,
        remote=remote,
        education=education, 
        experience=experience,
        sectors=sectors
    )


def get_hw_salary(html: BeautifulSoup) -> HelloWorkSalary:
    """Get salary information from HelloWork's page"""
    # Searchin within sum_up
    sum_up = html.find_all('section')[-1]
    if (result := sum_up.find('li', {'class': 'tw-tag-attractive-s'})) is not None:
        # Salary in sum_up
        output = (result
                  .text.strip()
                  .replace('\u202f', '').replace(' - ', ' ').replace('EUR', '€')
                  .split()
                 )
        salary_max = " ".join(output[1:])
        del output[1]
        salary_min = " ".join(output)
        
        return HelloWorkSalary(
            salary_min = salary_min,
            salary_med = None,
            salary_max = salary_max
            )
    else:
        # Salary to search in salary section
        salaries = dict()
        cats = ('low', 'median', 'high')
        for cat in cats:
            if (s := html.find('p', {'data-cy': f'{cat}Estimation'})) is not None:
                salaries[cat] = s.text.replace('\u202f', '')
            else:
                salaries[cat] = None
                
        return HelloWorkSalary(
            salary_min = salaries['low'],
            salary_med = salaries['median'],
            salary_max = salaries['high']
        )


def get_hw_description(html: BeautifulSoup) -> str:
    """Get the relevant text information on HelloWork's page."""
    keywords = ('poste', 'profil')
    output_texts = []
    
    for keyword in keywords:
        h2_tag = html.find('h2', string=lambda text: text and keyword in text.lower())
        if h2_tag:
            p_tag = h2_tag.find_next_sibling('p')
            if p_tag:
                output_texts.append(p_tag.text.strip())
    final_text = ' '.join(output_texts)
    
    return final_text


def scrape_hw(id: str, url: str) -> Optional[HelloWorkAd]:
    """Scrape the page and return a HelloWorkAd Class"""
    html = load_and_parse(url)
    
    # Initial testing if ad is outdated
    if is_ad_outdated(html):
        return None
        
    sum_up_data = get_hw_sum_up(html)    
    salary_data = get_hw_salary(html)
    description = get_hw_description(html)
    
    return HelloWorkAd(
        id=id,
        url=url,
        location=sum_up_data.location,
        contract=sum_up_data.contract,
        duration=sum_up_data.duration,
        remote=sum_up_data.remote,
        education=sum_up_data.education,
        experience=sum_up_data.experience,
        sectors=sum_up_data.sectors,
        description=description,
        salary_min=salary_data.salary_min,
        salary_med=salary_data.salary_med,
        salary_max=salary_data.salary_max
    )
