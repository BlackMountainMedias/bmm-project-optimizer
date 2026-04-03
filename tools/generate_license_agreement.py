#!/usr/bin/env python3
"""Generate BMM Software License & IP Protection Agreement PDF -- 3 tiers."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_License_Agreement.pdf")

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
TITLE = "SOFTWARE LICENSE & IP PROTECTION AGREEMENT"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV"]


class License(FPDF):
    def __init__(self):
        super().__init__(orientation="P", format="letter")
        self.set_auto_page_break(auto=True, margin=25)
        self._is_cover = True

    def _dark_header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, PW, 18, "F")
        self.set_fill_color(*GREEN)
        self.rect(0, 18, PW, 1.5, "F")
        self.set_font("Helvetica", "B", 8)
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

    def article(self, num, title):
        self.ln(4)
        y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(MX, y, 2, 7, "F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 6)
        self.cell(CW - 6, 7, f"ARTICLE {ROMAN[num - 1]}. {title}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.multi_cell(CW, 5, text)
        self.ln(1)

    def clause(self, label, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 8)
        self.multi_cell(CW - 8, 5, f"{label} {text}")
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

    def checkbox_line(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 12)
        y = self.get_y()
        self.set_draw_color(*DARK_TEXT)
        self.set_line_width(0.3)
        self.rect(MX + 12, y, 4, 4)
        self.set_x(MX + 20)
        self.multi_cell(CW - 20, 5, text)
        self.ln(1)

    def tier_table(self):
        """Draw the 3-tier comparison table."""
        col_w = CW / 4
        row_h = 8

        # Header row
        self.set_fill_color(*DARK)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        headers = ["", "Pilot", "Growth", "Enterprise"]
        self.set_x(MX)
        for h in headers:
            self.cell(col_w, row_h, h, border=1, fill=True, align="C",
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln(row_h)

        # Data rows
        rows = [
            ("License Fee", "CAD $5,000", "CAD $30,000", "CAD $125,000"),
            ("Projects", "1 project", "Up to 3 projects", "Unlimited"),
            ("Term", "60 days", "6 months", "12 months"),
            ("Performance Guarantee", "2% in 60 days", "2% in 60 days", "2% in 60 days"),
            ("AI Assistant", "No", "Yes", "Yes"),
            ("Dedicated Support", "Email only", "Email + calls", "Priority support"),
            ("Data Export", "Yes", "Yes", "Yes"),
        ]

        for i, (label, c1, c2, c3) in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(*LIGHT_BG)
            else:
                self.set_fill_color(*WHITE)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DARK_TEXT)
            self.set_x(MX)
            self.cell(col_w, row_h, label, border=1, fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_font("Helvetica", "", 9)
            for val in (c1, c2, c3):
                self.cell(col_w, row_h, val, border=1, fill=True, align="C",
                          new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.ln(row_h)
        self.ln(4)

    # --- pages ---
    def cover(self):
        self.add_page()
        self._is_cover = True

        self.set_fill_color(*DARK)
        self.rect(0, 0, PW, 80, "F")
        self.set_fill_color(*GREEN)
        self.rect(0, 80, PW, 3, "F")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*WHITE)
        self.set_xy(0, 22)
        self.cell(PW, 10, "SOFTWARE LICENSE &", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 34)
        self.cell(PW, 10, "IP PROTECTION AGREEMENT", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 50)
        self.cell(PW, 6, "Black Mountain Technologies Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 58)
        self.cell(PW, 6, "Construction Project Optimization Platform", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Effective Date: ____________________________",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(6)

        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 6, "PARTIES TO THIS AGREEMENT", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.party_box("Licensor", "Black Mountain Technologies Inc.")
        self.ln(4)
        self.party_box("Licensee")

        self.ln(6)
        self.body(
            "This Software License and Intellectual Property Protection Agreement "
            "(\"Agreement\") is entered into as of the Effective Date written above, by "
            "and between the Licensor and the Licensee (collectively, the \"Parties\"), "
            "for the licensing and use of Black Mountain Technologies' construction project "
            "optimization software platform and related services, subject to the terms "
            "and conditions set forth herein.")

        self._is_cover = False

    def build(self):
        self.cover()

        # --- ARTICLE I: Definitions ---
        self.article(1, "DEFINITIONS")
        defs = [
            ("1.1", "\"Software\" means the BMM Analytics Construction Project Optimization "
             "Suite, including but not limited to: project dashboards, portfolio analytics "
             "engines, health and risk scoring modules, cost forecasting systems, AI "
             "assistant interfaces, automated report generators, data ingestion and "
             "transformation pipelines, outlier detection engines, schedule analysis tools, "
             "and all related documentation, updates, and enhancements."),
            ("1.2", "\"Intellectual Property\" or \"IP\" means all patents, copyrights, "
             "trademarks, trade secrets, algorithms, source code, object code, data models, "
             "methodologies, processes, designs, and any other proprietary rights in or "
             "related to the Software."),
            ("1.3", "\"Confidential Information\" means any non-public information disclosed "
             "by either Party, including the Software, its functionality, pricing, business "
             "strategies, client data, and technical architecture."),
            ("1.4", "\"License Tier\" means the service level selected by the Licensee as "
             "defined in Article V (Pilot, Growth, or Enterprise). The License Term, Fee, "
             "and project scope are determined by the selected tier."),
            ("1.5", "\"Authorized Users\" means those employees and contractors of the "
             "Licensee designated in Exhibit A who are authorized to access and use the "
             "Software."),
        ]
        for label, text in defs:
            self.clause(label, text)

        # --- ARTICLE II: License Grant ---
        self.article(2, "LICENSE GRANT")
        self.clause("2.1",
            "Subject to the terms of this Agreement and payment of the applicable License "
            "Fee, Licensor grants Licensee a non-exclusive, non-transferable, revocable "
            "license to access and use the Software during the License Term for Licensee's "
            "internal business operations, limited to the number of projects specified by "
            "the selected License Tier.")
        self.clause("2.2",
            "The Software is delivered as a Software-as-a-Service (SaaS) platform "
            "accessible via web browser. No source code, executable files, or downloadable "
            "software components shall be provided to the Licensee.")
        self.body("Licensee shall not:")
        restrictions = [
            ("(a)", "Copy, reproduce, or duplicate any part of the Software."),
            ("(b)", "Reverse engineer, decompile, disassemble, or attempt to derive the "
             "source code, algorithms, or underlying logic of the Software."),
            ("(c)", "Sublicense, rent, lease, loan, or transfer access to the Software to "
             "any third party."),
            ("(d)", "Use automated tools to scrape, extract, or harvest data from the "
             "Software platform."),
            ("(e)", "Use the Software, or knowledge gained from it, to develop, enhance, "
             "or inform any competing product or service."),
        ]
        for label, text in restrictions:
            self.clause(label, text)
        self.clause("2.3", "All rights not expressly granted herein are reserved by the Licensor.")

        # --- ARTICLE III: IP Ownership ---
        self.article(3, "IP OWNERSHIP AND PROTECTION")
        self.clause("3.1",
            "The Software, including all modifications, improvements, derivative works, "
            "and enhancements (whether suggested by Licensee or not), shall remain the "
            "sole and exclusive property of the Licensor. No title or ownership interest "
            "in or to the Software or any IP is transferred to the Licensee under this "
            "Agreement.")
        self.clause("3.2",
            "Any feedback, suggestions, enhancement requests, or recommendations provided "
            "by Licensee regarding the Software shall become the property of the Licensor, "
            "and Licensor shall have an unrestricted right to use, incorporate, and "
            "commercialize such feedback without obligation or compensation to Licensee.")
        self.clause("3.3",
            "Licensee retains all rights in and to its own data uploaded to the Software. "
            "Licensor may use anonymized and aggregated data derived from Licensee's usage "
            "for benchmarking, product improvement, and industry analysis purposes.")
        self.clause("3.4",
            "Licensee acknowledges that the Software contains valuable trade secrets of "
            "the Licensor, and agrees to treat the Software and all related information "
            "as Confidential Information under the terms of this Agreement.")

        # --- ARTICLE IV: Non-Competition ---
        self.article(4, "NON-COMPETITION AND NON-CIRCUMVENTION")
        self.clause("4.1",
            "For a period of eighteen (18) months following the termination or expiration "
            "of this Agreement, Licensee shall not directly or indirectly develop, design, "
            "market, sell, license, or distribute any software product, platform, tool, or "
            "service that competes with the Licensor's offerings in the following areas:")
        self.clause("(a)", "Construction project optimization software.")
        self.clause("(b)", "Construction cost analytics platforms.")
        self.clause("(c)", "Construction schedule and risk analytics software.")
        self.clause("4.2",
            "Licensee shall not solicit, recruit, hire, or engage any employee, contractor, "
            "or consultant of the Licensor for a period of eighteen (18) months following "
            "termination.")
        self.clause("4.3",
            "Licensee shall not brief, advise, consult with, or provide information to any "
            "competitor of the Licensor regarding the Software's functionality, architecture, "
            "methodologies, pricing, or business strategy.")

        # --- ARTICLE V: License Tiers & Payment ---
        self.article(5, "LICENSE TIERS AND PAYMENT TERMS")
        self.body(
            "Licensee shall select one of the following License Tiers. The selected tier "
            "determines the License Fee, License Term, and project scope for this Agreement.")
        self.ln(2)
        self.tier_table()

        self.body("Select one License Tier:")
        self.ln(1)
        self.checkbox_line(
            "PILOT -- CAD $5,000. One (1) project. Sixty (60) day term. Full dashboard "
            "and analytics access for a single project. Email support. No AI Assistant. "
            "Payment due in full within thirty (30) days of the Effective Date.")
        self.checkbox_line(
            "GROWTH -- CAD $30,000. Up to three (3) projects. Six (6) month term. Full "
            "dashboard, analytics, and AI Assistant access. Email and phone support. "
            "Payment due in full within thirty (30) days of the Effective Date, OR split "
            "payment: CAD $15,000 due within thirty (30) days, remaining CAD $15,000 due "
            "at the three (3) month milestone.")
        self.checkbox_line(
            "ENTERPRISE -- CAD $125,000. Unlimited projects. Twelve (12) month term. Full "
            "platform access including AI Assistant and priority support. Two payment "
            "options: (A) Full payment of CAD $125,000 within thirty (30) days, OR "
            "(B) CAD $62,500 due within thirty (30) days, with the remaining CAD $62,500 "
            "due at the six (6) month milestone. Under Option B, if the Performance "
            "Guarantee in Article VI is not met, Licensee receives a full refund of the "
            "initial payment.")
        self.ln(1)
        self.clause("5.2",
            "Late Payment. Any amount not paid when due shall accrue interest at a rate "
            "of one and one-half percent (1.5%) per month, compounded monthly, until paid "
            "in full.")
        self.clause("5.3",
            "Taxes. All License Fees are exclusive of applicable taxes. Licensee shall be "
            "responsible for all Goods and Services Tax (GST), Harmonized Sales Tax (HST), "
            "and any other taxes or duties imposed by any governmental authority in "
            "connection with this Agreement.")
        self.clause("5.4",
            "Tier Upgrade. Licensee may upgrade to a higher License Tier at any time during "
            "the License Term by paying the difference between the current tier fee and the "
            "new tier fee, prorated for the remaining term.")

        # --- ARTICLE VI: Performance Guarantee ---
        self.article(6, "PERFORMANCE GUARANTEE")
        self.clause("6.1",
            "Licensor guarantees that, within sixty (60) days of receiving sufficient "
            "historical project data from Licensee, the Software will identify cost "
            "improvement opportunities representing at least two percent (2%) of total "
            "project costs analyzed. This guarantee applies to all License Tiers.")
        self.clause("6.2",
            "If the Software fails to identify such opportunities within the specified "
            "period, Licensee shall be entitled to a full refund of all License Fees "
            "paid to date.")
        self.clause("6.3",
            "The Performance Guarantee is contingent upon Licensee providing at least "
            "six (6) months of historical project data (including budget, actuals, and "
            "at least two additional data types) within fourteen (14) business days of "
            "the Effective Date. Failure to provide adequate data within this timeframe "
            "shall void the Performance Guarantee.")

        # --- ARTICLE VII: Confidentiality ---
        self.article(7, "CONFIDENTIALITY")
        self.clause("7.1",
            "Each Party shall hold the other Party's Confidential Information in strict "
            "confidence and shall not disclose it to any third party without the prior "
            "written consent of the disclosing Party.")
        self.clause("7.2",
            "Each Party shall protect Confidential Information using at least the same "
            "degree of care it uses to protect its own confidential information, but in "
            "no event less than reasonable care.")
        self.clause("7.3",
            "The obligations of confidentiality under this Article shall survive "
            "termination or expiration of this Agreement for a period of five (5) years.")
        self.clause("7.4",
            "Upon termination, each Party shall return or destroy all Confidential "
            "Information of the other Party within ten (10) business days and certify "
            "such return or destruction in writing.")

        # --- ARTICLE VIII: Term and Termination ---
        self.article(8, "TERM AND TERMINATION")
        self.clause("8.1",
            "This Agreement shall commence on the Effective Date and continue for the "
            "License Term specified by the selected License Tier (60 days for Pilot, "
            "6 months for Growth, 12 months for Enterprise), unless earlier terminated.")
        self.clause("8.2",
            "Termination for Cause. Either Party may terminate this Agreement if the "
            "other Party materially breaches any provision and fails to cure such breach "
            "within thirty (30) days of receiving written notice.")
        self.clause("8.3",
            "Termination for Convenience. Either Party may terminate this Agreement for "
            "any reason by providing sixty (60) days' prior written notice. In the event "
            "of termination for convenience by the Licensee, no refund of License Fees "
            "paid shall be due.")
        self.clause("8.4", "Effect of Termination. Upon termination or expiration:")
        self.clause("(a)",
            "Licensee's access to the Software shall be revoked immediately.")
        self.clause("(b)",
            "Licensee shall have thirty (30) days to export its own data from the "
            "platform. After such period, Licensor may delete all Licensee data.")
        self.clause("(c)",
            "The provisions of Articles III (IP Ownership), IV (Non-Competition), "
            "VII (Confidentiality), and IX (Remedies) shall survive termination.")

        # --- ARTICLE IX: Remedies ---
        self.article(9, "REMEDIES AND LIQUIDATED DAMAGES")
        self.clause("9.1",
            "The Parties acknowledge that a breach of the IP, non-competition, or "
            "confidentiality provisions of this Agreement would cause irreparable harm "
            "that cannot be adequately compensated by monetary damages.")
        self.clause("9.2",
            "In the event of a breach or threatened breach, the non-breaching Party shall "
            "be entitled to seek injunctive relief and specific performance without the "
            "necessity of posting a bond or proving actual damages.")
        self.clause("9.3",
            "In addition to equitable remedies, a material breach of Articles III, IV, "
            "or VII shall entitle the non-breaching Party to liquidated damages in the "
            "amount of Five Hundred Thousand Canadian Dollars (CAD $500,000.00). The "
            "Parties agree that this amount represents a reasonable pre-estimate of the "
            "damages likely to be suffered and is not a penalty. This liquidated damages "
            "provision applies regardless of the License Tier selected.")
        self.clause("9.4",
            "The non-breaching Party shall be entitled to disgorgement of any profits "
            "derived by the breaching Party from the unauthorized use of Confidential "
            "Information or Intellectual Property.")
        self.clause("9.5",
            "The prevailing Party in any legal action arising from this Agreement shall "
            "be entitled to recover its reasonable legal fees, court costs, expert "
            "witness fees, and related expenses from the non-prevailing Party.")

        # --- ARTICLE X: Limitation of Liability ---
        self.article(10, "LIMITATION OF LIABILITY")
        self.clause("10.1",
            "Except for breaches of Articles III (IP Ownership), IV (Non-Competition), "
            "and VII (Confidentiality), the total aggregate liability of either Party "
            "under this Agreement shall not exceed the total License Fees paid or payable "
            "by Licensee during the License Term.")
        self.clause("10.2",
            "Liability for breaches of Articles III, IV, and VII shall be uncapped.")
        self.clause("10.3",
            "Neither Party shall be liable for any indirect, incidental, special, "
            "consequential, or punitive damages, except in cases of willful misconduct "
            "or intentional breach of this Agreement.")

        # --- ARTICLE XI: General Provisions ---
        self.article(11, "GENERAL PROVISIONS")
        self.clause("11.1",
            "Governing Law. This Agreement shall be governed by and construed in accordance "
            "with the laws of the Province of British Columbia, Canada. The Parties submit "
            "to the exclusive jurisdiction of the courts of British Columbia.")
        self.clause("11.2",
            "Entire Agreement. This Agreement, including all Exhibits, constitutes the "
            "entire agreement between the Parties and supersedes all prior agreements and "
            "understandings.")
        self.clause("11.3",
            "Amendments. No amendment or modification shall be effective unless made in "
            "writing and signed by both Parties.")
        self.clause("11.4",
            "Severability. If any provision is held invalid, the remaining provisions shall "
            "continue in full force and the invalid provision shall be modified to the "
            "minimum extent necessary to make it enforceable.")
        self.clause("11.5",
            "No Assignment. Licensee may not assign or transfer this Agreement without the "
            "prior written consent of the Licensor.")
        self.clause("11.6",
            "Force Majeure. Neither Party shall be liable for failure to perform due to "
            "causes beyond its reasonable control, including acts of God, war, terrorism, "
            "pandemic, government action, or natural disaster.")
        self.clause("11.7",
            "Notices. All notices under this Agreement shall be in writing and delivered "
            "by email with read receipt, registered mail, or recognized courier service "
            "to the addresses specified in Exhibit A.")
        self.clause("11.8",
            "Independent Contractors. The Parties are independent contractors. Nothing in "
            "this Agreement creates a partnership, joint venture, agency, or employment "
            "relationship.")
        self.clause("11.9",
            "Audit Rights. Licensor shall have the right, upon reasonable notice and no "
            "more than once per calendar year, to audit Licensee's use of the Software "
            "to verify compliance with this Agreement.")

        # --- ARTICLE XII: Exhibit A ---
        self.article(12, "EXHIBIT A -- LICENSEE INFORMATION")
        self.body("Please complete the following information:")
        self.ln(2)
        fields = [
            "Company Name: ___________________________________________",
            "Primary Contact Name: ____________________________________",
            "Primary Contact Email: ____________________________________",
            "Primary Contact Phone: ____________________________________",
            "Number of Authorized Users: _______________________________",
            "License Tier Selected:  [ ] Pilot   [ ] Growth   [ ] Enterprise",
            "License Term Start Date: __________________________________",
            "License Term End Date: ____________________________________",
        ]
        for f in fields:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*DARK_TEXT)
            self.set_x(MX + 4)
            self.cell(CW - 4, 8, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(4)
        self.body("For Enterprise Tier only -- select payment option:")
        self.set_x(MX + 4)
        self.set_font("Helvetica", "", 10)
        self.cell(CW - 4, 8,
                  "Payment Option:  [ ] Option A (Full)   [ ] Option B (Split)",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # --- ARTICLE XIII: Signatures ---
        self.article(13, "SIGNATURES")
        self.body(
            "IN WITNESS WHEREOF, the Parties have executed this Software License and "
            "Intellectual Property Protection Agreement as of the Effective Date first "
            "written above.")
        self.ln(2)
        self.sig_block("LICENSOR", "Black Mountain Technologies Inc.")
        self.ln(6)
        self.sig_block("LICENSEE")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = License()
    doc.build()
    doc.output(OUT)
    print(f"License Agreement saved to {OUT}")


if __name__ == "__main__":
    main()
