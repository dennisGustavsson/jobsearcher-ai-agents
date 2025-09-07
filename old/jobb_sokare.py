import requests

# Bas-URL till det korrekta API:et
api_bas_url = "https://jobsearch.api.jobtechdev.se/search"

# Parametrar för vår sökning
params = {
    'q': 'utvecklare',  # Sökord
    'region': '18'      # ID för Örebro län
}

# Headers som identifierar vårt skript
headers = {
    'User-Agent': 'JobbSokarSkript/1.1 (Python/Requests)',
    'Accept': 'application/json'
}

print(f"Försöker anropa den korrigerade adressen...")
# Bygg den fullständiga URL:en med hjälp av requests-bibliotekets parameter-hantering
full_url_for_print = requests.Request('GET', api_bas_url, params=params).prepare().url
print(f"{full_url_for_print}\n")


try:
    # Gör anropet
    response = requests.get(api_bas_url, headers=headers, params=params, timeout=10)

    # Kolla om servern svarade med ett fel (som 404 eller 500)
    response.raise_for_status()

    # Om allt gick bra, ladda in datan
    data = response.json()
    
    # Hämta antalet träffar
    total_hits = data.get('total', {}).get('value', 0)
    
    print("✅✅✅ ANROPET LYCKADES! ✅✅✅")
    print(f"Hittade totalt {total_hits} jobb.")

    # Skriv ut rubriken för de första 5 jobben
    print("\nExempel på de första träffarna:")
    for annons in data.get('hits', [])[:5]:
        print(f"- {annons.get('headline', 'Ingen rubrik')}")

except requests.exceptions.HTTPError as err:
    print(f"❌ HTTP-fel inträffade: {err}")
    print(f"Statuskod: {err.response.status_code}")
    print("Detta betyder att URL:en är fel eller att servern inte hittade sidan.")

except requests.exceptions.RequestException as err:
    print(f"❌ Ett nätverksfel inträffade: {err}")
    print("Detta kan bero på problem med din internetanslutning eller en brandvägg.")