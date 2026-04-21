# ainews-it 🤖🇮🇹

Aggrega notizie sull'intelligenza artificiale dalle principali fonti in inglese, le traduce in italiano con stile editoriale e le salva come bozze su WordPress — pronte per essere rilette e pubblicate.

## Come funziona

```
Fonti EN                  Pipeline                 Output
──────────                ────────                 ──────
HN / TechCrunch           1. Fetch RSS             Bozza WordPress
The Verge / Wired    →    2. Filtro rilevanza  →   (titolo IT +
ArXiv / OpenAI Blog       3. Deduplicazione        corpo IT +
Anthropic / MIT TR        4. Traduzione IT         fonte originale)
...                       5. Salva bozza
                          6. Log locale
```

Il sistema gira ogni 6 ore (via cron), evita duplicati tramite SQLite, e non pubblica mai automaticamente — sei sempre tu a fare review e pubblicare.

## Installazione

```bash
git clone https://github.com/lollirokkylosi-lgtm/ainews-it
cd ainews-it
# Crea e attiva il virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con le tue credenziali
```

## Configurazione

### `.env`

```env
# WordPress
WP_URL=https://tuo-sito.it
WP_USERNAME=tuo-username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Opzionali
FETCH_INTERVAL_HOURS=6
MAX_ARTICLES_PER_RUN=10
```

### WordPress Application Password

1. Vai su **WP Admin → Utenti → Il tuo profilo**
2. Scorri fino a **Application Passwords**
3. Nome: `ainews-it` → clicca **Aggiungi**
4. Copia la password generata (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### `config.yaml`

Puoi aggiungere fonti, modificare keyword di boost/esclusione, e personalizzare il prompt di traduzione.

## Utilizzo

```bash
# Prima volta: testa senza tradurre/pubblicare
python main.py --dry-run

# Run normale (max 5 articoli)
python main.py --limit 5

# Con testo completo per traduzione migliore (più lento)
python main.py --limit 5 --full-text

# Config personalizzata
python main.py --config mia-config.yaml
```

## Installazione automatica (cron ogni 6 ore)

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

I log vanno in `logs/ainews.log`.

## Docker

```bash
docker build -t ainews-it .
docker run --env-file .env ainews-it
```

## Struttura progetto

```
ainews-it/
├── main.py              # Entry point
├── config.yaml          # Fonti, filtri, stile traduzione
├── .env.example         # Template credenziali
├── requirements.txt
├── ainews/
│   ├── fetcher.py       # Fetch RSS da tutte le fonti
│   ├── filter.py        # Filtro rilevanza + deduplicazione
│   ├── translator.py    # Traduzione EN→IT via OpenAI
│   ├── wordpress.py     # Salva bozze via WP REST API
│   └── storage.py       # SQLite per articoli già visti
├── setup_cron.sh        # Installa cron job
└── Dockerfile
```

## Aggiungere nuove fonti

Aggiungi una voce in `config.yaml` sotto `sources`:

```yaml
- name: "Nome Fonte"
  url: "https://esempio.com/rss"
  type: rss
  weight: 1.0
```

## Licenza

MIT
