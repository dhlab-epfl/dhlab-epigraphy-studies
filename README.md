# Armenian Epigraphy NLP Pipeline

This repository contains a research-oriented NLP pipeline for processing Armenian epigraphic corpora, extracting structured inscription data, and detecting inscription-type terminology using Named Entity Recognition (NER).

The project focuses on OCR-heavy, layout-complex historical sources and low-resource Armenian language settings.

## Repository Structure

- `Generated_data/`  
  Model outputs, predictions, and GT-labeled results

- `Inference/`  
  Contains `Inference.ipynb` for running trained models on unseen data

- `Notebooks/`  
  Experimental notebooks for training and evaluation. This is an aggregation of all the work that has been done. Main Folder to look at.

- `dataset_formation/`  
  Dataset construction, IOB tagging, and train/dev/test splits

- `preprocessing/`  
  OCR cleaning, paragraph restructuring, and sentence splitting

- `images/`  
  Figures used for analysis and reporting

- `corpus_inscription_terms.xlsx`  
  Expert-curated list of Armenian inscription-type terminology


## Main Features

- OCR-aware text cleaning and restructuring  
- Rule-based inscription extraction with metadata  
- GPT-assisted ground-truth generation (JSON via Pydantic)  
- NER training with:
  - spaCy baseline
  - Transformer models (mBERT, XLM-RoBERTa, Armenian-specific)
- Evaluation on seen vs unseen terminology

## Typical Workflow

1. Preprocess OCR text (`preprocessing/`)
2. Form NER-ready datasets (`dataset_formation/`)
3. Train and evaluate models (`Notebooks/`)
4. Run inference on new corpora (`Inference/`)
5. Inspect outputs (`Generated_data/`)

## Scope & Limitations

- Strong generalization to known inscription types in new contexts
- Limited discovery of entirely unseen terminology
- Designed as a research prototype, not a production system

## Use Cases

- Digital epigraphy
- Cultural heritage digitization
- Low-resource NLP research
- Historical corpus structuring

## License

See `LICENSE` for details.
