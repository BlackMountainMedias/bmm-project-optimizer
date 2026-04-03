#!/usr/bin/env python3
"""Generate BMM Pitch Deck V4 -- 12 slides, plain, high-converting.

Raskin narrative + Hormozi offer stack + Sequoia 'Why Now'.
Built for cold outreach to VP Ops at $50-300M ICI contractors.
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Pitch_Deck_V4.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

# Clean dark palette
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

# Landscape letter
PW = 279.4
PH = 215.9
MX = 30
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
        self.rect(0, 0, PW, 2.5, "F")

    def slide_num(self, n):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DIM)
        self.text(PW - 15, PH - 8, str(n))

    def new_slide(self, n):
        self.add_page()
        self.dark_bg()
        self.accent_bar()
        self.slide_num(n)

    def big_text(self, y, text, size=36, color=None):
        self.set_font("Helvetica", "B", size)
        self.set_text_color(*(color or WHITE))
        self.set_xy(MX, y)
        self.multi_cell(CW, size * 0.45, text, align="L")
        return self.get_y()

    def sub_text(self, y, text, size=16, color=None):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*(color or SUB))
        self.set_xy(MX, y)
        self.multi_cell(CW, size * 0.5, text, align="L")
        return self.get_y()

    def body_text(self, x, y, w, text, size=14, color=None):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*(color or BODY))
        self.set_xy(x, y)
        self.multi_cell(w, size * 0.5, text, align="L")
        return self.get_y()

    def card(self, x, y, w, h):
        self.set_fill_color(*SURFACE)
        self.rect(x, y, w, h, "F")

    def accent_line(self, x, y, w):
        self.set_fill_color(*ACCENT)
        self.rect(x, y, w, 2, "F")

    def stat_block(self, x, y, number, label, color=None):
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*(color or ACCENT))
        self.set_xy(x, y)
        self.cell(0, 12, number, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.set_xy(x, y + 14)
        self.multi_cell(70, 5, label)

    # ==================================================================
    # SLIDE 1: THE HOOK
    # ==================================================================
    def slide_01_hook(self):
        self.new_slide(1)

        cy = 55
        cy = self.big_text(cy,
            "ICI contractors lose 5-12%\n"
            "of every project's value\n"
            "to problems they can't see\n"
            "until it's too late.")
        cy += 12
        self.sub_text(cy,
            "On a $10,000,000 project, that's $500,000 to $1,200,000 gone.",
            size=16, color=ACCENT)

    # ==================================================================
    # SLIDE 2: THE COST OF DOING NOTHING
    # ==================================================================
    def slide_02_cost(self):
        self.new_slide(2)

        self.big_text(30, "The Real Cost of\nthe Status Quo", size=30)
        self.accent_line(MX, 58, 60)

        cy = 70
        items = [
            ("$500,000+", "lost per project to invisible cost drift"),
            ("3-6 weeks", "to catch a budget overrun manually"),
            ("68%", "of change orders mask true cost overruns"),
            ("Zero", "early warning before a project bleeds out"),
        ]
        for i, (num, desc) in enumerate(items):
            x = MX + (i % 2) * 110
            y = cy + (i // 2) * 45
            self.card(x, y, 100, 36)
            self.set_font("Helvetica", "B", 22)
            self.set_text_color(*ACCENT)
            self.text(x + 8, y + 14, num)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.set_xy(x + 8, y + 19)
            self.multi_cell(84, 5, desc)

    # ==================================================================
    # SLIDE 3: WHY IT HAPPENS (THE ENEMY)
    # ==================================================================
    def slide_03_enemy(self):
        self.new_slide(3)

        self.big_text(30, "Why It Happens", size=30)
        self.accent_line(MX, 58, 60)

        enemies = [
            ("Spreadsheets Don't Flag Risk",
             "They store numbers. By the time someone spots\n"
             "a variance, the damage is done."),
            ("Data Lives in Silos",
             "Budgets in one place, timecards in another,\n"
             "schedules in a third. Nobody has the full picture."),
            ("Change Orders Hide the Truth",
             "A project looks 15% over budget when it's\n"
             "actually on track after approved scope changes."),
        ]

        cy = 70
        for title, desc in enemies:
            self.card(MX, cy, CW, 32)
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*WHITE)
            self.text(MX + 10, cy + 11, title)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.set_xy(MX + 10, cy + 16)
            self.multi_cell(CW - 20, 5, desc)
            cy += 38

    # ==================================================================
    # SLIDE 4: WHY NOW
    # ==================================================================
    def slide_04_why_now(self):
        self.new_slide(4)

        self.big_text(30, "Why Now", size=30)
        self.accent_line(MX, 58, 60)

        cy = 70
        cy = self.body_text(MX, cy, CW,
            "AI can now detect project risk patterns across your entire "
            "portfolio -- in real time. Construction is the last major "
            "industry to get this capability.", size=16, color=BODY)
        cy += 12
        cy = self.body_text(MX, cy, CW,
            "The contractors who adopt project intelligence first will "
            "win more bids, protect more margin, and outmaneuver competitors "
            "who are still running on spreadsheets and gut feel.",
            size=16, color=WHITE)
        cy += 12
        self.body_text(MX, cy, CW,
            "This is not a 5-year trend. This is happening now.",
            size=16, color=ACCENT)

    # ==================================================================
    # SLIDE 5: THE PROMISED LAND
    # ==================================================================
    def slide_05_promised_land(self):
        self.new_slide(5)

        cy = 45
        cy = self.big_text(cy,
            "Imagine seeing every\n"
            "cost overrun, schedule slip,\n"
            "and crew inefficiency\n"
            "across all your projects --", size=28)
        cy += 6
        self.big_text(cy, "before they cost you a dollar.", size=28, color=ACCENT)

    # ==================================================================
    # SLIDE 6: HOW IT WORKS
    # ==================================================================
    def slide_06_how(self):
        self.new_slide(6)

        self.big_text(25, "How It Works", size=30)
        self.accent_line(MX, 50, 60)
        self.sub_text(55, "Three steps. No software to install. No IT project.", size=13)

        steps = [
            ("1", "Upload Your Data",
             "Drop in your budgets, actuals,\n"
             "schedules, timecards, change\n"
             "orders. CSV or Excel. Takes\n"
             "5 minutes."),
            ("2", "AI Analyzes Everything",
             "Health scores, outlier detection,\n"
             "schedule risk, labor anomalies,\n"
             "material delays -- computed\n"
             "instantly across every project."),
            ("3", "See What's Leaking",
             "Dashboard shows exactly where\n"
             "money is at risk, which projects\n"
             "need attention, and what to\n"
             "fix first. Ask the AI anything."),
        ]

        x = MX
        for num, title, desc in steps:
            self.card(x, 75, 68, 95)
            # Number circle
            self.set_fill_color(*ACCENT)
            self.ellipse(x + 8, 82, 14, 14, "F")
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(*WHITE)
            self.text(x + 12, 92, num)
            # Title
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(*WHITE)
            self.text(x + 8, 104, title)
            # Desc
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*SUB)
            self.set_xy(x + 8, 109)
            self.multi_cell(52, 5, desc)
            x += 76

    # ==================================================================
    # SLIDE 7: PROOF
    # ==================================================================
    def slide_07_proof(self):
        self.new_slide(7)

        self.big_text(25, "The Numbers Don't Lie", size=30)
        self.accent_line(MX, 50, 60)

        # Hero stat
        self.set_font("Helvetica", "B", 64)
        self.set_text_color(*ACCENT)
        self.text(MX, 90, "3.2%")
        self.set_font("Helvetica", "", 18)
        self.set_text_color(*WHITE)
        self.text(MX + 90, 82, "average cost recovery identified")
        self.set_text_color(*SUB)
        self.text(MX + 90, 90, "across 500 simulated ICI projects")

        # Supporting stats
        self.stat_block(MX, 115, "19:1", "average ROI\nfor optimized projects", TEAL)
        self.stat_block(MX + 80, 115, "87%", "of projects had\nhidden cost overruns", RED)
        self.stat_block(MX + 160, 115, "8", "risk patterns detected\nper project on average", BLUE)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DIM)
        self.text(MX, 170, "Based on Monte Carlo simulation of 500 ICI projects with realistic variance distributions.")

    # ==================================================================
    # SLIDE 8: VALUE STACK (HORMOZI)
    # ==================================================================
    def slide_08_value_stack(self):
        self.new_slide(8)

        self.big_text(25, "What You Get", size=30)
        self.accent_line(MX, 50, 60)

        items = [
            ("Portfolio Dashboard", "Real-time health scores, RAG status, and risk ranking across every project."),
            ("Budget Intelligence", "Phase-by-phase variance analysis. Change orders separated from true overruns."),
            ("Schedule Risk Detection", "Flags slipping tasks and late milestones before they cascade into cost."),
            ("Labor & Material Analytics", "Overtime anomalies, crew breakdowns, delivery risk, idle crew exposure."),
            ("Statistical Outlier Engine", "IQR, Z-score, and peer comparison catch what humans miss."),
            ("AI Assistant", "Ask anything about your projects in plain English. Instant, data-grounded answers."),
        ]

        cy = 58
        for i, (title, desc) in enumerate(items):
            x = MX + (i % 2) * 110
            y = cy + (i // 2) * 34
            # Bullet accent
            self.set_fill_color(*ACCENT)
            self.rect(x, y + 1, 3, 3, "F")
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*WHITE)
            self.text(x + 8, y + 4, title)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*SUB)
            self.set_xy(x + 8, y + 8)
            self.multi_cell(98, 4.5, desc)

    # ==================================================================
    # SLIDE 9: THE GUARANTEE
    # ==================================================================
    def slide_09_guarantee(self):
        self.new_slide(9)

        cy = 40
        cy = self.big_text(cy, "The Guarantee", size=30)
        self.accent_line(MX, cy + 4, 60)
        cy += 16

        # Big guarantee card
        self.card(MX, cy, CW, 60)
        self.set_fill_color(*GREEN)
        self.rect(MX, cy, 4, 60, "F")

        self.set_font("Helvetica", "B", 26)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 16, cy + 10)
        self.cell(CW - 32, 10,
                  "2% cost improvement on your first project,",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(MX + 16, cy + 24)
        self.set_text_color(*ACCENT)
        self.cell(CW - 32, 10,
                  "or you pay nothing. Full refund.",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.set_xy(MX + 16, cy + 40)
        self.multi_cell(CW - 32, 5,
            "We analyze your data within 60 days. If we can't find at least 2% "
            "in cost improvement opportunities, you get every dollar back. "
            "No questions. No risk.")

    # ==================================================================
    # SLIDE 10: PRICING
    # ==================================================================
    def slide_10_pricing(self):
        self.new_slide(10)

        self.big_text(20, "Start Small. Prove It. Scale.", size=26)
        self.accent_line(MX, 42, 60)

        tiers = [
            ("PILOT", "$5,000", "1 project", "60 days",
             ["Full dashboard", "Budget + schedule analysis",
              "Outlier detection", "Email support",
              "2% guarantee"]),
            ("GROWTH", "$30,000", "3 projects", "6 months",
             ["Everything in Pilot", "AI Assistant",
              "Labor + material analytics", "Phone + email support",
              "2% guarantee"]),
            ("ENTERPRISE", "$125,000", "Unlimited", "12 months",
             ["Everything in Growth", "Unlimited projects",
              "Priority support", "Custom onboarding",
              "2% guarantee", "Split payment option"]),
        ]

        card_w = 68
        gap = (CW - card_w * 3) / 2
        x = MX

        for i, (name, price, projects, term, features) in enumerate(tiers):
            cy_top = 52
            h = 145

            # Highlight enterprise
            if i == 2:
                self.set_fill_color(*ACCENT)
                self.rect(x - 1, cy_top - 1, card_w + 2, h + 2, "F")

            self.card(x, cy_top, card_w, h)

            # Tier name
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*ACCENT if i < 2 else WHITE)
            self.text(x + 8, cy_top + 12, name)

            # Price
            self.set_font("Helvetica", "B", 24)
            self.set_text_color(*WHITE)
            self.text(x + 8, cy_top + 28, price)

            # Scope
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*SUB)
            self.text(x + 8, cy_top + 36, f"{projects}  |  {term}")

            # Divider
            self.set_draw_color(*DIM)
            self.set_line_width(0.2)
            self.line(x + 8, cy_top + 42, x + card_w - 8, cy_top + 42)

            # Features
            fy = cy_top + 50
            for feat in features:
                self.set_font("Helvetica", "", 9)
                self.set_text_color(*TEAL)
                self.text(x + 8, fy, ">")
                self.set_text_color(*BODY)
                self.text(x + 14, fy, feat)
                fy += 10

            x += card_w + gap

        # Arrow annotation
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT)
        self.text(MX + 10, PH - 18, "Start here -->")

    # ==================================================================
    # SLIDE 11: CREDIBILITY
    # ==================================================================
    def slide_11_credibility(self):
        self.new_slide(11)

        self.big_text(30, "Built By Someone\nWho's Been on Your\nSide of the Table", size=28)
        self.accent_line(MX, 74, 60)

        cy = 85
        points = [
            "Construction industry background -- not a tech company guessing at your problems.",
            "Built specifically for ICI contractors running $50,000,000 to $300,000,000 in annual volume.",
            "Every feature exists because a real project manager needed it, not because an engineer thought it was cool.",
            "18-month non-compete in every contract -- we're committed to your competitive advantage.",
            "Full legal package ready: NDA, license agreement, SLA, DPA, privacy policy, security documentation.",
        ]

        for point in points:
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*ACCENT)
            self.text(MX, cy + 1, ">")
            self.set_text_color(*BODY)
            self.set_font("Helvetica", "", 12)
            self.set_xy(MX + 8, cy - 2)
            self.multi_cell(CW - 8, 6, point)
            cy = self.get_y() + 4

    # ==================================================================
    # SLIDE 12: THE CLOSE
    # ==================================================================
    def slide_12_close(self):
        self.new_slide(12)

        cy = 50
        cy = self.big_text(cy,
            "I have 3 pilot slots\n"
            "open this quarter.", size=32)
        cy += 10
        cy = self.big_text(cy,
            "Want to see what the\n"
            "optimizer finds in your data?",
            size=32, color=ACCENT)

        cy += 16
        self.sub_text(cy,
            "$5,000  |  1 project  |  60 days  |  2% guarantee or full refund",
            size=14, color=SUB)
        cy += 14
        self.sub_text(cy,
            "michael@blackmountaintechnologies.ca",
            size=13, color=TEAL)

    # ==================================================================
    # BUILD
    # ==================================================================
    def build(self):
        self.slide_01_hook()
        self.slide_02_cost()
        self.slide_03_enemy()
        self.slide_04_why_now()
        self.slide_05_promised_land()
        self.slide_06_how()
        self.slide_07_proof()
        self.slide_08_value_stack()
        self.slide_09_guarantee()
        self.slide_10_pricing()
        self.slide_11_credibility()
        self.slide_12_close()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = Deck()
    doc.build()
    doc.output(OUT)
    print(f"Pitch Deck V4 saved to {OUT}")


if __name__ == "__main__":
    main()
