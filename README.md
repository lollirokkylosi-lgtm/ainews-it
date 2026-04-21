# ainews-it 🤖🇮🇹

Aggrega notizie sull'intelligenza artificiale e sulle criptovalute dalle principali fonti in inglese, le traduce in italiano con stile editoriale e le salva come bozze su WordPress — pronte per essere rilette e pubblicate.

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
# Crea e attiva il virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copia il modello di configurazione
cp .env.example .env
```

## Configurazione

Compila **entrambi** i campi in `.env`:

### 1️⃣ WordPress Application Password

1. Vai su <https://aicryptoitalia.wordpress.com/wp-admin/profile.php>
2. Scorri fino a **Application Passwords**
3. Nome: `ainews-it` → clicca **Aggiungi**
4. **Copia la password generata** (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)
5. Inseriscila nel campo `WP_APP_PASSWORD` in `.env`

Esempio: `WP_APP_PASSWORD=qilj 4okc y63q vgap`

> Nota: WordPress.com richiede che la password sia lunga almeno 8 caratteri e contenga sia lettere maiuscole che minuscole.

### 2️⃣ OpenAI API Key

- Ottienila da <https://platform.openai.com/api-keys>
- Inseriscila nel campo `OPENAI_API_KEY` in `.env`

### 3️⃣ URL del sito

Il campo `WP_URL` è già impostato su `https://aicryptoitalia.wordpress.com`.

### 4️⃣ Configurazione aggiuntiva (opzionale)

Modifica `config.yaml` se vuoi:
- Aggiungere nuove fonti RSS
- Sintonizzare `keywords_boost`/`keywords_exclude`
- Cambiare il limite di articoli per run (`MAX_ARTICLES_PER_RUN`)

## Utilizzo

```bash
# Prima volta: testa senza tradurre/pubblicare
python main.py --dry-run

# Run normale (max 10 articoli)
python main.py --limit 5

# Con testo completo per traduzione migliore (più lento)
python main.py --limit 5 --full-text

# Config personalizzata
python main.py --config mia-config.yaml
```

Aggiungi un crontab ogni 6 ore:

```bash
# Usa il file setup_cron.sh (lo modifica a tuo piacimento)
bash setup_cron.sh
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
├── config.yaml          # Fonti, filtri, stile traduccione
├── .env.example         # Template credenziali
├── .env                 # ← CREA QUESTO FILE CON LE TUE CREDENZIALI
├── requirements.txt
├── ainews/
│   ├── fetcher.py       # Fetch RSS da tutte le fonti
│   ├── filter.py        # Rilevanza + dedup
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

## Note importanti per WordPress.com

- Questo sito è ospitato su **WordPress.com**, non su un self-hosted WordPress
- L'endpoint REST API è `https://aicryptoitalia.wordpress.com/wp-json/wp/v2/posts`
- Le richieste richiedono autenticazione via Application Password
- Non è necessario `wp-cron`; il sistema usa solo richieste HTTP regolari

## Licenza

MIT
