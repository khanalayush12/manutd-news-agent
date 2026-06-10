import feedparser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from news_sources import SOURCES

# ---------- CREDIBILITY SYSTEM ----------
def score_source(title, source):
    title = title.lower()
    source = source.lower()

    score = 50  # base

    # Trusted sources
    if "bbc" in source:
        score += 40
    elif "skysports" in source:
        score += 35
    elif "manutd.com" in source:
        score += 50

    # Important topics
    if "transfer" in title:
        score += 20
    if "injury" in title:
        score += 15
    if "ten hag" in title:
        score += 10
    if "rashford" in title or "bruno" in title:
        score += 10

    return min(score, 100)

# ---------- FETCH NEWS ----------
def fetch_news():
    articles = []

    for url in SOURCES:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.title.lower()

            # ONLY keep Manchester United related news
            if any(keyword in title for keyword in [
                "manchester united",
                "man utd",
                "man united",
                "rashford",
                "bruno",
                "old trafford",
                "ten hag",
                "red devils"
            ]):
                articles.append({
                    "title": entry.title,
                    "source": url,
                    "score": score_source(entry.title, url)
                })

    return articles

# ---------- RANK NEWS ----------
def rank_news(articles):
    return sorted(articles, key=lambda x: x["score"], reverse=True)[:10]

# ---------- GENERATE PDF ----------
def generate_pdf(news_list):
    filename = "manutd_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Manchester United AI News Briefing")

    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Generated: {datetime.now()}")

    y = 700

    for i, item in enumerate(news_list, start=1):
        text = f"{i}. ({item['score']}) {item['title']}"
        c.drawString(50, y, text[:100])
        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()
    print("PDF generated:", filename)

# ---------- MAIN ----------
if __name__ == "__main__":
    news = fetch_news()
    top_news = rank_news(news)
    generate_pdf(top_news)
