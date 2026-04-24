# 🚀 Guida al Deployment Base - Versione "Zero Coding"

Questa guida è pensata per chi **non ha mai programmato** e vuole mettere online il sistema `ainews-it` in 10 minuti, usando solo **copia-incolla**.

---

## 🎯 **Cosa faremo?**

Trasformeremo il tuo computer in un piccolo server che:
1. Legge le notizie di AI da vari siti (RSS)
2. Le filtra e le seleziona
3. Le traduce in italiano
4. Le salva su WordPress (o le mostra a video)

**Tutto in automatico, in background.**

---

## 📋 **FASE 0: I tre "Oggetti Magici"**

Non devi capirli, devi solo ricordarti che esistono:

1. **VS Code** → Un programma per scrivere codice (usa solo i bottoni, niente digitazione complessa)
2. **Il Terminale** → Un rettangolo nero dove scriveremo 2 comandi (copia-incolla)
3. **Il Browser** → Chrome/Edge, per vedere il risultato finale

---

## 🚦 **FASE 1: Preparare lo spazio**

### Passo 1.1: Aprire la cartella dei file
- Trova la cartella `ainews-it` (dovresti già averla sul notebook)
- Aprila e controlla di vedere questi file:
  - `config.yaml`
  - `main.py`
  - Una cartella chiamata `ainews`

### Passo 1.2: Installare VS Code (se non ce l'hai)
- Vai su: [code.visualstudio.com](https://code.visualstudio.com/)
- Clicca **Download**
- Installalo cliccando sempre **Avanti / Next** (non cambiare niente)

---

## 🛠️ **FASE 2: I dati segreti (File .env)**

### Passo 2.1: Copiare il template
- Nella cartella `ainews-it`, cerca il file **`.env.example`**
- Aprilo con un doppio click
- **Seleziona tutto → Copia (Ctrl+C)**

### Passo 2.2: Creare il file delle password
- Nella stessa cartella, crea un **Nuovo Documento di Testo**
- Nominalo esattamente **`.env`** (sì, con il punto davanti!)
- Se Windows ti avvisa, dì **Sì**
- Apri il file `.env` e **incolla** (Ctrl+V) il testo copiato prima

### Passo 2.3: Lascia tutto com'è (Per ora)
Non modificare nulla. Dovresti vedere:
```text
WP_URL=https://aicryptoitalia.wordpress.com
WP_USERNAME=lollirokkylosi
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

*Nota: per farlo funzionare in "modalità demo" senza pubblicare su WordPress, non serve compilare questi campi ora.*

---

## 🧪 **FASE 3: Far partire tutto (Il momento magico)**

### Passo 3.1: Aprire VS Code
- Apri il programma **Visual Studio Code**
- Clicca in alto: **File → Open Folder...**
- Scegli la cartella **`ainews-it`** → **Select Folder**
- Vedrai l'elenco dei file a sinistra

### Passo 3.2: Aprire il Terminale
- In alto nel menu: **Terminal → New Terminal**
- Si aprirà un rettangolo nero in basso. **Non scriverci niente!**

### Passo 3.3: Installare le scatoline necessarie
Nel rettangolo nero, **copia questo testo** e premi **Invio**:

```bash
pip install -r requirements.txt
```

⏳ **Aspetta.** Vedrai delle scritte scorrere. Ci mette 1-2 minuti. 
Quando il cursore lampeggiante torna, è pronto.

*(Se dice errore "pip non è riconosciuto", devi prima installare Python da python.org)*

### Passo 3.4: Avviare il programma! 🎉
Sempre nel rettangolo nero, **copia** questo e premi **Invio**:

```bash
python main.py --dry-run
```

Questo dice: *"Avvia il programma ma non pubblicare niente, mostrami solo cosa faresti"*.

### Passo 3.5: Guardare il risultato
Il rettangolo nero mostrerà:
- ✅ Quanti articoli ha letto
- ✅ Quanti ne ha filtrati
- ✅ Le traduzioni in italiano
- ✅ I titoli formattati

**Hai appena messo online il sistema!** Funziona sul tuo notebook!

---

## 🌍 **FASE 4: Vederlo come un vero sito (Opzionale)**

Se vuoi vederlo con la grafica:

1. Nella cartella `ainews-it`, c'è un file `index.html` o `dashboard.html`?
2. Tasto destro su quel file dentro VS Code
3. Scegli **"Open with Live Server"** (se non c'è, installa l'estensione gratuita *Live Server* su VS Code)
4. Si aprirà Chrome/Edge con il sito funzionante!

*(Se non c'è un file HTML, non preoccuparti: il programma lavora lo stesso, elabora i dati in background).*

---

## ⚙️ **FASE 5: Farlo funzionare tutti i giorni**

### Come tenerlo acceso:
1. Lascia **aperto VS Code**
2. Lascia **aperto il rettangolo nero**
3. Il computer deve essere **acceso** (non in stand-by)

### Come aggiornarlo ogni giorno:
- Ogni mattina, apri il rettangolo nero
- Premi **Freccia Su** (ti ripete l'ultimo comando)
- Premi **Invio**
- Leggi le nuove notizie tradotte!

### Per farlo partire automaticamente tutti i giorni:
Vedi il file `setup_cron.sh` nella cartella. Contiene le istruzioni per farlo partire ogni 6 ore in automatico.

---

## 🚨 **PROBLEMI COMUNI (e soluzioni)**

| Cosa succede | Perché | Soluzione |
|--------------|--------|-----------|
| **"pip" non funziona** | Manca Python | Installa Python da python.org (spunta "Add to PATH") |
| **Errore Red ❌** | Mancano file | Assicurati che `.env` sia uguale a `.env.example` |
| **Non si muove nulla** | Comando sbagliato | Ricopia i comandi, non scriverli a mano |
| **Errore OpenAI** | Manca la API Key | Per ora usa `--dry-run` (solo lettura) |
| **Errore WordPress** | Non configurato | Lascia stare, funziona in modalità demo |

---

## 🔄 **Come cambiare le API (Opzionale avanzato)**

Il programma usa OpenAI per tradurre. Puoi usare altre API (più economiche) modificando il file `translator.py`:

**Opzioni migliori (costano meno):**
- **Google Gemini 1.5 Flash**: Quasi gratis, molto veloce
- **Anthropic Claude 3.5 Sonnet**: Qualità altissima, costa meno di OpenAI
- **DeepSeek**: Costi bassissimi, ottime traduzioni

Chiedimi se vuoi che ti prepari la versione con queste API alternative!

---

## 📜 **RIASSUNTO PER STAMPARE**

```
✅ 1. Scarica VS Code (se non c'è)
✅ 2. Apri la cartella "ainews-it" in VS Code  
✅ 3. File → New Terminal
✅ 4. Copia: pip install -r requirements.txt → Invio
✅ 5. Copia: python main.py --dry-run → Invio
✅ 6. Goditi le notizie di AI in italiano!
```

---

## 🎓 **Prossimi passi (quando sei pronto)**

1. Leggi `README.md` per configurare WordPress
2. Chiedimi come usare **cron** per farlo partire in automatico ogni 6 ore
3. Studia come aggiungere nuove fonti RSS nel file `config.yaml`
4. Scopri come cambiare API (da OpenAI a Gemini/Claude) per risparmiare

Hai **completato la missione**! 🎉  
Il sistema è online e funzionante sul tuo notebook!