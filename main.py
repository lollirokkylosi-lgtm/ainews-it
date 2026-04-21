#!/usr/bin/env python3
"""
ainews-it: AI news aggregator → Italian → WordPress drafts
"""
import os
import sys
import yaml
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from ainews.storage import init_db, mark_seen, get_stats
from ainews.fetcher import fetch_source, fetch_full_text
from ainews.filter import filter_articles
from ainews.translator import translate_article
from ainews.wordpress import create_draft

console = Console()
load_dotenv()


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def run(config: dict, dry_run: bool = False, limit: int = None, fetch_fulltext: bool = False):
    console.rule("[bold blue]🤖 ainews-it — AI News Aggregator")

    init_db()
    stats = get_stats()
    console.print(f"[dim]DB: {stats['total']} articoli visti finora[/dim]")

    # Fetch da tutte le fonti
    all_articles = []
    for source in config["sources"]:
        console.print(f"[cyan]Fetching:[/cyan] {source['name']}...")
        articles = fetch_source(source, max_age_hours=config["filtering"].get("max_age_hours", 48))
        all_articles.extend(articles)
        console.print(f"  → {len(articles)} articoli trovati")

    console.print(f"\n[bold]Totale fetchati:[/bold] {len(all_articles)}")

    # Filtra e deduplicati
    filtered = filter_articles(all_articles, config["filtering"])
    console.print(f"[bold]Dopo il filtro:[/bold] {len(filtered)} articoli nuovi rilevanti")

    if limit:
        filtered = filtered[:limit]

    if not filtered:
        console.print("[yellow]Nessun nuovo articolo da processare.[/yellow]")
        return

    # Mostra tabella preview
    table = Table(title="Articoli da processare")
    table.add_column("#", style="dim")
    table.add_column("Titolo", max_width=55)
    table.add_column("Fonte")
    table.add_column("Score", justify="right")
    for i, art in enumerate(filtered, 1):
        table.add_row(str(i), art.title[:55], art.source, f"{art.relevance_score:.2f}")
    console.print(table)

    if dry_run:
        console.print("[yellow]Dry run — stop prima di traduzione/pubblicazione.[/yellow]")
        return

    # Processa ogni articolo
    max_per_run = int(os.environ.get("MAX_ARTICLES_PER_RUN", 10))
    processed = 0

    for art in filtered[:max_per_run]:
        console.print(f"\n[bold]Processo:[/bold] {art.title[:60]}...")

        if fetch_fulltext and art.url:
            console.print("  [dim]Scarico testo completo...[/dim]")
            art.full_text = fetch_full_text(art.url)

        # Traduzione
        try:
            console.print("  [dim]Traduco in italiano...[/dim]")
            translated = translate_article(
                art,
                style_prompt=config["translation"]["style_prompt"],
                model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            )
            console.print(f"  [green]✓[/green] Titolo: {translated['title_it'][:60]}")
        except Exception as e:
            console.print(f"  [red]✗ Traduzione fallita:[/red] {e}")
            continue

        # Salva su WordPress
        try:
            console.print("  [dim]Salvo come bozza WordPress...[/dim]")
            result = create_draft(art, translated, config["wordpress"])
            wp_id = result.get("id")
            wp_url = os.environ.get("WP_URL", "").rstrip("/")
            wp_edit_url = f"{wp_url}/wp-admin/post.php?post={wp_id}&action=edit"
            console.print(f"  [green]✓[/green] Bozza salvata → Post #{wp_id}: {wp_edit_url}")
            mark_seen(art.url, art.title, art.source, wp_post_id=wp_id)
            processed += 1
        except Exception as e:
            console.print(f"  [red]✗ WordPress fallito:[/red] {e}")
            mark_seen(art.url, art.title, art.source)

    console.rule(f"[green]Fatto — {processed} bozze salvate su WordPress[/green]")


def main():
    parser = argparse.ArgumentParser(description="ainews-it: AI news aggregator per WordPress italiano")
    parser.add_argument("--config", default="config.yaml", help="Percorso file config")
    parser.add_argument("--dry-run", action="store_true", help="Fetch e filtro senza traduzione/pubblicazione")
    parser.add_argument("--limit", type=int, default=None, help="Max articoli da processare in questo run")
    parser.add_argument("--full-text", action="store_true", help="Scarica testo completo per traduzione migliore")
    args = parser.parse_args()

    config = load_config(args.config)
    run(config, dry_run=args.dry_run, limit=args.limit, fetch_fulltext=args.full_text)


if __name__ == "__main__":
    main()
