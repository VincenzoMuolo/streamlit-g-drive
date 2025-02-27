import requests
from bs4 import BeautifulSoup

def scraper(link, el_list):
  response = requests.get(link)
  
  if response.status_code != 200:
    print(f"Errore nella richiesta : {response.status_code}")
    return None
  bsoup = BeautifulSoup(response.text,"html.parser")
  extracted_data = {}

  for el_name in el_list:
    elements = bsoup.find_all(class_ = el_name)
    extracted_data[el_name] = [el.get_text(strip =True) for el in elements]
  return extracted_data
  

