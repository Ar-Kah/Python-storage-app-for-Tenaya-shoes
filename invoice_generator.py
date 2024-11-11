from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import datetime


class InvoiceGenerator:
    def __init__(self, items, recipient, output_file="invoice.pdf"):
        """
        Initialize the InvoiceGenerator with the required data.

        Args:
            items (list of dict): List of items, where each item is a dict with 'quantity', 'description', and 'unit_price'.
            recipient (dict): Recipient info with keys 'name', 'address', and 'city'.
            output_file (str): The file name for the generated PDF.
        """
        self.items = items
        self.recipient = recipient
        self.output_file = output_file
        self.total = 0
        self.tax_rate = 0.0625  # Example tax rate of 6.25%

    def generate(self):
        """Generate the invoice PDF."""
        c = canvas.Canvas(self.output_file, pagesize=A4)
        width, height = A4

        # Draw the static parts of the invoice (headers, company info, etc.)
        self.draw_header(c, width, height)
        self.draw_recipient_info(c, width, height)
        self.draw_table(c, width, height)
        self.draw_footer(c, width)

        # Save the PDF
        c.save()

    def draw_header(self, c, width, height):
        """Draws the header section including the logo and company info."""
        c.setFont("Helvetica-Bold", 30)
        c.drawString(40, height - 80, "invoice")

        # Company logo placeholder
        c.setFillColor(colors.grey)
        c.circle(width - 80, height - 80, 30, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(width - 95, height - 85, "LOGO")

        # Company Info
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 120, "FROM")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, height - 135, "East Repair Inc.")
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 150, "1912 Harvest Lane")
        c.drawString(40, height - 165, "New York, NY 12210")

        # Invoice Details
        c.setFont("Helvetica-Bold", 10)
        c.drawString(width - 200, height - 120, "INVOICE #")
        c.drawString(width - 200, height - 135, "INVOICE DATE")
        c.drawString(width - 200, height - 150, "P.O. #")
        c.drawString(width - 200, height - 165, "DUE DATE")

        c.setFont("Helvetica", 10)
        c.drawString(width - 100, height - 120, "US-001")
        c.drawString(width - 100, height - 135, datetime.datetime.now().strftime("%d/%m/%Y"))
        c.drawString(width - 100, height - 150, "2312/2023")
        c.drawString(width - 100, height - 165, "30/12/2023")

    def draw_recipient_info(self, c, width, height):
        """Draws the recipient info in the BILL TO and SHIP TO sections."""
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, height - 200, "BILL TO")
        c.drawString(width / 2 + 40, height - 200, "SHIP TO")

        c.setFont("Helvetica", 10)
        # BILL TO section
        c.drawString(40, height - 215, self.recipient['name'])
        c.drawString(40, height - 230, self.recipient['address'])
        c.drawString(40, height - 245, self.recipient['city'])

        # SHIP TO section (Static for demo)
        c.drawString(width / 2 + 40, height - 215, self.recipient['name'])
        c.drawString(width / 2 + 40, height - 230, "3787 Pineview Drive")
        c.drawString(width / 2 + 40, height - 245, "Cambridge, MA 12210")

    def draw_table(self, c, width, height):
        """Draws the items table in the middle of the invoice."""
        table_data = [["QTY", "DESCRIPTION", "UNIT PRICE", "AMOUNT"]]

        # Populate table data with items
        for item in self.items:
            qty = item["quantity"]
            desc = item["description"]
            unit_price = item["unit_price"]
            amount = qty * unit_price
            self.total += amount
            table_data.append([qty, desc, f"${unit_price:.2f}", f"${amount:.2f}"])

        # Add subtotal and tax rows
        table_data.append(["", "", "Subtotal", f"${self.total:.2f}"])
        tax = self.total * self.tax_rate
        table_data.append(["", "", f"Sales Tax {self.tax_rate * 100:.2f}%", f"${tax:.2f}"])
        grand_total = self.total + tax
        table_data.append(["", "", "TOTAL", f"${grand_total:.2f}"])

        # Create Table
        table = Table(table_data, colWidths=[1 * inch, 3 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Position the table in the PDF
        table.wrapOn(c, width, height)
        table.drawOn(c, 40, height - 400)

    def draw_footer(self, c, width):
        """Draws the footer section including terms, conditions, and total."""
        # Terms & Conditions
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, 100, "TERMS & CONDITIONS")
        c.setFont("Helvetica", 10)
        c.drawString(40, 85, "Payment is due within 15 days")
        c.drawString(40, 70, "Please make checks payable to: East Repair Inc.")

        # Total and Signature
        grand_total = self.total * (1 + self.tax_rate)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, 140, "TOTAL")
        c.drawString(250, 140, f"${grand_total:.2f}")

        # Signature Placeholder
        c.setFont("Helvetica", 10)
        c.drawString(width - 150, 50, self.recipient["name"])
        c.line(width - 150, 40, width - 50, 40)  # Line for signature

