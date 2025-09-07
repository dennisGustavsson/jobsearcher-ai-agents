def run_criticism(model, blog_post, topic):
    """
    Kör kritikeragenten för att granska och ge feedback på ett blogginlägg.
    """
    print(f"\n--- Kritikeragenten startar granskning ---")

    prompt = f"""
    **Persona:** Du är en erfaren redaktör med ett skarpt öga för detaljer. Du är expert på att ge konstruktiv feedback som hjälper skribenter att förbättra sina texter. Ditt mål är att göra texten så engagerande och tydlig som möjligt.

    **Uppgift:** Granska följande blogginlägg om ämnet "{topic}". Ge feedback i tre punkter: "Vad som är bra", "Vad som kan förbättras", och en övergripande "Slutsats".

    **Blogginlägg att granska:**
    ---
    {blog_post}
    ---

    **Instruktioner:**
    Formatera din feedback exakt enligt följande mall:
    **Vad som är bra:** [En eller två meningar om textens styrkor.]
    **Vad som kan förbättras:** [En eller två konkreta förslag på förbättringar.]
    **Slutsats:** [En sammanfattande mening och ett betyg från 1-5, där 5 är bäst.]
    """

    try:
        response = model.generate_content(prompt)
        criticism = response.text.strip()
        print("--- Kritikeragenten slutförd. Feedback: ---")
        return criticism
    except Exception as e:
        print(f"Ett fel inträffade i kritikeragenten: {e}")
        return None