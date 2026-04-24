# ainews-it — AI News Aggregator (Italiano)

**ainews-it** è un piccolo progetto Python che aggrega notizie in lingua inglese su intelligenza artificiale da fonti RSS, ne filtra la rilevanza, le traduce in italiano con stile editoriale professionale e crea automaticamente bozze (*drafts*) su un sito **WordPress** tramite la REST API.

---

## 📦 Installazione

1. Clonare o creare la directory del progetto:
   ```bash
   cd /root/.openclaw/workspace/ainews-it
   ```

2. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Installare i pacchetti di sistema richiesti (su Debian/Ubuntu):
   ```bash
   apt-get update && apt-get install -y python3-dev libxml2-dev libxslt-dev zlib1g-dev
   ```

---

## ⚙️ Configurazione

### 1. Variabili d’ambiente (`.env`)
Copia `.env.example` in `.env` e compila i valori:

```env
# WordPress
WP_URL=https://your-wordpress-site.com
WP_USERNAME=your-wp-username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Opzionale
FETCH_INTERVAL_HOURS=6
MAX_ARTICLES_PER_RUN=10
```

- **WordPress Application Password**: crea un’app password su WordPress > Impostazioni > Sicurezza > Applicazioni password (o strumenti del genere) e incolla qui. Le bozze verranno create automaticamente.
- **OPENAI_API_KEY**: chiave API OpenAI con accesso al modello specificato.

### 2. Configurazione avanzata (`config.yaml`)
Modifica `config.yaml` se vuoi aggiungere fonti, cambiare soglie di rilevanza o parole chiave.

- `sources` — elenco di RSS da cui leggere.
- `filtering` — soglia di rilevanza, parole chiave da escludere/boostare, età massima degli articoli.
- `translation.style_prompt` — prompt stilistico per la traduzione (modificabile).
- `wordpress` — categoria, tag di default e stato di pubblicazione (di default *draft*).

---

## ▶️ Esecuzione

### Prova in modalità dry-run (consigliata prima della prima esecuzione)
```bash
python main.py --dry-run
```

Questo scarica i feed, applica i filtri e mostra una tabella con gli articoli che verrebbero processati, **senza** tradurre o pubblicare.

### Esecuzione completa
```bash
python main.py
```

L’elaborazione per ogni articolo include:
1. Recupero del testo completo (opzionale, richiede `lxml` e accesso HTTP).
2. Traduzione + adattamento editoriale tramite OpenAI.
3. Creazione di una bozza WordPress come **draft** (revisione umana richiesta prima della pubblicazione).
4. Registrazione dell’articolo nel database SQLite per evitare duplicati.

### Limitare il numero di articoli per run
```bash
python main.py --limit 5
```

### Ricerca del testo completo per una traduzione migliore
```bash
python main.py --full-text
```

---

## 🕓 Esecuzione automatica (cron)

Puoi installare un cron job che esegue il programma ogni 6 ore:

```bash
./setup_cron.sh
```

Lo script installa una voce crontab del tipo:
```
0 */6 * * * cd /root/.openclaw/workspace/ainews-it && python main.py --limit 10 >> logs/ainews.log 2>&1
```

I log verranno scritti in `logs/ainews.log`. Assicurati che il percorso del file `.env` e la cartella `logs/` siano corretti.

---

## 🧩 Struttura del progetto

```
/root/.openclaw/workspace/ainews-it/
├── README.md
├── requirements.txt
├── .env.example
├── config.yaml
├── main.py
├── ainews/
│   ├── __init__.py
│   ├── fetcher.py       # RSS + API fetching
│   ├── filter.py        # Relevance filtering + dedup
│   ├── translator.py    # EN→IT translation via OpenAI
│   ├── wordpress.py     # WordPress REST API draft creation
│   └── storage.py       # SQLite for seen articles
├── setup_cron.sh        # Helper to install as system cron
└── Dockerfile           # Optional containerized run
```

---

## 📝 Aggiungere nuove fonti

Modifica `config.yaml` nella sezione `sources`. Esempio:

```yaml
- name: "My Custom Source"
  url: "https://example.com/feed/"
  type: rss
  weight: 1.0
```

I parametri `weight` influenzano solo l’ordinamento interno (fonti con peso maggiore appariranno prima nei log). La rilevanza dipende principalmente dalle parole chiave.

---

## ⚠️ Note importanti

- **WordPress**: vengono create solo bozze (*draft*). Un amministratore dovrà revisionare e pubblicare.
- **Database**: il file SQLite (`ainews_seen.db`) mantiene gli URL già processati. Non verrà ritrasmesso a meno che non cambi la query o il filtro.
- **OpenAI**: il modello e la temperatura sono configurabili tramite `OPENAI_MODEL` e `temperature` nel codice (default 0.4).
- **Errori**: se una singola API fallisce, l’esecuzione continua con gli altri articoli; l’articulo problematico viene comunque marcato come "già visto" per evitare tentativi ripetuti.

---

## 🛡️ Sicurezza

- Le credenziali di WordPress vanno conservate nell’ambiente (`.env`), mai nel codice.
- L’accesso alla REST API WordPress usa Basic Auth con app password (sicuro quando combinato con HTTPS).
- Il programma non invia dati sensibili esternamente oltre che a WordPress ed OpenAI.

---

## 🙌 Ringraziamenti

Realizzato come strumento interno per l’aggregazione e la diffusione controllata di notizie tecnologiche in ambito AI.