#!/usr/bin/env python3
"""Generate BMM Project Optimizer -- Value Analysis & AI Feature Brief.

Internal strategy document covering:
  Section 1: AI Assistant feature analysis (value, risks, sales angle)
  Section 2: Full product value analysis (stress test, positioning, competition)
"""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Value_Analysis.pdf")
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets",
                    "logo.png")

# V4 Dark Professional palette
BG = (10, 14, 39)
WHITE = (255, 255, 255)
BODY = (204, 210, 222)
SUB = (148, 163, 184)
DIM = (74, 82, 112)
ACCENT = (255, 107, 53)
TEAL = (80, 200, 180)
SURFACE = (30, 41, 59)
RULE = (50, 60, 85)
DANGER = (255, 90, 70)
BLUE = (59, 130, 246)

# Portrait letter
PW = 215.9
PH = 279.4
MX = 24
CW = PW - MX * 2


class Doc(FPDF):
    def __init__(self):
        super().__init__(orientation="P", format="letter")
        self.set_auto_page_break(auto=False)

    def dark_bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")

    def nav_bar(self):
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, PW, 3, "F")

    def card(self, x, y, w, h):
        self.set_fill_color(*SURFACE)
        self.rect(x, y, w, h, "F")

    def rule(self, x, y, w):
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(x, y, x + w, y)

    def footer_bar(self, label=""):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DIM)
        self.text(MX, PH - 10, "Confidential  |  BMM  |  2026")
        if label:
            self.text(PW / 2 - 15, PH - 10, label)
        self.text(PW - MX - 4, PH - 10, str(self.page_no()))

    def section_title(self, y, text):
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*WHITE)
        self.text(MX, y, text)

    def sub_heading(self, y, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*ACCENT)
        self.text(MX, y, text)

    def body_text(self, x, y, w, text, size=11, color=None):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*(color or BODY))
        self.set_xy(x, y)
        self.multi_cell(w, size * 0.5, text)

    def bullet(self, x, y, w, text, size=11, color=None):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*(color or BODY))
        self.set_xy(x, y)
        self.multi_cell(w, size * 0.5, text)

    # ==================================================================
    # COVER PAGE
    # ==================================================================
    def page_cover(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        if os.path.exists(LOGO):
            self.image(LOGO, MX, 20, h=16)

        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 70)
        self.multi_cell(CW, 13, "Value Analysis &\nAI Feature Brief")

        self.rule(MX, 102, CW * 0.4)

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.text(MX, 115, "BMM Project Optimizer")
        self.text(MX, 125, "Internal Strategy Document  |  March 2026")

        # Contents
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*ACCENT)
        self.text(MX, 160, "CONTENTS")

        items = [
            ("01", "AI Assistant -- How It Works"),
            ("02", "AI Assistant -- Value Analysis"),
            ("03", "AI Assistant -- Risks & Honest Assessment"),
            ("04", "AI Assistant -- Sales Angle"),
            ("05", "Full Product -- What It Actually Is"),
            ("06", "Full Product -- Where The Value Lives"),
            ("07", "Full Product -- When It's NOT Valuable"),
            ("08", "Full Product -- Competition & Moat"),
            ("09", "Full Product -- Is It Bullshit?"),
            ("10", "Full Product -- Best Sales Angle"),
        ]
        y = 172
        for num, title in items:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*ACCENT)
            self.text(MX, y, num)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*BODY)
            self.text(MX + 12, y, title)
            y += 7

        self.footer_bar()

    # ==================================================================
    # AI ASSISTANT -- HOW IT WORKS
    # ==================================================================
    def page_ai_how(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "AI Assistant")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "How It Works")

        self.rule(MX, 35, CW)

        # Card
        self.card(MX, 42, CW, 48)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*WHITE)
        self.text(MX + 8, 52, "The Mechanism")
        self.body_text(MX + 8, 57, CW - 16,
                       "The bot sits on top of all data flowing through the dashboard -- "
                       "budgets, actuals, change orders, timecards, schedules, materials. "
                       "When someone asks a question, it serializes that data into context, "
                       "sends it to Claude (Anthropic's AI) with the question, and gets back "
                       "a natural-language answer.\n\n"
                       "It's not magic. It's a structured data lookup with an English interface.")

        # The comparison
        self.sub_heading(105, "Without the bot")
        steps = [
            "1.  Open the dashboard",
            "2.  Click into Project Detail",
            "3.  Look at the variance chart",
            "4.  Cross-reference with change orders",
            "5.  Check if it's labor-driven (flip to Labor)",
            "6.  Check if materials spiked (flip to Materials)",
            "7.  Synthesize all of that in your head",
        ]
        y = 113
        for step in steps:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*SUB)
            self.text(MX + 8, y, step)
            y += 6

        self.sub_heading(162, "With the bot")
        self.card(MX, 168, CW, 36)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEAL)
        self.text(MX + 8, 176, '"Why is Riverside over budget?"')
        self.body_text(MX + 8, 182, CW - 16,
                       '"Riverside is $142K over budget (+8.3%). $89K is from approved change orders '
                       '(scope additions in Phase 2). The remaining $53K true overrun is driven by '
                       'overtime -- the electrical crew logged 34% OT vs the 12% budget assumption."',
                       size=10)

        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*ACCENT)
        self.text(MX, 225, "30 seconds vs 10 minutes")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.text(MX, 233, "And it connects dots across data sources most people wouldn't cross-reference.")

        self.footer_bar("AI ASSISTANT")

    # ==================================================================
    # AI ASSISTANT -- VALUE ANALYSIS
    # ==================================================================
    def page_ai_value(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "AI Assistant")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "When It's Most Valuable")

        self.rule(MX, 35, CW)

        scenarios = [
            ("Monday Morning Leadership Meetings",
             '"Give me a summary of where we stand across all projects" '
             'instead of someone spending an hour prepping a report.'),
            ("Field-to-Office Questions",
             'A superintendent texts "are we still on budget for concrete at Building C?" '
             'and someone can just ask the bot.'),
            ("When Things Go Wrong",
             '"Which projects have the highest overtime right now?" '
             'is an urgent question during crunch periods.'),
            ("Onboarding New PMs",
             "A new PM can interrogate the data without knowing where to look "
             "in the system. The learning curve disappears."),
            ("Web-Enhanced Intelligence",
             "Industry benchmarks, material price trends, regulation lookups -- "
             "makes it feel like having a construction-savvy analyst on call."),
        ]

        y = 45
        for title, desc in scenarios:
            self.card(MX, y, CW, 30)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*WHITE)
            self.text(MX + 8, y + 10, title)
            self.body_text(MX + 8, y + 14, CW - 16, desc, size=10, color=SUB)
            y += 36

        # The test
        self.rule(MX, y + 5, CW)
        y += 15
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.set_xy(MX, y)
        self.multi_cell(CW, 6, "The Test: If you gave it to a VP of Ops for 3 months\nand took it away, would they care?")

        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*TEAL)
        self.text(MX, y + 18, "Yes.")

        self.body_text(MX, y + 24, CW,
                       "Because going back to manual cross-referencing feels like "
                       "going from GPS back to paper maps.",
                       size=11)

        self.footer_bar("AI ASSISTANT")

    # ==================================================================
    # AI ASSISTANT -- RISKS
    # ==================================================================
    def page_ai_risks(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "AI Assistant")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Risks & Honest Assessment")

        self.rule(MX, 35, CW)

        risks = [
            ("API Key Exposure", DANGER,
             "If the Anthropic key leaks (client-side, git, logs), anyone can run up "
             "your bill or access the API. Mitigation: key stays server-side only."),
            ("Data Exfiltration via Prompts", DANGER,
             "A user could ask 'show me all employee wages' and the bot complies. "
             "For V1 pilot this is fine -- the user already has data access."),
            ("Prompt Injection from Web", (245, 158, 11),
             "If the bot parses web content, a malicious site could embed instructions. "
             "Mitigation: sanitize web results before feeding to the LLM."),
            ("Cost Spiral", (245, 158, 11),
             "If every question triggers web search + LLM call, costs add up. "
             "Mitigation: rate limiting and token caps."),
        ]

        y = 45
        for title, color, desc in risks:
            self.card(MX, y, CW, 28)
            # Color bar on left
            self.set_fill_color(*color)
            self.rect(MX, y, 3, 28, "F")
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*WHITE)
            self.text(MX + 10, y + 10, title)
            self.body_text(MX + 10, y + 14, CW - 18, desc, size=9, color=SUB)
            y += 34

        # What's NOT a risk
        y += 5
        self.sub_heading(y, "What's NOT a risk for V1 pilot:")
        y += 10
        safe_items = [
            "The bot can't modify data -- it's read-only",
            "It's behind your app's login (authenticated users only)",
            "For a pilot with 1-2 clients, the attack surface is tiny",
        ]
        for item in safe_items:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*TEAL)
            self.text(MX + 8, y, item)
            y += 7

        # Bottom line
        y += 10
        self.rule(MX, y, CW)
        y += 10
        self.card(MX, y, CW, 22)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*WHITE)
        self.text(MX + 8, y + 9, "Bottom line:")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BODY)
        self.text(MX + 55, y + 9, "Safe enough for V1. Key server-side, sanitize web results, set token limits.")

        # Could someone build this?
        y += 35
        self.sub_heading(y, "Could someone build the bot alone?")
        y += 8
        self.body_text(MX, y, CW,
                       "Yes. Any developer could wire ChatGPT to a spreadsheet in a weekend.\n\n"
                       "The bot + the data pipeline + the dashboard + the domain context? No.\n"
                       "The value isn't the chat interface -- it's that the data is already structured, "
                       "validated, enriched, and contextualized for construction.",
                       size=10)

        self.footer_bar("AI ASSISTANT")

    # ==================================================================
    # AI ASSISTANT -- SALES ANGLE
    # ==================================================================
    def page_ai_sales(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "AI Assistant")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Best Sales Angle")

        self.rule(MX, 35, CW)

        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 48, "Don't sell the bot. Sell the outcome:")

        # Quote card
        self.card(MX, 55, CW, 40)
        self.set_fill_color(*ACCENT)
        self.rect(MX, 55, 3, 40, "F")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 12, 60)
        self.multi_cell(CW - 24, 6,
                        '"Your data already tells you which projects are bleeding money, '
                        'which crews are burning overtime, and where your schedule is slipping.\n\n'
                        'Right now that takes 3 people and a Monday morning meeting to figure out. '
                        'With this, anyone on your team can just ask."')

        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(MX, 112, "The angle:")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*BODY)
        self.set_xy(MX, 118)
        self.multi_cell(CW, 6,
                        "Time-to-insight for the people who don't live in spreadsheets.\n"
                        "The VP who wants answers. The owner who wants a pulse check.\n"
                        "The PM who's juggling 8 things at once.")

        # Dashboard = engine, bot = steering wheel
        self.rule(MX, 148, CW)
        self.card(MX, 158, CW, 30)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT)
        self.text(MX + 8, 168, "The dashboard is the engine. The bot is the steering wheel.")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SUB)
        self.text(MX + 8, 176, "Nobody buys a steering wheel. But nobody wants an engine without one either.")

        # It's the hook
        y = 200
        self.sub_heading(y, "Why it matters for adoption:")
        self.body_text(MX, y + 8, CW,
                       "The AI assistant is the hook that makes people actually open the app "
                       "instead of ignoring it like every other dashboard they've been sold. "
                       "It turns a reporting tool into a tool people use.",
                       size=11)

        self.footer_bar("AI ASSISTANT")

    # ==================================================================
    # FULL PRODUCT -- WHAT IT IS
    # ==================================================================
    def page_product_what(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "What It Actually Is")

        self.rule(MX, 35, CW)

        self.body_text(MX, 42, CW,
                       "A construction project cost monitoring tool that takes budget vs actual data, "
                       "change orders, timecards, schedules, and materials -- and shows variance, "
                       "outliers, health scores, data quality, and an AI assistant.",
                       size=12, color=BODY)

        # The core question
        y = 72
        self.card(MX, y, CW, 30)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 8, y + 6)
        self.multi_cell(CW - 16, 6,
                        "The test: If a VP of Ops at a $150M ICI contractor used this for "
                        "6 months and you took it away, would they care?")

        y += 40
        self.body_text(MX, y, CW,
                       "That depends on what they were doing before. And for 90% of them "
                       "the answer is: Excel. Shared drives. Monthly cost reports that are "
                       "2 weeks stale by the time they're reviewed. A PM who says 'we're "
                       "on track' until suddenly they're $400K over.",
                       size=11)

        y += 32
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*TEAL)
        self.text(MX, y, "Yes, they'd care.")

        self.body_text(MX, y + 8, CW,
                       "Going back feels like going from GPS to paper maps. Not because the "
                       "map doesn't work, but because you have to actively look at it, interpret it, "
                       "and you only check it when you're already lost.",
                       size=11)

        # Core value
        y += 42
        self.rule(MX, y, CW)
        y += 10
        self.sub_heading(y, "The core value isn't any single feature.")

        y += 10
        self.card(MX, y, CW, 24)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*ACCENT)
        self.set_xy(MX + 8, y + 5)
        self.multi_cell(CW - 16, 6,
                        "It compresses the time between 'money was spent wrong' and "
                        "'someone knows about it' from weeks to minutes.")

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # FULL PRODUCT -- WHERE THE VALUE LIVES
    # ==================================================================
    def page_product_value(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Where The Value Lives")

        self.rule(MX, 35, CW)

        features = [
            ("Portfolio View", BLUE,
             "One screen tells the owner/VP which projects are healthy and which "
             "aren't. Without this, that answer lives in 8 different PM's heads."),
            ("Outlier Detection", ACCENT,
             "Flags line items that are statistically abnormal. A human would never catch "
             "a $12K framing overrun buried in a $4M project. The tool does."),
            ("CO-Adjusted Variance", TEAL,
             'Separates "we approved this scope change" from "this is a real overrun." '
             "Without this, every over-budget project looks the same and PMs hide behind "
             "change orders."),
            ("Health + Data Quality Scoring", (245, 158, 11),
             "Tells you not just what the numbers say, but whether you can trust them. "
             "A project that looks green but has no timecards loaded is a blind spot, "
             "not a success."),
            ("AI Assistant", WHITE,
             "Makes all of this accessible to people who won't click through 7 dashboard tabs. "
             "The last mile that turns data infrastructure into daily usage."),
        ]

        y = 45
        for title, color, desc in features:
            self.card(MX, y, CW, 34)
            self.set_fill_color(*color)
            self.rect(MX, y, 3, 34, "F")
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*WHITE)
            self.text(MX + 10, y + 10, title)
            self.body_text(MX + 10, y + 15, CW - 20, desc, size=10, color=SUB)
            y += 40

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # FULL PRODUCT -- WHEN IT'S NOT VALUABLE
    # ==================================================================
    def page_product_not_valuable(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "When It's NOT Valuable")

        self.rule(MX, 35, CW)

        items = [
            ("Companies under $20M revenue",
             "They have 1-3 projects, the owner knows everything, "
             "they don't need a dashboard."),
            ("Companies that don't track actuals",
             "If they're not recording what they spend at the line-item level, "
             "there's nothing to analyze."),
            ("Companies with a strong controls team",
             "A $500M+ ENR-ranked GC with 3 cost engineers and a BI team "
             "already has this. You're not replacing enterprise infrastructure."),
            ("If the data isn't kept current",
             "A dashboard with last month's numbers is a decoration. "
             "The tool is only as good as the upload cadence."),
        ]

        y = 45
        for title, desc in items:
            self.card(MX, y, CW, 30)
            self.set_fill_color(*DANGER)
            self.rect(MX, y, 3, 30, "F")
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*WHITE)
            self.text(MX + 10, y + 10, title)
            self.body_text(MX + 10, y + 15, CW - 20, desc, size=10, color=SUB)
            y += 36

        # Sweet spot reminder
        y += 10
        self.rule(MX, y, CW)
        y += 12
        self.sub_heading(y, "The sweet spot:")

        y += 10
        self.card(MX, y, CW, 22)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*TEAL)
        self.set_xy(MX + 8, y + 8)
        self.cell(CW - 16, 6,
                  "Mid-tier ICI  |  $50-300M revenue  |  5-15 active projects")

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # FULL PRODUCT -- COMPETITION & MOAT
    # ==================================================================
    def page_product_competition(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Competition & Moat")

        self.rule(MX, 35, CW)

        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(MX, 48, "Could someone build this themselves?")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*ACCENT)
        self.text(MX, 58, "Could they? Yes.  Would they? No.  Have they? No.")

        # Three reasons
        reasons = [
            ("Their tech team is zero people",
             "They have Procore, maybe Sage or Vista, and Excel. Nobody on staff "
             "is writing Python. Nobody is building dashboards."),
            ("The big players don't do this well",
             "Procore and Autodesk are document management and field coordination. "
             "Their cost reporting is basic -- budget, actual, a number. No outlier "
             "detection, no health scoring, no cross-source analysis."),
            ("Consulting firms charge $200K+",
             "And deliver a static Power BI dashboard that nobody updates "
             "after the consultant leaves."),
        ]

        y = 70
        for i, (title, desc) in enumerate(reasons):
            self.card(MX, y, CW, 32)
            self.set_font("Helvetica", "B", 28)
            self.set_text_color(*ACCENT)
            self.text(MX + 8, y + 16, str(i + 1))
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*WHITE)
            self.text(MX + 22, y + 10, title)
            self.body_text(MX + 22, y + 15, CW - 30, desc, size=10, color=SUB)
            y += 38

        # Market position
        y += 5
        self.rule(MX, y, CW)
        y += 12
        self.card(MX, y, CW, 26)
        self.set_fill_color(*ACCENT)
        self.rect(MX, y, 3, 26, "F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 10, y + 5)
        self.multi_cell(CW - 20, 6,
                        "Your gap: too sophisticated for Excel, too niche for Procore, "
                        "too cheap for a consultant. That's a real market position.")

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # FULL PRODUCT -- IS IT BULLSHIT?
    # ==================================================================
    def page_product_bs_test(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Is It Bullshit?")

        self.rule(MX, 35, CW)

        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*TEAL)
        self.text(MX, 52, "No.")

        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(MX, 65, "But it CAN become bullshit if:")

        bs_items = [
            "You sell it as AI-powered when the core value is just organized math",
            "You claim it prevents overruns (it doesn't -- it detects them earlier)",
            "You pitch it to companies without the data discipline to feed it",
            "You pretend demo data proves it works on real-world messy data",
        ]

        y = 75
        for item in bs_items:
            self.card(MX, y, CW, 14)
            self.set_fill_color(*DANGER)
            self.rect(MX, y, 3, 14, "F")
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*BODY)
            self.text(MX + 10, y + 9, item)
            y += 18

        # The honest version
        y += 8
        self.sub_heading(y, "The honest version is strong enough:")

        y += 10
        self.card(MX, y, CW, 36)
        self.set_fill_color(*ACCENT)
        self.rect(MX, y, 3, 36, "F")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 10, y + 6)
        self.multi_cell(CW - 20, 6,
                        '"You already have the data. It\'s in Sage, Procore, your PM\'s '
                        "spreadsheets. This tool pulls it together, scores it, flags the "
                        "problems, and lets anyone on your team ask questions about it.\n\n"
                        "You'll catch a $50K overrun in week 2 instead of month 3.\"")

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # FULL PRODUCT -- BEST SALES ANGLE
    # ==================================================================
    def page_product_sales(self):
        self.add_page()
        self.dark_bg()
        self.nav_bar()

        self.section_title(22, "Full Product")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*SUB)
        self.text(MX, 30, "Best Sales Angle")

        self.rule(MX, 35, CW)

        self.set_font("Helvetica", "", 12)
        self.set_text_color(*BODY)
        self.text(MX, 48, "Don't sell the software. Sell the cost of not knowing.")

        # The question
        y = 60
        self.card(MX, y, CW, 30)
        self.set_fill_color(*ACCENT)
        self.rect(MX, y, 3, 30, "F")
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*WHITE)
        self.set_xy(MX + 10, y + 6)
        self.multi_cell(CW - 20, 6,
                        '"On your last project that went over budget -- when did you find out? '
                        'If you\'d found out 6 weeks earlier, what would you have done differently?"')

        y = 100
        self.body_text(MX, y, CW,
                       "Every GC has that story. The concrete sub who was 40% over before "
                       "anyone noticed. The change order that never got approved but the work "
                       "happened anyway. The overtime that crept up because nobody was watching.",
                       size=11)

        y = 130
        self.rule(MX, y, CW)
        y += 12

        self.card(MX, y, CW, 26)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*ACCENT)
        self.set_xy(MX + 8, y + 5)
        self.multi_cell(CW - 16, 6,
                        "Your tool doesn't prevent mistakes. "
                        "It makes them visible before they compound.")

        y += 38
        self.sub_heading(y, "The ROI math:")

        y += 10
        self.body_text(MX, y, CW,
                       "Catching one $50K overrun on a $5K/month subscription pays for itself. "
                       "At 5-15 active projects, the odds of catching at least one are basically 100%.",
                       size=12, color=WHITE)

        y += 22
        self.rule(MX, y, CW)
        y += 12
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*WHITE)
        self.text(MX, y, "The risk isn't that it's bullshit.")

        y += 10
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, y)
        self.multi_cell(CW, 6,
                        "The risk is adoption -- getting the data in, keeping it current, "
                        "and making it sticky enough that they can't go back to Excel.")

        y += 18
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.set_xy(MX, y)
        self.multi_cell(CW, 6,
                        "That's what the AI assistant helps with. It's the hook that makes "
                        "people actually open the app instead of ignoring it.")

        self.footer_bar("FULL PRODUCT")

    # ==================================================================
    # BUILD
    # ==================================================================
    def build(self):
        self.page_cover()
        self.page_ai_how()
        self.page_ai_value()
        self.page_ai_risks()
        self.page_ai_sales()
        self.page_product_what()
        self.page_product_value()
        self.page_product_not_valuable()
        self.page_product_competition()
        self.page_product_bs_test()
        self.page_product_sales()

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        self.output(OUT)
        print(f"Saved → {OUT}")


if __name__ == "__main__":
    Doc().build()
