#!/usr/bin/env python3
"""Generate BMM Project Optimizer -- Plain Setup & User Guide PDF."""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Setup_Guide.pdf")

PW = 215.9
PH = 279.4
MX = 20
CW = PW - MX * 2


class Doc(FPDF):
    def __init__(self):
        super().__init__(orientation="P", format="letter")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)

    def heading(self, text):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, text, ln=True)
        self.ln(2)
        self.set_font("Helvetica", "", 10)

    def sub(self, text):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, text, ln=True)
        self.set_font("Helvetica", "", 10)

    def body(self, text):
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_x(MX)
        self.cell(5, 5, "-")
        self.multi_cell(CW - 5, 5, text)

    def bullets(self, items):
        for item in items:
            self.bullet(item)
        self.ln(2)

    def code(self, text):
        self.set_font("Courier", "", 9)
        for line in text.strip().split("\n"):
            self.cell(0, 5, "  " + line, ln=True)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def build(self):
        self.add_page()
        self.set_font("Helvetica", "B", 22)
        self.cell(0, 12, "BMM Project Optimizer", ln=True)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, "Setup & User Guide  |  March 2026", ln=True)
        self.ln(6)

        # --- WHAT IT DOES ---
        self.heading("What This Platform Does")
        self.body(
            "A construction intelligence dashboard that shows budget health, "
            "schedule risk, labor productivity, material delivery, and change "
            "order impact across all your active projects. It replaces the "
            "spreadsheet-checking and manual report-building process with "
            "real-time scoring and anomaly detection.")
        self.ln(2)

        # --- QUICK START ---
        self.heading("Quick Start")
        self.sub("1. Install")
        self.code("pip install -r requirements.txt")
        self.sub("2. Launch")
        self.code("streamlit run tools/app.py")
        self.body(
            "Opens in your browser at http://localhost:8501. Loads with demo "
            "data so you can explore immediately.")
        self.sub("3. Upload Your Data")
        self.body(
            "Click 'Upload Data' in the sidebar. Download a template, fill it "
            "in, upload, review the quality score, and import. Toggle 'Use "
            "Uploaded Data' to switch from demo to real data.")
        self.sub("4. Enable AI Assistant (optional)")
        self.code("pip install anthropic\nexport ANTHROPIC_API_KEY=sk-ant-your-key-here")
        self.body("Restart the dashboard. The AI page activates automatically.")
        self.ln(2)

        # --- DATA TYPES ---
        self.heading("Data Types")
        self.body("You need Budget + Actuals at minimum. Each additional type unlocks more analysis.")
        types = [
            "Budget / Bid -- required fields: project_name, phase, cost_category, line_item, budgeted_amount",
            "Actuals / Costs -- required fields: project_name, phase, cost_category, line_item, actual_amount",
            "Change Orders -- required fields: project_name, co_number, description, cost_impact",
            "Schedule -- required fields: project_name, task_name, planned_start, planned_end",
            "Timecards -- required fields: project_name, worker_name, date, hours",
            "Materials -- required fields: project_name, material, quantity, unit_cost",
        ]
        self.bullets(types)
        self.body(
            "Column names don't need to match exactly. The system auto-detects "
            "common aliases like 'Job #', 'Hrs', 'Cost', etc. You can manually "
            "override any mapping before importing.")

        # --- PAGES ---
        self.heading("Dashboard Pages")
        pages = [
            "Portfolio Overview -- every project with health score, RAG status, top risk.",
            "Project Detail -- drill into one project by phase, category, and line item.",
            "Change Orders -- separates approved scope changes from true overruns.",
            "Schedule Intelligence -- flags slipping, late, and overdue tasks.",
            "Labor Productivity -- hours, overtime, rates, crew breakdowns.",
            "Materials -- delivery risk, overdue/backordered items, dollar exposure.",
            "Outliers -- statistical anomaly detection (IQR, Z-score, peer comparison).",
            "Upload Data -- import CSVs, download templates, validate quality.",
            "AI Assistant -- ask questions about your data in plain English.",
        ]
        self.bullets(pages)

        # --- HEALTH SCORES ---
        self.heading("Health Scores & Colors")
        self.sub("RAG Status")
        self.bullets([
            "Green: under 5% variance -- on track.",
            "Yellow: 5-10% variance -- needs attention.",
            "Red: over 10% variance -- at risk.",
        ])
        self.sub("Health Score (0-100)")
        self.body("Weighted average of five factors:")
        self.bullets([
            "Budget Variance (35%) -- how far actual spend is from budget.",
            "Change Order Impact (15%) -- CO cost as % of total budget.",
            "Schedule Performance (20%) -- % of tasks on track.",
            "Data Completeness (20%) -- how many data types are uploaded.",
            "Labor Productivity (10%) -- inverse of overtime percentage.",
        ])
        self.body("Grades: A = 90-100, B = 70-89, C = 50-69, D = below 50.")

        # --- AI ASSISTANT ---
        self.heading("AI Assistant")
        self.body(
            "Chat interface powered by Claude. Has full context of all loaded "
            "project data. Ask things like:")
        self.bullets([
            "\"Which project has the highest budget variance?\"",
            "\"Show me overtime trends across all projects\"",
            "\"Any schedule delays I should worry about?\"",
            "\"Summarize the health of my portfolio in three sentences\"",
        ])
        self.body(
            "Each question costs roughly $0.01-0.05 in API usage. A typical "
            "user asking 20-30 questions/day would cost under $1.00/day.")

        # --- IT DEPLOYMENT ---
        self.heading("IT / Admin Deployment")
        self.sub("Requirements")
        self.bullets([
            "Python 3.9+ (3.11 or 3.12 recommended)",
            "4 GB RAM minimum, 8 GB recommended",
            "Network access to api.anthropic.com (port 443) for AI features",
        ])
        self.sub("Full Install")
        self.code(
            "git clone <repo-url> bmm-optimizer\n"
            "cd bmm-optimizer\n"
            "python -m venv venv\n"
            "source venv/bin/activate\n"
            "pip install -r requirements.txt\n"
            "pip install anthropic\n"
            "export ANTHROPIC_API_KEY=sk-ant-your-key-here\n"
            "streamlit run tools/app.py")
        self.sub("Streamlit Cloud")
        self.bullets([
            "Push to GitHub, connect at share.streamlit.io.",
            "Set main file path to tools/app.py.",
            "Add ANTHROPIC_API_KEY in Secrets settings.",
        ])
        self.sub("Security Notes")
        self.bullets([
            "Never commit API keys to the repo. Use env vars or Streamlit secrets.",
            "Session data is temporary -- nothing persists between sessions.",
            "AI queries send project data to Anthropic's API. Review their data policy.",
            "Restrict Streamlit port (8501) with firewall rules for internal use.",
        ])

        # --- TROUBLESHOOTING ---
        self.heading("Troubleshooting")
        issues = [
            ("Dashboard shows demo data", "Upload Budget + Actuals, then toggle 'Use Uploaded Data'."),
            ("AI says 'API key not configured'", "Set ANTHROPIC_API_KEY env var and restart."),
            ("AI says 'anthropic not installed'", "Run: pip install anthropic"),
            ("Columns not auto-detected", "Use manual dropdown override, or rename to match template."),
            ("Health score seems low", "Upload all 6 data types. Data completeness is 20% of the score."),
            ("Data disappears after closing browser", "Sessions are temporary. Re-upload each time."),
            ("Port 8501 in use", "streamlit run tools/app.py --server.port 8502"),
        ]
        for q, a in issues:
            self.set_x(MX)
            self.set_font("Helvetica", "B", 10)
            self.multi_cell(CW, 5, q)
            self.set_x(MX)
            self.set_font("Helvetica", "", 10)
            self.multi_cell(CW, 5, a)
            self.ln(2)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = Doc()
    doc.build()
    doc.output(OUT)
    print(f"Guide saved to {OUT}")


if __name__ == "__main__":
    main()
