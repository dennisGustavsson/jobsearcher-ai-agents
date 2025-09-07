import google.generativeai as genai
from ratelimit import limits, sleep_and_retry

# Konfigurera modellen med API-nyckeln
def configure_model(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Använder den snabba modellen Flash
    return model

@sleep_and_retry
@limits(calls=5, period=60)  # 15 calls per 60 seconds
def bedom(min_profil, strukturerad_data, api_key):
    """
    Bedömningen av jobbmöjligheten baserat på användarens profil och den strukturerade data från annonsen.
    """
    print("\n--- ChansBedömningsAgent startar ---")

    prompt = f"""
    **Persona:** Du är en expert på jobbsökning och analys. Du är noggrann, faktabaserad och bra på att sammanfatta information.

    **Uppgift:** Bedöm jobbmöjligheten baserat på följande information:
    - Användarprofil: {min_profil}
    - Jobbannonsdata: {strukturerad_data}

    **Instruktioner:** Presentera ditt svar i JSON-format med nycklarna: "chans", "motivering".
    """

    try:
        model = configure_model(api_key)
        response = model.generate_content(prompt)
        bedomningsdata = response.text.strip()

        print("--- ChansBedömningsAgent slutförd. Bedömningsdata: ---")
        print(bedomningsdata)
        return bedomningsdata

    except Exception as e:
        print(f"Ett fel inträffade i ChansBedömningsAgent: {e}")
        return None