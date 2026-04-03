#!/usr/bin/env python3
"""Generate BMM Incident Response & Breach Notification Policy PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Incident_Response_Policy.pdf")

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
TITLE = "INCIDENT RESPONSE & BREACH NOTIFICATION POLICY"


class IncidentResponsePolicy(FPDF):
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
        self.set_xy(0, 22)
        self.cell(PW, 10, "INCIDENT RESPONSE &", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 34)
        self.cell(PW, 10, "BREACH NOTIFICATION POLICY", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 50)
        self.cell(PW, 6, "Black Mountain Technologies Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 58)
        self.cell(PW, 6, "Construction Project Optimization Platform", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
            "This policy defines Black Mountain Technologies Inc.'s (\"BMM\") process for "
            "identifying, responding to, and recovering from security incidents and "
            "data breaches affecting the BMM Analytics Construction Project "
            "Optimization Suite (the \"Platform\").")
        self.body(
            "This policy ensures compliance with the breach notification requirements "
            "under the Personal Information Protection and Electronic Documents Act "
            "(PIPEDA) and provides transparency to customers about how incidents are "
            "handled.")

        # --- Section 2: Definitions ---
        self.section(2, "DEFINITIONS")
        self.body(
            "Security Incident: Any event that compromises the confidentiality, "
            "integrity, or availability of the Platform or customer data.")
        self.body(
            "Data Breach: A security incident resulting in unauthorized access to, "
            "disclosure of, or loss of personal information.")
        self.body(
            "Near Miss: An event that could have resulted in a security incident "
            "but was prevented or contained before impact.")

        # --- Section 3: Incident Classification ---
        self.section(3, "INCIDENT CLASSIFICATION")
        self.body("All security incidents are classified by severity level:")
        self.bullet(
            "Critical -- Confirmed data breach affecting customer personal data, "
            "complete platform outage, or active attack in progress.")
        self.bullet(
            "High -- Unauthorized access attempt detected, partial service disruption, "
            "or vulnerability actively being exploited.")
        self.bullet(
            "Medium -- Suspicious activity detected, minor service degradation, or "
            "vulnerability discovered but not exploited.")
        self.bullet(
            "Low -- Failed login attempts, minor policy violations, or near misses.")

        # --- Section 4: Incident Response Phases ---
        self.section(4, "INCIDENT RESPONSE PHASES")

        self.body("Phase 1 -- Detection and Identification")
        self.sub_clause("a",
            "Automated monitoring systems alert on suspicious activity.")
        self.sub_clause("b",
            "User-reported incidents received via michael@blackmountaintechnologies.ca.")
        self.sub_clause("c",
            "Incident logged with timestamp, description, and initial severity "
            "classification.")
        self.sub_clause("d",
            "Incident response team activated based on severity.")

        self.body("Phase 2 -- Containment")
        self.sub_clause("a",
            "Immediate actions to limit the scope and impact of the incident.")
        self.sub_clause("b",
            "Short-term containment: isolate affected systems, revoke compromised "
            "credentials, block attack vectors.")
        self.sub_clause("c",
            "Evidence preservation: capture logs, screenshots, and forensic data "
            "before remediation.")
        self.sub_clause("d",
            "Assess whether customer data has been affected.")

        self.body("Phase 3 -- Eradication")
        self.sub_clause("a",
            "Identify and eliminate the root cause.")
        self.sub_clause("b",
            "Remove malware, close vulnerabilities, patch systems.")
        self.sub_clause("c",
            "Verify eradication is complete before restoring service.")

        self.body("Phase 4 -- Recovery")
        self.sub_clause("a",
            "Restore affected systems and data from clean backups.")
        self.sub_clause("b",
            "Verify system integrity before returning to production.")
        self.sub_clause("c",
            "Monitor closely for recurrence.")
        self.sub_clause("d",
            "Communicate restoration to affected customers.")

        self.body("Phase 5 -- Post-Incident Review")
        self.sub_clause("a",
            "Conduct root cause analysis within 5 business days.")
        self.sub_clause("b",
            "Document lessons learned and remediation actions.")
        self.sub_clause("c",
            "Update security measures to prevent recurrence.")
        self.sub_clause("d",
            "Update this policy if gaps are identified.")

        # --- Section 5: Customer Notification ---
        self.section(5, "CUSTOMER NOTIFICATION")
        self.body(
            "BMM will notify affected customers within 72 hours of confirming a "
            "data breach. Notification will include:")
        self.sub_clause("a",
            "Nature and scope of the breach.")
        self.sub_clause("b",
            "Categories of personal information affected.")
        self.sub_clause("c",
            "Approximate number of individuals affected.")
        self.sub_clause("d",
            "Likely consequences of the breach.")
        self.sub_clause("e",
            "Measures taken to contain and remediate the breach.")
        self.sub_clause("f",
            "Recommended actions for the customer.")
        self.sub_clause("g",
            "BMM contact for further information.")
        self.body(
            "Notification method: email to the primary contact on file, followed "
            "by phone call for Critical severity incidents.")
        self.body(
            "BMM will cooperate with customers in their own breach notification "
            "obligations to data subjects and regulators.")

        # --- Section 6: Regulatory Notification ---
        self.section(6, "REGULATORY NOTIFICATION")
        self.body(
            "Under PIPEDA, BMM will report breaches involving \"real risk of "
            "significant harm\" to the Office of the Privacy Commissioner of Canada.")
        self.body(
            "BMM will maintain records of all breaches for a minimum of 24 months "
            "as required by PIPEDA.")
        self.body(
            "BMM will assist customers with any regulatory filings or notifications "
            "required under applicable law.")

        # --- Section 7: Roles and Responsibilities ---
        self.section(7, "ROLES AND RESPONSIBILITIES")
        self.bullet(
            "Incident Response Lead: Responsible for coordinating the response, "
            "communication, and escalation.")
        self.bullet(
            "Technical Team: Responsible for containment, eradication, and recovery.")
        self.bullet(
            "Management: Responsible for customer communication, regulatory "
            "notification decisions, and resource allocation.")
        self.bullet(
            "All Employees: Responsible for reporting suspected incidents immediately.")

        # --- Section 8: Breach Register ---
        self.section(8, "BREACH REGISTER")
        self.body(
            "BMM maintains a register of all security incidents and data breaches.")
        self.body(
            "The register includes: date, description, severity, data affected, "
            "response actions taken, customer notifications sent, regulatory filings "
            "made, and lessons learned.")
        self.body(
            "The register is available for customer audit as specified in the Data "
            "Processing Addendum.")

        # --- Section 9: Testing and Updates ---
        self.section(9, "TESTING AND UPDATES")
        self.bullet(
            "Incident response plan is tested at least annually through tabletop "
            "exercises.")
        self.bullet(
            "Plan is reviewed and updated after every significant incident.")
        self.bullet(
            "Plan is reviewed annually regardless of incidents.")
        self.bullet(
            "All incident response team members receive training on this policy.")

        # --- Section 10: Contact ---
        self.section(10, "CONTACT")
        self.body(
            "To report a security incident or for questions about this policy, "
            "please contact us:")
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.cell(CW - 8, 5, "Black Mountain Technologies Inc.",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        fields = [
            "British Columbia, Canada",
            "Email: michael@blackmountaintechnologies.ca",
        ]
        for f in fields:
            self.set_x(MX + 8)
            self.cell(CW - 8, 5, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = IncidentResponsePolicy()
    doc.build()
    doc.output(OUT)
    print(f"Incident Response Policy saved to {OUT}")


if __name__ == "__main__":
    main()
