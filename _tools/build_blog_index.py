"""Generate /blog/index.html. JS on the page hides future-dated posts."""
import re
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path("/sessions/ecstatic-jolly-fermat/mnt/SCORM wrapper for Vibe Code/Marketing_Site/blog")

def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %B %Y")
    except ValueError:
        return datetime.min

def iso_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""

posts = []
for md_file in sorted(BLOG_DIR.glob("*.md")):
    fm = parse_frontmatter(md_file.read_text())
    if not fm.get("title"):
        continue
    posts.append({
        "title": fm.get("title", ""),
        "lede": fm.get("lede", ""),
        "date": fm.get("date", ""),
        "date_obj": parse_date(fm.get("date", "")),
        "date_iso": iso_date(fm.get("date", "")),
        "read_time": fm.get("read_time", ""),
        "slug": fm.get("slug", md_file.stem),
    })

posts.sort(key=lambda p: p["date_obj"], reverse=True)

post_cards = []
for p in posts:
    post_cards.append(f"""        <a href="/blog/{p['slug']}.html" class="post-card" data-publish-date="{p['date_iso']}">
          <p class="post-meta">{p['date']}, about {p['read_time']} read</p>
          <h2>{p['title']}</h2>
          <p class="post-lede">{p['lede']}</p>
          <span class="read-more">Read post &rarr;</span>
        </a>""")
post_cards_html = "\n".join(post_cards)

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blog, AI Learning Packager</title>
  <meta name="description" content="Practical, opinionated writing on SCORM, xAPI, and the gap between AI-generated learning content and the systems that have to host it.">

  <meta property="og:title" content="AI Learning Packager blog">
  <meta property="og:description" content="Practical, opinionated writing on SCORM and xAPI.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://packager.dtttech.com/blog/">
  <meta property="og:image" content="https://packager.dtttech.com/banner.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%230a0e27'/%3E%3Ctext x='50' y='66' font-size='52' text-anchor='middle' fill='%2300d4aa' font-family='Helvetica,Arial' font-weight='800'%3EP%3C/text%3E%3C/svg%3E">

  <style>
    :root {
      --navy-deep: #0a0e27; --navy-mid: #151a3d; --navy-card: #1a2050; --navy-border: #1e2650;
      --teal: #00d4aa; --teal-deep: #00b894; --text-white: #f0f4ff; --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: linear-gradient(135deg, var(--navy-deep), var(--navy-mid)); color: var(--text-white); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; min-height: 100vh; }
    body { background-attachment: fixed; }
    .container-wide { max-width: 960px; margin: 0 auto; padding: 0 24px; }
    .container { max-width: 760px; margin: 0 auto; padding: 0 24px; }
    header { padding: 24px 0; border-bottom: 1px solid var(--navy-border); }
    .nav { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
    .brand { font-weight: 800; font-size: 18px; color: var(--text-white); text-decoration: none; letter-spacing: -0.3px; }
    .brand span { color: var(--teal); }
    .nav-links { display: flex; gap: 24px; font-size: 14px; }
    .nav-links a { color: var(--text-muted); text-decoration: none; }
    .nav-links a:hover { color: var(--teal); }
    .page-header { padding: 64px 0 32px; text-align: left; }
    .eyebrow { display: inline-block; color: var(--teal); font-size: 12px; font-weight: 700; letter-spacing: 4px; margin-bottom: 20px; text-transform: uppercase; }
    h1 { font-size: clamp(34px, 5vw, 48px); font-weight: 800; letter-spacing: -1px; line-height: 1.15; margin: 0 0 20px; }
    .page-lede { font-size: 19px; color: var(--text-muted); max-width: 640px; margin: 0; line-height: 1.5; }
    .posts { padding: 24px 0 64px; display: grid; gap: 20px; }
    .post-card { background: var(--navy-card); border: 1px solid var(--navy-border); border-radius: 14px; padding: 32px; display: block; text-decoration: none; color: inherit; transition: border-color 0.15s ease, transform 0.15s ease; }
    .post-card:hover { border-color: var(--teal); transform: translateY(-2px); }
    .post-card .post-meta { font-size: 12px; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; margin: 0 0 10px; }
    .post-card h2 { font-size: 24px; font-weight: 800; letter-spacing: -0.4px; margin: 0 0 12px; color: var(--text-white); }
    .post-card .post-lede { font-size: 16px; color: var(--text-muted); margin: 0 0 16px; line-height: 1.5; }
    .post-card .read-more { font-size: 14px; color: var(--teal); font-weight: 700; }
    .empty-state { background: var(--navy-card); border: 1px solid var(--navy-border); border-radius: 14px; padding: 48px; text-align: center; color: var(--text-muted); }
    .cta-section { padding: 0 0 64px; }
    .cta { background: linear-gradient(180deg, var(--navy-card), var(--navy-mid)); border: 1px solid var(--navy-border); border-radius: 20px; padding: 40px; text-align: center; }
    .cta h2 { font-size: 24px; font-weight: 800; margin: 0 0 12px; }
    .cta p { color: var(--text-muted); margin: 0 0 24px; font-size: 15px; }
    .cta-button { display: inline-block; padding: 14px 28px; border-radius: 30px; background: var(--teal); color: var(--navy-deep); font-weight: 700; font-size: 15px; text-decoration: none; transition: background 0.15s ease; }
    .cta-button:hover { background: var(--teal-deep); }
    footer { padding: 40px 0; border-top: 1px solid var(--navy-border); color: var(--text-muted); font-size: 14px; text-align: center; }
    footer a { color: var(--teal); text-decoration: none; }
    footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <header>
    <div class="container-wide nav">
      <a href="/" class="brand">AI Learning <span>Packager</span></a>
      <nav class="nav-links">
        <a href="/#what">What it does</a>
        <a href="/#who">Who it is for</a>
        <a href="/blog/">Blog</a>
        <a href="/#signup">Get early access</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="container">
      <div class="page-header">
        <div class="eyebrow">Blog</div>
        <h1>Practical writing on SCORM and xAPI</h1>
        <p class="page-lede">Independent, opinionated, no vendor pitches. Notes from someone who builds SCORM packages and is tired of the marketing version of the answer.</p>
      </div>

      <div class="posts" id="posts-grid">
__POST_CARDS__
      </div>
    </div>

    <div class="container-wide cta-section">
      <div class="cta">
        <h2>Want to try the tool the blog is from?</h2>
        <p>Private beta. Drop in an HTML file or folder, get back a SCORM 1.2 zip in seconds.</p>
        <a href="/#signup" class="cta-button">Request access</a>
      </div>
    </div>
  </main>
  <footer>
    <div class="container-wide">
      <p>A project from <a href="https://dtttech.com">Digital Technology Training</a>. Built in public.</p>
    </div>
  </footer>

  <script>
    // Hide post cards whose publish date is in the future.
    (function() {
      var today = new Date().toISOString().slice(0, 10);
      var cards = document.querySelectorAll(".post-card[data-publish-date]");
      cards.forEach(function(card) {
        var d = card.getAttribute("data-publish-date");
        if (d && d > today) {
          card.style.display = "none";
        }
      });
    })();
  </script>
</body>
</html>
"""

out = BLOG_DIR / "index.html"
out.write_text(INDEX_TEMPLATE.replace("__POST_CARDS__", post_cards_html))
print(f"Built: {out}")
print(f"Posts in HTML: {len(posts)}")
for p in posts:
    print(f"  - {p['date_iso']}: {p['title']}")
