import requests 
from bs4 import BeautifulSoup 


def scrapingData(url):
    # Reclame aqui:

    headers = {'User-Agent': 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"} 

    req = requests.get(url=url, headers=headers) 
    print(req)

    soup = BeautifulSoup(req.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 

    # COMPANY NAME
    name = soup.find("h1", class_="short-name")

    # COMPANY SCORE
    score = soup.find("span", class_="score")
    score_text = score.text.split('/')[0]
    
    # COMPANY STATS
    complaintsAnswered = soup.find_all("span", class_="label")

    complaints_answered = []
    for element in complaintsAnswered:
        complaints_answered.append(element.text)

    return name.text, score_text, complaints_answered
