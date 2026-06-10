import feedparser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from news_sources import SOURCES

# ---------- CREDIBILITY SYSTEM ----------
def score_source(title, source):
    source = source.lower()

    if "bbc" in source or "manutd.com" in source:
        return 95
    elif "skysports" in source:
        return 85
    else:
        return 70

# ---------- FETCH NEWS ----------
def fetch_news():
    articles = []

    for url in SOURCES:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
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
