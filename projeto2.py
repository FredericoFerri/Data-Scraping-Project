from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initializing Firefox
service = Service(GeckoDriverManager().install()) 
navigator = webdriver.Firefox(service=service)

# Request data:
#-----------------------------------------------------------------
import requests 

url =  "https://www.reclameaqui.com.br/"
headers = {'User-Agent': 
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"} 
req = requests.get(url=url, headers=headers) 
print(req) # Request code
#-----------------------------------------------------------------

session = requests.Session()
navigator.get(url)


xpath_list = [
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[1]/a[1]",
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[1]/a[2]",
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[1]/a[3]",
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[2]/a[1]",
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[2]/a[2]",
    "/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[2]/a[3]"
]

from projeto import scrapingData

import pandas as pd
columns = ['Name', 'Score', 'complaintsAnswered', 'returnToDoBusiness', 'solutionIndex', 'consumerScore']
df_goodCompanies = pd.DataFrame(columns=columns)
df_badCompanies = pd.DataFrame(columns=columns)

#iterator for function scrapeData
it = 0

def scrapeData(xpath, url_moda):
    global df_goodCompanies, df_badCompanies, it

    element_store = WebDriverWait(navigator, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
        )
    element_store.click()

    #Scraping data
    #------------------------------------------------
    current_url = navigator.current_url
    company_name, company_score, complaints_answered = scrapingData(current_url)

    print("Company Name:", company_name)
    print("Company Score:", company_score)
    print("Complaints Answered:", complaints_answered)

    if (it<3):
        df_goodCompanies = df_goodCompanies.append({'Name': company_name, 'Score': company_score, 
                        'complaintsAnswered': complaints_answered[0],
                        'returnToDoBusiness': complaints_answered[1],
                        'solutionIndex': complaints_answered[2],
                        'consumerScore': complaints_answered[3]}, ignore_index=True)
    else:
        df_badCompanies = df_badCompanies.append({'Name': company_name, 'Score': company_score, 
                        'complaintsAnswered': complaints_answered[0],
                        'returnToDoBusiness': complaints_answered[1],
                        'solutionIndex': complaints_answered[2],
                        'consumerScore': complaints_answered[3]}, ignore_index=True)

    navigator.get(url_moda)
    it=it+1

try:
    for xpaths in xpath_list:
        element_sliding_bar = WebDriverWait(navigator, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/astro-island[6]/section/div/div[2]/nav/div[2]/button[2]"))
        )
        element_sliding_bar.click()
        print("Button clicked successfully.")
        scrapeData(xpaths, url)
    
    if not df_goodCompanies.empty and not df_badCompanies.empty:
        df_goodCompanies.to_excel('good_companies.xlsx', index=False)
        df_badCompanies.to_excel('bad_companies.xlsx', index=False)
    else:
        print("DataFrame(s) vazio(s).")

except Exception as e:
    print(f"Error: {e}")
finally:
    navigator.quit()

