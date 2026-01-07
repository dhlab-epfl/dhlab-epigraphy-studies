import pandas as pd
import numpy as np
import re 
import os
import glob
import json
import seaborn as sns
import matplotlib.pyplot as plt
import math

def load_extractions_from_dir(directory: str) -> pd.DataFrame:
    records = []

    for file in os.listdir(directory):
        if file.endswith(".json"):  # only JSON files
            filepath = os.path.join(directory, file)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)  # load full JSON

            # walk through terms → extractions
            for term_entry in data.get("terms", []):
                for occ in term_entry.get("extractions", []):
                    records.append({
                        "dict_term": term_entry.get("term"),
                        "definition": term_entry.get("definition"),
                        "term": occ.get("term"),
                        "context": occ.get("context"),
                        "file_name": occ.get("file_name"),
                        "page_number": occ.get("page_number"),
                        "source_file": file,
                    })

    return pd.DataFrame(records)



def split_arm_sentence(text):
    """
    Splits a paragraph into sentences using only Armenian full stop (։)
    """
    # Replace line breaks with spaces
    text = text.replace("\n", " ").replace("\r", " ")
    
    # Split by Armenian full stop
    sentences = [s.strip() for s in text.split('։') if s.strip()]
    
    return sentences



def create_ner_dataset(df: pd.DataFrame, output_name: str, complete: bool = True):
    dataset = []

    for _, row in df.iterrows():
        text = str(row['cleaned_text'])
        sentences = split_arm_sentence(text)

        term = row['term']
        context = row['context']
        page_number = row['page_number']
        file_name = row.get('file_name', None)  # safer access

        for sentence in sentences:
            input_text = sentence
            output_entities = []

            if term and not (isinstance(term, float) and math.isnan(term)):
                if str(term) in sentence or (context and str(context) in sentence):
                    output_entities.append(f"{term}: type of inscription")

            output_text = ", ".join(output_entities) if output_entities else ""

            entry = {"input": input_text, "output": output_text, "page_number": page_number}
            if complete and file_name:
                entry["file_name"] = file_name

            dataset.append(entry)

    # Save to JSONL
    with open(output_name, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Dataset created! Total rows: {len(dataset)}, saved to {output_name}")
