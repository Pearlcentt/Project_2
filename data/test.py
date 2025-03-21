import pdfplumber
import fitz  # PyMuPDF

pdf_file = "../Data_pdf/QCDT_2023.pdf"
output_pdfplumber_txt = "../Chunks/pdfplumber_output.txt"
output_pymupdf_txt = "../Chunks/pymupdf_output.txt"

# Extract text using pdfplumber and save to a text file
with pdfplumber.open(pdf_file) as pdf:
    with open(output_pdfplumber_txt, mode="w", encoding="utf-8") as txtfile:
        for pagenumber, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            txtfile.write(f"Page {pagenumber}:\n")
            txtfile.write(text if text else "No text extracted.\n")
            txtfile.write("\n" + "-" * 80 + "\n")
            print(f"Page {pagenumber} written to pdfplumber text file.")

# Extract text using PyMuPDF and save to a text file
pdf_document = fitz.open(pdf_file)
with open(output_pymupdf_txt, mode="w", encoding="utf-8") as txtfile:
    for pagenumber in range(pdf_document.page_count):
        page = pdf_document.load_page(pagenumber)
        text = page.get_text()
        txtfile.write(f"Page {pagenumber + 1}:\n")
        txtfile.write(text if text else "No text extracted.\n")
        txtfile.write("\n" + "-" * 80 + "\n")
        print(f"Page {pagenumber + 1} written to PyMuPDF text file.")