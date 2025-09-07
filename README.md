# AI Job Search Agent Network

## Overview

This project demonstrates an autonomous agent network built with Python to streamline the job search process for new developers. It integrates with external APIs to find relevant job postings and leverages Google's Gemini AI model (via the Google AI Studio API) to analyze job descriptions and provide personalized suitability assessments.

The network consists of three main agents:

1.  **Job Search Agent:** Scrapes job listings from Arbetsförmedlingen (Platsbanken) based on specified locations and keywords.
2.  **Ad Analysis Agent:** Parses job descriptions and extracts structured information (e.g., required skills, experience, company details).
3.  **Chance Assessment Agent:** Compares the extracted job requirements with a defined candidate profile and assesses the likelihood of getting the job for a new, entry-level developer.

This project serves as an excellent practical example of how to build multi-agent AI systems, handle API integrations, and manage AI model interactions for real-world applications.

## Features

- **Multi-Agent Architecture:** Demonstrates collaboration between specialized AI agents.
- **API Integration:** Connects to Arbetsförmedlingen's Jobtech API for job data.
- **AI-Powered Analysis:** Utilizes Google Gemini to understand job requirements and generate insights.
- **Personalized Assessment:** Provides suitability scores for job postings based on a custom developer profile.
- **Structured Output:** Generates clear, actionable results saved to a text file.
- **Robust Error Handling:** Designed to gracefully handle common API and AI model interaction issues.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- **Python 3.8+**
- **Visual Studio Code** (or any preferred Python IDE)
- **Google AI Studio API Key:** Obtain one from [aistudio.google.com](https://aistudio.google.com/).

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

    _(Remember to replace `YOUR_USERNAME` and `YOUR_REPO_NAME`)_

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(You'll need to create `requirements.txt` next!)_

4.  **Set up your Google API Key:**
    - Create a file named `.env` in the root of your project.
    - Add your API key to this file:
      ```
      GOOGLE_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY_HERE"
      ```
    - **Important:** Add `.env` to your `.gitignore` file to prevent committing your API key to GitHub.

### Running the Application

1.  **Ensure your virtual environment is active.**
2.  **Run the main script:**
    ```bash
    python main.py
    ```
3.  The application will print its progress to the terminal and save the final analyzed job postings and assessments to `agent_results.txt`.

## Project Structure

- `main.py`: The orchestrator script that manages the workflow and agent interactions.
- `jobb_sokar_agent.py`: Handles fetching job listings from the Jobtech API.
- `annons_analyserings_agent.py`: (You will implement this) Uses Gemini to extract structured data from job descriptions.
- `chans_bedomnings_agent.py`: (You will implement this) Uses Gemini to assess job suitability based on a profile.
- `myprofile.py`: Defines the candidate's personal profile for job matching.
- `.env`: Stores environment variables, including your API key (excluded from Git).
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `requirements.txt`: Lists all Python dependencies.

## Future Enhancements (Ideas for you!)

- **Interactive Input:** Allow users to define job search criteria dynamically.
- **Feedback Loop:** Implement a mechanism for the "Chance Assessment Agent" to provide feedback to the "Ad Analysis Agent" for refinement, or for the "Ad Analysis Agent" to request more information from the Job Search Agent.
- **Database Integration:** Store job data and assessments in a database instead of a text file.
- **Web UI:** Develop a simple web interface (e.g., with Flask or FastAPI) to interact with the agent network.
- **More Agents:** Add agents for resume generation, cover letter customization, or interview preparation.
- **Tool Use:** Equip agents with tools like real-time web search for more dynamic information gathering.

## Contributing

Feel free to fork this repository, open issues, and submit pull requests. Any contributions are welcome!

## License

This project is open source and available under the [MIT License](LICENSE). _(You'll need to create a `LICENSE` file if you want to include one)_

---

### Sista förberedelser innan commit

1.  **Skapa `requirements.txt`:** I din terminal, med den virtuella miljön aktiv, kör:

    ```bash
    pip freeze > requirements.txt
    ```

    Detta skapar en fil som listar alla Python-bibliotek du har installerat.

2.  **Skapa `myprofile.py`:** Se till att du har filen `myprofile.py` med din profil-dictionary. Om du inte har den sedan tidigare:

    ```python
    # myprofile.py
    my_profile = {
        "utbildning": "Systemutvecklare, examen 2025",
        "erfarenhet_år": 0,
        "plats": "Örebro",
        "primära_färdigheter": ["Python", "JavaScript", "React", "SQL", "Git"],
        "sekundära_färdigheter": ["Docker", "AWS", "CI/CD", "HTML", "CSS"],
        "intressen": ["AI och maskininlärning", "Backend-utveckling", "Cloud-arkitektur"]
    }
    ```

    **(Anpassa gärna `my_profile` med dina faktiska färdigheter!)**

3.  **Skapa `annons_analyserings_agent.py` och `chans_bedomnings_agent.py`:** Just nu är dessa tomma eller bara stubs. Se till att du har grundläggande funktioner i dem för att koden ska kunna importera dem utan fel (även om de ännu inte anropar AI).

    Exempel på start-kod för `annons_analyserings_agent.py`:

    ```python
    # annons_analyserings_agent.py
    import google.generativeai as genai
    import json

    def analysera(jobb_beskrivning, api_key):
        # Konfigurera Gemini-modellen
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        **Persona:** Du är en expert på att extrahera nyckelinformation från jobbannonser.
        **Uppgift:** Läs följande jobbannons och extrahera viktig information till ett JSON-format.
        **Jobbannons:**
        {jobb_beskrivning}
        **Instruktioner:**
        Returnera en JSON-objekt med följande fält:
        - `foretag`: Namn på företaget.
        - `titel`: Jobbtitel.
        - `plats`: Arbetsplatsens ort.
        - `krav_erfarenhet_år`: Antal års erfarenhet som krävs. Ange 0 om ingen specifik erfarenhet nämns, eller om det står "junior" / "nyutexaminerad".
        - `teknologier_krav`: En lista med obligatoriska teknologier.
        - `teknologier_meriterande`: En lista med meriterande teknologier.
        - `keywords`: En lista med 5-7 andra viktiga nyckelord från annonsen.
        """
        try:
            response = model.generate_content(prompt)
            # Försök att parsa svaret som JSON
            return json.loads(response.text.strip())
        except Exception as e:
            print(f"Ett fel inträffade i AnnonsAnalyseringsAgent: {e}")
            return None
    ```

    Exempel på start-kod för `chans_bedomnings_agent.py`:

    ```python
    # chans_bedomnings_agent.py
    import google.generativeai as genai
    import json

    def bedom(min_profil, strukturerad_jobb_data, api_key):
        # Konfigurera Gemini-modellen
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Formatera profilen och jobbdatan för prompten
        profil_str = json.dumps(min_profil, indent=2, ensure_ascii=False)
        jobb_data_str = json.dumps(strukturerad_jobb_data, indent=2, ensure_ascii=False)

        prompt = f"""
        **Persona:** Du är en erfaren teknisk rekryterare som bedömer jobbkandidaters matchning. Du är objektiv och realistisk.
        **Uppgift:** Jämför kandidatens profil med den strukturerade jobbdatan och bedöm sannolikheten för att en nyutexaminerad utvecklare utan kommersiell erfarenhet kan få detta jobb.
        **Kandidatprofil:**
        {profil_str}
        **Jobbdata:**
        {jobb_data_str}
        **Instruktioner:**
        Returnera en JSON-objekt med följande fält:
        - `sannolikhet`: En sträng: 'Mycket Hög', 'Hög', 'Medel', 'Låg', 'Mycket Låg'.
        - `matchningsbetyg_1_till_5`: Ett numeriskt betyg (1=dåligt, 5=utmärkt) baserat på matchning.
        - `motivering`: En kortfattad text som förklarar bedömningen, med fokus på erfarenhetskrav, matchande/saknade teknologier och eventuella "junior"-markeringar i annonsen.
        - `actions_for_candidate`: En lista med 1-2 konkreta åtgärder kandidaten kan göra för att förbättra sina chanser för just detta jobb.
        """
        try:
            response = model.generate_content(prompt)
            # Försök att parsa svaret som JSON
            return json.loads(response.text.strip())
        except Exception as e:
            print(f"Ett fel inträffade i ChansBedömningsAgent: {e}")
            return None
    ```

