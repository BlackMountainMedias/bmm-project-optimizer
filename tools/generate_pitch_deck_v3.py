#!/usr/bin/env python3
"""Generate BMM Construction Margin Intelligence pitch deck V3.

V3: Dark Professional theme (Option A) from the 32-page design spec.
Deep navy background, white text, construction orange accent on money/CTAs only.
Modeled after Zuora/Drift/Segment enterprise sales decks.
"""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Margin_Intelligence_Deck_V3.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

# Option A -- Dark Professional palette
BG = (10, 14, 39)                  # #0A0E27 deep navy
WHITE = (255, 255, 255)            # primary text
GRAY = (148, 163, 184)             # #94A3B8 cool gray -- secondary text
ACCENT = (255, 107, 53)            # #FF6B35 construction orange -- money, CTAs
SURFACE = (30, 41, 59)             # #1E293B slate -- card backgrounds
FOOTER_GRAY = (148, 163, 184)      # footer at 50% opacity (simulated)

# Layout -- landscape letter
PW = 279.4
PH = 215.9
MX = 28
CW = PW - MX * 2


class Deck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="letter")
        self.set_auto_page_break(auto=False)

    def dark_bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")

    def surface_card(self, x, y, w, h):
        self.set_fill_color(*SURFACE)
        self.rect(x, y, w, h, "F")

    def accent_left_border(self, x, y, h, width=4):
        self.set_fill_color(*ACCENT)
        self.rect(x, y, width, h, "F")

    def footer(self):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(74, 82, 112)
        self.text(MX, PH - 10, "Black Mountain Technologies  |  Confidential  |  2026")

    # =================================================================
    # SLIDE 1 -- PROBLEM RECOGNITION
    # =================================================================
    def slide_problem(self):
        self.add_page()
        self.dark_bg()

        # 1. Company + product name -- top, subtle
        self.set_font("Helvetica", "", 12)
        self.set_text_color(178, 188, 204)
        self.text(MX, 20, "Black Mountain Technologies  --  Construction Margin Intelligence")

        # 2. Primary headline
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 34)
        self.cell(CW, 14, "You're losing $400,000 per project.")

        # 3. Secondary headline
        self.set_font("Helvetica", "", 20)
        self.set_text_color(204, 210, 222)
        self.set_xy(MX, 52)
        self.cell(CW, 10, "And you find out weeks too late to fix it.")

        # 4. Proof block -- surface card with hero number
        proof_y = 74
        proof_h = 48
        self.surface_card(MX, proof_y, CW * 0.55, proof_h)

        # Hero number
        self.set_font("Helvetica", "B", 54)
        self.set_text_color(*ACCENT)
        self.text(MX + 14, proof_y + 26, "$400,000")

        # Context line
        self.set_font("Helvetica", "", 15)
        self.set_text_color(*WHITE)
        self.text(MX + 14, proof_y + 37, "lost on a single $4M project")

        # Supporting stat
        self.set_font("Helvetica", "", 13)
        self.set_text_color(178, 188, 204)
        self.text(MX + 14, proof_y + 46, "10% overrun destroys your margin")

        # 5. Amplification
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 134)
        self.multi_cell(CW * 0.75, 7,
                        "Most contractors run 5-15 active projects.\n"
                        "Your exposure is millions.")

        # 6. Solution line -- accent left border
        sol_y = 160
        self.accent_left_border(MX, sol_y, 12)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*WHITE)
        self.text(MX + 10, sol_y + 9,
                  "We catch cost overruns, schedule slippage, and productivity losses before they hit profit.")

        self.footer()

    # =================================================================
    # SLIDE 2 -- BEFORE / AFTER (TWO-COLUMN)
    # =================================================================
    def slide_before_after(self):
        self.add_page()
        self.dark_bg()

        # Title
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 16)
        self.cell(CW, 12, "What This Looks Like on Your Jobs")

        # Two columns
        col_w = (CW - 16) / 2
        left_x = MX
        right_x = MX + col_w + 16
        col_y = 38

        # -- LEFT COLUMN: WITHOUT --
        self.surface_card(left_x, col_y, col_w, 110)

        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*ACCENT)
        self.text(left_x + 12, col_y + 12, "WITHOUT MARGIN INTELLIGENCE")

        # Scenario description
        self.set_font("Helvetica", "", 13)
        self.set_text_color(230, 233, 240)
        self.set_xy(left_x + 12, col_y + 18)
        self.multi_cell(col_w - 24, 6,
                        "Steel deliveries slip 2 days.\n"
                        "Nobody notices until week 8.\n"
                        "By then, zero schedule float remains.")

        # Cost figures
        self.set_font("Helvetica", "B", 38)
        self.set_text_color(*ACCENT)
        self.text(left_x + 12, col_y + 60, "$60,000")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*WHITE)
        self.text(left_x + 12, col_y + 69, "idle crew cost")

        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*ACCENT)
        self.text(left_x + 12, col_y + 84, "$15,000/day")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*WHITE)
        self.text(left_x + 12, col_y + 93, "in liquidated damages")

        self.set_font("Helvetica", "", 15)
        self.set_text_color(204, 210, 222)
        self.text(left_x + 12, col_y + 105, "= $75,000+ unrecoverable loss")

        # -- RIGHT COLUMN: WITH --
        self.surface_card(right_x, col_y, col_w, 110)

        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*ACCENT)
        self.text(right_x + 12, col_y + 12, "WITH MARGIN INTELLIGENCE")

        # Alert fires early
        self.set_font("Helvetica", "", 13)
        self.set_text_color(230, 233, 240)
        self.set_xy(right_x + 12, col_y + 20)
        self.multi_cell(col_w - 24, 6,
                        "Alert fires on Day 3:\n"
                        "Steel delivery trending 2 days late.")

        # Response options
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(right_x + 12, col_y + 48, "Option A:")
        self.set_font("Helvetica", "", 13)
        self.text(right_x + 50, col_y + 48, "Pre-order replacement steel")

        self.set_font("Helvetica", "", 12)
        self.set_text_color(*GRAY)
        self.text(right_x + 50, col_y + 56, "$8,000 cost, 0 delay")

        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(right_x + 12, col_y + 68, "Option B:")
        self.set_font("Helvetica", "", 13)
        self.text(right_x + 50, col_y + 68, "Switch to local supplier")

        self.set_font("Helvetica", "", 12)
        self.set_text_color(*GRAY)
        self.text(right_x + 50, col_y + 76, "$12,000 cost, 0.3 day delay")

        # Resolved line
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*ACCENT)
        self.text(right_x + 12, col_y + 98,
                  "Problem solved for $8,000-$12,000")

        # -- BOTTOM: 3-col feature grid --
        grid_y = 158
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*WHITE)
        self.text(MX, grid_y, "Every alert includes:")

        features = [
            ("Real-Time Tracking", "Budget vs. actual\nby line item"),
            ("Predictive Alerts", "Risk flags before\nmargin impact"),
            ("Actionable Decisions", "Dollar-costed options\nwith tradeoffs"),
        ]
        feat_w = CW / 3
        feat_y = grid_y + 9
        for i, (title, desc) in enumerate(features):
            fx = MX + i * feat_w
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(*ACCENT)
            self.text(fx, feat_y, title)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(204, 210, 222)
            self.set_xy(fx, feat_y + 3)
            self.multi_cell(feat_w - 10, 5, desc)

        self.footer()

    # =================================================================
    # SLIDE 3 -- PRICING & CTA
    # =================================================================
    def slide_pricing(self):
        self.add_page()
        self.dark_bg()

        # Headline
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 16)
        self.cell(CW, 12, "See it on your data. 48 hours.", align="C")

        # Pilot card -- dominant, surface bg, accent left border
        pilot_y = 42
        pilot_h = 54
        self.surface_card(MX, pilot_y, CW, pilot_h)
        self.accent_left_border(MX, pilot_y, pilot_h, width=5)

        # "PAID PILOT" label
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(MX + 16, pilot_y + 12, "PAID PILOT")

        # $5,000 hero price
        self.set_font("Helvetica", "B", 48)
        self.set_text_color(*ACCENT)
        self.text(MX + 16, pilot_y + 40, "$5,000")

        # Pilot details -- right side
        rx = CW * 0.4 + MX
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*WHITE)
        self.text(rx, pilot_y + 16, "One project. Full platform. Live dashboard in 48 hours.")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(204, 210, 222)
        self.text(rx, pilot_y + 30,
                  "Pilot fee credits 100% toward annual license.")

        # Two-column pricing tiers
        tw = (CW - 16) / 2
        ty = 108

        # Starter
        self.surface_card(MX, ty, tw, 40)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*GRAY)
        self.text(MX + 14, ty + 12, "Starter")
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.text(MX + 14, ty + 32, "$30,000/year")

        # Full Platform
        tx2 = MX + tw + 16
        self.surface_card(tx2, ty, tw, 40)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*GRAY)
        self.text(tx2 + 14, ty + 12, "Full Platform")
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.text(tx2 + 14, ty + 32, "$125,000/year")

        # Supporting line
        self.set_font("Helvetica", "", 12)
        self.set_text_color(178, 188, 204)
        self.set_xy(MX, ty + 46)
        self.cell(CW, 8,
                  "2-year license  |  Procore, Sage 300, P6  |  No IT required",
                  align="C")

        # CTA -- isolated with whitespace
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*WHITE)
        self.set_xy(MX, PH - 34)
        self.cell(CW, 10, "Ready to see what you're missing?", align="C")

        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, PH - 20)
        self.cell(CW, 10, "michael@blackmountainmedia.com", align="C")

        self.footer()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d = Deck()
    d.slide_problem()       # 1 -- Problem Recognition
    d.slide_before_after()  # 2 -- Before/After
    d.slide_pricing()       # 3 -- Pricing & CTA
    d.output(OUT)
    print(f"Done: {OUT}")


if __name__ == "__main__":
    main()
