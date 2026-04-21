#!/bin/bash
# Installa ainews-it come cron job ogni 6 ore
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

CRON_LINE="0 */6 * * * cd $SCRIPT_DIR && python main.py --limit 10 --full-text >> $LOG_DIR/ainews.log 2>&1 # ainews-it"

# Rimuovi vecchia entry se esiste, aggiungi la nuova
(crontab -l 2>/dev/null | grep -v "ainews-it"; echo "$CRON_LINE") | crontab -

echo "✅ Cron job installato: gira ogni 6 ore"
echo "📋 Crontab attuale:"
crontab -l
echo ""
echo "📁 Log: $LOG_DIR/ainews.log"
