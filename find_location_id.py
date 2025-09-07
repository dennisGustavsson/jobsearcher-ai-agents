# I filen hitta_plats_id.py
import requests

def get_plats_id(plats_namn):
    """
    Använder Jobtechs autocomplete-API för att hitta ID för en kommun.
    """
    # Vi söker efter kommuner (municipality)
    api_url = f"https://taxonomy.api.jobtechdev.se/v1/taxonomy/autocomplete?type=municipality&q={plats_namn}"
    headers = {'User-Agent': 'IDFinder/1.0'}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            # Ta det första, mest relevanta förslaget
            # Svaret är en lista, vi vill ha 'id' från första elementet
            return data[0]['id']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Kunde inte hämta ID för '{plats_namn}': {e}")
        return None

if __name__ == "__main__":
    städer_att_hitta = ["Örebro", "Karlstad", "Stockholm", "Västerås"]
    
    print("--- Söker efter kommunkoder via Jobtech Taxonomy API ---")
    for stad in städer_att_hitta:
        plats_id = get_plats_id(stad)
        if plats_id:
            print(f"✅ Hittade ID för {stad}: {plats_id}")
        else:
            print(f"❌ Kunde inte hitta ID för {stad}")