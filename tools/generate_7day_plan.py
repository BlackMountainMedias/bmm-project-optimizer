#!/usr/bin/env python3
"""Generate BMM 7-Day Plan to $250K PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_7Day_Plan_250K.pdf")

# Palette
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

PW = 215.9
PH = 279.4
MX = 22
CW = PW - MX * 2


class Plan(FPDF):
    def __init__(self):
        super().__init__(orientation="P", format="letter")
        self.set_auto_page_break(auto=True, margin=20)
        self._is_cover = True

    def header(self):
        if self._is_cover:
            return
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, 14, "F")
        self.set_fill_color(*ACCENT)
        self.rect(0, 14, PW, 1, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 4)
        self.cell(CW, 6, "7-DAY PLAN TO $250,000  |  BMM PROJECT OPTIMIZER",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(20)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*DIM)
        self.cell(0, 5, f"Confidential  |  Black Mountain Technologies  |  Page {self.page_no()}",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def dark_page(self):
        # Called after add_page via header, need to fill bg
        pass

    def section(self, text, color=None):
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*(color or ACCENT))
        self.rect(MX, y, 3, 8, "F")
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*WHITE)
        self.set_x(MX + 7)
        self.cell(CW - 7, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def sub(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT)
        self.set_x(MX)
        self.cell(CW, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BODY)
        self.set_x(MX)
        self.multi_cell(CW, 5, text)
        self.ln(1)

    def bullet(self, text, bold_prefix=""):
        self.set_x(MX + 4)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEAL)
        self.cell(5, 5, ">")
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*WHITE)
            self.cell(self.get_string_width(bold_prefix) + 2, 5, bold_prefix)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BODY)
        self.multi_cell(CW - 14 - (self.get_string_width(bold_prefix) + 2 if bold_prefix else 0), 5, text)

    def metric_row(self, label, value, color=None):
        self.set_x(MX + 4)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SUB)
        self.cell(55, 6, label)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*(color or ACCENT))
        self.cell(40, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def card_start(self):
        self._card_y = self.get_y()
        self.set_fill_color(*SURFACE)

    def card_end(self):
        h = self.get_y() - self._card_y + 4
        # Draw card behind content (we'll just add spacing)
        self.ln(2)

    def build(self):
        # === COVER ===
        self.add_page()
        self._is_cover = True
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, PW, 3, "F")

        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 50)
        self.multi_cell(CW, 16, "7-Day Plan\nto $250,000")

        self.set_fill_color(*ACCENT)
        self.rect(MX, 98, 50, 2, "F")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, 108)
        self.multi_cell(CW, 7,
            "Skip the pilot. Find contractors in pain.\n"
            "Show them their own money leaking.\n"
            "Close on the call.")

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*SUB)
        self.set_xy(MX, 145)
        self.multi_cell(CW, 6,
            "Target: 2 Enterprise deals at $125,000 each\n"
            "Method: 48-hour data analysis, live reveal, same-week close\n"
            "Guarantee: 2% cost improvement or full refund\n"
            "Timeline: 7 days from today")

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DIM)
        self.text(MX, 185, "Black Mountain Technologies Inc.  |  March 2026  |  Confidential")

        self._is_cover = False

        # === PAGE 2: THE MATH ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("The Math")
        self.body(
            "A $200,000,000 ICI contractor spends $125,000 in about 4 hours of "
            "operating. Their material budget on a single project is $2,000,000 to "
            "$5,000,000. You are asking for less than a rounding error.")
        self.ln(2)

        self.sub("The Value Equation")
        self.metric_row("Their annual project volume:", "$50,000,000 - $300,000,000")
        self.metric_row("Money at risk (5-12%):", "$2,500,000 - $36,000,000", RED)
        self.metric_row("Your price:", "$125,000", TEAL)
        self.metric_row("As % of their risk:", "0.3% - 5%", GREEN)
        self.metric_row("Guaranteed minimum ROI:", "2% of project costs", GREEN)
        self.ln(4)

        self.sub("The Framing")
        self.body(
            "You are not selling $125,000 software. You are selling insurance against "
            "the $2,500,000 to $36,000,000 they are currently blind to. The price is "
            "irrelevant next to the problem.")
        self.ln(2)

        self.sub("Target for the Week")
        self.metric_row("Conversations needed:", "15-20")
        self.metric_row("Data analyses to run:", "4-6")
        self.metric_row("Live reveals:", "4-6")
        self.metric_row("Closes:", "2")
        self.metric_row("Revenue:", "$250,000", ACCENT)

        # === PAGE 3: THE STRATEGY ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("The Strategy: 48-Hour Reveal")
        self.body(
            "Do not sell software. Sell the reveal. The demo IS the proof. "
            "When they see their own numbers on screen showing where money leaked, "
            "the software sells itself.")
        self.ln(2)

        self.sub("Step 1: Get Their Data")
        self.body(
            "\"Send me one project's budget vs actuals. I'll show you where your "
            "money went. Free. Takes me 48 hours. If you don't like what you see, "
            "we shake hands and walk away.\"")
        self.ln(1)

        self.sub("Step 2: Run the Analysis (Same Day)")
        self.bullet("Load their data into the dashboard")
        self.bullet("Run outlier detection, variance analysis, health scoring")
        self.bullet("Identify the 2-3 biggest cost leaks")
        self.bullet("Quantify the dollar impact")
        self.bullet("Prepare a 10-minute walkthrough of THEIR numbers")
        self.ln(2)

        self.sub("Step 3: The Live Reveal")
        self.body(
            "Share screen. Walk them through their own data. Show them exactly where "
            "money leaked and how much. Do not pitch features. Just show numbers. "
            "Let the silence after each finding do the selling.")
        self.ln(1)

        self.sub("Step 4: Close on the Call")
        self.body(
            "\"You just saw what we found on one project. Imagine this across your "
            "entire portfolio. $125,000 for the year, and if we don't deliver at least "
            "2% in cost improvement, you get every dollar back. I have 3 slots left "
            "this quarter.\"")

        # === PAGE 4: DAY BY DAY ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("Day 1: Monday -- Pipeline Blitz", ACCENT)
        self.sub("Morning (6 AM - 12 PM)")
        self.bullet("Build target list: 50 VPs of Ops / Project Directors at $50-300M ICI contractors in Western Canada", "")
        self.bullet("Sources: LinkedIn Sales Nav, VRCA member directory, BCCSA, local construction news", "")
        self.bullet("Prioritize anyone who posted about cost overruns, project delays, or budget issues", "")
        self.ln(1)
        self.sub("Afternoon (12 PM - 6 PM)")
        self.bullet("Send 30 personalized LinkedIn DMs with the hook message", "")
        self.bullet("Send 20 cold emails to targets with public email addresses", "")
        self.bullet("Follow up with MacLean Sprung and Colin Duffy immediately", "")
        self.bullet("Post on LinkedIn: construction cost overrun insight with a soft CTA", "")
        self.ln(1)
        self.sub("Evening (6 PM - 10 PM)")
        self.bullet("Research every company that responded. Know their projects, size, recent news.", "")
        self.bullet("Customize the reveal pitch for each warm lead", "")
        self.ln(1)
        self.sub("The DM / Email Script")
        self.body(
            "\"Hey [name] -- quick question. Do you know exactly where your margin "
            "is leaking across your active projects right now? I built a tool that "
            "finds it in 48 hours. Send me one project's budget vs actuals and I'll "
            "show you for free. If I can't find at least 2% in savings, I'll buy you "
            "lunch. Worth 5 minutes?\"")

        # === PAGE 5: DAYS 2-3 ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("Day 2: Tuesday -- Follow Up + First Data", ACCENT)
        self.sub("Morning")
        self.bullet("Follow up on every DM and email from yesterday. Second touch converts.", "")
        self.bullet("Send 20 more fresh outreach messages to expand the net", "")
        self.bullet("Book every call you can for Wednesday and Thursday", "")
        self.ln(1)
        self.sub("Afternoon + Evening")
        self.bullet("Analyze any data that's come in. Run it through the dashboard immediately.", "")
        self.bullet("Prepare reveal presentations -- screenshot their dashboard, annotate the findings", "")
        self.bullet("Goal: have 2-3 analyses ready to present by end of day", "")
        self.ln(3)

        self.section("Day 3: Wednesday -- First Reveals", ACCENT)
        self.sub("Morning")
        self.bullet("Run live reveal calls with the first 2-3 prospects", "")
        self.bullet("10 minutes: walk through their data. 5 minutes: show the guarantee. 5 minutes: close.", "")
        self.bullet("If they need time, schedule the decision call for Friday. Do not let it drift.", "")
        self.ln(1)
        self.sub("Afternoon")
        self.bullet("Send 15 more outreach messages -- keep the pipeline full", "")
        self.bullet("Analyze any new data that arrived", "")
        self.bullet("Follow up with morning reveal prospects: \"Any questions from what I showed you?\"", "")
        self.ln(1)
        self.sub("Evening")
        self.bullet("Prep reveals for Thursday", "")
        self.bullet("Update your tracking: who's hot, who's warm, who's dead", "")

        # === PAGE 6: DAYS 4-5 ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("Day 4: Thursday -- More Reveals + Push", ACCENT)
        self.sub("All Day")
        self.bullet("Run 3-4 more live reveal calls", "")
        self.bullet("Every call ends with: \"I have 3 slots. One just filled. Want one of the last two?\"", "")
        self.bullet("For anyone who saw a reveal and hasn't decided: \"I'm holding your slot until Friday 5 PM\"", "")
        self.bullet("Continue outreach: 10 more messages minimum", "")
        self.ln(3)

        self.section("Day 5: Friday -- Close Day", RED)
        self.sub("Morning")
        self.bullet("Call every warm prospect. This is decision day.", "")
        self.bullet("\"I showed you $X in savings on one project. You have 15 projects. The math is simple.\"", "")
        self.bullet("Send the license agreement to anyone who says yes. Get it signed today.", "")
        self.ln(1)
        self.sub("Afternoon")
        self.bullet("For anyone who needs \"one more look\" -- do a second reveal with their boss on the call", "")
        self.bullet("The VP sees it, the decision maker sees it, close together", "")
        self.bullet("\"I'm sending the agreement now. Payment terms are net 30. Want the full year or the split?\"", "")
        self.ln(1)
        self.sub("Evening")
        self.bullet("Tally: how many signed, how many pending, how many need the weekend", "")
        self.bullet("Send a follow-up to every pending: \"I held your slot. Let's lock it in Monday.\"", "")

        # === PAGE 7: DAYS 6-7 ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("Day 6: Saturday -- Overflow + Prep", ACCENT)
        self.bullet("Analyze any remaining data that came in late", "")
        self.bullet("Prep reveals for Monday morning", "")
        self.bullet("Send 10 more outreach messages -- weekend LinkedIn gets higher open rates", "")
        self.bullet("Refine your pitch based on what worked this week. What objections came up? What closed?", "")
        self.ln(3)

        self.section("Day 7: Sunday -- Close the Gaps", ACCENT)
        self.bullet("Review every open deal. What does each one need to close?", "")
        self.bullet("Pre-write Monday morning follow-ups for every pending prospect", "")
        self.bullet("Schedule Monday calls for anyone who said \"let me think about it\"", "")
        self.bullet("Plan Week 2 outreach if target not hit -- who else can you reach?", "")
        self.ln(4)

        self.section("The Objection Kills")
        self.ln(1)

        objections = [
            ("\"We need to think about it\"",
             "\"Totally understand. What specifically do you need to think through? "
             "Because the 2% guarantee means there's zero risk -- you either save money "
             "or you pay nothing.\""),
            ("\"$125,000 is a lot\"",
             "\"You're running $X million in projects. I just showed you $Y leaking on "
             "one project. Across your portfolio, that's $Z at risk. $125,000 is less "
             "than half a percent of that exposure.\""),
            ("\"We already have project controls\"",
             "\"Great -- send me one project's data and I'll show you what your current "
             "system missed. Free. If I can't find anything, I'll tell you your controls "
             "are solid and you'll never hear from me again.\""),
            ("\"Can we start with a pilot?\"",
             "\"Absolutely. $5,000, one project, 60 days. But I'll tell you -- every "
             "contractor who starts with a pilot ends up going Enterprise once they see "
             "the first results. Want to save 60 days and just start?\""),
            ("\"I need to run this by my boss\"",
             "\"Let's get them on a 15-minute call. I'll show them exactly what I showed "
             "you. Same data, same findings. I can do tomorrow morning.\""),
        ]

        for q, a in objections:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*WHITE)
            self.set_x(MX)
            self.multi_cell(CW, 5, q)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*SUB)
            self.set_x(MX + 4)
            self.multi_cell(CW - 4, 5, a)
            self.ln(2)

        # === FINAL PAGE: SCOREBOARD ===
        self.add_page()
        self.set_fill_color(*BG)
        self.rect(0, 15, PW, PH - 15, "F")

        self.section("Your Scoreboard")
        self.body("Track these numbers every day. If the inputs are right, the output is inevitable.")
        self.ln(2)

        metrics = [
            ("Outreach messages sent:", "_____ / 150 target"),
            ("Responses received:", "_____ / 30 target"),
            ("Calls booked:", "_____ / 10 target"),
            ("Data sets received:", "_____ / 6 target"),
            ("Analyses completed:", "_____ / 6 target"),
            ("Live reveals delivered:", "_____ / 6 target"),
            ("Proposals sent:", "_____ / 4 target"),
            ("Deals closed:", "_____ / 2 target"),
            ("Revenue signed:", "$ _____ / $250,000 target"),
        ]

        for label, value in metrics:
            self.set_x(MX + 4)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*BODY)
            self.cell(80, 8, label)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*ACCENT)
            self.cell(80, 8, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(6)
        self.section("Remember", GREEN)
        self.ln(1)

        rules = [
            "You are not selling software. You are selling the answer to \"where did our margin go?\"",
            "The 48-hour reveal is the weapon. Their own data on screen closes the deal.",
            "Loss framing beats gain framing. \"You are losing $500,000\" not \"You could save $500,000.\"",
            "The guarantee eliminates risk. If they still say no, they don't have the problem.",
            "Scarcity is real -- you physically cannot onboard more than 3-4 clients at once.",
            "Every \"no\" gets you closer to the next \"yes.\" Volume solves everything.",
            "The price is a rounding error on their exposure. Never apologize for it.",
            "One signed deal changes everything. The second one is 10x easier.",
        ]

        for rule in rules:
            self.set_x(MX + 4)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*TEAL)
            self.cell(5, 5, ">")
            self.set_text_color(*BODY)
            self.multi_cell(CW - 9, 5, rule)
            self.ln(1)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = Plan()
    doc.build()
    doc.output(OUT)
    print(f"7-Day Plan saved to {OUT}")


if __name__ == "__main__":
    main()
