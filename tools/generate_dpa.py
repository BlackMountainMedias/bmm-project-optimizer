#!/usr/bin/env python3
"""Generate BMM Data Processing Addendum PDF."""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp",
                   "BMM_Data_Processing_Addendum.pdf")

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
TITLE = "DATA PROCESSING ADDENDUM"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV"]


class DPA(FPDF):
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

    def exhibit_category(self, title, measures):
        """Render an exhibit category with bullet-point measures."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX + 4)
        self.cell(CW - 4, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        for m in measures:
            self.set_x(MX + 10)
            self.multi_cell(CW - 10, 5, f"- {m}")
            self.ln(0.5)
        self.ln(2)

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
        self.set_xy(0, 22)
        self.cell(PW, 10, "DATA PROCESSING", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 34)
        self.cell(PW, 10, "ADDENDUM", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 50)
        self.cell(PW, 6, "Black Mountain Technologies Inc.", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(0, 58)
        self.cell(PW, 6, "Construction Project Optimization Platform", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*LIGHT_BG)
        self.set_xy(0, 68)
        self.cell(PW, 6, "Addendum to the Software License & IP Protection Agreement",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(MX, 95)
        self.cell(CW, 6, "Effective Date: ____________________________",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(6)

        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK_TEXT)
        self.set_x(MX)
        self.cell(CW, 6, "PARTIES TO THIS ADDENDUM",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.party_box("Data Controller (Licensee)")
        self.ln(4)
        self.party_box("Data Processor (Licensor)", "Black Mountain Technologies Inc.")

        self.ln(6)
        self.body(
            "This Data Processing Addendum (\"DPA\") is entered into as of the "
            "Effective Date written above, by and between the Data Controller "
            "(\"Controller\") and the Data Processor (\"Processor\"), collectively "
            "the \"Parties\". This DPA is incorporated into and forms part of the "
            "Software License & IP Protection Agreement (the \"License Agreement\") "
            "between the Parties. This DPA sets out the terms under which the "
            "Processor will process Personal Data on behalf of the Controller in "
            "connection with the services provided under the License Agreement.")

        self.ln(2)
        self.body(
            "This DPA is governed by the Personal Information Protection and "
            "Electronic Documents Act (PIPEDA), the British Columbia Personal "
            "Information Protection Act (BC PIPA), and where applicable, the "
            "European Union General Data Protection Regulation (GDPR).")

        self._is_cover = False

    def build(self):
        self.cover()

        # --- ARTICLE I: DEFINITIONS ---
        self.article(1, "DEFINITIONS")
        defs = [
            ("1.1", "\"Personal Data\" means any information about an identifiable "
             "individual, as defined under Applicable Data Protection Law, that is "
             "processed by the Processor on behalf of the Controller in connection "
             "with the License Agreement."),
            ("1.2", "\"Processing\" means any operation or set of operations performed "
             "on Personal Data, whether or not by automated means, including "
             "collection, recording, organization, structuring, storage, adaptation, "
             "alteration, retrieval, consultation, use, disclosure by transmission, "
             "dissemination, alignment, combination, restriction, erasure, or "
             "destruction."),
            ("1.3", "\"Data Controller\" or \"Controller\" means the Licensee, being "
             "the Party that determines the purposes and means of the Processing of "
             "Personal Data."),
            ("1.4", "\"Data Processor\" or \"Processor\" means Black Mountain Technologies "
             "Inc. (the Licensor), being the Party that processes Personal Data on "
             "behalf of the Controller."),
            ("1.5", "\"Sub-processor\" means any third party engaged by the Processor "
             "to process Personal Data on behalf of the Controller."),
            ("1.6", "\"Data Subject\" means an identified or identifiable natural person "
             "to whom Personal Data relates."),
            ("1.7", "\"Data Breach\" means a breach of security leading to the "
             "accidental or unlawful destruction, loss, alteration, unauthorized "
             "disclosure of, or access to, Personal Data transmitted, stored, or "
             "otherwise processed."),
            ("1.8", "\"Applicable Data Protection Law\" means all laws and regulations "
             "applicable to the Processing of Personal Data under this DPA, "
             "including the Personal Information Protection and Electronic Documents "
             "Act (PIPEDA), the British Columbia Personal Information Protection Act "
             "(BC PIPA), and where applicable, the European Union General Data "
             "Protection Regulation (GDPR)."),
        ]
        for label, text in defs:
            self.clause(label, text)

        # --- ARTICLE II: SCOPE AND PURPOSE ---
        self.article(2, "SCOPE AND PURPOSE OF PROCESSING")
        self.clause("2.1",
            "The Processor shall process Personal Data solely for the purpose of "
            "providing the Software services under the License Agreement. The "
            "Processor shall not process Personal Data for any other purpose unless "
            "expressly instructed in writing by the Controller.")
        self.clause("2.2",
            "Categories of Personal Data processed under this DPA include: "
            "employee and worker names from timecards, hours worked, hourly rates, "
            "overtime data, crew assignments, project names and identifiers, and "
            "contact information of authorized platform users (name, email, phone).")
        self.clause("2.3",
            "Categories of Data Subjects include: the Controller's employees, "
            "contractors, subcontractors, and authorized platform users.")
        self.clause("2.4",
            "Processing activities include: data ingestion from uploaded files, "
            "analytics computation, health and risk scoring, outlier detection, "
            "AI-assisted query responses via the AI Assistant feature, and report "
            "generation.")
        self.clause("2.5",
            "Duration of Processing: the Processor shall process Personal Data for "
            "the duration of the License Term plus thirty (30) days to allow for "
            "data export or deletion as set out in Article IX.")

        # --- ARTICLE III: PROCESSOR OBLIGATIONS ---
        self.article(3, "PROCESSOR OBLIGATIONS")
        self.clause("3.1",
            "The Processor shall process Personal Data only on documented "
            "instructions from the Controller, including with respect to transfers "
            "of Personal Data to a third country, unless required to do so by "
            "applicable law. In such case, the Processor shall inform the Controller "
            "of that legal requirement before Processing, unless prohibited by law.")
        self.clause("3.2",
            "The Processor shall ensure that persons authorized to process Personal "
            "Data have committed to confidentiality or are under an appropriate "
            "statutory obligation of confidentiality.")
        self.clause("3.3",
            "The Processor shall implement appropriate technical and organizational "
            "security measures to ensure a level of security appropriate to the "
            "risk, including: encryption in transit using TLS 1.2 or higher, "
            "encryption at rest using AES-256, role-based access controls, audit "
            "logging of all data access events, and regular security assessments.")
        self.clause("3.4",
            "The Processor shall not engage any Sub-processor to process Personal "
            "Data without the prior written consent of the Controller, subject to "
            "the terms set out in Article IV.")
        self.clause("3.5",
            "The Processor shall assist the Controller in responding to Data "
            "Subject access requests within ten (10) business days of receiving "
            "the Controller's instructions, taking into account the nature of the "
            "Processing.")
        self.clause("3.6",
            "The Processor shall assist the Controller with data protection impact "
            "assessments and prior consultations with supervisory authorities, if "
            "required under Applicable Data Protection Law.")
        self.clause("3.7",
            "Upon termination of the License Agreement, the Processor shall, at "
            "the Controller's choice, delete or return all Personal Data within "
            "thirty (30) days and certify such deletion or return in writing, "
            "subject to the terms set out in Article IX.")
        self.clause("3.8",
            "The Processor shall make available to the Controller all information "
            "necessary to demonstrate compliance with this DPA, and shall allow "
            "for and contribute to audits, including inspections, conducted by the "
            "Controller or an auditor mandated by the Controller.")

        # --- ARTICLE IV: SUB-PROCESSORS ---
        self.article(4, "SUB-PROCESSORS")
        self.clause("4.1",
            "The Controller acknowledges and approves the following Sub-processors "
            "as of the Effective Date:")
        self.clause("(a)",
            "Anthropic PBC -- AI query processing. Project data is sent to the "
            "Anthropic Claude API to power the AI Assistant feature of the Software.")
        self.clause("(b)",
            "Cloud hosting provider -- to be specified at deployment. The Processor "
            "shall notify the Controller of the specific cloud hosting provider "
            "prior to deployment.")
        self.clause("4.2",
            "The Processor shall notify the Controller in writing at least thirty "
            "(30) days before engaging any new Sub-processor or replacing an "
            "existing Sub-processor.")
        self.clause("4.3",
            "The Controller may object to the appointment of a new Sub-processor "
            "within fourteen (14) days of receiving notice. If the objection is not "
            "resolved to the Controller's reasonable satisfaction, the Controller "
            "may terminate the License Agreement and this DPA upon written notice.")
        self.clause("4.4",
            "The Processor shall remain fully liable for the acts and omissions of "
            "its Sub-processors with respect to Personal Data Processing under "
            "this DPA.")
        self.clause("4.5",
            "Anthropic-specific provisions: Data sent to the Anthropic API is not "
            "used for model training, in accordance with Anthropic's commercial "
            "API terms. Data is not retained by Anthropic beyond the API request "
            "lifecycle. The Processor shall monitor Anthropic's data handling "
            "policies and promptly notify the Controller of any material changes.")

        # --- ARTICLE V: DATA SECURITY ---
        self.article(5, "DATA SECURITY")
        self.body("Technical measures:")
        self.clause("(a)",
            "TLS 1.2 or higher for all data in transit.")
        self.clause("(b)",
            "AES-256 encryption for all data at rest.")
        self.clause("(c)",
            "Role-based access control limiting data access to authorized personnel.")
        self.clause("(d)",
            "Multi-factor authentication required for all administrative access.")
        self.clause("(e)",
            "Automated session timeout after periods of inactivity.")
        self.clause("(f)",
            "Regular vulnerability scanning and penetration testing.")

        self.body("Organizational measures:")
        self.clause("(g)",
            "Employee background checks for all personnel with access to Personal Data.")
        self.clause("(h)",
            "Mandatory security awareness training for all personnel.")
        self.clause("(i)",
            "Least privilege access principle applied across all systems.")
        self.clause("(j)",
            "Documented incident response plan maintained and tested regularly.")

        self.clause("5.2",
            "The Processor shall conduct an annual review of its security measures "
            "and update them as necessary to address evolving threats and "
            "vulnerabilities. The results of such reviews shall be made available "
            "to the Controller upon request.")

        # --- ARTICLE VI: DATA BREACH NOTIFICATION ---
        self.article(6, "DATA BREACH NOTIFICATION")
        self.clause("6.1",
            "The Processor shall notify the Controller without undue delay, and "
            "in any event within seventy-two (72) hours of becoming aware of a "
            "Data Breach affecting Personal Data processed under this DPA.")
        self.clause("6.2",
            "The notification shall include, to the extent available: the nature "
            "of the Data Breach including the categories and approximate number "
            "of Data Subjects affected; the likely consequences of the Data Breach; "
            "and the measures taken or proposed to be taken to address the Data "
            "Breach and mitigate its effects.")
        self.clause("6.3",
            "The Processor shall cooperate fully with the Controller in the "
            "investigation of any Data Breach and in any required notifications "
            "to Data Subjects or regulatory authorities under Applicable Data "
            "Protection Law.")
        self.clause("6.4",
            "The Processor shall maintain a register of all Data Breaches, "
            "including the facts surrounding the breach, its effects, and the "
            "remedial actions taken. This register shall be made available to the "
            "Controller upon request.")

        # --- ARTICLE VII: CROSS-BORDER DATA TRANSFERS ---
        self.article(7, "CROSS-BORDER DATA TRANSFERS")
        self.clause("7.1",
            "Personal Data shall be processed and stored within Canada unless "
            "otherwise agreed in writing by the Controller.")
        self.clause("7.2",
            "If Personal Data must be transferred outside of Canada, the Processor "
            "shall ensure adequate protection through appropriate contractual "
            "clauses, adequacy decisions, or Data Subject consent, as required "
            "under Applicable Data Protection Law.")
        self.clause("7.3",
            "For EU Data Subjects (if applicable): any transfers of Personal Data "
            "outside the European Economic Area shall comply with the requirements "
            "of GDPR Chapter V, including the use of Standard Contractual Clauses "
            "or other approved transfer mechanisms.")
        self.clause("7.4",
            "Anthropic API calls: the Controller acknowledges that data submitted "
            "to the AI Assistant feature transits to Anthropic's servers located "
            "in the United States. The Controller consents to this transfer for the "
            "purpose of AI Assistant functionality. The Controller may disable the "
            "AI Assistant feature at any time to prevent cross-border data transfer "
            "for this purpose.")

        # --- ARTICLE VIII: DATA SUBJECT RIGHTS ---
        self.article(8, "DATA SUBJECT RIGHTS")
        self.clause("8.1",
            "The Processor shall assist the Controller in fulfilling its obligations "
            "to respond to Data Subject requests exercising their rights under "
            "Applicable Data Protection Law, including: access to Personal Data, "
            "correction of inaccurate data, deletion of Personal Data, data "
            "portability, restriction of Processing, and objection to Processing.")
        self.clause("8.2",
            "The Processor shall respond to the Controller's instructions regarding "
            "Data Subject requests within ten (10) business days.")
        self.clause("8.3",
            "The Processor shall not respond directly to Data Subjects regarding "
            "their Personal Data unless expressly instructed to do so by the "
            "Controller in writing.")

        # --- ARTICLE IX: DATA RETENTION AND DELETION ---
        self.article(9, "DATA RETENTION AND DELETION")
        self.clause("9.1",
            "The Processor shall retain Personal Data only for the duration of "
            "the License Term as defined in the License Agreement.")
        self.clause("9.2",
            "Upon termination or expiration of the License Agreement: the "
            "Controller shall have thirty (30) days to export its data from the "
            "Software platform. After the thirty (30) day export period, the "
            "Processor shall securely delete all Personal Data and certify such "
            "deletion to the Controller in writing.")
        self.clause("9.3",
            "Deletion method: secure overwrite for all digital records containing "
            "Personal Data, in accordance with industry-standard data sanitization "
            "practices.")
        self.clause("9.4",
            "Exception: the Processor may retain anonymized, aggregated data that "
            "cannot be linked to any identifiable individual, as permitted under "
            "the License Agreement for benchmarking and product improvement "
            "purposes. Such anonymized data shall not constitute Personal Data "
            "under this DPA.")

        # --- ARTICLE X: LIABILITY AND INDEMNIFICATION ---
        self.article(10, "LIABILITY AND INDEMNIFICATION")
        self.clause("10.1",
            "Each Party shall be liable for damages caused by Processing that "
            "violates this DPA or Applicable Data Protection Law.")
        self.clause("10.2",
            "The Processor shall indemnify, defend, and hold harmless the "
            "Controller from and against any losses, liabilities, damages, costs, "
            "and expenses (including reasonable legal fees) arising from the "
            "Processor's breach of this DPA or Applicable Data Protection Law.")
        self.clause("10.3",
            "The total aggregate liability of the Processor under this DPA shall "
            "be subject to the same liability cap as set out in the License "
            "Agreement (total fees paid or payable by the Controller during the "
            "License Term), except that liability for willful misconduct shall "
            "be uncapped.")

        # --- ARTICLE XI: GENERAL PROVISIONS ---
        self.article(11, "GENERAL PROVISIONS")
        self.clause("11.1",
            "This DPA is incorporated into and forms part of the License Agreement "
            "between the Parties. References to the License Agreement shall include "
            "this DPA.")
        self.clause("11.2",
            "In the event of any conflict between the terms of this DPA and the "
            "License Agreement, the terms of this DPA shall prevail with respect "
            "to all matters relating to data protection and the Processing of "
            "Personal Data.")
        self.clause("11.3",
            "Governing Law. This DPA shall be governed by and construed in "
            "accordance with the laws of the Province of British Columbia, Canada, "
            "consistent with the License Agreement. The Parties submit to the "
            "exclusive jurisdiction of the courts of British Columbia.")
        self.clause("11.4",
            "Amendments. No amendment or modification of this DPA shall be "
            "effective unless made in writing and signed by both Parties.")
        self.clause("11.5",
            "Severability. If any provision of this DPA is held to be invalid or "
            "unenforceable, the remaining provisions shall continue in full force "
            "and effect, and the invalid provision shall be modified to the minimum "
            "extent necessary to make it enforceable.")

        # --- ARTICLE XII: SIGNATURES ---
        self.article(12, "SIGNATURES")
        self.body(
            "IN WITNESS WHEREOF, the Parties have executed this Data Processing "
            "Addendum as of the Effective Date first written above.")
        self.ln(2)
        self.sig_block("DATA CONTROLLER (LICENSEE)")
        self.ln(6)
        self.sig_block("DATA PROCESSOR (LICENSOR)", "Black Mountain Technologies Inc.")

        # --- EXHIBIT: TECHNICAL AND ORGANIZATIONAL MEASURES ---
        self.add_page()
        self.article(13, "EXHIBIT -- TECHNICAL AND ORGANIZATIONAL MEASURES")
        self.body(
            "The following technical and organizational measures are implemented "
            "by the Processor to protect Personal Data processed under this DPA. "
            "These measures are subject to annual review and update.")
        self.ln(2)

        self.exhibit_category("Access Control", [
            "Role-based access control (RBAC) with least privilege enforcement",
            "Multi-factor authentication (MFA) required for all administrative access",
            "Automated session timeout after period of inactivity",
        ])

        self.exhibit_category("Encryption", [
            "TLS 1.2 or higher for all data in transit",
            "AES-256 encryption for all data at rest",
            "Encryption key management with regular key rotation",
        ])

        self.exhibit_category("Network Security", [
            "Firewall protection with intrusion detection and prevention",
            "Network segmentation isolating production environments",
            "Regular vulnerability scanning and penetration testing",
        ])

        self.exhibit_category("Application Security", [
            "Secure software development lifecycle (SDLC) practices",
            "Input validation and output encoding to prevent injection attacks",
            "Regular code reviews and security testing",
        ])

        self.exhibit_category("Physical Security", [
            "Cloud hosting in data centers with SOC 2 Type II certification",
            "Physical access controls and environmental monitoring",
            "Redundant power and connectivity systems",
        ])

        self.exhibit_category("Personnel Security", [
            "Background checks for all personnel with access to Personal Data",
            "Mandatory security awareness training upon hire and annually",
            "Confidentiality agreements executed by all personnel",
        ])

        self.exhibit_category("Incident Response", [
            "Documented incident response plan tested at least annually",
            "Designated incident response team with defined roles",
            "72-hour breach notification process as set out in Article VI",
        ])

        self.exhibit_category("Business Continuity", [
            "Regular automated backups with tested restoration procedures",
            "Disaster recovery plan with defined recovery time objectives",
            "Geographic redundancy for critical systems and data",
        ])


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = DPA()
    doc.build()
    doc.output(OUT)
    print(f"Data Processing Addendum saved to {OUT}")


if __name__ == "__main__":
    main()
