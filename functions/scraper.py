
import requests
from typing import List, Optional
from bs4 import BeautifulSoup

def scrape_result(urls:Optional[list]):
    info = ""
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        info += data
        return info, response.status_code     
