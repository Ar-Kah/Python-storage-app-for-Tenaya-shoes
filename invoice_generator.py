from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime, timedelta
import json


TODAY = datetime.today()
DUEDATE = TODAY + timedelta(days=14)
TODAY = TODAY.strftime("%d.%m.%Y")
DUEDATE = DUEDATE.strftime("%d.%m.%Y")
BANK_NAME = "Nordea"
BANK_NUMBER = "FI83 1146 3001 1475 83"
SWIFT_BIC = "NDEAFIHH"


class InvoiceGenerator:
    def __init__(self, items, customer, output_file="exact_invoice.pdf"):
        self.billing_info = None
        self.customer_email = None
        self.customer = customer
        # find the billing info of customer
        self.get_customer_details()
        self.items = items
        self.output_file = output_file
        self.total_excl_vat = 0
        self.vat_total = 0
        self.total_incl_vat = 0
    def get_customer_details(self):
        saved = self.customer
        if self.customer in ['Salmisaari', 'Ristikko', 'Kalasatama']:
            self.customer = "Kiipeilyvisio Oy"

        try:
            with open("Jsonfiles/asiakas.json", 'r') as json_file:
                data = json.load(json_file)
                for cust, details in data.items():
                    if cust == self.customer:
                        if self.customer == "Kiipeilyvisio Oy":
                            self.customer = self.customer + " " + "(" + saved + ")"
                        self.billing_info = details["Laskutustiedot"]
                        self.customer_email = details["Sposti"]


        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Json syntax fucked")
    def generate(self):
        c = canvas.Canvas(self.output_file, pagesize=A4)
        width, height = A4

        self.draw_header(c, width, height)
        self.draw_invoice_details(c, width, height)
        self.draw_item_table(c, width, height)
        self.draw_footer(c, width, height)

        c.save()

    def draw_header(self, c, width, height):
        # Company details on the left
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, height - 20 * mm, "RK-AviaTech Oy")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, height - 25 * mm, "Tahkokatu 1")
        c.drawString(20 * mm, height - 30 * mm, "37120 Nokia")
        c.drawString(20 * mm, height - 35 * mm, "www.rk-aviatech.com")

        # Logo on the right
        #logo_path = "logo.png"  # Replace with your logo file path
        #c.drawImage(logo_path, width - 50 * mm, height - 30 * mm, 30 * mm, 15 * mm)

        # Invoice title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(width / 2 - 10 * mm, height - 20 * mm, "LASKU")

    def draw_invoice_details(self, c, width, height):
        # Buyer info on the left
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, height - 50 * mm, "Ostaja")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, height - 55 * mm, self.customer)
        c.drawString(20 * mm, height - 60 * mm, self.billing_info[0])
        c.drawString(20 * mm, height - 65 * mm, self.billing_info[1])
        c.drawString(20 * mm, height - 70 * mm, self.billing_info[2])
        c.drawString(20 * mm, height - 75 * mm, self.customer_email)
        c.drawString(20 * mm, height - 85 * mm, "Lisätiedot")
        c.drawString(20 * mm, height - 90 * mm, "Kengille myönnämme kuukauden takuun joka kattaa materiaali ja valmistusvirheet")
        c.drawString(20 * mm, height - 100 * mm, "Ostajan viite: 113428, 113429, 113430, 115537, 14418, 117452")

        # Invoice metadata on the right
        details = [
            ["Päiväys:", TODAY],
            ["Laskun numero:", "1024"],
            ["Eräpäivä:", DUEDATE],
            ["Viivästyskorko:", "8.0 %"],
            ["Viitenumero:", "10249"],
            ["Maksuehto:", "14 päivää netto"],
            ["Pankki:", BANK_NAME],
            ["Tilinumero:", BANK_NUMBER],
            ["SWIFT/BIC:", SWIFT_BIC]
        ]

        # Draw details table
        table = Table(details, colWidths=[30 * mm, 40 * mm])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, width - 90 * mm, height - 80 * mm)

    def draw_item_table(self, c, width, height):
        # Item table headers
        headers = ["Tuotekuvaus", "Määrä", "Yksikkö", "à hinta", "Alv %", "Yhteensä"]
        table_data = [headers]

        # Add items
        for item in self.items:
            desc = item["description"]
            qty = item["quantity"]
            unit = item["unit"]
            unit_price = item["unit_price"]
            excl_vat = qty * unit_price
            vat = excl_vat * 0.255  # 25.5% tax rate
            incl_vat = excl_vat + vat

            table_data.append([desc, qty, unit, f"{unit_price:.2f}", "25.5%", f"{incl_vat:.2f}"])
            self.total_excl_vat += excl_vat
            self.vat_total += vat

        # Add totals
        table_data.append(["", "", "", "", "Veroton yht:", f"{self.total_excl_vat:.2f}"])
        table_data.append(["", "", "", "", "ALV 25.5%:", f"{self.vat_total:.2f}"])
        table_data.append(["", "", "", "", "Yhteensä:", f"{self.total_excl_vat + self.vat_total:.2f}"])

        # Create and style the table
        table = Table(table_data, colWidths=[50 * mm, 20 * mm, 20 * mm, 30 * mm, 20 * mm, 30 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        # Draw table
        table.wrapOn(c, width, height)
        table.drawOn(c, 20 * mm, height - 140 * mm)

    def draw_footer(self, c, width, height):
        # Footer details
        c.setFont("Helvetica", 9)
        c.drawString(20 * mm, 85, "Pyydämme käyttämään maksaessanne viitenumeroa: 10249")
        c.line(20 * mm, 75, 200 * mm, 75)
        c.drawString(20 * mm, 60, "RK-AviaTeck Oy")
        c.drawString(20 * mm, 50, "Tahkokatu 1")
        c.drawString(20 * mm, 40, "37120 Nokia")
        c.drawString(20 * mm, 30, "Y-tunnus 2602150-4")
        c.drawString(90 * mm, 60, "Yhteystiedot")
        c.drawString(90 * mm, 50, "Risto Kallinen")
        c.drawString(90 * mm, 40, "+358 50 410 6994")
        c.drawString(90 * mm, 30, "risto@rk-aviatech.com")
        c.drawString(160 * mm, 60, "Pankkiyhteys")
        c.drawString(160 * mm, 50, BANK_NAME)
        c.drawString(160 * mm, 40, BANK_NUMBER)
        c.drawString(160 * mm, 30, SWIFT_BIC)
