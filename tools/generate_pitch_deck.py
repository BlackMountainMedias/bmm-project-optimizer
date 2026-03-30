#!/usr/bin/env python3
"""Generate BMM Project Optimizer pitch deck PDF -- 3-page cold outreach deck.

Design: Hook -> Proof -> Ask. Modeled on Stripe/Brex enterprise deck patterns.
White background, navy text, single orange accent. Max 3 blocks per page.
Clean enough to print, forward to a CFO, or project in a boardroom.
"""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Project_Optimizer_Pitch_Deck.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

# Palette
BG = (255, 255, 255)
NAVY = (27, 42, 74)             # headlines, primary text — 100% weight
BODY = (65, 75, 95)             # body copy — ~75-85% visual weight
SUB = (110, 118, 135)           # support lines — ~60-70%
DIM = (175, 180, 192)           # footer, divider labels — ~45-55%
ACCENT = (212, 101, 44)         # orange — hero numbers + CTA
TEAL = (26, 122, 109)           # positive/solution
CARD_BG = (246, 247, 250)
RULE = (225, 227, 232)
DANGER = (190, 50, 40)

# Layout — landscape letter
PW = 279.4
PH = 215.9
MX = 28
CW = PW - MX * 2


class Deck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="letter")
        self.set_auto_page_break(auto=False)

    def bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")

    def rule(self, x, y, w):
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(x, y, x + w, y)

    def card(self, x, y, w, h):
        self.set_fill_color(*CARD_BG)
        self.rect(x, y, w, h, "F")

    def nav_bar(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, PW, 3, "F")

    def logo(self, x, y, h=18):
        if os.path.exists(LOGO):
            self.image(LOGO, x, y, h=h)

    def footer(self):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DIM)
        self.text(MX, PH - 7, "Confidential  |  2026")
        self.text(PW - MX - 4, PH - 7, str(self.page_no()))

    # =================================================================
    # PAGE 1 — THE HOOK
    # Logo/title top, one pain headline, one hero number, positioning.
    # Hero = $400,000. Everything else supports it.
    # =================================================================
    def page_hook(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Logo + title — top-left, clear but not dominant
        self.logo(MX, 6, h=28)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*NAVY)
        self.text(MX + 32, 20, "Project Optimizer")

        # Pain headline — second biggest element
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 44)
        self.multi_cell(CW * 0.65, 14,
                        "Your projects are\nleaking margin.")

        # Consequence — body weight
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*BODY)
        self.text(MX, 84, "And you find out weeks too late to fix it.")

        # Hero number — THE dominant element on this slide
        self.set_font("Helvetica", "B", 60)
        self.set_text_color(*ACCENT)
        self.text(MX, 122, "$400,000")

        # Proof line — tightly grouped under the number
        self.set_font("Helvetica", "", 15)
        self.set_text_color(*BODY)
        self.text(MX, 134,
                  "lost on a single $4,000,000 project at 10% overrun.")

        # Amplification — grouped with proof, slightly lighter
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.text(MX, 148,
                  "Built for ICI contractors running 5-15 active projects.")
        self.text(MX, 160, "The exposure is millions.")

        # Positioning — bottom, breathing room above
        self.rule(MX, PH - 38, CW)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*NAVY)
        self.set_xy(MX, PH - 32)
        self.cell(CW, 8,
                  "We surface margin problems while they're still cheap to fix.")

        self.footer()

    # =================================================================
    # PAGE 2 — THE PROOF
    # Two-column: WITHOUT (left) vs WITH (right), same vertical level.
    # Hero = the cost contrast. Pillars as summary strip at bottom.
    # =================================================================
    def page_proof(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Section title
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*NAVY)
        self.text(MX, 20, "What This Looks Like in Practice")

        # Two-column layout
        col_w = (CW - 16) / 2  # 16px gutter
        col_h = 120
        left_x = MX
        right_x = MX + col_w + 16
        top_y = 30

        # ---- LEFT COLUMN: WITHOUT ----
        self.card(left_x, top_y, col_w, col_h)
        self.set_fill_color(*DANGER)
        self.rect(left_x, top_y, col_w, 4, "F")  # top stripe

        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*DANGER)
        self.text(left_x + 14, top_y + 18, "Without Project Optimizer")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*BODY)
        self.set_xy(left_x + 14, top_y + 24)
        self.multi_cell(col_w - 28, 7,
                        "Steel deliveries slip 2 days.\n"
                        "Nobody notices until week 8.\n"
                        "Zero schedule float remains.")

        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*DANGER)
        self.text(left_x + 14, top_y + 72, "$60,000")
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*SUB)
        self.text(left_x + 14, top_y + 80, "idle crew cost")

        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*DANGER)
        self.text(left_x + 14, top_y + 102, "$15,000/day")
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*SUB)
        self.text(left_x + 14, top_y + 110, "in liquidated damages")

        # ---- RIGHT COLUMN: WITH ----
        self.card(right_x, top_y, col_w, col_h)
        self.set_fill_color(*TEAL)
        self.rect(right_x, top_y, col_w, 4, "F")  # top stripe

        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*TEAL)
        self.text(right_x + 14, top_y + 18, "With Project Optimizer")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*BODY)
        self.set_xy(right_x + 14, top_y + 24)
        self.multi_cell(col_w - 28, 7,
                        "Alert fires on day 3:\n"
                        "steel trending late.\n"
                        "Two options presented:")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*TEAL)
        self.text(right_x + 14, top_y + 62, "Option A:")
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*NAVY)
        self.text(right_x + 52, top_y + 62, "Pre-order steel now")
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*TEAL)
        self.text(right_x + 14, top_y + 74, "$8,000")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*TEAL)
        self.text(right_x + 14, top_y + 92, "Option B:")
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*NAVY)
        self.text(right_x + 52, top_y + 92, "Switch supplier")
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*TEAL)
        self.text(right_x + 14, top_y + 104, "$12,000")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(right_x + 60, top_y + 104, "0.3 day avg delay")

        # Bridge line
        bridge_y = top_y + col_h + 10
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*NAVY)
        self.set_xy(MX, bridge_y)
        self.cell(CW, 8,
                  "Every alert shows the problem, the dollar impact, and what to do next.",
                  align="L")

        # Three pillars — horizontal strip at bottom
        py = bridge_y + 20
        self.rule(MX, py - 6, CW)
        pillars = [
            ("Real-time", "budget vs. actual by line item"),
            ("Predictive", "risk alerts before they hit margin"),
            ("Actionable", "dollar-denominated next steps"),
        ]
        pw_col = CW / 3
        for i, (title, desc) in enumerate(pillars):
            x = MX + i * pw_col
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*ACCENT)
            self.text(x, py, title)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.text(x, py + 7, desc)

        self.footer()

    # =================================================================
    # PAGE 3 — THE ASK
    # Pilot is the hero. Tiers support. CTA closes with whitespace.
    # =================================================================
    def page_ask(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Headline
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 16)
        self.cell(CW, 14, "See it on your data. 48 hours.", align="C")

        # Pilot — dominant block
        gy = 40
        self.card(MX, gy, CW, 52)
        self.set_fill_color(*ACCENT)
        self.rect(MX, gy, 5, 52, "F")

        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*NAVY)
        self.text(MX + 18, gy + 18, "Paid Pilot")
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*ACCENT)
        self.text(MX + 18, gy + 34, "$5,000")

        self.set_font("Helvetica", "", 15)
        self.set_text_color(*BODY)
        self.text(CW / 2 + MX - 30, gy + 18,
                  "One project. Full platform.")
        self.text(CW / 2 + MX - 30, gy + 30,
                  "Live dashboard in 48 hours.")
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*SUB)
        self.text(CW / 2 + MX - 30, gy + 44,
                  "Pilot fee credits toward your annual license.")

        # Two pricing tiers — smaller, secondary
        tw = (CW - 16) / 2
        ty = 102

        # Starter tier
        self.card(MX, ty, tw, 46)
        self.set_fill_color(*NAVY)
        self.rect(MX, ty, tw, 3, "F")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX + 14, ty + 14, "Starter")
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*ACCENT)
        self.text(MX + 14, ty + 30, "$30,000 / year")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(MX + 14, ty + 40, "Up to 3 projects  --  Alerts + Dashboard")

        # Full Platform tier
        tx2 = MX + tw + 16
        self.card(tx2, ty, tw, 46)
        self.set_fill_color(*ACCENT)
        self.rect(tx2, ty, tw, 3, "F")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(tx2 + 14, ty + 14, "Full Platform")
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*ACCENT)
        self.text(tx2 + 14, ty + 30, "$125,000 / year")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(tx2 + 14, ty + 40, "Unlimited projects  --  Out of the box")

        # Compatibility — quiet
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DIM)
        self.set_xy(MX, ty + 50)
        self.cell(CW, 8,
                  "2-year license  |  Works with Procore, Sage, P6  |  No IT required",
                  align="C")

        # CTA — isolated with whitespace
        self.set_font("Helvetica", "", 20)
        self.set_text_color(*NAVY)
        self.set_xy(MX, PH - 38)
        self.cell(CW, 10, "Ready to see what you're missing?", align="C")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, PH - 24)
        self.cell(CW, 10, "michael@blackmountainmedia.com", align="C")

        self.footer()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d = Deck()
    d.page_hook()    # 1 -- Hook: pain + hero number
    d.page_proof()   # 2 -- Proof: without vs. with
    d.page_ask()     # 3 -- Ask: pilot + tiers + CTA
    d.output(OUT)
    print(f"Done: {OUT}")


if __name__ == "__main__":
    main()
