#!/usr/bin/env python3
"""Generate BMM Mutual Non-Disclosure Agreement PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Mutual_NDA.pdf")

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
TITLE = "MUTUAL NON-DISCLOSURE AGREEMENT"


class NDA(FPDF):
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

    def party_box(self, label, prefill=""):
        y = self.get_y()
        self.set_fill_color(*LIGHT_BG)
        self.rect(MX, y, CW, 38, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*GREEN)
        self.set_xy(MX + 6, y + 4)
        self.cell(CW - 12, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_TEXT)
        fields = ["Name:", "Title:", "Company:", "Signature:", "Date:"]
        fy = y + 12
        for f in fields:
            self.set_xy(MX + 8, fy)
            if prefill and f == "Company:":
                self.cell(20, 4, f)
                self.cell(60, 4, prefill)
            else:
                self.cell(20, 4, f)
                self.set_draw_color(*GRAY)
                self.line(MX + 30, fy + 4, MX + CW - 10, fy + 4)
            fy += 5
        self.set_y(y + 42)

    def sig_block(self, label, prefill=""):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        fields = ["Name:", "Title:", "Company:", "Signature:", "Date:"]
        for f in fields:
            self.set_x(MX + 4)
            self.set_font("Helvetica", "", 9)
            self.cell(22, 5, f)
            if prefill and f == "Company:":
                self.cell(60, 5, prefill, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                self.set_draw_color(*GRAY)
                self.line(MX + 28, self.get_y() + 5, MX + CW - 10, self.get_y() + 5)
                self.ln(6)

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

        # Date line
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Effective Date: ____________________________",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(6)

        # Party boxes
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 6, "PARTIES TO THIS AGREEMENT", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.party_box("Disclosing Party / Party A", "Black Mountain Technologies Inc.")
        self.ln(4)
        self.party_box("Receiving Party / Party B")

        self.ln(6)
        self.body(
            "This Mutual Non-Disclosure Agreement (\"Agreement\") is entered into as of "
            "the Effective Date written above, by and between the Disclosing Party and "
            "the Receiving Party (collectively, the \"Parties\"), for the purpose of "
            "protecting confidential and proprietary information disclosed in connection "
            "with the evaluation, demonstration, or use of Black Mountain Technologies' "
            "construction project optimization software platform and related services.")

        self._is_cover = False

    def build(self):
        self.cover()

        # --- Section 1: Definitions ---
        self.section(1, "Definition of Confidential Information")
        self.body(
            "\"Confidential Information\" means any and all non-public information "
            "disclosed by either Party to the other Party, whether orally, in writing, "
            "electronically, or by any other means, including but not limited to:")
        items = [
            ("a", "Software source code, object code, algorithms, formulas, data models, "
             "and analytical methodologies related to construction project optimization."),
            ("b", "Dashboard designs, user interface elements, data visualization techniques, "
             "and user experience workflows."),
            ("c", "Business plans, pricing models, client lists, prospect databases, marketing "
             "strategies, and sales methodologies."),
            ("d", "Technical architecture, application programming interfaces (APIs), system "
             "integration methods, and deployment configurations."),
            ("e", "Project optimization models, risk scoring algorithms, schedule analysis logic, "
             "health scoring methodologies, and outlier detection engines."),
            ("f", "Recommendation engines, cost forecasting models, decision support logic, "
             "AI assistant training data, and predictive analytics frameworks."),
            ("g", "Financial projections, cost structures, revenue models, contract terms, "
             "licensing fees, and investment information."),
            ("h", "Any demonstrations, prototypes, beta versions, trial access credentials, "
             "sample data sets, or proof-of-concept materials."),
        ]
        for label, text in items:
            self.sub_clause(label, text)

        # --- Section 2: Obligations ---
        self.section(2, "Obligations of the Receiving Party")
        self.body(
            "The Receiving Party agrees to the following obligations with respect to "
            "all Confidential Information received from the Disclosing Party:")
        obligations = [
            ("a", "Hold all Confidential Information in strict confidence and protect it "
             "using at least the same degree of care used to protect its own confidential "
             "information, but in no event less than reasonable care."),
            ("b", "Use Confidential Information solely for the purpose of evaluating, "
             "testing, or implementing the Disclosing Party's construction project "
             "optimization platform (the \"Permitted Purpose\")."),
            ("c", "Restrict access to Confidential Information to those employees, "
             "contractors, and advisors who have a need to know and who are bound by "
             "confidentiality obligations at least as restrictive as those contained herein."),
            ("d", "Not reverse engineer, decompile, disassemble, or otherwise attempt to "
             "derive the source code, algorithms, or underlying logic of any software, "
             "tools, or systems disclosed as Confidential Information."),
            ("e", "Not copy, reproduce, summarize, or create derivative works based on "
             "Confidential Information without the prior written consent of the "
             "Disclosing Party."),
            ("f", "Immediately notify the Disclosing Party in writing upon discovery of "
             "any unauthorized use, disclosure, or breach of Confidential Information, "
             "and cooperate fully in remediation efforts."),
        ]
        for label, text in obligations:
            self.sub_clause(label, text)

        # --- Section 3: Non-Compete ---
        self.section(3, "Non-Competition and Non-Circumvention")
        self.body(
            "For a period of eighteen (18) months following the termination or "
            "expiration of this Agreement, the Receiving Party shall not:")
        nc_items = [
            ("a", "Develop, design, market, sell, or distribute any software product, "
             "platform, or service that competes with the Disclosing Party's construction "
             "project optimization, construction cost analytics, or construction "
             "schedule/risk analytics offerings, using any knowledge, methodologies, or "
             "techniques gained through access to Confidential Information."),
            ("b", "Solicit, recruit, hire, or engage any employee, contractor, or consultant "
             "of the Disclosing Party who was involved in the development, delivery, or "
             "support of the construction project optimization platform."),
            ("c", "Circumvent the Disclosing Party to contact, solicit, or engage directly "
             "with any client, prospect, partner, or vendor relationship disclosed or "
             "introduced through the Permitted Purpose."),
            ("d", "Use any disclosed methodologies, scoring models, analytical frameworks, "
             "or optimization logic to build, enhance, or inform any competing product "
             "or service in the construction technology sector."),
        ]
        for label, text in nc_items:
            self.sub_clause(label, text)

        # --- Section 4: Exclusions ---
        self.section(4, "Exclusions from Confidential Information")
        self.body(
            "The obligations set forth in this Agreement shall not apply to information that:")
        exclusions = [
            ("a", "Is or becomes publicly available through no fault or action of the "
             "Receiving Party."),
            ("b", "Was already in the Receiving Party's possession prior to disclosure, "
             "as evidenced by written records predating the Effective Date."),
            ("c", "Is independently developed by the Receiving Party without reference to "
             "or use of the Disclosing Party's Confidential Information."),
            ("d", "Is lawfully obtained from a third party who is not under any obligation "
             "of confidentiality with respect to such information."),
            ("e", "Is required to be disclosed by law, regulation, or court order, provided "
             "that the Receiving Party gives the Disclosing Party prompt written notice "
             "and cooperates in seeking a protective order."),
        ]
        for label, text in exclusions:
            self.sub_clause(label, text)

        # --- Section 5: Term ---
        self.section(5, "Term and Termination")
        self.sub_clause("a",
            "This Agreement shall remain in effect for a period of twelve (12) months from "
            "the Effective Date, unless earlier terminated in accordance with this Section.")
        self.sub_clause("b",
            "Either Party may terminate this Agreement at any time by providing thirty "
            "(30) days' prior written notice to the other Party.")
        self.sub_clause("c",
            "Upon termination or expiration, the Receiving Party shall promptly return "
            "or destroy all Confidential Information, including all copies, summaries, "
            "notes, and derivative materials, and shall certify such return or "
            "destruction in writing within ten (10) business days.")
        self.sub_clause("d",
            "The obligations of confidentiality, non-competition, non-circumvention, "
            "and intellectual property ownership shall survive termination or expiration "
            "of this Agreement for the full duration specified in each respective section.")

        # --- Section 6: Remedies ---
        self.section(6, "Remedies and Liquidated Damages")
        self.sub_clause("a",
            "The Parties acknowledge that a breach of this Agreement may cause "
            "irreparable harm to the Disclosing Party that cannot be adequately "
            "compensated by monetary damages alone.")
        self.sub_clause("b",
            "In the event of a breach or threatened breach, the Disclosing Party shall "
            "be entitled to seek injunctive relief, specific performance, and any other "
            "equitable remedies available under applicable law, without the necessity of "
            "posting a bond or proving actual damages.")
        self.sub_clause("c",
            "In addition to equitable remedies, the Parties agree that a material breach "
            "of Sections 1, 2, or 3 of this Agreement shall entitle the non-breaching "
            "Party to liquidated damages in the amount of Five Hundred Thousand Canadian "
            "Dollars (CAD $500,000.00). The Parties agree that this amount represents a "
            "reasonable pre-estimate of the damages likely to be suffered and is not a "
            "penalty.")
        self.sub_clause("d",
            "The prevailing Party in any legal action arising from this Agreement shall "
            "be entitled to recover its reasonable legal fees, court costs, and related "
            "expenses from the non-prevailing Party.")

        # --- Section 7: Ownership ---
        self.section(7, "Ownership and Intellectual Property")
        self.sub_clause("a",
            "All Confidential Information shall remain the sole and exclusive property "
            "of the Disclosing Party. Nothing in this Agreement grants the Receiving "
            "Party any right, title, interest, or license in or to any Confidential "
            "Information, except the limited right to use it for the Permitted Purpose.")
        self.sub_clause("b",
            "No license, whether express or implied, is granted under any patent, "
            "copyright, trademark, trade secret, or other intellectual property right "
            "of the Disclosing Party by virtue of this Agreement or any disclosure "
            "made hereunder.")

        # --- Section 8: General ---
        self.section(8, "General Provisions")
        self.sub_clause("a",
            "Governing Law. This Agreement shall be governed by and construed in "
            "accordance with the laws of the Province of British Columbia, Canada, "
            "without regard to its conflict of laws principles. The Parties submit to "
            "the exclusive jurisdiction of the courts of British Columbia.")
        self.sub_clause("b",
            "Entire Agreement. This Agreement constitutes the entire agreement between "
            "the Parties with respect to the subject matter hereof and supersedes all "
            "prior or contemporaneous oral or written agreements, understandings, and "
            "representations.")
        self.sub_clause("c",
            "Amendments. No amendment, modification, or waiver of any provision of this "
            "Agreement shall be effective unless made in writing and signed by both Parties.")
        self.sub_clause("d",
            "Severability. If any provision of this Agreement is held to be invalid or "
            "unenforceable, the remaining provisions shall continue in full force and "
            "effect, and the invalid provision shall be modified to the minimum extent "
            "necessary to make it enforceable.")
        self.sub_clause("e",
            "No Assignment. Neither Party may assign or transfer this Agreement or any "
            "rights or obligations hereunder without the prior written consent of the "
            "other Party.")
        self.sub_clause("f",
            "No Waiver. The failure of either Party to enforce any provision of this "
            "Agreement shall not constitute a waiver of such provision or the right to "
            "enforce it at a later time.")
        self.sub_clause("g",
            "Audit Rights. The Disclosing Party shall have the right, upon thirty (30) "
            "days' prior written notice, to audit the Receiving Party's compliance with "
            "this Agreement, including inspection of systems and records related to the "
            "handling of Confidential Information.")

        # --- Signatures ---
        self.ln(6)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 7, "IN WITNESS WHEREOF", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.set_x(MX)
        self.multi_cell(CW, 5,
            "The Parties have executed this Mutual Non-Disclosure Agreement as of the "
            "Effective Date first written above.")
        self.ln(4)

        self.sig_block("DISCLOSING PARTY / PARTY A", "Black Mountain Technologies Inc.")
        self.ln(6)
        self.sig_block("RECEIVING PARTY / PARTY B")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = NDA()
    doc.build()
    doc.output(OUT)
    print(f"NDA saved to {OUT}")


if __name__ == "__main__":
    main()
