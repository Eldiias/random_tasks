### Compress PDF files using PyMuPDF
# This script provides two functions to compress PDF files using the PyMuPDF library.
# The first function compresses the PDF by removing garbage and deflating the content.
# The second function compresses the PDF by rendering each page as an image and saving it in a specified format.
# When a heavy image iimflated PDF is compressed, the second function can significantly reduce the file size.


# Import necessary libraries
import fitz
import io

def compress_pdf(input_pdf_path, output_pdf_path):
    # Open the input PDF
    pdf_document = fitz.open(input_pdf_path)

    # Compress the PDF
    pdf_document.save(output_pdf_path, garbage=4, deflate=True)

    # Close the PDF document
    pdf_document.close()

def compress_pdf2(input_pdf_path, output_pdf_path, scale=1.0, image_format="jpeg", jpeg_quality=75):
    # Open the input PDF
    pdf_document = fitz.open(input_pdf_path)

    # Create a new empty PDF
    new_pdf_document = fitz.open()

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # Scale page for rendering (matrix controls resolution)
        zoom_matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=zoom_matrix)

        # Save image to memory as JPEG or PNG
        image_bytes = io.BytesIO()
        if image_format.lower() == "jpeg":
            pix.save(image_bytes, format="jpeg", quality=jpeg_quality)
        else:
            pix.save(image_bytes, format="png")  # fallback
        image_bytes.seek(0)

        # Create a PDF page from image and insert it
        img_pdf = fitz.open("pdf", fitz.Pixmap(image_bytes).convert_to_pdf())
        new_pdf_document.insert_pdf(img_pdf)

    # Save the final compressed PDF
    new_pdf_document.save(output_pdf_path, garbage=4, deflate=True)
    new_pdf_document.close()
    pdf_document.close()


