#!/usr/bin/env python3
"""Generate BMM Terms of Service PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Terms_of_Service.pdf")

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
TITLE = "TERMS OF SERVICE"


class TermsOfService(FPDF):
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
        self.cell(PW, 6, "BMM Analytics Construction Project Optimization Suite", align="C",
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

        # --- Section 1: Acceptance of Terms ---
        self.section(1, "ACCEPTANCE OF TERMS")
        self.bullet(
            "By accessing or using the BMM Analytics platform, you agree to "
            "these Terms of Service.")
        self.bullet(
            "If you do not agree, do not use the platform.")
        self.bullet(
            "These Terms apply to all users, including Authorized Users under "
            "a License Agreement.")
        self.bullet(
            "BMM reserves the right to update these Terms with 30 days notice.")

        # --- Section 2: Account Responsibilities ---
        self.section(2, "ACCOUNT RESPONSIBILITIES")
        self.bullet(
            "You are responsible for maintaining the confidentiality of your "
            "login credentials.")
        self.bullet(
            "You must not share your account or credentials with unauthorized "
            "persons.")
        self.bullet(
            "You must notify BMM immediately of any unauthorized use of your "
            "account.")
        self.bullet(
            "You are responsible for all activity under your account.")
        self.bullet(
            "BMM may suspend or terminate accounts that violate these Terms.")

        # --- Section 3: Permitted Use ---
        self.section(3, "PERMITTED USE")
        self.bullet(
            "You may use the platform solely for your organization's internal "
            "business purposes related to construction project management.")
        self.bullet(
            "You may upload, view, analyze, and export your organization's "
            "project data.")
        self.bullet(
            "You may use the AI Assistant to ask questions about your project "
            "data and general construction management topics.")
        self.bullet(
            "You must comply with all applicable laws and regulations in your "
            "use of the platform.")

        # --- Section 4: Prohibited Conduct ---
        self.section(4, "PROHIBITED CONDUCT")
        self.body("Users shall not:")
        self.sub_clause("a",
            "Share login credentials with anyone not designated as an "
            "Authorized User.")
        self.sub_clause("b",
            "Attempt to access data belonging to other organizations or users.")
        self.sub_clause("c",
            "Upload files containing malware, viruses, or malicious code.")
        self.sub_clause("d",
            "Use automated bots, scrapers, or crawlers to extract data from "
            "the platform.")
        self.sub_clause("e",
            "Reverse engineer, decompile, or attempt to derive source code "
            "from the platform.")
        self.sub_clause("f",
            "Use the platform to develop, train, or improve competing products "
            "or services.")
        self.sub_clause("g",
            "Circumvent or disable any security features of the platform.")
        self.sub_clause("h",
            "Upload data you do not have the right to use or share.")
        self.sub_clause("i",
            "Use the AI Assistant to attempt to extract system prompts, "
            "training data, or proprietary logic.")
        self.sub_clause("j",
            "Intentionally overload the platform or interfere with other "
            "users' access.")
        self.sub_clause("k",
            "Resell, sublicense, or commercially redistribute any platform "
            "output.")
        self.sub_clause("l",
            "Use the platform for any unlawful purpose.")

        # --- Section 5: Intellectual Property ---
        self.section(5, "INTELLECTUAL PROPERTY")
        self.bullet(
            "The platform, including all software, algorithms, designs, and "
            "content, is the property of Black Mountain Media Inc.")
        self.bullet(
            "Nothing in these Terms grants you ownership of any BMM "
            "intellectual property.")
        self.bullet(
            "You retain ownership of data you upload to the platform.")
        self.bullet(
            "Platform outputs (charts, scores, reports, AI responses) are "
            "generated using BMM's proprietary algorithms and are provided "
            "for your internal use only.")
        self.bullet(
            "You may not claim BMM's analytics methodology, scoring logic, "
            "or AI capabilities as your own.")

        # --- Section 6: AI Assistant Terms ---
        self.section(6, "AI ASSISTANT TERMS")
        self.bullet(
            "The AI Assistant provides informational responses based on your "
            "uploaded data and general knowledge.")
        self.bullet(
            "AI responses are not professional advice (legal, financial, "
            "engineering, or otherwise).")
        self.bullet(
            "You should verify AI-generated insights before making business "
            "decisions.")
        self.bullet(
            "AI queries send your project data to Anthropic's API for "
            "processing; by using the AI Assistant, you consent to this "
            "data transfer.")
        self.bullet(
            "BMM is not responsible for the accuracy or completeness of "
            "AI-generated responses.")
        self.bullet(
            "AI conversation history exists only in your browser session "
            "and is not stored server-side.")

        # --- Section 7: Data and Content ---
        self.section(7, "DATA AND CONTENT")
        self.bullet(
            "You are solely responsible for the accuracy and legality of "
            "data you upload.")
        self.bullet(
            "You represent that you have all necessary rights and consents "
            "to upload any data, including any personal information of "
            "employees or contractors.")
        self.bullet(
            "BMM processes uploaded data as described in the Privacy Policy "
            "and Data Processing Addendum.")
        self.bullet(
            "Session-based data is not persisted between sessions -- you are "
            "responsible for maintaining your source files.")

        # --- Section 8: Disclaimer of Warranties ---
        self.section(8, "DISCLAIMER OF WARRANTIES")
        self.bullet(
            "The platform is provided \"as is\" and \"as available\" without "
            "warranties of any kind.")
        self.bullet(
            "BMM does not warrant that the platform will be uninterrupted, "
            "error-free, or completely secure.")
        self.bullet(
            "BMM does not warrant the accuracy of analytics, scores, or "
            "AI responses.")
        self.bullet(
            "The Performance Guarantee (if applicable) is governed by the "
            "License Agreement, not these Terms.")

        # --- Section 9: Limitation of Liability ---
        self.section(9, "LIMITATION OF LIABILITY")
        self.bullet(
            "To the maximum extent permitted by law, BMM shall not be liable "
            "for any indirect, incidental, special, consequential, or punitive "
            "damages arising from your use of the platform.")
        self.bullet(
            "BMM's total liability shall not exceed the fees paid by your "
            "organization under the License Agreement.")
        self.bullet(
            "This limitation does not apply to BMM's willful misconduct.")

        # --- Section 10: Termination ---
        self.section(10, "TERMINATION")
        self.bullet(
            "BMM may suspend or terminate your access immediately if you "
            "violate these Terms.")
        self.bullet(
            "Upon termination of the underlying License Agreement, your "
            "access to the platform ends.")
        self.bullet(
            "Sections on intellectual property, limitation of liability, "
            "and governing law survive termination.")

        # --- Section 11: Governing Law ---
        self.section(11, "GOVERNING LAW")
        self.bullet(
            "These Terms are governed by the laws of British Columbia, Canada.")
        self.bullet(
            "Disputes shall be resolved in the courts of British Columbia.")

        # --- Section 12: Contact ---
        self.section(12, "CONTACT")
        self.body(
            "Questions about these Terms: michael@blackmountainmedias.ca")
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.cell(CW - 8, 5, "Black Mountain Media Inc.",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.set_x(MX + 8)
        self.cell(CW - 8, 5, "British Columbia, Canada",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = TermsOfService()
    doc.build()
    doc.output(OUT)
    print(f"Terms of Service saved to {OUT}")


if __name__ == "__main__":
    main()
