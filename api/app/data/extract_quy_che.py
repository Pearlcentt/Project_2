import pdfplumber
import re
import uuid
import pandas as pd

PDF_FILE = "raw/Quy_che_2023.pdf"
OUTPUT_CSV = "processed/quy_che_2023_structured.csv"

PDF_FILE2 = "raw/Quy_che_2018.pdf"
OUTPUT_CSV2 = "processed/quy_che_2018_structured.csv"

TOP_CROP = 50 
BOTTOM_CROP = 70 

DIEU_REGEX = re.compile(r'Điều\s+\d+\.\s+.*')
CHUONG_REGEX = re.compile(r'CHƯƠNG\s+[IVXLCDM]+\s+.*', re.IGNORECASE)

def fill_none_with_above(table):
    for row_idx in range(1, len(table)):
        for col_idx in range(len(table[row_idx])):
            cell_value = table[row_idx][col_idx]
            if not cell_value or str(cell_value).strip() == "":
                table[row_idx][col_idx] = table[row_idx - 1][col_idx]
    return table

def table_to_sentences(table, table_title="Bảng"):
    sentences = []
    table = fill_none_with_above(table)
    headers = table[0]

    for row_idx, row in enumerate(table[1:], start=1):
        row_desc = []
        for col_idx, cell in enumerate(row):
            header = headers[col_idx] or f"Cột {col_idx + 1}"
            row_desc.append(f"{header} là {cell}")
        full_sentence = f"{table_title} ({row_idx}): " + "; ".join(row_desc) + "."
        sentences.append(full_sentence)

    return sentences

def remove_headers_and_footers(cropped_page, page_number):
    raw_text = cropped_page.extract_text()

    if not raw_text:
        return ""

    lines = raw_text.split("\n")
    while lines and re.match(r'^\s*(Page|Trang)?\s*\d+\s*$', lines[0]):
        lines.pop(0)

    if lines and re.search(r'(BỘ GIÁO DỤC|ĐẠI HỌC BÁCH KHOA|QUY CHẾ)', lines[0], re.IGNORECASE):
        lines.pop(0)

    cutoff_index = None
    for idx, line in enumerate(lines):
        if re.match(r'^\s*[-_]{3,}\s*$', line):
            cutoff_index = idx
            break

    if cutoff_index is not None:
        lines = lines[:cutoff_index]

    lines = [line.strip() for line in lines if line.strip() != ""]

    return "\n".join(lines)

def clean_footnotes(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\(\d+\)', '', text)
    text = re.sub(r'\s\d+\s', ' ', text)
    text = re.sub(r'\s\d+\n', '\n', text)
    return text.strip()

def save_article(chunks, chuong_title, dieu_title, article_buffer):
    if not article_buffer.strip():
        return
    chunks.append({
        "id": str(uuid.uuid4()),
        "chuong": chuong_title,
        "dieu": dieu_title,
        "content": article_buffer.strip()
    })

def process_pdf(pdf_path):
    chunks = []
    current_chuong = None
    current_dieu = None
    article_buffer = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            width, height = page.width, page.height
            cropped_page = page.crop((0, TOP_CROP, width, height - BOTTOM_CROP))
            page_text = remove_headers_and_footers(cropped_page, page_idx)

            lines = page_text.split("\n")
            for i in range(len(lines) - 1):
                line = lines[i].strip()
                next_line = lines[i + 1].strip()

                chuong_only_match = re.match(r'^CHƯƠNG\s+([IVXLCDM]+)$', line, re.IGNORECASE)
                chuong_fallback_match = re.match(r'^([IVXLCDM]+)\s*[-.]\s*(.+)', line, re.IGNORECASE)

                if chuong_only_match:
                    roman = chuong_only_match.group(1)
                    full_chuong = f"CHƯƠNG {roman} {next_line}".upper()
                elif chuong_fallback_match:
                    roman = chuong_fallback_match.group(1)
                    title = chuong_fallback_match.group(2)
                    full_chuong = f"CHƯƠNG {roman} {title}".upper()
                else:
                    continue

                save_article(chunks, current_chuong, current_dieu, article_buffer)
                article_buffer = ""
                current_dieu = None
                current_chuong = full_chuong
                break

            page_text = "\n".join(lines)

            dieu_matches = list(DIEU_REGEX.finditer(page_text))
            if dieu_matches:
                for idx, match in enumerate(dieu_matches):
                    save_article(chunks, current_chuong, current_dieu, article_buffer)
                    article_buffer = ""
                    current_dieu = match.group(0)
                    start = match.end()
                    if idx + 1 < len(dieu_matches):
                        end = dieu_matches[idx + 1].start()
                    else:
                        end = len(page_text)
                    article_buffer = page_text[start:end]
            else:
                if current_dieu:
                    article_buffer += "\n" + page_text

            tables = cropped_page.extract_tables()
            for t_idx, table in enumerate(tables, start=1):
                table_title = f"{page_idx} - {t_idx}"
                table_sentences = table_to_sentences(table, table_title)
                if current_dieu:
                    article_buffer += "\n" + "\n".join(table_sentences)

        save_article(chunks, current_chuong, current_dieu, article_buffer)

    return chunks

if __name__ == "__main__":
    chunks = process_pdf(PDF_FILE)
    df = pd.DataFrame(chunks)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    chunks2 = process_pdf(PDF_FILE2)
    df2 = pd.DataFrame(chunks2)
    df2.to_csv(OUTPUT_CSV2, index=False, encoding='utf-8-sig')
    print(f"✅ Hoàn tất! Đã lưu {len(chunks)} điều vào {OUTPUT_CSV}")
    print(f"✅ Hoàn tất! Đã lưu {len(chunks2)} điều vào {OUTPUT_CSV2}")