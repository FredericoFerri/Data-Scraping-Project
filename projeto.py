import requests 
from bs4 import BeautifulSoup 

#dados dos produtos 
#lucro_liquido = {'Pino tensor':{'virgem':1600,'recondicionado':1280}, 
#                 'Coxim motor':{'virgem':2500,'recondicionado':2000}, 
#                 'Batente':{'virgem':1000,'recondicionado':800}, 
#                 'Bucha amortecedora':{'virgem':750,'recondicionado':600}}

#url = "https://www.reclameaqui.com.br/empresa/lojas-renner/"

def scrapingData(url):
    # Reclame aqui:

    headers = {'User-Agent': 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"} 

    req = requests.get(url=url, headers=headers) 
    print(req)

    soup = BeautifulSoup(req.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    #print(soup.prettify()) 

    # NOME DA EMPRESA
    name = soup.find("h1", class_="short-name")

    # NOTA DA EMPRESA
    score = soup.find("span", class_="score")
    score_text = score.text.split('/')[0]
    
    # DADOS DA EMPRESA
    complaintsAnswered = soup.find_all("span", class_="label")

    complaints_answered = []
    for element in complaintsAnswered:
        complaints_answered.append(element.text)

    #for element in complaintsAnswered:
    #    print(element.text)

    return name.text, score_text, complaints_answered
