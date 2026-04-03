#!/usr/bin/env python3
"""Generate BMM Service Level Agreement PDF -- exhibit to the License Agreement."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Service_Level_Agreement.pdf")

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
TITLE = "SERVICE LEVEL AGREEMENT"


class SLA(FPDF):
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

    def section(self, num, title):
        self.ln(4)
        y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(MX, y, 2, 7, "F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 6)
        self.cell(CW - 6, 7, f"{num}. {title}",
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

    def support_table(self):
        """Draw the support response times table."""
        cols = [("Severity", 22), ("Description", 48),
                ("Pilot", 30), ("Growth", 30), ("Enterprise", 36)]
        row_h = 10

        # Header row
        self.set_fill_color(*DARK)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_x(MX)
        for label, w in cols:
            self.cell(w, row_h, label, border=1, fill=True, align="C",
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln(row_h)

        rows = [
            ("Critical",
             "Platform unavailable\nor data loss",
             "4 biz hours", "2 biz hours", "1 biz hour"),
            ("High",
             "Major feature down,\nno workaround",
             "8 biz hours", "4 biz hours", "2 biz hours"),
            ("Medium",
             "Feature impaired,\nworkaround exists",
             "2 biz days", "1 biz day", "4 biz hours"),
            ("Low",
             "Questions, minor\nissues, requests",
             "3 biz days", "2 biz days", "1 biz day"),
        ]

        for i, (sev, desc, pilot, growth, ent) in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(*LIGHT_BG)
            else:
                self.set_fill_color(*WHITE)

            # Calculate row height based on description lines
            rh = 12

            self.set_x(MX)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*DARK_TEXT)
            y_start = self.get_y()

            self.cell(cols[0][1], rh, sev, border=1, fill=True, align="C",
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_font("Helvetica", "", 7)
            x_desc = self.get_x()
            self.multi_cell(cols[1][1], rh / 2, desc, border=1, fill=True,
                            align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_xy(x_desc + cols[1][1], y_start)
            self.set_font("Helvetica", "", 8)
            for val, (_, w) in zip([pilot, growth, ent], cols[2:]):
                self.cell(w, rh, val, border=1, fill=True, align="C",
                          new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.ln(rh)

        self.ln(4)

    def credit_table(self):
        """Draw the service credits table."""
        col_w = CW / 3
        row_h = 8

        self.set_fill_color(*DARK)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_x(MX)
        headers = ["Monthly Uptime", "Credit Amount", "Example"]
        for h in headers:
            self.cell(col_w, row_h, h, border=1, fill=True, align="C",
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln(row_h)

        rows = [
            ("99.0% - 99.5%", "5% of monthly fee", "$5,000/yr = ~$21 credit"),
            ("95.0% - 99.0%", "10% of monthly fee", "$5,000/yr = ~$42 credit"),
            ("Below 95.0%", "25% of monthly fee", "$5,000/yr = ~$104 credit"),
        ]

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_TEXT)
        for i, (uptime, credit, example) in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(*LIGHT_BG)
            else:
                self.set_fill_color(*WHITE)
            self.set_x(MX)
            for val in (uptime, credit, example):
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
        self.set_xy(0, 28)
        self.cell(PW, 10, "SERVICE LEVEL AGREEMENT", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 44)
        self.cell(PW, 6, "Black Mountain Technologies Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 52)
        self.cell(PW, 6, "BMM Analytics Construction Project Optimization Suite",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 60)
        self.cell(PW, 6, "Exhibit to Software License & IP Protection Agreement",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Effective Date: ____________________________",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(6)

        self.body(
            "This Service Level Agreement (\"SLA\") is an exhibit and schedule to "
            "the Software License & IP Protection Agreement (the \"Agreement\") "
            "between Black Mountain Technologies Inc. (\"BMM\") and the Licensee. This SLA "
            "defines the service commitments, support standards, and remedies for "
            "the BMM Analytics Construction Project Optimization Suite (the "
            "\"Platform\"). Capitalized terms not defined herein have the meanings "
            "given in the Agreement.")

        self._is_cover = False

    def build(self):
        self.cover()

        # --- 1. OVERVIEW ---
        self.section(1, "OVERVIEW")
        self.clause("1.1",
            "This SLA defines the service commitments, support standards, and "
            "remedies for the BMM Analytics platform provided by Black Mountain "
            "Media Inc. (\"BMM\") to the Licensee.")
        self.clause("1.2",
            "This SLA applies to all License Tiers (Pilot, Growth, and Enterprise) "
            "as defined in the Agreement. Where service levels differ by tier, "
            "those differences are specified below.")
        self.clause("1.3",
            "This SLA forms part of the Software License & IP Protection Agreement "
            "and is subject to all terms and conditions therein.")

        # --- 2. PLATFORM AVAILABILITY ---
        self.section(2, "PLATFORM AVAILABILITY")
        self.clause("2.1",
            "Uptime Commitment. BMM commits to a monthly platform uptime of "
            "ninety-nine point five percent (99.5%), excluding scheduled "
            "maintenance windows.")
        self.clause("2.2",
            "\"Uptime\" means the Platform is accessible and functional via web "
            "browser for Authorized Users. Uptime is measured as a percentage of "
            "total minutes in a calendar month, excluding scheduled maintenance.")
        self.clause("2.3",
            "Measurement Period. Uptime is calculated on a calendar month basis, "
            "from the first day to the last day of each month.")
        self.clause("2.4",
            "Scheduled Maintenance. Routine maintenance will be performed during "
            "off-peak hours (10:00 PM to 6:00 AM Pacific Time). BMM will provide "
            "at least forty-eight (48) hours advance notice of scheduled "
            "maintenance via email to the Licensee's primary contact.")
        self.clause("2.5",
            "Emergency Maintenance. BMM may perform emergency maintenance without "
            "advance notice when critical security patches or urgent fixes are "
            "required. BMM will notify the Licensee as soon as reasonably possible "
            "after initiating emergency maintenance.")

        # --- 3. SUPPORT RESPONSE TIMES ---
        self.section(3, "SUPPORT RESPONSE TIMES")
        self.body(
            "BMM provides tiered support based on the severity of the issue and "
            "the Licensee's License Tier. Response times are measured from the "
            "time BMM receives a properly submitted support request.")
        self.ln(2)
        self.support_table()

        self.clause("3.1",
            "Business Hours. Support is available Monday through Friday, 8:00 AM "
            "to 6:00 PM Pacific Time, excluding British Columbia statutory "
            "holidays. Response times are measured in business hours or business "
            "days as specified above.")
        self.clause("3.2",
            "Support Channels. Email support is available for all License Tiers. "
            "Phone and video support are available for Growth and Enterprise tiers "
            "only.")
        self.clause("3.3",
            "Enterprise Dedicated Contact. Enterprise tier Licensees are assigned "
            "a dedicated account contact who serves as the primary point of "
            "communication for all support and service matters.")

        # --- 4. SERVICE CREDITS ---
        self.section(4, "SERVICE CREDITS")
        self.body(
            "If monthly uptime falls below 99.5%, the Licensee is entitled to "
            "service credits as follows:")
        self.ln(2)
        self.credit_table()

        self.clause("4.1",
            "Monthly License Fee. For the purpose of calculating service credits, "
            "the monthly license fee equals the total License Fee divided by the "
            "number of months in the License Term.")
        self.clause("4.2",
            "Credit Application. Service credits are applied to future invoices "
            "and are not refunded as cash or any other form of payment.")
        self.clause("4.3",
            "Maximum Credit. The maximum service credit in any single calendar "
            "month shall not exceed twenty-five percent (25%) of the monthly "
            "license fee.")
        self.clause("4.4",
            "Credit Request. Licensee must submit a written request for service "
            "credits within thirty (30) days following the end of the affected "
            "month. Requests submitted after this period will not be honored.")
        self.clause("4.5",
            "Sole Remedy. Service credits are the Licensee's sole and exclusive "
            "remedy for BMM's failure to meet the uptime commitment specified in "
            "Section 2.")

        # --- 5. EXCLUSIONS ---
        self.section(5, "EXCLUSIONS")
        self.body(
            "The uptime calculation and service credit eligibility exclude "
            "downtime or performance issues caused by:")
        self.clause("(a)",
            "Scheduled maintenance windows performed in accordance with "
            "Section 2.4.")
        self.clause("(b)",
            "Force majeure events as defined in the Agreement, including but not "
            "limited to natural disasters, acts of war, pandemics, or government "
            "action.")
        self.clause("(c)",
            "Issues caused by Licensee's equipment, network connectivity, browser "
            "configuration, or internet service provider.")
        self.clause("(d)",
            "Issues caused by Licensee's uploaded data, including corrupt files, "
            "unsupported file formats, or data that does not conform to the "
            "Platform's documented requirements.")
        self.clause("(e)",
            "Third-party service outages beyond BMM's control, including but not "
            "limited to Anthropic API outages (affecting AI Assistant features) "
            "and cloud hosting provider outages.")
        self.clause("(f)",
            "Periods during which Licensee's account is suspended due to "
            "non-payment of License Fees or breach of the Agreement.")

        # --- 6. DATA BACKUP AND RECOVERY ---
        self.section(6, "DATA BACKUP AND RECOVERY")
        self.clause("6.1",
            "Current Architecture. The Platform currently operates on a "
            "session-based architecture where uploaded data exists within the "
            "user's active browser session. Data is not persistently stored on "
            "BMM's servers between sessions.")
        self.clause("6.2",
            "Session Recovery Assistance. BMM will provide reasonable assistance "
            "in data recovery if Platform errors cause data loss or corruption "
            "during an active session.")
        self.clause("6.3",
            "Licensee Responsibility. The Licensee is responsible for maintaining "
            "its own source data files and backups. BMM is not liable for data "
            "loss resulting from session expiration, browser closure, or "
            "Licensee's failure to maintain source files.")
        self.clause("6.4",
            "Future Persistent Storage. When persistent storage features are "
            "implemented, BMM will provide: (i) daily automated backups; "
            "(ii) thirty (30) day backup retention; and (iii) data recovery "
            "within four (4) hours of a recovery request. Licensees will be "
            "notified when persistent storage becomes available.")

        # --- 7. PLATFORM UPDATES ---
        self.section(7, "PLATFORM UPDATES")
        self.clause("7.1",
            "BMM may update the Platform at any time to improve functionality, "
            "performance, or security.")
        self.clause("7.2",
            "Non-Breaking Updates. Updates that do not alter existing data "
            "formats, remove features, or change the Licensee's workflow may be "
            "deployed without advance notice.")
        self.clause("7.3",
            "Breaking Changes. Updates that change data formats, remove existing "
            "features, or materially alter the Platform's behavior will be "
            "communicated to the Licensee with at least fourteen (14) days "
            "advance notice via email.")
        self.clause("7.4",
            "Major Update Notification. The Licensee will be notified of all "
            "major updates, new features, and significant improvements via email "
            "to the primary contact on file.")

        # --- 8. REPORTING ---
        self.section(8, "REPORTING")
        self.clause("8.1",
            "Enterprise Tier. BMM will provide monthly uptime and performance "
            "reports to Enterprise Licensees, including incident summaries and "
            "resolution details.")
        self.clause("8.2",
            "Growth Tier. BMM will provide quarterly uptime reports to Growth "
            "Licensees.")
        self.clause("8.3",
            "Pilot Tier. Uptime and performance reports are available to Pilot "
            "Licensees upon written request.")
        self.clause("8.4",
            "Status Page. Real-time platform status will be made available to "
            "all Licensees when BMM implements a public or authenticated status "
            "page. Licensees will be notified when this resource becomes "
            "available.")

        # --- 9. ESCALATION PROCESS ---
        self.section(9, "ESCALATION PROCESS")
        self.body(
            "Support requests that are not resolved within the initial response "
            "time are escalated as follows:")
        self.clause("9.1",
            "Level 1 -- Support Team. Initial response and troubleshooting per "
            "the severity and response time table in Section 3.")
        self.clause("9.2",
            "Level 2 -- Technical Lead. If the issue remains unresolved within "
            "two times (2x) the initial response time, it is escalated to a "
            "technical lead for advanced diagnosis and resolution.")
        self.clause("9.3",
            "Level 3 -- Management. If the issue remains unresolved within four "
            "times (4x) the initial response time, it is escalated to BMM "
            "management for priority resolution and direct communication with "
            "the Licensee.")
        self.clause("9.4",
            "Enterprise Direct Escalation. Enterprise tier Licensees may request "
            "direct escalation to BMM management at any time, bypassing the "
            "standard escalation process.")

        # --- 10. TERM ---
        self.section(10, "TERM")
        self.clause("10.1",
            "Effective Period. This SLA is effective for the duration of the "
            "License Term as specified in the Agreement and the selected License "
            "Tier.")
        self.clause("10.2",
            "SLA Updates. BMM may update the terms of this SLA with thirty (30) "
            "days written notice to the Licensee. Updates will be communicated "
            "via email to the Licensee's primary contact.")
        self.clause("10.3",
            "Non-Reduction. Changes to this SLA shall not reduce service "
            "commitments, response times, or uptime guarantees during the "
            "current License Term. Any reductions take effect only upon renewal "
            "or execution of a new License Term.")

        # --- SIGNATURES ---
        self.ln(6)
        self.body(
            "IN WITNESS WHEREOF, the Parties have executed this Service Level "
            "Agreement as an exhibit to the Software License & IP Protection "
            "Agreement as of the Effective Date first written above.")
        self.ln(4)
        self.sig_block("BMM -- BLACK MOUNTAIN MEDIA INC.", "Black Mountain Technologies Inc.")
        self.ln(6)
        self.sig_block("LICENSEE")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = SLA()
    doc.build()
    doc.output(OUT)
    print(f"Service Level Agreement saved to {OUT}")


if __name__ == "__main__":
    main()
