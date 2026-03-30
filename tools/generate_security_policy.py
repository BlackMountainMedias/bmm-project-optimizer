#!/usr/bin/env python3
"""Generate BMM Information Security Policy PDF (customer-facing)."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Information_Security_Policy.pdf")

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
TITLE = "INFORMATION SECURITY POLICY"


class SecurityPolicy(FPDF):
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
        self.cell(0, 5, f"Page {self.page_no()}  |  Confidential  |  Black Mountain Media",
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
        self.cell(PW, 6, "Black Mountain Media Inc.", align="C",
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

        # --- Section 1: Overview ---
        self.section(1, "Overview")
        self.body(
            "Black Mountain Media Inc. (\"BMM\") is committed to protecting the "
            "confidentiality, integrity, and availability of customer data entrusted "
            "to us through the BMM Analytics platform.")
        self.body(
            "This document summarizes the technical and organizational security "
            "measures in place for the BMM Analytics Construction Project "
            "Optimization Suite. It is provided to customers and prospects as a "
            "summary of our security practices.")
        self.body(
            "We align our practices with industry standards and Canadian privacy "
            "legislation, including the Personal Information Protection and "
            "Electronic Documents Act (PIPEDA) and the British Columbia Personal "
            "Information Protection Act (PIPA).")

        # --- Section 2: Data Encryption ---
        self.section(2, "Data Encryption")
        self.sub_clause("a",
            "In Transit: All data transmitted between user browsers and the "
            "platform is encrypted using TLS 1.2 or higher. No unencrypted data "
            "transmission is permitted.")
        self.sub_clause("b",
            "At Rest: All stored data is encrypted using AES-256 encryption.")
        self.sub_clause("c",
            "API Communications: All API calls to third-party services, including "
            "Anthropic for AI features, use encrypted HTTPS connections.")
        self.sub_clause("d",
            "No unencrypted data transmission is permitted at any point in the "
            "data lifecycle.")

        # --- Section 3: Access Control ---
        self.section(3, "Access Control")
        self.sub_clause("a",
            "Role-based access control (RBAC) ensures users only access data "
            "relevant to their organization and role.")
        self.sub_clause("b",
            "Multi-factor authentication (MFA) is available for all user accounts "
            "and required for administrative access.")
        self.sub_clause("c",
            "Least-privilege principle: employees and systems are granted the "
            "minimum access necessary to perform their functions.")
        self.sub_clause("d",
            "Automated session timeout after period of inactivity.")
        self.sub_clause("e",
            "Unique credentials required for every user -- shared accounts are "
            "prohibited.")

        # --- Section 4: Application Security ---
        self.section(4, "Application Security")
        self.sub_clause("a",
            "Secure development lifecycle with code review for all changes.")
        self.sub_clause("b",
            "Input validation and output encoding to prevent injection attacks "
            "(SQL injection, XSS, etc.).")
        self.sub_clause("c",
            "Regular dependency scanning for known vulnerabilities.")
        self.sub_clause("d",
            "Session management with secure, HTTP-only cookies.")
        self.sub_clause("e",
            "CSRF protection on all state-changing operations.")

        # --- Section 5: Infrastructure Security ---
        self.section(5, "Infrastructure Security")
        self.sub_clause("a",
            "Platform hosted on enterprise-grade cloud infrastructure with "
            "SOC 2 certified providers.")
        self.sub_clause("b",
            "Network segmentation and firewall rules restrict access to "
            "production systems.")
        self.sub_clause("c",
            "Regular vulnerability scanning and penetration testing.")
        self.sub_clause("d",
            "Automated monitoring and alerting for suspicious activity.")
        self.sub_clause("e",
            "DDoS protection through cloud provider security features.")

        # --- Section 6: AI Assistant Security ---
        self.section(6, "AI Assistant Security")
        self.sub_clause("a",
            "AI queries are processed by Anthropic's commercial API (Claude).")
        self.sub_clause("b",
            "Anthropic's commercial terms: customer data is NOT used for model "
            "training and is NOT retained beyond the API request lifecycle.")
        self.sub_clause("c",
            "AI conversations exist only in the user's browser session -- not "
            "stored server-side.")
        self.sub_clause("d",
            "Users can opt out of the AI Assistant feature entirely, preventing "
            "any data from being sent to Anthropic.")
        self.sub_clause("e",
            "AI responses are generated in real-time and not cached or logged "
            "by BMM.")

        # --- Section 7: Personnel Security ---
        self.section(7, "Personnel Security")
        self.sub_clause("a",
            "All employees with access to customer data undergo background "
            "checks.")
        self.sub_clause("b",
            "Mandatory security awareness training for all staff.")
        self.sub_clause("c",
            "Confidentiality agreements required for all employees and "
            "contractors.")
        self.sub_clause("d",
            "Access is revoked immediately upon termination of employment.")
        self.sub_clause("e",
            "Security responsibilities are clearly defined and documented.")

        # --- Section 8: Incident Response ---
        self.section(8, "Incident Response")
        self.sub_clause("a",
            "Documented incident response plan covering detection, containment, "
            "eradication, and recovery.")
        self.sub_clause("b",
            "Security incidents are classified by severity and escalated "
            "accordingly.")
        self.sub_clause("c",
            "Customer notification within 72 hours of confirmed data breach, "
            "per PIPEDA requirements and Data Processing Agreement commitments.")
        self.sub_clause("d",
            "Post-incident review and remediation to prevent recurrence.")
        self.sub_clause("e",
            "Incident response plan tested and updated annually.")

        # --- Section 9: Business Continuity ---
        self.section(9, "Business Continuity")
        self.sub_clause("a",
            "Regular data backups with tested recovery procedures.")
        self.sub_clause("b",
            "Recovery Time Objective (RTO): 4 hours for critical services.")
        self.sub_clause("c",
            "Recovery Point Objective (RPO): 24 hours maximum data loss.")
        self.sub_clause("d",
            "Disaster recovery plan covering infrastructure failure, data "
            "corruption, and service disruption.")
        self.sub_clause("e",
            "Geographic redundancy for critical systems (where applicable).")

        # --- Section 10: Third-Party Management ---
        self.section(10, "Third-Party Management")
        self.body(
            "All sub-processors are vetted for security practices before "
            "engagement. Contractual security requirements are imposed on all "
            "sub-processors.")
        self.body("Current sub-processors:")
        self.bullet(
            "Anthropic PBC -- AI query processing (US-based, SOC 2 compliant)")
        self.bullet(
            "Cloud hosting provider -- infrastructure (specified per deployment)")
        self.body(
            "A complete sub-processor list is maintained and available to "
            "customers on request.")

        # --- Section 11: Compliance ---
        self.section(11, "Compliance")
        self.sub_clause("a",
            "Aligned with PIPEDA (Personal Information Protection and Electronic "
            "Documents Act).")
        self.sub_clause("b",
            "Aligned with BC PIPA (Personal Information Protection Act).")
        self.sub_clause("c",
            "GDPR considerations addressed for customers with European "
            "operations.")
        self.sub_clause("d",
            "Annual security review and policy updates.")
        self.sub_clause("e",
            "SOC 2 Type I certification planned (timeline available on request).")

        # --- Section 12: Contact ---
        self.section(12, "Contact")
        self.body(
            "For security inquiries, to report a security vulnerability, or to "
            "report a security incident, please contact us:")
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.cell(CW - 8, 5, "Black Mountain Media Inc.",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        fields = [
            "British Columbia, Canada",
            "Email: michael@blackmountainmedias.ca",
        ]
        for f in fields:
            self.set_x(MX + 8)
            self.cell(CW - 8, 5, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = SecurityPolicy()
    doc.build()
    doc.output(OUT)
    print(f"Information Security Policy saved to {OUT}")


if __name__ == "__main__":
    main()
