
import jobb_sokar_agent
import annons_analyserings_agent
import chans_bedomnings_agent
import myprofile
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def main():
    if not api_key:
        print("Fel: Kunde inte hitta GOOGLE_API_KEY. Kontrollera din .env-fil.")
        return

    # STEG 1: DEFINIERA MÅL
    # --------------------------------------------------------------------
    städer_med_id = {
        # "Stockholm": "0180",
        "Örebro": "1880",
        "Karlstad": "1780",
        "Västerås": "1980"
    }
    # Skapa en bred söksträng för att fånga alla relevanta jobb
    bred_sok_strang = "utvecklare OR developer OR programmerare OR .NET OR C# OR systemutvecklare"
    # --------------------------------------------------------------------
    
    alla_analyserade_jobb = []

    for stad, kommun_id in städer_med_id.items():
        print(f"\n{'='*40}")
        print(f"SÖKER JOBB I: {stad.upper()} MED SÖKSTRÄNG: '{bred_sok_strang}'")
        print(f"{'='*40}")

        # STEG 2: HÄMTA JOBBLISTA MED DEN NYA, BREDDARE METODEN
        jobb_lista = jobb_sokar_agent.hitta_jobb(
            kommun_id=kommun_id, 
            sök_sträng=bred_sok_strang
        )
        print(f"Hittade {len(jobb_lista)} relevanta utvecklarjobb.")

        jobb_att_analysera = jobb_lista[:5]
        print(f"Analyserar de {len(jobb_att_analysera)} första jobben...\n")

        for jobb in jobb_att_analysera: 
            headline = jobb.get('headline', 'N/A')
            print(f"--- Analyserar jobb: {headline} ---")

            jobb_beskrivning = jobb.get('description', {}).get('text', '')
            if not jobb_beskrivning:
                print("   -> Hoppar över jobb utan beskrivning.")
                continue

            # STEG 3: KOPPLA IN AI-AGENTERNA
            strukturerad_data = annons_analyserings_agent.analysera(jobb_beskrivning, api_key)
            if not strukturerad_data:
                print("   -> Fel i analysen, hoppar över detta jobb.")
                continue

            bedomning = chans_bedomnings_agent.bedom(myprofile.my_profile, strukturerad_data, api_key)
            if not bedomning:
                print("   -> Fel i bedömningen, hoppar över detta jobb.")
                continue
            
            alla_analyserade_jobb.append({
                "stad": stad,
                "job_title": headline,
                "structured_data": strukturerad_data,
                "bedomning": bedomning,
                "link": jobb.get('webpage_url', 'N/A')
            })
            print(f"   -> Analys och bedömning klar för: {headline}")

    # STEG 4: SPARA RESULTATET
    with open("agent_results.txt", "w", encoding="utf-8") as f:
        f.write("RESULTAT FRÅN AGENTISKT JOBBSÖKAR-NÄTVERK\n\n")
        for result in alla_analyserade_jobb:
            f.write(f"Stad: {result['stad']}\n")
            f.write(f"Jobbtitel: {result['job_title']}\n")
            f.write(f"Länk: {result['link']}\n")
            f.write(f"Strukturerad data: {result['structured_data']}\n")
            f.write(f"Bedömning: {result['bedomning']}\n")
            f.write("\n" + "="*50 + "\n\n")

    print("\n✅ Hela processen är slutförd! Resultat sparade i agent_results.txt")

if __name__ == "__main__":
    main()