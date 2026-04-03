#!/usr/bin/env python3
"""Generate BMM Acceptable Use Policy PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Acceptable_Use_Policy.pdf")

# Palette
DARK = (15, 23, 42)
GREEN = (74, 124, 89)
WHITE = (255, 255, 255)
LIGHT_BG = (248, 250, 252)
GRAY = (100, 116, 139)
DARK_TEXT = (30, 41, 59)

PW = 215.9
PH = 279.4
MX = 25
CW = PW - MX * 2
TITLE = "ACCEPTABLE USE POLICY"


class AcceptableUsePolicy(FPDF):
    def __init__(self):
        super().__init__(orientation="P", format="letter")
        self.set_auto_page_break(auto=True, margin=25)
        self._is_cover = True

    # --- reusable helpers ---
    def _dark_header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, PW, 18, "F")
        self.set_fill_color(*GREEN)
        self.rect(0, 18, PW, 1.5, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(MX, 6)
        self.cell(CW, 6, TITLE, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def header(self):
        if self._is_cover:
            return
        self._dark_header()
        self.set_y(24)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}  |  Confidential  |  Black Mountain Technologies",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def section(self, num, title):
        self.ln(4)
        y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(MX, y, 2, 7, "F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 6)
        self.cell(CW - 6, 7, f"{num}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.multi_cell(CW, 5, text)
        self.ln(1)

    def sub_clause(self, label, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.multi_cell(CW - 8, 5, f"({label}) {text}")
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.multi_cell(CW - 8, 5, f"- {text}")
        self.ln(1)

    # --- pages ---
    def cover(self):
        self.add_page()
        self._is_cover = True

        # Dark header block
        self.set_fill_color(*DARK)
        self.rect(0, 0, PW, 80, "F")
        self.set_fill_color(*GREEN)
        self.rect(0, 80, PW, 3, "F")

        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*WHITE)
        self.set_xy(0, 28)
        self.cell(PW, 10, TITLE, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 44)
        self.cell(PW, 6, "Black Mountain Technologies Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 52)
        self.cell(PW, 6, "BMM Analytics Construction Project Optimization Suite",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Last updated line
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Last Updated: March 2026", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self._is_cover = False

    def build(self):
        self.cover()

        # --- Section 1: Purpose ---
        self.section(1, "PURPOSE")
        self.body(
            "This Acceptable Use Policy (\"AUP\") defines acceptable and prohibited "
            "uses of the BMM Analytics Construction Project Optimization Suite "
            "(the \"Platform\") operated by Black Mountain Technologies Inc. (\"BMM\"), "
            "a company based in British Columbia, Canada.")
        self.body(
            "This policy applies to all users of the Platform, including employees, "
            "contractors, and authorized users of Licensee organizations.")
        self.body(
            "Violations of this policy may result in suspension or termination of "
            "access to the Platform. This AUP is referenced by and incorporated "
            "into the BMM Terms of Service.")

        # --- Section 2: Acceptable Use ---
        self.section(2, "ACCEPTABLE USE")
        self.body("You may:")
        self.sub_clause("a",
            "Upload your organization's construction project data for analysis.")
        self.sub_clause("b",
            "Use dashboard features to view budgets, schedules, labor, materials, "
            "and change orders.")
        self.sub_clause("c",
            "Use the AI Assistant to ask questions about your project data.")
        self.sub_clause("d",
            "Export reports and analytics for internal business use.")
        self.sub_clause("e",
            "Share platform-generated reports within your organization with "
            "authorized personnel.")
        self.sub_clause("f",
            "Provide feedback and feature requests to BMM.")

        # --- Section 3: Prohibited Use ---
        self.section(3, "PROHIBITED USE")
        self.body("You must not:")
        self.sub_clause("a",
            "Share login credentials or allow unauthorized persons to access "
            "your account.")
        self.sub_clause("b",
            "Upload data containing malware, viruses, or malicious code.")
        self.sub_clause("c",
            "Upload data you do not have legal rights to use.")
        self.sub_clause("d",
            "Attempt to access other users' or organizations' data.")
        self.sub_clause("e",
            "Use automated tools (bots, scrapers, crawlers) to extract data "
            "from the platform.")
        self.sub_clause("f",
            "Reverse engineer, decompile, or probe the platform's source code "
            "or algorithms.")
        self.sub_clause("g",
            "Use the platform or its outputs to build, train, or improve "
            "competing products.")
        self.sub_clause("h",
            "Overload the platform intentionally or interfere with service "
            "for other users.")
        self.sub_clause("i",
            "Circumvent, disable, or tamper with any platform security features.")
        self.sub_clause("j",
            "Use the AI Assistant to attempt prompt injection, extract system "
            "instructions, or manipulate AI behavior.")
        self.sub_clause("k",
            "Upload personally identifiable information beyond what is necessary "
            "for project management (do not upload SINs, banking info, health "
            "data, etc.).")
        self.sub_clause("l",
            "Use the platform for any purpose that violates applicable law.")

        # --- Section 4: Data Responsibilities ---
        self.section(4, "DATA RESPONSIBILITIES")
        self.bullet(
            "You are responsible for ensuring all uploaded data is accurate, "
            "lawful, and properly authorized.")
        self.bullet(
            "You must have appropriate consent from individuals whose personal "
            "information appears in uploaded data (worker names, hours, rates "
            "in timecards).")
        self.bullet(
            "You must comply with all applicable privacy laws (PIPEDA, PIPA, "
            "GDPR where applicable).")
        self.bullet(
            "Do not upload data classified as sensitive or restricted beyond "
            "normal construction project information.")

        # --- Section 5: Security Obligations ---
        self.section(5, "SECURITY OBLIGATIONS")
        self.bullet("Use strong, unique passwords for your account.")
        self.bullet("Enable multi-factor authentication when available.")
        self.bullet(
            "Do not access the platform from public or unsecured networks "
            "without VPN.")
        self.bullet("Log out after each session on shared devices.")
        self.bullet(
            "Report any suspected security incidents to "
            "michael@blackmountaintechnologies.ca immediately.")

        # --- Section 6: Enforcement ---
        self.section(6, "ENFORCEMENT")
        self.body(
            "BMM monitors platform usage for compliance with this policy.")
        self.body(
            "Violations may result in: written warning, temporary suspension "
            "of access, permanent termination of access, or legal action "
            "depending on severity.")
        self.body(
            "BMM may suspend access immediately without notice for severe "
            "violations (security threats, data breaches, illegal activity).")
        self.body(
            "Appeals may be directed to michael@blackmountaintechnologies.ca.")

        # --- Section 7: Changes to This Policy ---
        self.section(7, "CHANGES TO THIS POLICY")
        self.body("BMM may update this policy at any time.")
        self.body(
            "Material changes will be communicated via email or platform "
            "notification.")
        self.body(
            "Continued use after notification constitutes acceptance of the "
            "updated policy.")

        # --- Contact ---
        self.ln(4)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 5, "Contact", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_font("Helvetica", "", 10)
        fields = [
            "Black Mountain Technologies Inc.",
            "British Columbia, Canada",
            "Email: michael@blackmountaintechnologies.ca",
        ]
        for f in fields:
            self.set_x(MX + 8)
            self.cell(CW - 8, 5, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = AcceptableUsePolicy()
    doc.build()
    doc.output(OUT)
    print(f"Acceptable Use Policy saved to {OUT}")


if __name__ == "__main__":
    main()
