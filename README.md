# Repository di test per Codex

Questo repository viene utilizzato per verificare il funzionamento delle automazioni di creazione dei contenuti.
Include esempi di struttura minima su cui effettuare prove e sperimentazioni.

## Novità: SEO Prompt Generator
Il progetto include ora una web-app sviluppata con Streamlit per generare spunti ottimizzati per la SEO a partire da una query target. L'applicazione:

- Recupera i risultati della SERP tramite le API di DataForSEO (endpoint Google Organic Live Regular).
- Analizza i contenuti dei primi competitor prelevando automaticamente un estratto delle loro pagine.
- Elabora outline, keyword e suggerimenti editoriali grazie alle API di OpenAI.
- Consente di scaricare in formato Markdown il brief generato.

### Prerequisiti
- Python 3.9 o superiore
- Account DataForSEO con credenziali API valide
- API key OpenAI

Installa le dipendenze richieste con:

```bash
pip install -r requirements.txt
```

### Avvio dell'app Streamlit

```bash
streamlit run streamlit_app.py
```

L'applicazione si avvierà sul browser locale (di default su `http://localhost:8501`). Inserisci le credenziali DataForSEO e OpenAI direttamente nella sidebar dell'interfaccia.

## Struttura
- `README.md`: breve descrizione del progetto e delle istruzioni operative.
- `app.py`: applicazione Streamlit che integra DataForSEO e OpenAI per la generazione degli spunti SEO.
- `streamlit_app.py`: semplice entrypoint da utilizzare su Streamlit Cloud o ambienti che richiedono questo nome di file.
- `requirements.txt`: elenco delle dipendenze Python richieste.

## Utilizzo
Apri il repository, configura le variabili richieste nell'app e personalizza il flusso secondo le esigenze delle tue prove.
