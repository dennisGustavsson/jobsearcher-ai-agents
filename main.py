
import jobb_sokar_agent
import annons_analyserings_agent
import chans_bedomnings_agent
import myprofile
import database_manager
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def main():
    if not api_key:
        print("Fel: Kunde inte hitta GOOGLE_API_KEY. Kontrollera din .env-fil.")
        return
    
    database_manager.initialize_database()

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
            job_id = jobb.get('id')
            headline = jobb.get('headline', 'N/A')
            print(f"--- Analyserar jobb: {headline} ---")

            jobb_beskrivning = jobb.get('description', {}).get('text', '')
            if not jobb_beskrivning:
                print("   -> Hoppar över jobb utan beskrivning.")
                continue

            if not job_id:
                print(f"   -> Hoppar över jobb utan ID: {headline}")
                continue

            # KONTROLLERA MINNET (DATABASEN)!
            if database_manager.job_exists(job_id):
                print(f"   -> Jobbet '{headline}' finns redan i databasen. Hoppar över.")
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
            
            # Skapa ett dictionary med all information som ska sparas
            job_details_to_save = {
                "id": job_id, # Glöm inte ID!
                "stad": stad,
                "job_title": headline,
                "structured_data": strukturerad_data,
                "bedomning": bedomning,
                "link": jobb.get('webpage_url', 'N/A')
            }

            alla_analyserade_jobb.append({
                "stad": stad,
                "job_title": headline,
                "structured_data": strukturerad_data,
                "bedomning": bedomning,
                "link": jobb.get('webpage_url', 'N/A')
            })

            # HÄR ÄR DEN VIKTIGA ÄNDRINGEN!
            # Spara det nya, analyserade jobbet till databasen.
            database_manager.add_job_analysis(job_details_to_save)

            # Lägg till i listan för att skriva till textfilen i slutet
            alla_analyserade_jobb.append(job_details_to_save)
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