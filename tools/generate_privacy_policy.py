#!/usr/bin/env python3
"""Generate BMM Privacy Policy PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Privacy_Policy.pdf")

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
TITLE = "PRIVACY POLICY"


class PrivacyPolicy(FPDF):
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

        # --- Section 1: Introduction ---
        self.section(1, "Introduction")
        self.body(
            "Black Mountain Technologies Inc. (\"BMM,\" \"we,\" \"us,\" or \"our\") is a "
            "technology company based in British Columbia, Canada. We operate the BMM "
            "Analytics Construction Project Optimization Suite (the \"Platform\"), a "
            "software-as-a-service platform that helps construction companies analyze "
            "project performance, identify cost savings, and optimize operations.")
        self.body(
            "This Privacy Policy explains how we collect, use, store, and protect "
            "personal information through the Platform. It applies to all users of "
            "the Platform, including administrators, authorized users, and anyone "
            "whose personal information may be contained in data uploaded to the "
            "Platform.")
        self.body(
            "By accessing or using the Platform, you consent to the collection, use, "
            "and disclosure of your information as described in this Privacy Policy. "
            "If you do not agree with this policy, you should not use the Platform.")
        self.body(
            "This policy is designed to comply with the Personal Information "
            "Protection and Electronic Documents Act (PIPEDA) at the federal level, "
            "the Personal Information Protection Act (PIPA) of British Columbia at "
            "the provincial level, and the General Data Protection Regulation (GDPR) "
            "where applicable to individuals in the European Union.")

        # --- Section 2: Information We Collect ---
        self.section(2, "Information We Collect")

        self.body("Account Information")
        self.body(
            "When your organization sets up an account on the Platform, we collect "
            "the following information about authorized users: name, email address, "
            "phone number, company name, and job title. This information is provided "
            "directly by your organization's administrator.")

        self.body("Project Data")
        self.body(
            "The Platform processes construction project data uploaded by your "
            "organization, including budget figures, actual costs, change orders, "
            "schedule tasks, and material orders. This is primarily business data, "
            "not personal data, but it may contain identifying information about "
            "individuals involved in project activities.")

        self.body("Labor and Timecard Data")
        self.body(
            "This is the most sensitive category of data processed by the Platform. "
            "Labor data may include worker names, hours worked, hourly rates, overtime "
            "hours, crew assignments, and cost codes. Under PIPEDA, this information "
            "may constitute personal information when it can be linked to identifiable "
            "individuals.")

        self.body("Usage Data")
        self.body(
            "We automatically collect information about how you interact with the "
            "Platform, including login timestamps, pages visited, features used, and "
            "session duration. This data is collected for platform improvement and "
            "security monitoring purposes.")

        self.body("AI Assistant Queries")
        self.body(
            "When you use the AI Assistant feature, we temporarily process the "
            "questions you type and the responses generated. These interactions are "
            "processed in real-time and are not permanently stored on our servers.")

        self.body("Information We Do Not Collect")
        self.body(
            "We do not collect social insurance numbers, banking information, health "
            "data, biometric data, or any data not directly related to construction "
            "project management.")

        # --- Section 3: How We Use Your Information ---
        self.section(3, "How We Use Your Information")
        self.body(
            "We use the information we collect for the following purposes:")
        self.bullet(
            "To provide the Platform services, including analytics, health scoring, "
            "risk assessments, reporting, and AI-powered responses.")
        self.bullet(
            "To compute project health scores, cost outlier detection, schedule "
            "analysis, and other optimization metrics.")
        self.bullet(
            "To generate anonymized, aggregated benchmarking data for industry "
            "comparisons. Individual records are never shared or identifiable in "
            "benchmarking outputs.")
        self.bullet(
            "To improve Platform performance, reliability, and user experience.")
        self.bullet(
            "To communicate service updates, security notices, and support responses "
            "to authorized users.")
        self.bullet(
            "To comply with applicable legal obligations.")
        self.body(
            "We will NEVER sell personal information to third parties. We will NEVER "
            "use personal information for advertising or marketing to individuals.")

        # --- Section 4: AI Assistant and Third-Party Processing ---
        self.section(4, "AI Assistant and Third-Party Processing")
        self.body(
            "The AI Assistant feature uses Anthropic PBC's Claude API to process "
            "natural language queries about your project data. When you use the AI "
            "Assistant, the following applies:")
        self.sub_clause("a",
            "Project data relevant to your query -- including any personal information "
            "contained in uploaded data -- is sent to Anthropic's API for processing.")
        self.sub_clause("b",
            "Under Anthropic's commercial API terms, your data is NOT used for model "
            "training and is NOT retained beyond the API request lifecycle.")
        self.sub_clause("c",
            "AI queries are processed on Anthropic's servers located in the United "
            "States. This constitutes a cross-border data transfer from Canada to the "
            "United States.")
        self.sub_clause("d",
            "Use of the AI Assistant is optional. If you or your organization's "
            "administrator chooses not to use this feature, no data is sent to "
            "Anthropic. All other Platform features function independently.")
        self.sub_clause("e",
            "BMM does not store AI conversation history on our servers. Conversations "
            "exist only in the user's browser session and are cleared when the session "
            "ends.")

        # --- Section 5: Data Storage and Security ---
        self.section(5, "Data Storage and Security")
        self.body(
            "We take the security of your information seriously and implement "
            "appropriate technical and organizational measures to protect it:")
        self.sub_clause("a",
            "Data is processed within Canada unless the AI Assistant feature is used, "
            "in which case query data is transferred to the United States via "
            "Anthropic's API.")
        self.sub_clause("b",
            "All data in transit is encrypted using TLS 1.2 or higher. Data at rest "
            "is encrypted using AES-256 encryption.")
        self.sub_clause("c",
            "Access to the Platform is protected by role-based access control, "
            "multi-factor authentication, and automated session timeout.")
        self.sub_clause("d",
            "The Platform uses a session-based architecture. Uploaded data exists in "
            "the user's browser session and is not persisted on our servers between "
            "sessions under the current architecture.")
        self.sub_clause("e",
            "We conduct regular security assessments and vulnerability scanning to "
            "identify and address potential risks.")
        self.sub_clause("f",
            "Employee access to personal information is restricted on a strict "
            "need-to-know basis.")

        # --- Section 6: Data Retention ---
        self.section(6, "Data Retention")
        self.body(
            "We retain personal information only as long as necessary to fulfill the "
            "purposes for which it was collected:")
        self.sub_clause("a",
            "Session data: Deleted when the browser session ends. Under the current "
            "architecture, uploaded project data is not persisted between sessions.")
        self.sub_clause("b",
            "Account information: Retained for the duration of the License Agreement "
            "plus thirty (30) days following termination.")
        self.sub_clause("c",
            "Anonymized and aggregated data: Retained indefinitely for benchmarking "
            "purposes. This data cannot be linked back to identifiable individuals.")
        self.sub_clause("d",
            "AI query data: Not retained. Queries are processed in real-time and "
            "discarded immediately after the response is generated.")
        self.sub_clause("e",
            "Upon termination of the License Agreement, all personal data associated "
            "with your account is deleted within thirty (30) days.")

        # --- Section 7: Your Rights ---
        self.section(7, "Your Rights")
        self.body(
            "Under PIPEDA and the BC Personal Information Protection Act (PIPA), "
            "you have the following rights regarding your personal information:")
        self.sub_clause("a",
            "Access your personal information held by us and receive a copy upon "
            "request.")
        self.sub_clause("b",
            "Request correction of any inaccurate or incomplete personal information.")
        self.sub_clause("c",
            "Withdraw your consent to the collection, use, or disclosure of your "
            "personal information, subject to legal or contractual limitations.")
        self.sub_clause("d",
            "Request deletion of your personal information from our systems.")
        self.sub_clause("e",
            "Know what personal information we hold about you and how it is being "
            "used.")
        self.sub_clause("f",
            "File a complaint with the Office of the Privacy Commissioner of Canada "
            "if you believe your privacy rights have been violated.")
        self.body(
            "For individuals located in the European Union (where GDPR applies), you "
            "have additional rights including data portability, restriction of "
            "processing, and the right to object to processing.")
        self.body(
            "To exercise any of these rights, please contact us using the information "
            "provided in Section 11 below. We will respond to all requests within "
            "thirty (30) days.")

        # --- Section 8: Cookies and Tracking ---
        self.section(8, "Cookies and Tracking")
        self.body(
            "The Platform uses essential session cookies that are required for the "
            "Platform to function properly. These cookies maintain your login session "
            "and remember your preferences during a browsing session.")
        self.body(
            "We do not use advertising cookies or third-party tracking technologies. "
            "We do not share browsing data with advertisers or data brokers.")
        self.body(
            "Usage analytics are collected in aggregate form only and cannot be used "
            "to identify individual users.")

        # --- Section 9: Children's Privacy ---
        self.section(9, "Children's Privacy")
        self.body(
            "The Platform is designed exclusively for business use by construction "
            "industry professionals. We do not knowingly collect personal information "
            "from anyone under the age of 18. If we become aware that we have "
            "inadvertently collected information from a minor, we will take steps to "
            "delete that information promptly.")

        # --- Section 10: Changes to This Policy ---
        self.section(10, "Changes to This Policy")
        self.body(
            "We may update this Privacy Policy from time to time to reflect changes "
            "in our practices, the Platform, or applicable laws. When we make material "
            "changes, we will notify the primary contact on file for your organization "
            "via email.")
        self.body(
            "Continued use of the Platform after notification of changes constitutes "
            "your acceptance of the updated Privacy Policy. We encourage you to review "
            "this policy periodically.")

        # --- Section 11: Contact Information ---
        self.section(11, "Contact Information")
        self.body(
            "If you have questions about this Privacy Policy, wish to exercise your "
            "privacy rights, or need to report a privacy concern, please contact us:")
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
        self.ln(2)
        self.body(
            "For privacy inquiries, data access requests, correction requests, or "
            "complaints, please include your name, the organization you are associated "
            "with, and a detailed description of your request. We will acknowledge "
            "receipt of your request within five (5) business days and provide a "
            "substantive response within thirty (30) days.")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = PrivacyPolicy()
    doc.build()
    doc.output(OUT)
    print(f"Privacy Policy saved to {OUT}")


if __name__ == "__main__":
    main()
