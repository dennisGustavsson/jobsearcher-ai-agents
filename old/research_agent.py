import google.generativeai as genai

# Konfigurera modellen med API-nyckeln
def configure_model(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Använder den snabba modellen Flash
    return model

def run_research(model, topic):
    """
    Kör jobbsökning för att samla in information om ett ämne.
    """
    print(f"\n--- Jobbsökningsagenten startar för ämnet: '{topic}' ---")

    prompt = f"""
    **Persona:** Du är en expert på jobbsökning och analys. Du är noggrann, faktabaserad och bra på att sammanfatta information.

    **Uppgift:** Samla in och sammanfatta de fem viktigaste punkterna om ämnet: "{topic}". Informationen ska vara koncis och lättförståelig.

    **Instruktioner (ReAct-format):**
    Strukturera ditt svar enligt följande:
    1. **Tanke:** Beskriv din plan för att lösa uppgiften.
    2. **Handling:** Utför din efterforskning (simulerat).
    3. **Observation:** Presentera de fem viktigaste punkterna i en numrerad lista med en kort beskrivning för varje. Ditt svar ska endast innehålla denna del.
    """

    try:
        response = model.generate_content(prompt)
        full_response = response.text
        
        # ---- HÄR ÄR FÖRBÄTTRINGEN ----
        # Hitta startpunkten för observationen på ett säkrare sätt.
        # Vi delar upp strängen vid "Observation:" men bara en gång.
        parts = full_response.split("Observation:", 1)

        if len(parts) > 1:
            # Om listan har mer än en del, betyder det att "Observation:" fanns.
            # Då tar vi den andra delen.
            observation = parts[1].strip()
        else:
            # Om "Observation:" inte fanns, antar vi att hela svaret är observationen.
            # Detta gör koden mer flexibel.
            print("Varning: 'Observation:' hittades inte i svaret. Använder hela texten.")
            observation = full_response.strip()
        
        # --------------------------------

        print("--- Forskningsagenten slutförd. Resultat: ---")
        print(observation)
        return observation
        
    except Exception as e:
        # Denna felhantering fångar nu andra, mer oväntade fel.
        print(f"Ett oväntat fel inträffade i forskningsagenten: {e}")
        return None