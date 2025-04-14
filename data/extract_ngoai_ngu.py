import pdfplumber
import pandas as pd
import re
import uuid

PDF_FILE = "raw/Ngoai_ngu_2024.pdf"
OUTPUT_CSV = "processed/ngoai_ngu_2024_structured.csv"

TOP_CROP = 50
BOTTOM_CROP = 70

#===========================
# Table cleaning utilities
#===========================
def fill_none_with_above(table):
    for row_idx in range(1, len(table)):
        for col_idx in range(len(table[row_idx])):
            if not table[row_idx][col_idx] or table[row_idx][col_idx].strip() == "":
                table[row_idx][col_idx] = table[row_idx - 1][col_idx]
    return table

def table_to_sentences(table, table_title="Bảng"):
    sentences = []
    table = fill_none_with_above(table)
    headers = table[0]

    for row_idx, row in enumerate(table[1:], start=1):
        parts = []
        for col_idx, cell in enumerate(row):
            header = headers[col_idx] or f"Cột {col_idx + 1}"
            parts.append(f"{header} là {cell}")
        sentence = f"{table_title} ({row_idx}): " + "; ".join(parts) + "."
        sentences.append(sentence)
    return sentences

#===========================
# Header/footer cleaning
#===========================
def remove_headers_and_footers(cropped_page):
    raw_text = cropped_page.extract_text()
    if not raw_text:
        return ""

    lines = raw_text.split("\n")
    lines = [line.strip() for line in lines if line.strip() != ""]

    if lines and re.match(r'^\d+$', lines[0]):
        lines.pop(0)

    cutoff_index = None
    for idx, line in enumerate(lines):
        if re.match(r'^[-_]{3,}$', line):
            cutoff_index = idx
            break
    if cutoff_index:
        lines = lines[:cutoff_index]

    return "\n".join(lines)

#===========================
# Process PDF
#===========================
def process_pdf(pdf_path):
    chunks = []
    appendix_title = None
    article_buffer = ""
    section_id = 0
    chapter_title = "QUY ĐỊNH"

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            width, height = page.width, page.height
            cropped_page = page.crop((0, TOP_CROP, width, height - BOTTOM_CROP))
            page_text = remove_headers_and_footers(cropped_page)

            appendix_match = re.search(r'PHỤ LỤC\s+[A-Z0-9]+\.?\s+.*', page_text, re.IGNORECASE)
            if appendix_match:
                if article_buffer:
                    section_id += 1
                    chunks.append({
                        "id": str(uuid.uuid4()),
                        "chapter": chapter_title,
                        "section": f"MỤC {section_id:02d}",
                        "appendix": appendix_title,
                        "content": article_buffer.strip()
                    })
                    article_buffer = ""
                appendix_title = appendix_match.group(0).strip().upper()
                page_text = page_text.replace(appendix_title, "")

            article_buffer += "\n" + page_text

            tables = cropped_page.extract_tables()
            for t_idx, table in enumerate(tables, start=1):
                table_title = f"Bảng {page_idx}.{t_idx}"
                table_sentences = table_to_sentences(table, table_title)
                article_buffer += "\n" + "\n".join(table_sentences)

        if article_buffer:
            section_id += 1
            chunks.append({
                "id": str(uuid.uuid4()),
                "chapter": chapter_title,
                "section": f"MỤC {section_id:02d}",
                "appendix": appendix_title,
                "content": article_buffer.strip()
            })

    return chunks

if __name__ == "__main__":
    chunks = process_pdf(PDF_FILE)
    df = pd.DataFrame(chunks)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"✅ Done! Saved {len(chunks)} chunks to {OUTPUT_CSV}")
