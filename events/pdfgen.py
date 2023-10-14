from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Image
from reportlab.pdfgen import canvas
import qrcode
from io import BytesIO

def generate_certificate(event_name, student_name, path):
    # Create a BytesIO buffer to store the PDF
    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add background color
    pdf.setFillColorRGB(1, 1, 1)  # White
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    # Add border
    pdf.setStrokeColor(colors.black)
    pdf.rect(50, 50, letter[0] - 100, letter[1] - 100, fill=False, stroke=True)

    # Add logo
    logo_path = "static/logo.png"
    pdf.drawImage(logo_path, 60, letter[1] - 160, width=100, height=100)

    # Set up the certificate content
    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColor(colors.black)
    pdf.drawString(180, 500, "Certificate of Participation")
    pdf.setFont("Helvetica", 18)
    pdf.drawString(180, 450, "This is to certify that")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 400, student_name)
    pdf.setFont("Helvetica", 18)
    pdf.drawString(180, 350, "has successfully participated in the")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 300, event_name)

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(path)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Create a BytesIO buffer for the QR code image
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format='PNG')

    # Move the buffer position to the beginning of the buffer
    qr_buffer.seek(0)

    # Add the QR code image to the certificate
    pdf.drawInlineImage(qr_buffer, 450, 55, width=1.5 * inch, height=1.5 * inch)

    # Save the PDF content to the buffer
    pdf.save()

    # Move the buffer position to the beginning of the PDF
    pdf_buffer.seek(0)

    return pdf_buffer