#!/usr/bin/env python3
"""Generate BMM Construction Margin Intelligence pitch deck V2 -- 3-page cold outreach deck.

V2 fixes: product definition is now as strong as the pain definition.
Buyer understands what they're buying, how it works, and why it's worth the price.
"""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Margin_Intelligence_Deck_V2.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

# 4-tier palette
BG = (255, 255, 255)
NAVY = (27, 42, 74)
BODY = (65, 75, 95)
SUB = (110, 118, 135)
DIM = (175, 180, 192)
ACCENT = (212, 101, 44)
TEAL = (26, 122, 109)
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

    def footer_bar(self):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DIM)
        self.text(MX, PH - 7, "Confidential  |  2026")
        self.text(PW - MX - 4, PH - 7, str(self.page_no()))

    # =================================================================
    # PAGE 1 — THE HOOK
    # Title that defines the product category.
    # One-line value promise. One proof number. Mechanism line.
    # Buyer should know WHAT this is, WHO it's for, and HOW it works.
    # =================================================================
    def page_hook(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Logo + product name — top-left
        self.logo(MX, 6, h=28)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*NAVY)
        self.text(MX + 32, 18, "Black Mountain Technologies")

        # Product category — THE title of the deck
        self.set_font("Helvetica", "B", 38)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 40)
        self.cell(CW, 14, "Construction Margin Intelligence")

        # Value promise — one line, plain English
        self.set_font("Helvetica", "", 18)
        self.set_text_color(*BODY)
        self.set_xy(MX, 58)
        self.cell(CW, 10,
                  "Catch overruns, delays, and productivity losses before they hit profit.")

        # Hero number — dominant visual element
        self.set_font("Helvetica", "B", 60)
        self.set_text_color(*ACCENT)
        self.text(MX, 105, "$400,000")

        # Proof context — tight under the number
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*BODY)
        self.text(MX, 117,
                  "destroyed by a 10% overrun on a single $4,000,000 project.")

        # Mechanism — THIS is what the buyer was missing in V1
        self.rule(MX, 130, CW)
        self.set_font("Helvetica", "", 15)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 135)
        self.multi_cell(CW * 0.75, 7,
                        "We connect to your project data, flag margin risk early,\n"
                        "and show the cost impact and next-best action\n"
                        "before the job gets away from you.")

        # Fit line
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.text(MX, 168,
                  "Built for ICI contractors running 5-15 active projects.")
        self.text(MX, 180,
                  "The exposure across your portfolio is millions.")

        self.footer_bar()

    # =================================================================
    # PAGE 2 — THE PROOF
    # Three real scenarios (not just one) proving the system works
    # across labor, materials, and schedule. Each shows:
    # what happened → what the system caught → what it saved.
    # =================================================================
    def page_proof(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Section title
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*NAVY)
        self.text(MX, 22, "Three Problems. Caught Early.")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.text(MX, 32,
                  "Every alert shows the problem, the dollar impact, and what to do next.")

        # Three scenario cards — horizontal layout
        card_w = (CW - 20) / 3  # 10px between each
        card_h = 115
        card_y = 40
        gap = 10

        scenarios = [
            {
                "color": DANGER,
                "icon_color": DANGER,
                "tag": "Materials",
                "title": "Steel delivery slipping",
                "without": "Noticed at week 8.\nZero float left.\nIdle crew: $60,000.\nLD exposure: $15,000/day.",
                "with_title": "Alert fires day 3",
                "with_text": "Pre-order steel now",
                "cost": "$8,000",
                "saved": "$67,000 saved",
            },
            {
                "color": DANGER,
                "icon_color": DANGER,
                "tag": "Labor",
                "title": "Crew productivity dropping",
                "without": "PM notices at month-end.\nOvertime already approved.\nBudget blown by $45,000.",
                "with_title": "Alert fires week 2",
                "with_text": "Reassign or add crew",
                "cost": "$6,000",
                "saved": "$39,000 saved",
            },
            {
                "color": DANGER,
                "icon_color": DANGER,
                "tag": "Schedule",
                "title": "Concrete pour delayed",
                "without": "Weather + supplier.\nFound out day-of.\nReschedule cost: $28,000.",
                "with_title": "Alert fires 5 days out",
                "with_text": "Shift pour or swap supplier",
                "cost": "$4,000",
                "saved": "$24,000 saved",
            },
        ]

        for i, s in enumerate(scenarios):
            x = MX + i * (card_w + gap)

            # Card background
            self.card(x, card_y, card_w, card_h)

            # Category tag
            self.set_fill_color(*s["color"])
            self.rect(x, card_y, card_w, 3.5, "F")
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*s["color"])
            self.text(x + 8, card_y + 13, s["tag"])

            # Problem title
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*NAVY)
            self.text(x + 8, card_y + 23, s["title"])

            # Without — what happens if you miss it
            self.set_font("Helvetica", "", 9.5)
            self.set_text_color(*SUB)
            self.set_xy(x + 8, card_y + 27)
            self.multi_cell(card_w - 16, 5.5, s["without"])

            # Divider
            self.set_draw_color(*RULE)
            self.set_line_width(0.3)
            div_y = card_y + 66
            self.line(x + 8, div_y, x + card_w - 8, div_y)

            # With — what the system does
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*TEAL)
            self.text(x + 8, div_y + 10, s["with_title"])

            self.set_font("Helvetica", "", 11)
            self.set_text_color(*BODY)
            self.text(x + 8, div_y + 20, s["with_text"])

            # Cost to fix
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*TEAL)
            self.text(x + 8, div_y + 35, s["cost"])

            # Savings
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*TEAL)
            self.text(x + 8, div_y + 45, s["saved"])

        # How it works strip — bottom, well clear of cards
        strip_y = 172
        self.rule(MX, strip_y - 6, CW)

        steps = [
            ("1. Connect", "Your existing data -- Procore, Sage, P6, spreadsheets"),
            ("2. Detect", "AI flags cost, schedule, and labor risks automatically"),
            ("3. Act", "Dollar-denominated alerts with recommended next steps"),
        ]
        col_w = CW / 3
        for i, (title, desc) in enumerate(steps):
            x = MX + i * col_w
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*ACCENT)
            self.text(x, strip_y, title)
            self.set_font("Helvetica", "", 10.5)
            self.set_text_color(*SUB)
            self.text(x, strip_y + 8, desc)

        self.footer_bar()

    # =================================================================
    # PAGE 3 — THE ASK
    # Clear path: pilot → starter → full platform.
    # Pilot is the obvious next step. Make it feel low-risk and fast.
    # =================================================================
    def page_ask(self):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Headline — reframe as "see it working on YOUR data"
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 14)
        self.cell(CW, 14, "See it on your data. Live in 48 hours.", align="C")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.set_xy(MX, 30)
        self.cell(CW, 8,
                  "Pick one project. We build the dashboard. You decide if it's worth scaling.",
                  align="C")

        # Pilot — dominant block, THE thing to buy
        gy = 48
        self.card(MX, gy, CW, 56)
        self.set_fill_color(*ACCENT)
        self.rect(MX, gy, 5, 56, "F")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*SUB)
        self.text(MX + 18, gy + 14, "Start Here")

        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*NAVY)
        self.text(MX + 18, gy + 30, "Paid Pilot")

        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*ACCENT)
        self.text(MX + 18, gy + 46, "$5,000")

        # Pilot details — right side of the card
        rx = CW / 2 + MX - 20
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*BODY)
        self.text(rx, gy + 16, "One project. Full platform. Live dashboard.")
        self.text(rx, gy + 28, "48-hour setup. No IT lift.")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*TEAL)
        self.text(rx, gy + 42,
                  "Pilot fee credits 100% toward your annual license.")

        # Two pricing tiers — smaller, secondary
        tw = (CW - 16) / 2
        ty = 114

        # Starter tier
        self.card(MX, ty, tw, 46)
        self.set_fill_color(*NAVY)
        self.rect(MX, ty, tw, 3, "F")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(MX + 14, ty + 14, "Starter")
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*ACCENT)
        self.text(MX + 14, ty + 28, "$30,000 / year")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(MX + 14, ty + 38, "Up to 3 projects  --  Alerts + Dashboard")

        # Full Platform tier
        tx2 = MX + tw + 16
        self.card(tx2, ty, tw, 46)
        self.set_fill_color(*ACCENT)
        self.rect(tx2, ty, tw, 3, "F")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(tx2 + 14, ty + 14, "Full Platform")
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*ACCENT)
        self.text(tx2 + 14, ty + 28, "$125,000 / year")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(tx2 + 14, ty + 38,
                  "Unlimited projects  --  Full risk engine")

        # Compatibility — quiet
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DIM)
        self.set_xy(MX, ty + 50)
        self.cell(CW, 8,
                  "Works with Procore, Sage, P6, or spreadsheets  |  No IT required  |  2-year license",
                  align="C")

        # CTA — isolated with whitespace
        self.set_font("Helvetica", "", 18)
        self.set_text_color(*NAVY)
        self.set_xy(MX, PH - 36)
        self.cell(CW, 10, "Ready to see what you're missing?", align="C")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, PH - 22)
        self.cell(CW, 10, "michael@blackmountainmedia.com", align="C")

        self.footer_bar()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d = Deck()
    d.page_hook()    # 1 -- Hook: category + pain + mechanism
    d.page_proof()   # 2 -- Proof: three scenarios + how it works
    d.page_ask()     # 3 -- Ask: pilot + tiers + CTA
    d.output(OUT)
    print(f"Done: {OUT}")


if __name__ == "__main__":
    main()
