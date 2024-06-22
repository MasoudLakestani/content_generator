import requests

import urllib.request as urllib
from bs4 import BeautifulSoup

def search(query, lang="fa"):
    search_query = '+'.join(query.split()) 
    url = f"https://www.google.com/search?q={search_query}&hl={lang}"
    headers = {
            "content-type": "charset=utf-8",
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            }  
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result_block = soup.find_all("div", attrs={"class": "g"})
    links = list()
    filtered_urls = ["telewebion", "aparat", "youtube"]
    for result in result_block:
        link = result.find("a", href=True)
        title = result.find("h3")
        description_box = result.find(
            "div", {"style": "-webkit-line-clamp:2"})
        if description_box:
            description = description_box.text
            if link and title and description:
                filter = False
                for filter_key in filtered_urls:
                    if filter_key in link["href"]:
                        filter = True
                if filter is not True:
                    links.append(link["href"])   
    return links





