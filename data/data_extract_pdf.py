import pdfplumber
import re
import uuid
import pandas as pd

PDF_FILE = "../Data_pdf/QCDT_2023.pdf"
OUTPUT_CSV = "../Chunks/chuong_dieu_structured.csv"

TOP_CROP = 50 
BOTTOM_CROP = 70 

CHUONG_REGEX = re.compile(r'CHƯƠNG\s+[IVXLCDM]+\s+.*', re.IGNORECASE)
DIEU_REGEX = re.compile(r'Điều\s+\d+\.\s+.*')

#=====================================
# Xử lý bảng: điền None và chuyển thành câu
# =====================================
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

# =====================================
# Loại bỏ header/footer và footnotes
# =====================================
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

# =====================================
# Xử lý toàn bộ PDF
# =====================================
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

            if "Quy chế" not in page_text and not current_chuong:
                continue

            chuong_match = CHUONG_REGEX.search(page_text)
            if chuong_match:
                save_article(chunks, current_chuong, current_dieu, article_buffer)
                article_buffer = ""
                current_dieu = None
                current_chuong = chuong_match.group(0)
                page_text = page_text.replace(current_chuong, "")

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

# =====================================
# Chạy và xuất kết quả
# =====================================
if __name__ == "__main__":
    # Xử lý PDF file chính
    chunks = process_pdf(PDF_FILE)

    # Xuất ra CSV
    df = pd.DataFrame(chunks)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')

    print(f"✅ Hoàn tất! Đã lưu {len(chunks)} điều vào {OUTPUT_CSV}")
