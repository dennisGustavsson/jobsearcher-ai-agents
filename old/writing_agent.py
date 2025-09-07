import google.generativeai as genai

# Vi behöver inte konfigurera modellen här igen, den skickas med från main.py

def write_blog_post(model, research_result, topic):
    """
    Kör skrivagenten för att skapa ett blogginlägg baserat på forskningsresultat.
    """
    print(f"\n--- Skrivagenten startar för ämnet: '{topic}' ---")

    prompt = f"""
    **Persona:** Du är en kreativ och engagerande innehållsskapare. Din ton är inspirerande och lätt att läsa.

    **Uppgift:** Använd följande information för att skriva ett kort och inspirerande blogginlägg (cirka 200 ord) om "{topic}".

    **Information från Forskningsagenten:**
    {research_result}

    **Instruktioner:**
    1. Skapa en fängslande rubrik.
    2. Börja med en kort, intresseväckande inledning.
    3. Väv in punkterna från forskningsagenten i löpande text på ett naturligt sätt.
    4. Avsluta med en uppmuntrande sammanfattning.
    """

    try:
        response = model.generate_content(prompt)
        blog_post = response.text.strip()
        print("--- Skrivagenten slutförd. Färdigt blogginlägg: ---")
        return blog_post
    except Exception as e:
        print(f"Ett fel inträffade i skrivagenten: {e}")
        return None