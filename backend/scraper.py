import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from typing import Tuple

# A friendly User-Agent to reduce being blocked by web servers
DEFAULT_HEADERS = {
    "User-Agent": "AI-Quiz-Generator/1.0 (+https://example.com; contact@example.com)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def _extract_title_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    if "/wiki/" in path:
        # article title is everything after /wiki/
        return path.split("/wiki/")[-1]
    # fallback: last part of path
    return path.rstrip("/").split("/")[-1]

def scrape_wikipedia(url: str) -> Tuple[str, str]:
    """
    Retrieve a clean text and title for a Wikipedia article.

    Strategy:
    1) Extract article title from URL and call the Wikipedia REST summary API (fast, reliable).
    2) If the REST API fails or returns insufficient content, fetch the article HTML
       with a proper User-Agent and parse the main content (#mw-content-text),
       removing tables, sup tags, scripts/styles, and collapsing paragraphs.

    Returns:
      (title, article_text)
    Raises:
      requests.HTTPError for HTTP errors, ValueError for invalid input.
    """
    if not url or "wikipedia.org" not in url:
        raise ValueError("URL must be a Wikipedia article URL")

    article_title_fragment = _extract_title_from_url(url)
    # try the REST summary endpoint first (returns JSON with extract)
    summary_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_title_fragment}"
    try:
        resp = requests.get(summary_api, headers=DEFAULT_HEADERS, timeout=10)
        if resp.status_code == 200:
            j = resp.json()
            title = j.get("title", unquote(article_title_fragment))
            # prefer the 'extract' field which is clean plain text
            extract = j.get("extract", "")
            if extract and len(extract.strip()) > 50:
                return title, extract
        # if API returns something else (e.g. 404) fall through to HTML fetch
    except requests.RequestException:
        # If API failed (network, etc.), fallback to HTML fetch
        pass

    # Fallback: fetch the full HTML page (with headers to avoid 403)
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    resp.raise_for_status()  # will raise HTTPError if status >= 400
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract Title
    title_tag = soup.find("h1", {"id": "firstHeading"})
    title = title_tag.get_text(strip=True) if title_tag else unquote(article_title_fragment)

    # Find main article content
    content = soup.find("div", {"id": "mw-content-text"})
    if content is None:
        # If structure differs, attempt to grab main paragraphs as fallback
        paragraphs = soup.find_all("p")
        paragraphs_text = "\n".join(p.get_text(" ", strip=True) for p in paragraphs)
        if not paragraphs_text:
            raise requests.HTTPError(f"Failed to extract content from {url}")
        return title, paragraphs_text

    # Remove undesired tags
    for tag in content.find_all(["table", "sup", "style", "script", "aside", "figure"]):
        tag.decompose()

    # Collect paragraphs in the article body
    paragraphs = []
    for p in content.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if txt:
            paragraphs.append(txt)

    article_text = "\n\n".join(paragraphs).strip()
    if not article_text:
        raise requests.HTTPError(f"No readable article text found at {url}")

    return title, article_text