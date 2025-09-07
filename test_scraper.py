import requests
from bs4 import BeautifulSoup   

# URL = "https://arbetsformedlingen.se/platsbanken/annonser?q=%C3%96rebro"

URL = "https://platsbanken-api.arbetsformedlingen.se/taxonomy/v1/trees?type=location"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

#print(soup.title.string)

if page.status_code == 200:
    job_cards = soup.find_all("div", class_="bottom__left")

    for card in job_cards:
        title = card.find("div", class_="pb-job-role").get_text(strip=True)
        print(title)    