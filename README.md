# Case_oppgave

## For brukere
Denne nettsiden lar deg sende inn tilbakemeldinger ved å fylle ut et skjema med navn, e-postadresse og en melding. Etter innsending vil du få en bekreftelse, og du kan også se tidligere tilbakemeldinger fra andre brukere.

### Hvordan bruke nettsiden:
1. **Gå til forsiden (`index.html`)** – Her finner du skjemaet for å sende inn en tilbakemelding.
2. **Fyll ut skjemaet** – Skriv inn navn, e-post og tilbakemelding, og trykk på "Send inn"-knappen.
3. **Bekreftelse (`result.html`)** – Etter innsending ser du en bekreftelse med informasjonen du sendte.
4. **Se alle tilbakemeldinger (`feedbacks.html`)** – Du kan også se en liste over alle tidligere tilbakemeldinger.

## For utviklere
Nettsiden er bygget ved hjelp av **Flask (Python) for backend**, samt **HTML og CSS** for frontend. Tilbakemeldingene lagres i en **SQLite-database**.

### Teknologistakk:
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite

### Prosjektstruktur:
```
/
├── static/
│   ├── style.css      # CSS for stilsetting
├── templates/
│   ├── index.html     # Skjema for innsending av tilbakemeldinger
│   ├── result.html    # Bekreftelsesside etter innsending
│   ├── feedbacks.html # Liste over alle tilbakemeldinger
├── app.py             # Flask-backend
├── tilbakemeldinger.db # SQLite-database (genereres automatisk)
├── requirements.txt   # Avhengigheter
├── README.md          # Dokumentasjon
```

### Hvordan kjøre applikasjonen lokalt:
1. **Klone prosjektet**
```bash
git clone <repo-url>
cd <repo-folder>
```

3. **Start Flask-serveren**
```bash
python app.py
```
Nettsiden vil være tilgjengelig på `http://127.0.0.1:5000/`.

### Videreutvikling og forbedringer
Hvis du ønsker å videreutvikle prosjektet, kan du vurdere følgende:
- **Legge til frontend-validering** for å forbedre brukeropplevelsen.
- **Implementere autentisering** for å sikre at kun autoriserte brukere kan se tilbakemeldinger.
- **Bytte ut SQLite med en skyløsning** for bedre skalerbarhet.
- **Forbedre UI/UX** ved å bruke et frontend-rammeverk som React eller Bootstrap.

Dersom du har spørsmål eller ønsker å bidra, vennligst opprett en issue eller send en pull request.




