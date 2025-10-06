# Repository di test per Codex

Questo repository viene utilizzato per verificare il funzionamento delle automazioni di creazione dei contenuti.
Include esempi di struttura minima su cui effettuare prove e sperimentazioni.

## Novità: SEO Prompt Generator
Il progetto include ora una web-app sviluppata con Streamlit per generare spunti ottimizzati per la SEO a partire da una query target. L'applicazione:

- Recupera i risultati della SERP tramite le API di DataForSEO (endpoint Google Organic Live Regular) inviando il payload JSON conforme alla [documentazione ufficiale](https://docs.dataforseo.com/v3/serp/google/organic/live/regular/).
- Analizza i contenuti dei primi competitor prelevando automaticamente un estratto delle loro pagine.
- Elabora outline, keyword e suggerimenti editoriali grazie alle API di OpenAI.
- Consente di scaricare in formato Markdown il brief generato.

### Prerequisiti
- Python 3.9 o superiore
- Account DataForSEO con credenziali API valide (ricorda di abilitare eventuali whitelist IP)
- API key OpenAI

Installa le dipendenze richieste con:

```bash
pip install -r requirements.txt
```

### Avvio dell'app Streamlit

```bash
streamlit run streamlit_app.py
```

Il comando segue le indicazioni della [guida ufficiale di Streamlit](https://docs.streamlit.io/get-started/installation/community-cloud) e avvierà l'applicazione sul browser locale (di default su `http://localhost:8501`). Inserisci le credenziali DataForSEO e OpenAI direttamente nella sidebar dell'interfaccia.

> ℹ️ Se l'app segnala `Accesso non autorizzato a DataForSEO`, verifica la correttezza di login e password e che l'indirizzo IP da cui stai eseguendo l'app sia autorizzato nel tuo account DataForSEO.
>
> ℹ️ Se non vengono mostrati risultati SERP, assicurati che la query scelta generi risultati organici per la lingua/località indicate in DataForSEO, che il task risulti `status_code=20000` nella risposta e valuta di aumentare la profondità o cambiare dispositivo di ricerca.
>
> ℹ️ Se ricevi l'errore `POST Data Is Invalid (40503)`, verifica che keyword, lingua e località corrispondano esattamente ai valori supportati da DataForSEO e che il payload rispetti la struttura prevista dalla documentazione. L'app invia automaticamente i campi richiesti (incluso il sistema operativo coerente con il dispositivo selezionato) e arrotonda il numero di risultati richiesti al valore di profondità più vicino consentito dall'API (multipli di 10 fino a un massimo di 100).

## Struttura
- `README.md`: breve descrizione del progetto e delle istruzioni operative.
- `app.py`: applicazione Streamlit che integra DataForSEO e OpenAI per la generazione degli spunti SEO.
- `streamlit_app.py`: semplice entrypoint da utilizzare su Streamlit Cloud o ambienti che richiedono questo nome di file.
- `requirements.txt`: elenco delle dipendenze Python richieste.

### Distribuzione su Streamlit Community Cloud

- Mantieni `streamlit_app.py` come entrypoint principale: è il file che Streamlit Cloud esegue automaticamente.
- Assicurati che `requirements.txt` contenga tutte le dipendenze necessarie (Streamlit, Requests, BeautifulSoup e OpenAI) prima di effettuare il deploy.
- Configura le credenziali sensibili (login e password DataForSEO, API key OpenAI) tramite gli `Secrets` del progetto Streamlit, come indicato dalla [documentazione ufficiale](https://docs.streamlit.io/get-started/installation/community-cloud).

## Utilizzo
Apri il repository, configura le variabili richieste nell'app e personalizza il flusso secondo le esigenze delle tue prove.
