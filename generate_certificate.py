#!/usr/bin/env python3
"""
DCperf 2024 Best Paper Award Certificate
Futuristic / tech-forward design — landscape
"""

import os, tempfile, shutil
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Spacer
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.expanduser("~/Desktop")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "DCperf_2024_Best_Paper_Award_Certificate.pdf")

# Colors — dark futuristic palette
BG_DEEP = colors.HexColor("#070b17")
BG_CARD = colors.HexColor("#0f1525")
CYAN = colors.HexColor("#22d3ee")
BLUE = colors.HexColor("#3b82f6")
PURPLE = colors.HexColor("#8b5cf6")
TEAL = colors.HexColor("#14b8a6")
TEXT_PRIMARY = colors.HexColor("#e2e8f0")
TEXT_SECONDARY = colors.HexColor("#94a3b8")
TEXT_MUTED = colors.HexColor("#64748b")
WHITE = colors.white
DARK = colors.HexColor("#0a0f1e")

CHANCERY = "/System/Library/Fonts/Supplemental/Apple Chancery.ttf"


def draw_certificate(c, doc):
    w, h = landscape(A4)  # 841.89 x 595.28

    # === BACKGROUND ===
    c.setFillColor(BG_DEEP)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # === SUBTLE GRID PATTERN ===
    c.setStrokeColor(colors.HexColor("#0f1a30"))
    c.setLineWidth(0.3)
    for x in range(0, int(w), 40):
        c.line(x, 0, x, h)
    for y in range(0, int(h), 40):
        c.line(0, y, w, y)

    # === BORDER ===
    margin = 10 * mm
    ox, oy = margin, margin
    pw = w - 2 * margin
    ph = h - 2 * margin

    # Outer border — gradient-like with cyan
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.8)
    c.rect(ox, oy, pw, ph, stroke=1, fill=0)

    # Inner border — subtle
    c.setStrokeColor(colors.HexColor("#1a2d50"))
    c.setLineWidth(0.4)
    c.rect(ox + 4, oy + 4, pw - 8, ph - 8, stroke=1, fill=0)

    # === GLOW LINE TOP ===
    glow_y = oy + ph - 24*mm
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.5)
    c.line(ox + 15*mm, glow_y, ox + pw - 15*mm, glow_y)
    # Glow dot center
    c.setFillColor(CYAN)
    c.circle(w/2, glow_y, 2.5, stroke=0, fill=1)

    # === TOP SECTION ===
    # Badge
    badge_w, badge_h = 28*mm, 7*mm
    c.setFillColor(CYAN)
    c.roundRect(w/2 - badge_w/2, glow_y + 7*mm, badge_w, badge_h, 3.5, stroke=0, fill=1)
    c.setFillColor(BG_DEEP)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(w/2, glow_y + 8.5*mm, "DCperf 2024  •  BEST PAPER AWARD")

    # === CERTIFICATE TITLE ===
    title_y = glow_y - 8*mm
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w/2, title_y, "BEST PAPER AWARD")

    # === BODY ===
    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_SECONDARY)
    c.drawCentredString(w/2, title_y - 12*mm, "This certificate is presented to")

    # Name
    name_y = title_y - 24*mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w/2, name_y, "Yinan Qian")

    # Name underline
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.4)
    c.line(w/2 - 40*mm, name_y - 3*mm, w/2 + 40*mm, name_y - 3*mm)

    # Affiliation
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(w/2, name_y - 9*mm, "Pinterest, Inc.  |  Tufts University, United States")

    # "in recognition"
    c.setFillColor(TEXT_SECONDARY)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(w/2, name_y - 16*mm, "in recognition of the outstanding paper entitled")

    # Paper title
    paper_y = name_y - 24*mm
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-BoldOblique", 10)
    c.drawCentredString(w/2, paper_y, "Adaptive Edge-to-Cloud Traffic Steering for")
    c.drawCentredString(w/2, paper_y - 4*mm, "Latency-Critical Applications in Next-Generation CDN Architectures")

    # Award line
    award_y = paper_y - 10*mm
    c.setFillColor(TEXT_SECONDARY)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(w/2, award_y, "selected as the recipient of the DCperf 2024 Best Paper Award")
    c.setFont("Helvetica", 8)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(w/2, award_y - 4*mm, "by the Technical Program Committee — Workshop on Data Center Performance for Future Network Architectures")

    # === GLOW LINE BOTTOM ===
    bot_line_y = award_y - 10*mm
    c.setStrokeColor(PURPLE)
    c.setLineWidth(0.4)
    c.line(ox + 15*mm, bot_line_y, ox + pw - 15*mm, bot_line_y)
    c.setFillColor(PURPLE)
    c.circle(w/2, bot_line_y, 2, stroke=0, fill=1)

    # === SIGNATURES with Apple Chancery ===
    sig_y = bot_line_y - 18*mm
    sig_w = 50*mm

    def draw_sig(name, cx, sy, font_size=20):
        img = Image.new('RGBA', (300, 55), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(CHANCERY, font_size)
        bbox = draw.textbbox((0, 0), name, font=font)
        tw = bbox[2] - bbox[0]
        tx = (300 - tw) / 2
        draw.text((tx, 6), name, fill=(34, 211, 238, 220), font=font)
        draw.line([(30, 44), (270, 44)], fill=(34, 211, 238, 120), width=1)
        sig_path = tempfile.mktemp(suffix=".png")
        img.save(sig_path, 'PNG')
        c.drawImage(sig_path, cx - sig_w/2, sy - 16*mm, width=sig_w, height=16*mm, preserveAspectRatio=True, mask='auto')
        os.remove(sig_path)

    left_x = w/2 - sig_w - 18*mm + sig_w/2
    center_x = w/2
    right_x = w/2 + sig_w + 18*mm - sig_w/2

    draw_sig("Liting Hu", left_x, sig_y, 20)
    draw_sig("Xin Wang", center_x, sig_y, 22)
    draw_sig("Xingbo Wu", right_x, sig_y, 20)

    # Labels
    label_y = sig_y - 20*mm
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(left_x, label_y, "Prof. Liting Hu")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(left_x, label_y - 3.5*mm, "Workshop Chair")
    c.drawCentredString(left_x, label_y - 7*mm, "Florida International Univ.")

    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(center_x, label_y, "Dr. Xin Wang")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(center_x, label_y - 3.5*mm, "TPC Chair")
    c.drawCentredString(center_x, label_y - 7*mm, "Stony Brook University")

    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(right_x, label_y, "Prof. Xingbo Wu")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(right_x, label_y - 3.5*mm, "Workshop Co-Chair")
    c.drawCentredString(right_x, label_y - 7*mm, "Univ. of Illinois Chicago")

    # Date
    date_y = label_y - 12*mm
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(w/2, date_y, "Date Conferred  |  23 July 2024")

    # Footer
    footer_y = oy + 8*mm
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Oblique", 6)
    c.drawCentredString(w/2, footer_y, "DCperf 2024 Best Paper Award  |  dcperf.networkofthefuture.org")
    c.drawCentredString(w/2, footer_y - 3*mm, "Workshop on Data Center Performance for Future Network Architectures  |  Held in conjunction with IEEE ICDCS 2024")


def generate_certificate():
    temp_cert = tempfile.mktemp(suffix=".pdf")
    class CertDoc(BaseDocTemplate):
        def __init__(self, *a, **kw):
            BaseDocTemplate.__init__(self, *a, **kw)
            lw, lh = landscape(A4)
            self.t_cert = PageTemplate(id='cert', frames=Frame(0, 0, lw, lh, id='c'), onPage=draw_certificate)
            self.addPageTemplates([self.t_cert])
    doc = CertDoc(temp_cert, pagesize=landscape(A4))
    doc.build([Spacer(0.1*mm, 0.1*mm)])
    return temp_cert


def main():
    print("Generating DCperf 2024 Best Paper Award Certificate...")
    cert_pdf = generate_certificate()
    shutil.copy2(cert_pdf, OUTPUT_PDF)
    os.remove(cert_pdf)
    print(f"Certificate saved to: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
