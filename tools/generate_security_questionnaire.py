#!/usr/bin/env python3
"""Generate BMM Pre-Filled Security Questionnaire Response PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Security_Questionnaire.pdf")

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
TITLE = "SECURITY QUESTIONNAIRE RESPONSES"


class SecurityQuestionnaire(FPDF):
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

    def qa(self, question, answer):
        """Render a Question / Answer pair."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 4)
        self.multi_cell(CW - 4, 5, f"Q: {question}")
        self.ln(1)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 4)
        self.multi_cell(CW - 4, 5, f"A: {answer}")
        self.ln(3)

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
        self.set_xy(0, 60)
        self.cell(PW, 6, "michael@blackmountainmedias.ca",
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

        # --- 1. Company Information ---
        self.section(1, "Company Information")

        self.qa("Company legal name?",
                "Black Mountain Media Inc.")

        self.qa("Company location?",
                "British Columbia, Canada.")

        self.qa("What services do you provide?",
                "SaaS construction project optimization platform providing budget "
                "analytics, schedule risk detection, labor productivity analysis, "
                "material delivery tracking, change order management, statistical "
                "outlier detection, and AI-powered project intelligence.")

        self.qa("How is the service delivered?",
                "Software-as-a-Service (SaaS) accessible via web browser. No "
                "software installation required.")

        # --- 2. Data Handling ---
        self.section(2, "Data Handling")

        self.qa("What customer data do you collect and process?",
                "Project budgets, actual costs, change orders, schedule tasks, "
                "timecard/labor data (worker names, hours, rates), material orders, "
                "and authorized user account information (name, email, company).")

        self.qa("Do you process personally identifiable information (PII)?",
                "Yes. Timecard data may contain worker names, hours worked, and "
                "hourly rates, which constitute PII under PIPEDA. Account "
                "information (name, email) is also PII.")

        self.qa("Where is customer data stored?",
                "Currently session-based architecture -- data exists in the user's "
                "browser session and is not persisted server-side between sessions. "
                "For cloud deployments, data is processed on Streamlit Cloud "
                "(hosted by Snowflake, US/Canada).")

        self.qa("Do you share customer data with third parties?",
                "Only with Anthropic PBC for AI Assistant queries (when the feature "
                "is used by the customer). No data is sold or shared for marketing "
                "purposes.")

        self.qa("Can customers opt out of third-party data sharing?",
                "Yes. The AI Assistant is optional. If not used, no data is sent "
                "to Anthropic or any third party.")

        self.qa("What is your data retention policy?",
                "Session data is deleted when the browser session ends. Account "
                "information is retained for the License Term plus 30 days. "
                "Anonymized/aggregated data may be retained for benchmarking.")

        self.qa("How is data deleted at end of contract?",
                "All customer data is deleted within 30 days of contract "
                "termination. Deletion is certified in writing upon request.")

        # --- 3. Encryption and Security ---
        self.section(3, "Encryption and Security")

        self.qa("Is data encrypted in transit?",
                "Yes. TLS 1.2 or higher for all data transmission.")

        self.qa("Is data encrypted at rest?",
                "Yes. AES-256 encryption for any stored data.")

        self.qa("Do you support multi-factor authentication (MFA)?",
                "MFA is available for all accounts and required for "
                "administrative access.")

        self.qa("Do you have role-based access controls?",
                "Yes. Users only access data for their organization. "
                "Administrative functions are restricted to authorized personnel.")

        self.qa("Do you perform regular vulnerability assessments?",
                "Yes. Regular dependency scanning, code review for all changes, "
                "and periodic vulnerability assessments.")

        self.qa("Do you have a penetration testing program?",
                "Penetration testing is conducted periodically. Results and "
                "remediation available on request under NDA.")

        self.qa("Do you have DDoS protection?",
                "Yes, through cloud provider security infrastructure.")

        # --- 4. Access Control ---
        self.section(4, "Access Control")

        self.qa("How do employees access production systems?",
                "Least-privilege access, unique credentials, MFA required, "
                "access logged and audited.")

        self.qa("How is employee access revoked?",
                "Immediately upon termination of employment.")

        self.qa("Do employees undergo background checks?",
                "Yes. All employees with access to customer data undergo "
                "background checks.")

        self.qa("Do employees receive security training?",
                "Yes. Mandatory security awareness training for all staff.")

        # --- 5. Incident Response ---
        self.section(5, "Incident Response")

        self.qa("Do you have a documented incident response plan?",
                "Yes. Covering detection, containment, eradication, recovery, "
                "and post-incident review.")

        self.qa("What is your breach notification timeline?",
                "Customers are notified within 72 hours of a confirmed data "
                "breach, per PIPEDA requirements and our DPA commitments.")

        self.qa("Do you maintain a breach register?",
                "Yes. All incidents are logged and retained for a minimum of "
                "24 months.")

        self.qa("Has there been a data breach in the past 12 months?",
                "No.")

        # --- 6. Compliance and Certifications ---
        self.section(6, "Compliance and Certifications")

        self.qa("What privacy regulations do you comply with?",
                "PIPEDA (federal Canada), BC PIPA (provincial), with GDPR "
                "considerations for customers with European operations.")

        self.qa("Do you have SOC 2 certification?",
                "SOC 2 Type I is planned. Timeline available on request.")

        self.qa("Do you have ISO 27001 certification?",
                "Not currently. Under consideration for future compliance "
                "roadmap.")

        self.qa("Do you have cyber liability insurance?",
                "[To be confirmed -- recommend answering \"Yes, CAD $X million "
                "coverage\" once obtained, or \"In process of obtaining\" if not "
                "yet in place]")

        # --- 7. Business Continuity ---
        self.section(7, "Business Continuity")

        self.qa("Do you have a business continuity plan?",
                "Yes. Covering infrastructure failure, data corruption, and "
                "service disruption scenarios.")

        self.qa("What is your Recovery Time Objective (RTO)?",
                "4 hours for critical services.")

        self.qa("What is your Recovery Point Objective (RPO)?",
                "24 hours maximum data loss.")

        self.qa("Do you have geographic redundancy?",
                "Dependent on deployment architecture. Cloud deployments "
                "leverage provider redundancy.")

        # --- 8. Subprocessors ---
        self.section(8, "Subprocessors")

        self.qa("What third-party subprocessors do you use?",
                "Anthropic PBC (AI query processing, US-based, SOC 2), "
                "Streamlit/Snowflake (application hosting), GitHub/Microsoft "
                "(source code only, no customer data).")

        self.qa("How are subprocessors vetted?",
                "Security practices reviewed before engagement. Contractual "
                "security requirements imposed.")

        self.qa("How are customers notified of new subprocessors?",
                "30 days advance written notice, with 14-day objection period "
                "per the DPA.")

        # --- 9. AI-Specific ---
        self.section(9, "AI-Specific")

        self.qa("How does the AI feature process customer data?",
                "Project data is serialized into context and sent to Anthropic's "
                "Claude API via encrypted HTTPS. Responses are returned to the "
                "user's browser session.")

        self.qa("Is customer data used to train AI models?",
                "No. Anthropic's commercial API terms prohibit use of customer "
                "data for model training.")

        self.qa("Is AI data retained by the third party?",
                "No. Per Anthropic's commercial terms, data is not retained "
                "beyond the API request lifecycle.")

        self.qa("Can the AI feature be disabled?",
                "Yes. If the AI Assistant is not used, no data is sent to "
                "Anthropic.")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = SecurityQuestionnaire()
    doc.build()
    doc.output(OUT)
    print(f"Security Questionnaire saved to {OUT}")


if __name__ == "__main__":
    main()
