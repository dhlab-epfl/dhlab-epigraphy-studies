import re
import os
import glob
import json



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


def corpus_formation(input_dir, output_file):
    files = glob.glob(f"{input_dir}/*.txt")
    page_pattern = re.compile(r"---\s*Page\s*(\d+)\s*---", re.IGNORECASE)
    
    with open(output_file, "w", encoding="utf-8") as out_f:
        for file_path in tqdm(files, desc="Processing files"):
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            splits = page_pattern.split(text)
            
            for i in range(1, len(splits), 2):
                page_number = splits[i].strip()
                page_text = splits[i+1].strip()
                cleaned = clean_text(page_text)
                
                json_line = json.dumps({
                    "file_name": file_name,
                    "page_number": page_number,
                    "cleaned_text": cleaned
                }, ensure_ascii=False)
                
                out_f.write(json_line + "\n")
    
    print(f"JSONL file created: {output_file}")
