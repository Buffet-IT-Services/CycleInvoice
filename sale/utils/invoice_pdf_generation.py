from django.template.loader import render_to_string
from django.http import FileResponse
from weasyprint import HTML
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from sale.utils.swiss_qr import generate_swiss_qr
from dataclasses import dataclass


def prepare_invoice_context(context_data):
    """
    Prepare the context data for invoice rendering.
    
    Args:
        context_data (dict): The original context data
        
    Returns:
        dict: The prepared context data with QR code
    """
    # Set page number flag to false for first pass
    context_data['show_page_number'] = False
    
    # Generate the QR bill and add it to the context
    generate_swiss_qr(context_data, context_data['financial_details']['total_sum'])
    
    return context_data


def render_invoice_html(context_data, template_name='invoice.html'):
    """
    Render the invoice HTML template with the given context.
    
    Args:
        context_data (dict): The context data for rendering
        template_name (str): The name of the template to render
        
    Returns:
        str: The rendered HTML
    """
    return render_to_string(template_name, context_data)


def generate_base_pdf(html_content, base_url=None):
    """
    Generate a PDF from HTML content using WeasyPrint.
    
    Args:
        html_content (str): The HTML content to convert to PDF
        base_url (str, optional): The base URL for resolving relative URLs
        
    Returns:
        tuple: (PDF bytes, total page count)
    """
    document = HTML(string=html_content, base_url=base_url).render()
    total_pages = len(document.pages)
    pdf_file = document.write_pdf()
    
    return pdf_file, total_pages


def create_page_number_overlay(page_num, total_pages):
    """
    Create a PDF overlay with page numbers.
    
    Args:
        page_num (int): The current page number (0-based)
        total_pages (int): The total number of pages
        
    Returns:
        BytesIO: A BytesIO object containing the page number overlay PDF
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Draw the page number (positioned to overlap with footer)
    can.setFont("Helvetica", 22)  # Smaller font size
    can.setFillColorRGB(1, 1, 1)  # White color
    text = f"Seite {page_num + 1} von {total_pages}"
    
    # Position in the bottom right area of the footer
    can.drawRightString(530, 20, text)
    can.save()
    
    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    
    return packet


def add_page_numbers_to_pdf(pdf_data, total_pages):
    """
    Add page numbers to each page of a PDF.
    
    Args:
        pdf_data (bytes): The original PDF data
        total_pages (int): The total number of pages
        
    Returns:
        BytesIO: A BytesIO object containing the PDF with page numbers
    """
    input_pdf = PdfReader(BytesIO(pdf_data))
    output_pdf = PdfWriter()
    
    # For each page, add page number
    for page_num in range(total_pages):
        # Get the page from the original PDF
        page = input_pdf.pages[page_num]
        
        # Create the page number overlay
        packet = create_page_number_overlay(page_num, total_pages)
        
        # Create a new PDF with the page number
        new_pdf = PdfReader(packet)
        
        # Merge the original page with the page number
        page.merge_page(new_pdf.pages[0])
        
        # Add the page to the output PDF
        output_pdf.add_page(page)
    
    # Write the output PDF to BytesIO
    output_stream = BytesIO()
    output_pdf.write(output_stream)
    output_stream.seek(0)
    
    return output_stream


@dataclass
class PDFContent:
    """Class for storing PDF content and metadata"""
    content: bytes
    filename: str
    mime_type: str = 'application/pdf'


def create_pdf_content(pdf_stream, invoice_id):
    """
    Create a PDFContent object with the PDF content.
    
    Args:
        pdf_stream (BytesIO): The PDF content as a BytesIO stream
        invoice_id (str): The invoice ID for the filename
        
    Returns:
        PDFContent: Object containing PDF content and metadata
    """
    filename = f"invoice_{invoice_id}_numbered.pdf"
    
    # Get the bytes from the BytesIO stream
    pdf_stream.seek(0)
    content = pdf_stream.getvalue()
    
    return PDFContent(
        content=content,
        filename=filename
    )


def generate_invoice_pdf_two_pass(request, context_data):
    """
    Generate a PDF invoice using WeasyPrint with manual page numbering.
    
    Args:
        request: The HTTP request object
        context_data (dict): The context data for the invoice
        
    Returns:
        PDFContent: Object containing PDF content and metadata
    """
    # Step 1: Prepare the context data
    prepared_context = prepare_invoice_context(context_data)
    
    # Step 2: Render the HTML
    html_content = render_invoice_html(prepared_context)
    
    # Step 3: Generate the base PDF and get page count
    pdf_data, total_pages = generate_base_pdf(html_content, request.build_absolute_uri('/'))
    print(f"Total pages detected: {total_pages}")
    
    # Step 4: Add page numbers to the PDF
    pdf_with_page_numbers = add_page_numbers_to_pdf(pdf_data, total_pages)
    
    # Step 5: Create and return the PDF content
    return create_pdf_content(pdf_with_page_numbers, context_data['invoice_details']['invoice_id'])

