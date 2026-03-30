#!/usr/bin/env python3
"""Generate BMM Subprocessor List PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Subprocessor_List.pdf")

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
TITLE = "SUBPROCESSOR LIST"


class SubprocessorList(FPDF):
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
        self.cell(0, 5, f"Page {self.page_no()}  |  Confidential  |  Black Mountain Media",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def section(self, num, title):
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(MX, y, 2, 7, "F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 6)
        self.cell(CW - 6, 7, f"{num}. {title}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.multi_cell(CW, 5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 6)
        self.multi_cell(CW - 6, 4.5, f"- {text}")
        self.ln(0.3)

    # --- pages ---
    def cover(self):
        self.add_page()
        self._is_cover = True

        self.set_fill_color(*DARK)
        self.rect(0, 0, PW, 80, "F")
        self.set_fill_color(*GREEN)
        self.rect(0, 80, PW, 3, "F")

        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*WHITE)
        self.set_xy(0, 28)
        self.cell(PW, 10, "SUBPROCESSOR LIST", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 46)
        self.cell(PW, 6, "Black Mountain Media Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 54)
        self.cell(PW, 6, "Construction Project Optimization Platform", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*LIGHT_BG)
        self.set_xy(0, 66)
        self.cell(PW, 6, "Third-Party Data Processing Disclosure",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Last Updated: March 2026",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(MX, 103)
        self.cell(CW, 6, "Contact: michael@blackmountainmedias.ca",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(MX, 111)
        self.cell(CW, 6, "Black Mountain Media Inc., British Columbia, Canada",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def content_pages(self):
        self._is_cover = False
        self.add_page()

        # 1. PURPOSE
        self.section(1, "PURPOSE")
        self.bullet(
            "This document lists all third-party subprocessors engaged by "
            "Black Mountain Media Inc. to process customer data in connection "
            "with the BMM Analytics Construction Project Optimization Suite."
        )
        self.bullet(
            "Maintained in accordance with the Data Processing Addendum."
        )
        self.bullet(
            "Updated as subprocessors are added or removed."
        )

        # 2. NOTIFICATION OF CHANGES
        self.section(2, "NOTIFICATION OF CHANGES")
        self.bullet(
            "BMM will notify customers at least 30 days before engaging "
            "a new subprocessor."
        )
        self.bullet(
            "Notification sent via email to the primary contact on file."
        )
        self.bullet(
            "Customers may object within 14 days of notification per the "
            "terms of the DPA."
        )
        self.bullet(
            "If an objection cannot be resolved, the customer may terminate "
            "the License Agreement."
        )

        # 3. CURRENT SUBPROCESSORS (table)
        self.section(3, "CURRENT SUBPROCESSORS")

        cols = [
            ("Subprocessor", 32),
            ("Purpose", 34),
            ("Data Processed", 42),
            ("Location", 28),
            ("Security", 30),
        ]
        col_widths = [c[1] for c in cols]
        col_headers = [c[0] for c in cols]

        # Table header
        self.set_font("Helvetica", "B", 7)
        self.set_fill_color(*DARK)
        self.set_text_color(*WHITE)
        x = MX
        for i, hdr in enumerate(col_headers):
            self.set_xy(x, self.get_y())
            self.cell(col_widths[i], 6, hdr, border=1, fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += col_widths[i]
        self.ln(6)

        rows = [
            [
                "Anthropic PBC",
                "AI Assistant query processing",
                "Project data included in AI queries (budgets, actuals, "
                "schedules, labor data, materials, change orders as "
                "uploaded by user)",
                "United States",
                "SOC 2 Type II",
            ],
            [
                "Streamlit (Snowflake Inc.)",
                "Application hosting framework",
                "Session data, uploaded files during active sessions",
                "United States / Canada (depends on deployment)",
                "SOC 2 Type II (Snowflake)",
            ],
            [
                "GitHub (Microsoft)",
                "Source code repository and CI/CD",
                "Application source code only -- no customer data",
                "United States",
                "SOC 2 Type II, ISO 27001",
            ],
        ]

        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DARK_TEXT)

        for row_idx, row in enumerate(rows):
            bg = LIGHT_BG if row_idx % 2 == 0 else WHITE
            self.set_fill_color(*bg)
            y_start = self.get_y()
            # Calculate max height for this row
            max_h = 0
            for i, val in enumerate(row):
                # Estimate lines needed
                nlines = self.multi_cell(col_widths[i], 4, val,
                                         dry_run=True, output="LINES")
                h = len(nlines) * 4
                if h > max_h:
                    max_h = h
            # Draw cells
            for i, val in enumerate(row):
                x = MX + sum(col_widths[:i])
                self.set_xy(x, y_start)
                self.rect(x, y_start, col_widths[i], max_h, "F")
                self.set_draw_color(*GRAY)
                self.rect(x, y_start, col_widths[i], max_h, "D")
                self.set_xy(x + 1, y_start + 0.5)
                self.multi_cell(col_widths[i] - 2, 4, val)
            self.set_y(y_start + max_h)

        self.ln(2)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.set_x(MX)
        self.multi_cell(CW, 4,
            "Note: For self-hosted or Streamlit Cloud deployments, the "
            "specific cloud infrastructure provider may vary. BMM will "
            "confirm the hosting subprocessor at the time of deployment."
        )
        self.ln(1)

        # 4. DATA FLOW SUMMARY
        self.section(4, "DATA FLOW SUMMARY")
        self.bullet(
            "Customer uploads data via browser to the BMM Analytics "
            "platform (hosted on Streamlit)."
        )
        self.bullet(
            "Data is processed locally within the application session "
            "for analytics, scoring, and reporting."
        )
        self.bullet(
            "If the AI Assistant is used, relevant project data is sent "
            "to Anthropic's API for query processing and the response is "
            "returned to the user's session."
        )
        self.bullet(
            "No customer data is stored in GitHub -- only application "
            "source code."
        )
        self.bullet(
            "Session data is not persisted between browser sessions in "
            "the current architecture."
        )

        # 5. PREVIOUS SUBPROCESSORS
        self.section(5, "PREVIOUS SUBPROCESSORS")
        self.bullet("None to date (platform launched March 2026).")

        # 6. CONTACT
        self.section(6, "CONTACT")
        self.bullet(
            "For questions about subprocessors: "
            "michael@blackmountainmedias.ca"
        )
        self.bullet(
            "To request notification of subprocessor changes: "
            "michael@blackmountainmedias.ca"
        )
        self.bullet(
            "Black Mountain Media Inc., British Columbia, Canada"
        )


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = SubprocessorList()
    pdf.cover()
    pdf.content_pages()
    pdf.output(OUT)
    print(f"Saved to {OUT}")


if __name__ == "__main__":
    main()
