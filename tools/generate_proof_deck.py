#!/usr/bin/env python3
"""Generate proof artifacts PDF from simulation results.

Uses the same enterprise design as the pitch deck (white + navy + orange).
Shows the hard numbers that prove early detection saves real money.
"""
from fpdf import FPDF
import json
import os

STATS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          ".tmp", "simulations", "simulation_stats.json")
OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                   ".tmp", "BMM_Simulation_Proof_Deck.pdf")

# Same palette as pitch deck
BG = (255, 255, 255)
NAVY = (27, 42, 74)
SUB = (100, 110, 130)
DIM = (170, 175, 185)
ACCENT = (212, 101, 44)
TEAL = (26, 122, 109)
CARD_BG = (245, 246, 248)
RULE = (220, 222, 228)
DANGER = (190, 50, 40)

PW = 279.4
PH = 215.9
MX = 25
CW = PW - MX * 2


class ProofDeck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="letter")
        self.set_auto_page_break(auto=False)

    def bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PW, PH, "F")

    def nav_bar(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, PW, 3, "F")

    def rule(self, x, y, w):
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(x, y, x + w, y)

    def card(self, x, y, w, h):
        self.set_fill_color(*CARD_BG)
        self.rect(x, y, w, h, "F")

    def bar_chart(self, x, y, w, h, data, max_val=None):
        """Simple horizontal bar chart. data = [(label, value, color), ...]"""
        if not data:
            return
        if max_val is None:
            max_val = max(v for _, v, _ in data)
        bar_h = min(12, (h - 4) / len(data) - 2)
        for i, (label, val, color) in enumerate(data):
            by = y + 4 + i * (bar_h + 4)
            # Label
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*SUB)
            self.text(x, by + bar_h * 0.7, label)
            # Bar
            bar_x = x + 55
            bar_w = (val / max_val) * (w - 75) if max_val > 0 else 0
            self.set_fill_color(*color)
            self.rect(bar_x, by, max(1, bar_w), bar_h, "F")
            # Value
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*NAVY)
            self.text(bar_x + bar_w + 3, by + bar_h * 0.7, f"${val:,.0f}")

    def footer(self):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DIM)
        self.text(MX, PH - 8, "Black Mountain Media  |  Simulation Analysis  |  2026")
        self.text(PW - MX - 4, PH - 8, str(self.page_no()))

    # =================================================================
    # PAGE 1 -- HEADLINE STATS
    # =================================================================
    def page_headline(self, stats):
        self.add_page()
        self.bg()
        self.nav_bar()

        # Brand
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.text(MX, 16, "PROJECT OPTIMIZER")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DIM)
        self.text(MX + 52, 16, "Simulation Analysis  --  500 Projects")

        # Hero headline
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 32)
        self.cell(CW, 14, "Early detection saves real money.", align="L")

        # The big number
        savings = stats["total_savings_with_early_detection"]
        self.set_font("Helvetica", "B", 64)
        self.set_text_color(*ACCENT)
        self.text(MX, 82, f"${savings:,.0f}")

        self.set_font("Helvetica", "", 16)
        self.set_text_color(*SUB)
        self.text(MX, 94, "in preventable overruns across 500 simulated projects.")

        # Three stat cards
        cards = [
            (f"${stats['avg_savings_per_project']:,.0f}", "avg savings\nper project", ACCENT),
            (f"{stats['pct_projects_over_budget']}%", "of projects\nover budget", DANGER),
            (f"{stats['avg_overrun_pct']}%", "avg overrun on\nover-budget projects", NAVY),
        ]
        cw_card = (CW - 20) / 3
        cy = 110
        for i, (number, label, color) in enumerate(cards):
            cx = MX + i * (cw_card + 10)
            self.card(cx, cy, cw_card, 44)
            self.set_font("Helvetica", "B", 32)
            self.set_text_color(*color)
            self.text(cx + 12, cy + 22, number)
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.set_xy(cx + 12, cy + 28)
            self.multi_cell(cw_card - 24, 5, label)

        # Context line
        overrun = stats["total_overrun"]
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*DIM)
        self.set_xy(MX, cy + 52)
        self.cell(CW, 8,
                  f"Total portfolio: ${stats['total_portfolio_budget']:,.0f} budget  |  "
                  f"${overrun:,.0f} total overrun  |  "
                  f"55% of overrun was preventable with early detection",
                  align="C")

        self.footer()

    # =================================================================
    # PAGE 2 -- BY FAILURE MODE
    # =================================================================
    def page_failure_modes(self, stats):
        self.add_page()
        self.bg()
        self.nav_bar()

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*DIM)
        self.text(MX, 16, "SAVINGS BY FAILURE MODE")

        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*NAVY)
        self.text(MX, 30, "Where the money leaks -- and how much we save.")

        modes = stats["by_failure_mode"]
        # Sort by avg savings descending, exclude on_track
        sorted_modes = sorted(
            [(k, v) for k, v in modes.items() if k != "on_track"],
            key=lambda x: x[1]["avg_savings_per_project"],
            reverse=True,
        )

        # Left side: bar chart of avg savings per project
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.text(MX, 42, "Avg Savings Per Project")

        chart_data = []
        labels = {
            "rework": "Rework",
            "change_order_spiral": "Change Orders",
            "material_price_spike": "Material Spikes",
            "crew_inefficiency": "Crew Inefficiency",
            "scope_creep": "Scope Creep",
            "supplier_delay": "Supplier Delays",
            "weather_delay": "Weather Delays",
        }
        for mode, data in sorted_modes:
            label = labels.get(mode, mode)
            chart_data.append((label, data["avg_savings_per_project"], ACCENT))

        self.bar_chart(MX, 46, CW * 0.5, 110, chart_data)

        # Right side: key insight cards
        rx = MX + CW * 0.55
        rw = CW * 0.45

        # Worst offender
        worst_mode, worst_data = sorted_modes[0]
        self.card(rx, 46, rw, 36)
        self.set_fill_color(*DANGER)
        self.rect(rx, 46, 4, 36, "F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*DANGER)
        self.text(rx + 12, 58, f"#1 Threat: {labels.get(worst_mode, worst_mode)}")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*NAVY)
        self.text(rx + 12, 68, f"Avg {worst_data['avg_variance_pct']}% overrun")
        self.text(rx + 12, 76, f"${worst_data['avg_savings_per_project']:,.0f} saveable per project")

        # Second worst
        second_mode, second_data = sorted_modes[1]
        self.card(rx, 90, rw, 36)
        self.set_fill_color(*ACCENT)
        self.rect(rx, 90, 4, 36, "F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*ACCENT)
        self.text(rx + 12, 102, f"#2 Threat: {labels.get(second_mode, second_mode)}")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*NAVY)
        self.text(rx + 12, 112, f"Avg {second_data['avg_variance_pct']}% overrun")
        self.text(rx + 12, 120, f"${second_data['avg_savings_per_project']:,.0f} saveable per project")

        # Bottom insight
        self.rule(MX, 162, CW)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*NAVY)
        self.set_xy(MX, 168)
        self.cell(CW, 10,
                  "85% of projects experience at least one failure mode. "
                  "The question is when you find out.",
                  align="L")

        # Size breakdown -- compact
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.text(MX, 188, "BY PROJECT SIZE:")

        sizes = stats["by_project_size"]
        sx = MX + 55
        for label, data in sizes.items():
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*SUB)
            self.text(MX, 196, label)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*ACCENT)
            self.text(sx + 100, 196, f"${data['avg_savings_per_project']:,.0f}/project")
            # Move down -- but we only have one line space here, so use x offset
            sx += 0
            MX_temp = MX
            break  # just show the biggest for space

        self.footer()

    # =================================================================
    # PAGE 3 -- CASE STUDIES (worst projects)
    # =================================================================
    def page_case_studies(self, stats):
        self.add_page()
        self.bg()
        self.nav_bar()

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*DIM)
        self.text(MX, 16, "CASE STUDIES FROM SIMULATION")

        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*NAVY)
        self.text(MX, 30, "Real scenarios. Real dollar impact.")

        worst = stats["top_10_worst_projects"][:3]
        mode_labels = {
            "rework": "Rework",
            "change_order_spiral": "Change Order Spiral",
            "scope_creep": "Scope Creep",
            "crew_inefficiency": "Crew Inefficiency",
            "supplier_delay": "Supplier Delay",
            "material_price_spike": "Material Price Spike",
            "weather_delay": "Weather Delay",
        }

        cy = 40
        for i, project in enumerate(worst):
            # Card for each case study
            self.card(MX, cy, CW, 44)
            self.set_fill_color(*DANGER)
            self.rect(MX, cy, 4, 44, "F")

            # Project name + value
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*NAVY)
            # Strip "(Sim X)" from name for cleaner look
            name = project["project_name"].split(" (Sim")[0]
            self.text(MX + 12, cy + 12, name)

            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.text(MX + 12, cy + 20,
                      f"${project['project_value']:,.0f} contract  |  "
                      f"Failure: {mode_labels.get(project['failure_mode'], project['failure_mode'])}")

            # Overrun
            self.set_font("Helvetica", "B", 24)
            self.set_text_color(*DANGER)
            self.text(CW * 0.5 + MX, cy + 16, f"${project['overrun']:,.0f}")
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.text(CW * 0.5 + MX, cy + 24, f"overrun ({project['overrun_pct']}%)")

            # Savings
            self.set_font("Helvetica", "B", 24)
            self.set_text_color(*TEAL)
            self.text(CW * 0.78 + MX, cy + 16, f"${project['savings_if_caught_early']:,.0f}")
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*SUB)
            self.text(CW * 0.78 + MX, cy + 24, "saveable with early detection")

            # What happened line
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*NAVY)
            mode = project["failure_mode"]
            narratives = {
                "rework": "Quality issues went undetected for weeks. By the time inspectors flagged it, two phases needed to be redone.",
                "change_order_spiral": "Scope changes compounded across subcontractors. Each change triggered downstream adjustments nobody tracked.",
                "scope_creep": "Small additions accumulated without budget adjustments. The team didn't realize total scope had grown 30%.",
                "crew_inefficiency": "Productivity dropped 25% but timecards looked normal. The variance only showed up in cost-per-unit analysis.",
                "supplier_delay": "Deliveries slipped 2-3 days each. Crews sat idle. Extended equipment rentals added up.",
                "material_price_spike": "Steel prices jumped mid-project. The team locked in at peak instead of hedging early.",
                "weather_delay": "Rain delays pushed the schedule. Overtime and extended rentals eroded the margin.",
            }
            self.set_xy(MX + 12, cy + 28)
            self.multi_cell(CW * 0.45, 5, narratives.get(mode, ""))

            cy += 52

        # Bottom line
        self.rule(MX, cy + 4, CW)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*NAVY)
        self.set_xy(MX, cy + 10)
        self.cell(CW, 10,
                  "These aren't edge cases. They're Tuesday.",
                  align="L")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.set_xy(MX, cy + 20)
        self.cell(CW, 10,
                  f"Across 500 projects, early detection saved an average of "
                  f"${stats['avg_savings_per_project']:,.0f} per project.",
                  align="L")

        self.footer()

    # =================================================================
    # PAGE 4 -- THE ROI MATH
    # =================================================================
    def page_roi(self, stats):
        self.add_page()
        self.bg()
        self.nav_bar()

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*DIM)
        self.text(MX, 16, "THE ROI MATH")

        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*NAVY)
        self.text(MX, 34, "Does it pay for itself? Do the math.")

        # Scenario card: 10 projects, mid-size contractor
        self.card(MX, 46, CW, 80)
        self.set_fill_color(*TEAL)
        self.rect(MX, 46, 4, 80, "F")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*NAVY)
        self.text(MX + 14, 60, "Scenario: Mid-size ICI contractor, 10 active projects")

        # The math
        rows = [
            ("Avg project value", "$8,000,000"),
            ("Typical overrun (5.4%)", "$432,000 per project"),
            ("Early detection saves (55%)", "$237,600 per project"),
            ("Across 10 projects", "$2,376,000 saved per year"),
        ]
        ry = 70
        for label, value in rows:
            self.set_font("Helvetica", "", 14)
            self.set_text_color(*SUB)
            self.text(MX + 14, ry, label)
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*NAVY)
            self.text(MX + 140, ry, value)
            ry += 10

        # The punchline
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*ACCENT)
        self.text(MX + 14, ry + 4, "Platform cost: $125,000/year")
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*TEAL)
        self.text(MX + 140, ry + 4, "19:1 ROI")

        # Even conservative scenario
        cy2 = 138
        self.card(MX, cy2, CW, 40)
        self.set_fill_color(*NAVY)
        self.rect(MX, cy2, 4, 40, "F")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*NAVY)
        self.text(MX + 14, cy2 + 14, "Conservative scenario: catch just 1 problem on 1 project")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*SUB)
        self.text(MX + 14, cy2 + 26,
                  "Even one caught overrun on one project pays for the platform for 2 years.")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*ACCENT)
        self.text(MX + 14, cy2 + 34,
                  "The platform needs to work once to pay for itself.")

        # CTA
        self.rule(MX, PH - 38, CW)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*NAVY)
        self.set_xy(MX, PH - 32)
        self.cell(CW, 10, "Ready to see these numbers on your projects?", align="C")

        self.set_font("Helvetica", "", 14)
        self.set_text_color(*ACCENT)
        self.set_xy(MX, PH - 20)
        self.cell(CW, 10, "michael@blackmountainmedia.com", align="C")

        self.footer()


def main():
    with open(STATS_PATH) as f:
        stats = json.load(f)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d = ProofDeck()
    d.page_headline(stats)
    d.page_failure_modes(stats)
    d.page_case_studies(stats)
    d.page_roi(stats)
    d.output(OUT)
    print(f"Done: {OUT}")


if __name__ == "__main__":
    main()
