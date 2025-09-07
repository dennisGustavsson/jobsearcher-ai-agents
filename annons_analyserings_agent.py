import google.generativeai as genai
from ratelimit import limits, sleep_and_retry
import os
# Ta bort automatisk hämtning av api_key här, den skickas in från main.py

# Konfigurera modellen med API-nyckeln
def configure_model(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Använder den snabba modellen Flash
    return model

@sleep_and_retry
@limits(calls=5, period=60)  # 15 calls per 60 seconds
def analysera(jobbannons_text, api_key):
    """
    Analysera en jobbbeskrivning och extrahera strukturerad data.
    """
    print("\n--- AnnonsAnalyseringsAgent startar ---")

    prompt = f"""
    **Persona:** Du är en expert på jobbsökning och analys. Du är noggrann, faktabaserad och bra på att sammanfatta information.

    **Uppgift:** Analysera följande jobbbeskrivning och extrahera följande strukturerade data:
    1. Jobbtitel
    2. Företagsnamn
    3. Plats
    4. Nyckelkrav (lista)
    5. Ansvarsområden (lista)
    6. Förmåner (lista)

    **Jobbbeskrivning:**
    \"\"\"{jobbannons_text}\"\"\"

    **Instruktioner:** Presentera ditt svar i JSON-format med nycklarna: "job_title", "company_name", "location", "key_requirements", "responsibilities", "benefits".
    """

    try:
        model = configure_model(api_key)
        response = model.generate_content(prompt)
        structured_data = response.text.strip()
        
        print("--- AnnonsAnalyseringsAgent slutförd. Strukturerad data: ---")
        print(structured_data)
        return structured_data
        
    except Exception as e:
        print(f"Ett fel inträffade i AnnonsAnalyseringsAgent: {e}")
        return None