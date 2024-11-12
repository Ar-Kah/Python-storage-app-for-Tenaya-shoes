from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


class InvoiceGenerator:
    def __init__(self, items, output_file="invoice.pdf"):
        self.items = items
        self.output_file = output_file
        self.total = 0
        self.tax_rate = 0.24  # 24% tax rate as per the example

    def generate(self):
        c = canvas.Canvas(self.output_file, pagesize=A4)
        width, height = A4

        self.draw_header(c, width, height)
        self.draw_recipient_sender_info(c, width, height)
        self.draw_invoice_details(c, width, height)
        self.draw_extra_info_box(c, width, height)
        self.draw_item_table(c, width, height)
        self.draw_footer(c, width)

        c.save()

    def draw_header(self, c, width, height):
        # Draws the main header with sender information
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, height - 20 * mm, "Laskuttava Yritys Oy")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, height - 25 * mm, "Laskuttajantie 10")
        c.drawString(20 * mm, height - 30 * mm, "123456 Laskutus")

        # Invoice title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(120 * mm, height - 20 * mm, "LASKU")

    def draw_recipient_sender_info(self, c, width, height):
        # Draws recipient and sender information
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, height - 45 * mm, "Asiakkaan Yritys Oy")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, height - 50 * mm, "Asiakkaantie 10")
        c.drawString(20 * mm, height - 55 * mm, "123456 Asiakas")

    def draw_invoice_details(self, c, width, height):
        # Draws invoice-specific details
        details = [
            ["Laskun päivays:", "1.1.2016"],
            ["Laskunumero:", "123"],
            ["Maksuehto:", "14 pv netto"],
            ["Eräpäivä:", "15.1.2016"],
            ["Viivästyskorko:", "8 %"],
            ["Asiakkaan Y-tunnus:", "124567-8"],
            ["Viitteemme:", "Matti Myyjä"],
            ["Viitteenne:", "Olli Ostaja"],
            ["Toimitusehto:", "vapaasti varastosta"]
        ]

        table_data = [[f"{label} {value}"] for label, value in details]
        table = Table(table_data, colWidths=[85 * mm, 85 * mm])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))

        # Adjusted position to avoid overlap with the title
        table.wrapOn(c, width, height)
        table.drawOn(c, 100 * mm, height - 85 * mm)

    def draw_extra_info_box(self, c, width, height):
        # Box for additional information
        c.setFont("Helvetica", 9)
        c.drawString(20 * mm, height - 108 * mm, "Lisätietoja voi kirjoittaa tähän kenttään")
        c.rect(20 * mm, height - 115 * mm, 170 * mm, 10 * mm, stroke=1, fill=0)

    def draw_item_table(self, c, width, height):
        # Table header and items
        table_data = [["Nimike", "Määrä", "Yks.", "A'Hinta EUR", "Alv %", "Verollinen yht. EUR"]]

        # Adding each item to the table
        for item in self.items:
            qty = item["quantity"]
            unit = item["unit"]
            desc = item["description"]
            unit_price = item["unit_price"]
            amount = qty * unit_price
            tax_amount = amount * self.tax_rate
            total_amount = amount + tax_amount
            table_data.append(
                [desc, qty, unit, f"{unit_price:.2f}", f"{self.tax_rate * 100:.0f}", f"{total_amount:.2f}"])
            self.total += total_amount

        # Total amounts at the end of the table
        table_data.append(["", "", "", "", "Veroton yhteensä EUR:", f"{self.total / (1 + self.tax_rate):.2f}"])
        table_data.append(["", "", "", "", "Verollinen yhteensä EUR:", f"{self.total:.2f}"])

        # Create and style the table
        table = Table(table_data, colWidths=[50 * mm, 20 * mm, 15 * mm, 30 * mm, 20 * mm, 35 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        # Adjusted vertical position to fit on the page correctly
        table.wrapOn(c, width, height)
        table.drawOn(c, 20 * mm, height - 170 * mm)

    def draw_footer(self, c, width):
        # Draws footer with payment information and total
        c.setFont("Helvetica", 9)
        c.drawString(20 * mm, 40, "IBAN: FI12 1234 1234 1234 12")
        c.drawString(80 * mm, 40, "BIC / SWIFT: OKOYFIHH")
        c.drawString(140 * mm, 40, "Eräpäivä: 15.1.2016")

        c.drawString(20 * mm, 30, "Viitenumero: 100 01235")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80 * mm, 30, "Yhteensä EUR:")
        c.drawString(120 * mm, 30, f"{self.total:.2f}")

        # Footer contact info
        c.setFont("Helvetica", 9)
        c.drawString(20 * mm, 20, "Laskuttava Yritys Oy")
        c.drawString(20 * mm, 15, "Laskuttajantie 10, 123456 Laskutus")
        c.drawString(100 * mm, 20, "Y-tunnus: 1234567-8")
        c.drawString(100 * mm, 15, "Puhelin: 040 111 111")
        c.drawString(100 * mm, 10, "Sähköposti: sahkoposti@osoite.com")
        c.drawString(20 * mm, 5, "Laskupohja: www.laskuhari.fi")
