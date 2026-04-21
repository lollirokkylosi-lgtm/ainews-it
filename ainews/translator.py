import os
import json
from openai import OpenAI
from ainews.fetcher import Article


def translate_article(article: Article, style_prompt: str, model: str = "gpt-4o") -> dict:
    """
    Translate and editorially adapt an article to Italian.

    Returns dict with keys: title_it, body_it, excerpt_it, tags_it
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    source_text = f"""
TITOLO ORIGINALE: {article.title}
FONTE: {article.source}
URL: {article.url}

CONTENUTO:
{article.summary}
{article.full_text[:1500] if article.full_text else ''}
""".strip()

    system = style_prompt.strip()

    user_prompt = f"""Traduci e adatta in italiano questo articolo di tecnologia/AI.

{source_text}

Rispondi SOLO con questo JSON (nessun testo extra):
{{
  "titolo": "Il titolo in italiano (max 80 caratteri)",
  "corpo": "Il testo dell'articolo in italiano (2-3 paragrafi, ~200-300 parole). Includi alla fine: Fonte: {article.source}",
  "excerpt": "Un riassunto di 1-2 frasi per l'anteprima (max 160 caratteri)",
  "tags": ["tag1", "tag2", "tag3"]
}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    result = json.loads(response.choices[0].message.content)
    return {
        "title_it": result.get("titolo", article.title),
        "body_it": result.get("corpo", ""),
        "excerpt_it": result.get("excerpt", ""),
        "tags_it": result.get("tags", []),
    }
