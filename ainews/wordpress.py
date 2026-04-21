import os
import requests
from requests.auth import HTTPBasicAuth
from ainews.fetcher import Article


def get_or_create_category(wp_url: str, auth: HTTPBasicAuth, category_name: str) -> int:
    r = requests.get(
        f"{wp_url}/wp-json/wp/v2/categories",
        params={"search": category_name},
        auth=auth,
    )
    r.raise_for_status()
    cats = r.json()
    for cat in cats:
        if cat["name"].lower() == category_name.lower():
            return cat["id"]
    # Create it
    r = requests.post(
        f"{wp_url}/wp-json/wp/v2/categories",
        json={"name": category_name},
        auth=auth,
    )
    r.raise_for_status()
    return r.json()["id"]


def get_or_create_tags(wp_url: str, auth: HTTPBasicAuth, tag_names: list[str]) -> list[int]:
    tag_ids = []
    for name in tag_names:
        r = requests.get(
            f"{wp_url}/wp-json/wp/v2/tags",
            params={"search": name},
            auth=auth,
        )
        tags = r.json() if r.ok else []
        found = next((t for t in tags if t["name"].lower() == name.lower()), None)
        if found:
            tag_ids.append(found["id"])
        else:
            r2 = requests.post(
                f"{wp_url}/wp-json/wp/v2/tags",
                json={"name": name},
                auth=auth,
            )
            if r2.ok:
                tag_ids.append(r2.json()["id"])
    return tag_ids


def create_draft(article: Article, translated: dict, wp_config: dict) -> dict:
    wp_url = os.environ["WP_URL"].rstrip("/")
    username = os.environ["WP_USERNAME"]
    app_password = os.environ["WP_APP_PASSWORD"]
    auth = HTTPBasicAuth(username, app_password)

    category_id = get_or_create_category(wp_url, auth, wp_config.get("category_name", "AI News"))

    all_tags = wp_config.get("default_tags", []) + translated.get("tags_it", [])
    tag_ids = get_or_create_tags(wp_url, auth, list(set(all_tags)))

    # Build the post body with a source link at the bottom
    body_html = translated["body_it"].replace("\n\n", "</p><p>")
    body_html = f"<p>{body_html}</p>"
    body_html += (
        f'\n<p><em>Articolo originale: '
        f'<a href="{article.url}" target="_blank" rel="noopener">{article.source}</a>'
        f'</em></p>'
    )

    post_data = {
        "title": translated["title_it"],
        "content": body_html,
        "excerpt": translated["excerpt_it"],
        "status": wp_config.get("status", "draft"),
        "categories": [category_id],
        "tags": tag_ids,
        "meta": {
            "original_url": article.url,
            "original_source": article.source,
        },
    }

    r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", json=post_data, auth=auth)
    r.raise_for_status()
    return r.json()
