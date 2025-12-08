"""
Flask Blog Application
----------------------
This app loads, displays, creates, edits, and deletes article JSON files
stored under the /articles directory.

It also includes simple HTTP Basic Authentication for admin routes.
"""

from flask import Flask, render_template, request, abort, redirect, url_for, Response
from pathlib import Path
import json
import re
from functools import wraps

app = Flask(__name__)

# Path where all article JSON files are stored
ARTICLES_DIR = Path(__file__).parent / "articles"


# -------------------------------------------------------------------
# BASIC AUTHENTICATION SETUP
# -------------------------------------------------------------------

# Hardcoded admin credentials (simple, not secure for production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secret"


def check_auth(username, password):
    """Return True if the provided credentials match admin credentials."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


def authenticate():
    """
    Returns a 401 response with a 'WWW-Authenticate' header.
    This forces the browser to show the login popup.
    """
    return Response(
        "Authentication required. Please enter admin username and password.",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    """
    Decorator that protects routes using HTTP Basic Authentication.
    Runs BEFORE the actual view function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization  # Extract the Authorization header

        # If no credentials OR invalid credentials → ask again
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        # Credentials valid → allow access
        return f(*args, **kwargs)

    return decorated


# -------------------------------------------------------------------
# ARTICLE LOADING / READING HELPERS
# -------------------------------------------------------------------

def read_json(path: Path) -> dict | None:
    """Load a JSON file and return its content as a Python dictionary."""
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("JSON Error:", e)
        return None


def make_slug(path: Path) -> str:
    """Return the filename (without extension) as the article slug."""
    return path.stem


def normalize_json(raw_json: dict, slug_from_file: str) -> dict:
    """
    Ensure article JSON always contains consistent fields when used in templates.
    Missing keys are replaced with defaults.
    """
    slug = raw_json.get("slug", slug_from_file)

    return {
        "title": raw_json.get("title", "Untitled Article"),
        "slug": slug,
        "category": raw_json.get("category", "Unknown Category"),
        "author": raw_json.get("author", "Unknown Author"),
        "summary": raw_json.get("summary", "No summary available."),
        "content": raw_json.get("content", "No content available."),
        "published_date": raw_json.get("published_date", "Unknown Date"),
    }


def load_all_articles():
    """
    Load ALL articles from the ARTICLES_DIR folder.
    Returns a list of normalized article dictionaries.
    """
    articles = []

    if not ARTICLES_DIR.exists():
        print("The articles/ directory does not exist.")
        return articles

    for json_file in sorted(ARTICLES_DIR.glob("*.json")):
        raw_json = read_json(json_file)
        if raw_json is None:
            continue

        slug = make_slug(json_file)
        articles.append(normalize_json(raw_json, slug))

    return articles


def load_article(slug: str) -> dict | None:
    """
    Load a single article by slug.
    Returns None if slug is invalid or file does not exist.
    """
    # Only allow safe filename characters
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", slug):
        return None

    file = ARTICLES_DIR / f"{slug}.json"
    if not file.exists():
        return None

    raw_json = read_json(file)
    if raw_json is None:
        return None

    return normalize_json(raw_json, slug)


# -------------------------------------------------------------------
# ROUTES (PUBLIC)
# -------------------------------------------------------------------

@app.route("/")
def index():
    """Public homepage: shows a list of all articles."""
    articles = load_all_articles()
    return render_template("index.html", articles=articles)


@app.route("/articles/<slug>")
def article(slug):
    """Display a single article page."""
    art = load_article(slug)

    if not art:
        abort(404)

    return render_template("article.html", article=art)


# -------------------------------------------------------------------
# ADMIN ROUTES (PROTECTED BY BASIC AUTH)
# -------------------------------------------------------------------

@app.route("/admin")
@requires_auth
def admin():
    """Admin panel: lists all articles with edit/delete buttons."""
    articles = load_all_articles()
    return render_template("admin.html", articles=articles)


@app.route("/edit/<slug>", methods=["GET", "POST"])
@requires_auth
def edit(slug):
    """Edit an existing article."""
    article = load_article(slug)
    if not article:
        abort(404)

    if request.method == "POST":
        # Update article fields with form input
        article["title"] = request.form["title"]
        article["category"] = request.form["category"]
        article["published_date"] = request.form["published_date"]
        article["content"] = request.form["content"]

        # Save updated JSON file
        filepath = ARTICLES_DIR / f"{slug}.json"
        filepath.write_text(json.dumps(article, indent=2))

        return redirect(url_for("admin"))

    return render_template("edit.html", article=article)


def calculate_slug() -> str:
    """
    Generate the next article number based on highest existing number.
    Example: article1.json, article2.json → returns "3".
    """
    numbers = []

    for file in ARTICLES_DIR.glob("*.json"):
        match = re.search(r"(\d+)$", file.stem)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers) + 1 if numbers else 0
    return str(next_number)


@app.route("/new", methods=["GET", "POST"])
@requires_auth
def new():
    """Create a brand new article and save it as a JSON file."""
    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        published_date = request.form["published_date"]
        content = request.form["content"]
        author = request.form["author"]

        summary = content[:200]  # auto-summary
        slug = f"article{calculate_slug()}"

        # Build JSON data
        data = {
            "title": title,
            "category": category,
            "published_date": published_date,
            "content": content,
            "summary": summary,
            "author": author,
            "slug": slug,
        }

        # Save file
        file_path = ARTICLES_DIR / f"{slug}.json"
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        return redirect(url_for("admin"))

    return render_template("new.html")


@app.route("/delete/<slug>", methods=["GET", "POST"])
@requires_auth
def delete(slug):
    """Delete an article from the filesystem."""
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", slug):
        abort(400)

    file = ARTICLES_DIR / f"{slug}.json"
    if file.exists():
        file.unlink()

    return redirect(url_for("admin"))


# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
