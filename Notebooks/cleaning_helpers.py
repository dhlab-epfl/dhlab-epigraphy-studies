import re
import pandas as pd

def clean_armenian_text(text: str) -> str:
    # 1) Split text into pages (keep page numbers)
    pages = re.split(r"(---\s*Page\s+\d+\s*---)", text, flags=re.IGNORECASE)

    cleaned_pages = []

    for page in pages:
        page = page.strip()
        if not page:
            continue

        # If this is a page marker, keep as its own paragraph
        if re.match(r"---\s*Page\s+\d+\s*---", page, flags=re.IGNORECASE):
            cleaned_pages.append(page)
            continue

        # Otherwise, clean the page content
        
        # Fix hyphenated line breaks
        page = re.sub(r'-\n\s*', '', page)

        # Force paragraph breaks before lines starting with special markers
        page = re.sub(r'\n(?=(Հրատ\.|Ծանոթ\.))', r'\n\n', page)

        # Split lines to detect ALL CAPS blocks
        lines = page.splitlines()
        cleaned_lines = []
        valid_pattern = re.compile(r"^[Ա-Ֆ0-9\s\.\-,:;#\[\]\(\)]+$")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                cleaned_lines.append("")
                i += 1
                continue

            # Check if this line starts an ALL CAPS block
            if valid_pattern.match(line):
                block = [line]
                i += 1
                while i < len(lines) and valid_pattern.match(lines[i].strip()):
                    block.append(lines[i].strip())
                    i += 1
                cleaned_lines.append("\n".join(block))
            else:
                # Normal text: merge lines until next blank line
                normal_para = [line]
                i += 1
                while i < len(lines) and lines[i].strip() and not valid_pattern.match(lines[i].strip()):
                    normal_para.append(lines[i].strip())
                    i += 1
                # Flatten single newlines into spaces
                para_text = " ".join(normal_para)
                para_text = re.sub(r'\s{2,}', ' ', para_text)
                cleaned_lines.append(para_text)

        cleaned_pages.append("\n\n".join(cleaned_lines))

    # Reassemble all pages with double newlines
    return "\n\n".join(cleaned_pages)


def clean_file(input_path: str, output_path: str):
    # Read original text
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean it
    cleaned_text = clean_armenian_text(text)

    # Write new cleaned file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Cleaned file saved as: {output_path}")


def is_all_caps_armenian(line: str) -> bool:
    armenian_letters = re.findall(r'[Ա-Ֆա-ֆ]', line)
    if not armenian_letters:
        return False
    upper_count = sum(1 for ch in armenian_letters if ch.isupper())
    return upper_count / len(armenian_letters) > 0.8

def split_paragraph_custom(paragraph: str) -> list:
    n = len(paragraph)
    start = 0
    i = 0
    sentences = []
    while i < n:
        if paragraph[i] == ':':
            end = i + 1
            sentences.append(paragraph[start:end].strip())
            start = end
            i = end
            continue
        if paragraph[i:i+2] == '..':
            end = i + 2
            sentences.append(paragraph[start:end].strip())
            start = end
            i = end
            continue
        if paragraph[i] == '։':
            j = i + 1
            while j < n and paragraph[j].isspace():
                j += 1
            boundary = False
            if j >= n:
                boundary = True
            else:
                if paragraph[j].isupper():
                    boundary = True
            if boundary:
                end = i + 1
                sentences.append(paragraph[start:end].strip())
                start = end
                i = end
                continue
        i += 1
    if start < n:
        sentences.append(paragraph[start:].strip())
    return [s for s in sentences if s and not is_all_caps_armenian(s)]

def process_txt_file(filename: str) -> pd.DataFrame:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    pages = re.split(r'--- Page (\d+) ---', content)
    rows = []
    for i in range(1, len(pages), 2):
        page_num = int(pages[i])
        page_text = pages[i+1].strip()
        paragraphs = [p for p in page_text.split("\n\n") if p.strip()]
        for p in paragraphs:
            sents = split_paragraph_custom(p)
            rows.extend((page_num, s) for s in sents)
    return pd.DataFrame(rows, columns=["page", "sentence"])


def clean_text(text):
    text = text.lower()
    
    # Remove line breaks
    text = text.replace("\n", " ").replace("\r", " ")
    
    # Remove sequences of special characters longer than 3
    text = re.sub(r"[^\w\s]{4,}", " ", text)
    
    # Keep only Armenian letters + spaces
    text = re.sub(r"[^\u0530-\u058F\s]", " ", text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text).strip()
    
    return text