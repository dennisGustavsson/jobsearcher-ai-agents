# I filen jobb_sokar_agent.py
import requests

def hitta_jobb(kommun_id, sök_sträng):
    """
    Använder Jobtech-API:et för att hitta jobb baserat på en bred söksträng och en specifik kommun.
    Returnerar en lista med jobbannonser.
    """
    api_url = "https://jobsearch.api.jobtechdev.se/search"
    params = {
        'municipality': kommun_id,
        'q': sök_sträng,
        'limit': 100 # Hämta upp till 100 annonser
    }
    headers = {'User-Agent': 'JobbSokarSkript/1.3 (Python/Requests)'}

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('hits', []) # Returnera listan med annonser
    except requests.exceptions.RequestException as e:
        print(f"Ett fel inträffade i jobb_sokar_agent: {e}")
        return [] # Returnera en tom lista vid fel