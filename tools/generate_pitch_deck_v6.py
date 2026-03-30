#!/usr/bin/env python3
"""Generate BMM Pitch Deck V6 -- 2-page dense info pack."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Pitch_Deck_V6.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

BG = (10, 14, 39)
WHITE = (255, 255, 255)
BODY = (204, 210, 222)
SUB = (148, 163, 184)
DIM = (74, 82, 112)
ACCENT = (255, 107, 53)
TEAL = (80, 200, 180)
SURFACE = (30, 41, 59)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
BLUE = (59, 130, 246)

PW = 279.4
PH = 215.9
MX = 18
CW = PW - MX * 2


class Deck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="letter")
        self.set_auto_page_break(auto=False)

    def dark_bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")

    def accent_bar(self):
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, PW, 2, "F")

    def card(self, x, y, w, h):
        self.set_fill_color(*SURFACE)
        self.rect(x, y, w, h, "F")

    def build(self):
        # ============================================================
        # PAGE 1: THE PROBLEM + THE PRODUCT
        # ============================================================
        self.add_page()
        self.dark_bg()
        self.accent_bar()

        # --- Header ---
        if os.path.exists(LOGO):
            self.image(LOGO, MX, 6, h=10)

        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*WHITE)
        self.text(MX + 50, 14, "BMM Project Optimizer")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*SUB)
        self.text(MX + 50, 19, "Construction Project Intelligence  |  Black Mountain Media Inc.")

        self.set_fill_color(*ACCENT)
        self.rect(MX, 23, CW, 1, "F")

        # --- The Problem (left column) ---
        col_w = (CW - 6) / 2
        lx = MX
        rx = MX + col_w + 6

        cy = 28
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(lx, cy, "THE PROBLEM")

        cy += 6
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BODY)
        self.set_xy(lx, cy)
        self.multi_cell(col_w, 4.2,
            "ICI contractors lose 5-12% of every project's value to cost overruns, "
            "schedule delays, and inefficiencies they can't see until it's too late. "
            "On a $10,000,000 project, that's $500,000 to $1,200,000 gone. Across a "
            "portfolio of 10 projects, that's $5,000,000 to $12,000,000 per year.")
        cy = self.get_y() + 3

        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*RED)
        self.set_xy(lx, cy)
        self.multi_cell(col_w, 4.2,
            "Spreadsheets don't flag risk. Data lives in silos. Change orders mask "
            "true overruns. By the time someone spots the problem, the damage is done.")
        cy = self.get_y() + 4

        # --- What We Do ---
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(lx, cy, "WHAT WE DO")
        cy += 6

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BODY)
        self.set_xy(lx, cy)
        self.multi_cell(col_w, 4.2,
            "We give you a real-time health score for every project in your portfolio. "
            "Upload your data -- budgets, actuals, schedules, timecards, change orders, "
            "materials -- and our AI-powered engine instantly identifies where money is "
            "at risk, which tasks are slipping, where labor costs are abnormal, and what "
            "your change orders are really hiding.")
        cy = self.get_y() + 4

        # --- How It Works ---
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(lx, cy, "HOW IT WORKS")
        cy += 6

        steps = [
            ("1. Upload", "Drop your CSVs or Excel files. Budget, actuals, schedules, "
             "timecards, COs, materials. Takes 5 minutes. No software to install."),
            ("2. Analyze", "AI scans everything: health scores, outlier detection, schedule "
             "risk, labor anomalies, material delays, change order impact. Instant results."),
            ("3. Act", "Dashboard shows exactly what needs attention. Ask the AI assistant "
             "anything. \"Which project is bleeding?\" \"Where's our overtime problem?\""),
        ]
        for title, desc in steps:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*TEAL)
            self.text(lx, cy, title)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*SUB)
            self.set_xy(lx + 18, cy - 3)
            self.multi_cell(col_w - 18, 4, desc)
            cy = self.get_y() + 2

        # --- Right Column: Health Score + What You See ---
        cy_r = 28
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(rx, cy_r, "PROJECT HEALTH SCORE (0-100)")
        cy_r += 6

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BODY)
        self.set_xy(rx, cy_r)
        self.multi_cell(col_w, 4.2,
            "Every project gets a single score from 0 to 100 based on five weighted factors:")
        cy_r = self.get_y() + 2

        factors = [
            ("Budget Variance", "35%", "How far actual spend is from budget"),
            ("Change Order Impact", "15%", "CO cost as % of total budget"),
            ("Schedule Performance", "20%", "% of tasks on track or complete"),
            ("Data Completeness", "20%", "How many data types are loaded"),
            ("Labor Productivity", "10%", "Overtime patterns and efficiency"),
        ]
        for name, weight, desc in factors:
            self.card(rx, cy_r, col_w, 10)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*WHITE)
            self.text(rx + 3, cy_r + 4, name)
            self.set_text_color(*ACCENT)
            self.text(rx + col_w - 18, cy_r + 4, weight)
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*SUB)
            self.text(rx + 3, cy_r + 8.5, desc)
            cy_r += 12

        cy_r += 2
        # RAG
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.text(rx, cy_r, "Risk Status:")
        rag_items = [
            (GREEN, "Green (<5%)", rx + 26),
            ((245, 158, 11), "Yellow (5-10%)", rx + 60),
            (RED, "Red (>10%)", rx + 102),
        ]
        for color, label, x_pos in rag_items:
            self.set_fill_color(*color)
            self.rect(x_pos, cy_r - 3, 4, 4, "F")
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*BODY)
            self.text(x_pos + 6, cy_r, label)
        cy_r += 7

        # What dashboard shows
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(rx, cy_r, "WHAT THE DASHBOARD SHOWS")
        cy_r += 6

        pages = [
            "Portfolio Overview -- every project, one screen, health + risk ranked",
            "Project Drill-Down -- phase-by-phase and line-item budget vs actual",
            "Change Orders -- true overruns separated from approved scope changes",
            "Schedule Intelligence -- slipping tasks flagged before they cascade",
            "Labor Analytics -- hours, overtime, crew costs, anomaly detection",
            "Materials -- overdue deliveries, backorders, idle crew risk",
            "Outlier Detection -- IQR, Z-score, peer comparison engine",
            "AI Assistant -- ask anything about your data in plain English",
        ]
        for page in pages:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*TEAL)
            self.text(rx, cy_r, ">")
            self.set_text_color(*BODY)
            self.text(rx + 5, cy_r, page)
            cy_r += 5.5

        # Footer
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*DIM)
        self.text(MX, PH - 6, "Confidential  |  Black Mountain Media Inc.  |  michael@blackmountainmedias.ca")
        self.text(PW - 22, PH - 6, "Page 1 of 2")

        # ============================================================
        # PAGE 2: THE OFFER + GUARANTEE + PRICING
        # ============================================================
        self.add_page()
        self.dark_bg()
        self.accent_bar()

        # --- Header ---
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*WHITE)
        self.text(MX, 14, "The Offer")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*SUB)
        self.text(MX + 55, 14, "What you get, what it costs, and why there's zero risk.")

        self.set_fill_color(*ACCENT)
        self.rect(MX, 18, CW, 1, "F")

        # --- The Insurance Policy ---
        cy = 24
        self.card(MX, cy, CW, 36)
        self.set_fill_color(*GREEN)
        self.rect(MX, cy, 3, 36, "F")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*WHITE)
        self.text(MX + 10, cy + 10, "THE GUARANTEE: Your Insurance Policy Against Cost Overruns")

        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*ACCENT)
        self.text(MX + 10, cy + 20,
                  "We find at least 2% in cost improvement opportunities, or you pay nothing. Full refund.")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*SUB)
        self.set_xy(MX + 10, cy + 25)
        self.multi_cell(CW - 20, 4,
            "We analyze your historical project data within 60 days. If we cannot identify cost "
            "improvement opportunities equal to at least 2% of total project costs, you receive a "
            "complete refund. No questions asked. You provide the data, we prove the value -- or you walk away whole.")
        cy += 40

        # --- The Math ---
        cy += 2
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(MX, cy, "THE MATH: WHY THIS IS A NO-BRAINER")
        cy += 6

        self.card(MX, cy, CW, 28)
        scenarios = [
            ("Your Annual Volume", "$50,000,000", "$100,000,000", "$200,000,000"),
            ("At Risk (5-12%)", "$2,500,000 - $6,000,000", "$5,000,000 - $12,000,000", "$10,000,000 - $24,000,000"),
            ("Minimum 2% Recovery", "$1,000,000", "$2,000,000", "$4,000,000"),
            ("Our Fee (Enterprise)", "$125,000", "$125,000", "$125,000"),
            ("Your ROI", "8:1", "16:1", "32:1"),
        ]
        ty = cy + 2
        # Column headers
        col_positions = [MX + 4, MX + 60, MX + 105, MX + 155]
        col_widths = [52, 42, 46, 46]
        for row_i, (label, v1, v2, v3) in enumerate(scenarios):
            vals = [label, v1, v2, v3]
            for col_i, val in enumerate(vals):
                if col_i == 0:
                    self.set_font("Helvetica", "B" if row_i == 4 else "", 8)
                    self.set_text_color(*SUB)
                else:
                    self.set_font("Helvetica", "B" if row_i == 4 else "", 8)
                    if row_i == 4:
                        self.set_text_color(*GREEN)
                    elif row_i == 1:
                        self.set_text_color(*RED)
                    elif row_i == 2:
                        self.set_text_color(*TEAL)
                    else:
                        self.set_text_color(*BODY)
                self.text(col_positions[col_i], ty + 4, val)
            ty += 5
        cy += 32

        # --- Pricing Tiers ---
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(MX, cy, "PRICING: START SMALL, PROVE IT, SCALE")
        cy += 5

        tiers = [
            ("PILOT", "$5,000", [
                "1 project  |  60 days",
                "Full dashboard + analytics",
                "Outlier detection + health score",
                "Email support",
                "2% guarantee or full refund",
            ]),
            ("GROWTH", "$30,000", [
                "Up to 3 projects  |  6 months",
                "Everything in Pilot",
                "AI Assistant included",
                "Labor + material analytics",
                "Phone + email support",
                "2% guarantee or full refund",
            ]),
            ("ENTERPRISE", "$125,000", [
                "Unlimited projects  |  12 months",
                "Everything in Growth",
                "Priority support + custom onboarding",
                "Split payment: $62,500 now, $62,500 at 6 months",
                "2% guarantee or full refund",
                "18-month non-compete -- we protect your edge",
            ]),
        ]

        tier_w = (CW - 8) / 3
        tx = MX
        for i, (name, price, features) in enumerate(tiers):
            if i == 2:
                self.set_fill_color(*ACCENT)
                self.rect(tx - 1, cy, tier_w + 2, 68, "F")
            self.card(tx, cy + 1, tier_w, 66)

            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*ACCENT if i < 2 else WHITE)
            self.text(tx + 4, cy + 8, name)

            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*WHITE)
            self.text(tx + 4, cy + 18, price)

            self.set_draw_color(*DIM)
            self.set_line_width(0.2)
            self.line(tx + 4, cy + 22, tx + tier_w - 4, cy + 22)

            fy = cy + 27
            for feat in features:
                self.set_font("Helvetica", "", 7.5)
                self.set_text_color(*TEAL)
                self.text(tx + 4, fy, ">")
                self.set_text_color(*BODY)
                self.text(tx + 9, fy, feat)
                fy += 5.5

            tx += tier_w + 4

        cy += 72

        # --- The Process ---
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(MX, cy, "THE PROCESS: HOW WE GET STARTED")
        cy += 5

        process = [
            ("Day 1:", "Sign NDA. Send us one project's budget vs actuals. We start immediately."),
            ("Day 2-3:", "We load your data and run the full analysis. Health scores, outliers, risk flags -- everything."),
            ("Day 4:", "Live walkthrough of your results. You see your own numbers on screen. We show you exactly where money is at risk."),
            ("Day 5:", "You decide. Sign the license agreement. We onboard the rest of your portfolio."),
            ("Day 6-60:", "Full platform access. Your team uses the dashboard daily. AI assistant answers questions instantly."),
            ("Day 60:", "Guarantee check. If we found 2%+ -- you're already saving. If not -- full refund, no questions."),
        ]

        lx2 = MX
        rx2 = MX + CW / 2 + 2
        for i, (day, desc) in enumerate(process):
            x = lx2 if i < 3 else rx2
            y = cy + (i % 3) * 8
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*TEAL)
            self.text(x, y + 3, day)
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*SUB)
            self.set_xy(x + 16, y)
            self.multi_cell(CW / 2 - 20, 3.8, desc)

        # --- Bottom bar ---
        self.set_fill_color(*SURFACE)
        self.rect(0, PH - 14, PW, 14, "F")
        self.set_fill_color(*ACCENT)
        self.rect(0, PH - 14, PW, 1, "F")

        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.text(MX, PH - 7,
                  "Ready to see where your money is going?")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEAL)
        self.text(MX + 95, PH - 7,
                  "michael@blackmountainmedias.ca")
        self.set_text_color(*SUB)
        self.text(MX + 160, PH - 7,
                  "3 pilot slots open this quarter  |  2% guarantee or full refund")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = Deck()
    doc.build()
    doc.output(OUT)
    print(f"Pitch Deck V6 saved to {OUT}")


if __name__ == "__main__":
    main()
