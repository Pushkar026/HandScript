from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from pathlib import Path

# BASE PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = STATIC_DIR / "handwriting_template_v1.pdf"

chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

c = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
width, height = A4

# Title
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2, height - 2 * cm, "Custom Handwriting Template")

# Instructions
c.setFont("Helvetica", 10)
c.drawCentredString(
    width / 2,
    height - 2.7 * cm,
    "Use black pen only • One character per box • Do not touch borders"
)

# Grid settings
cols = 7
rows = 8
box_size = 2.5 * cm
start_x = 2 * cm
start_y = height - 4 * cm

c.setFont("Helvetica", 9)

idx = 0
for row in range(rows):
    for col in range(cols):
        x = start_x + col * box_size
        y = start_y - row * box_size

        c.rect(x, y - box_size, box_size, box_size)

        if idx < len(chars):
            c.drawString(x + 4, y - 14, chars[idx])
            idx += 1

c.save()

print(f"Template generated at: {OUTPUT_FILE}")
