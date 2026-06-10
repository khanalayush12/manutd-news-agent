from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Dummy Manchester United news (we can upgrade later)
news = [
    "Man United linked with new midfielder signing",
    "Rashford injury update released by club",
    "Ten Hag press conference ahead of next match",
    "Manchester United exploring transfer options in January",
    "Academy player promoted to first team training"
]

def generate_pdf(news_list):
    filename = "manutd_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Manchester United News Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Generated: {datetime.now()}")

    y = 700

    for i, item in enumerate(news_list[:10], start=1):
        c.drawString(50, y, f"{i}. {item}")
        y -= 20

    c.save()
    print(f"PDF generated: {filename}")

if __name__ == "__main__":
    generate_pdf(news)
