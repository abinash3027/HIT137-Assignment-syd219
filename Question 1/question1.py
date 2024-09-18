import pandas as pd
from collections import Counter
import csv
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import spacy
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Function to read and process text in chunks to avoid memory issues
def process_text_in_chunks(filename, chunk_size=1000):
    with open(filename, 'r') as infile:
        while True:
            # Read a chunk of lines
            lines = infile.readlines(chunk_size)
            if not lines:
                break
            yield ''.join(lines)


# Function to split a long text into smaller chunks with a maximum number of tokens
def split_into_token_chunks(text, tokenizer, max_length=512):
    tokens = tokenizer.tokenize(text)
    # Split the tokens into chunks of the maximum allowed size
    for i in range(0, len(tokens), max_length):
        yield tokens[i:i + max_length]


# Task 1: Extract 'text' column from CSVs and save to a single .txt file
csv_files = ['CSV1.csv', 'CSV2.csv', 'CSV3.csv', 'CSV4.csv']

# Open a text file to store all the extracted text
with open('combined_text.txt', 'w') as outfile:
    for csv_file in csv_files:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Check if 'SHORT-TEXT' or 'TEXT' column exists and extract the appropriate column
        if 'SHORT-TEXT' in df.columns:
            texts = df['SHORT-TEXT'].tolist()
        elif 'TEXT' in df.columns:
            texts = df['TEXT'].tolist()
        else:
            print(f"Neither 'SHORT-TEXT' nor 'TEXT' found in {csv_file}")
            continue

        # Write each text into the output file
        for text in texts:
            outfile.write(text + '\n')


# Task 3.2: Use Hugging Face to extract unique tokens and save to a text file
def extract_unique_tokens(text_file, chunk_size=1000, output_file='unique_tokens.txt'):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    unique_tokens = set()  # Use a set to store unique tokens

    # Process the text file in chunks
    for chunk in process_text_in_chunks(text_file, chunk_size=chunk_size):
        tokens = tokenizer.tokenize(chunk)
        unique_tokens.update(tokens)  # Add tokens to the set (automatically removes duplicates)

    # Save the unique tokens to a separate text file
    with open(output_file, 'w') as file:
        for token in unique_tokens:
            file.write(f"{token}\n")

    return unique_tokens


# Extract unique tokens and save to 'unique_tokens.txt'
unique_tokens = extract_unique_tokens('combined_text.txt', chunk_size=1000, output_file='unique_tokens.txt')

# Print the number of unique tokens
print(f"Total unique tokens extracted: {len(unique_tokens)}")

# Task 4: Named-Entity Recognition (NER)

# Load SpaCy models
nlp_sci = spacy.load("en_core_sci_sm")
nlp_bc5cdr = spacy.load("en_ner_bc5cdr_md")


# Extract entities using SpaCy
def extract_entities_spacy(model, text_file, chunk_size=1000):
    entities = []

    # Process the text file in chunks to avoid memory overload
    for chunk in process_text_in_chunks(text_file, chunk_size=chunk_size):
        doc = model(chunk)
        entities.extend([(ent.text, ent.label_) for ent in doc.ents])

    return entities


# Extract entities with both SpaCy models
entities_sci = extract_entities_spacy(nlp_sci, 'combined_text.txt')
entities_bc5cdr = extract_entities_spacy(nlp_bc5cdr, 'combined_text.txt')

# Separate diseases and drugs for both models
diseases_sci = [ent for ent in entities_sci if ent[1] == 'DISEASE']
drugs_sci = [ent for ent in entities_sci if ent[1] == 'DRUG']
diseases_bc5cdr = [ent for ent in entities_bc5cdr if ent[1] == 'DISEASE']
drugs_bc5cdr = [ent for ent in entities_bc5cdr if ent[1] == 'DRUG']

# Print results for SpaCy
print("Diseases detected by en_core_sci_sm:", diseases_sci)
print("Drugs detected by en_core_sci_sm:", drugs_sci)
print("Diseases detected by en_ner_bc5cdr_md:", diseases_bc5cdr)
print("Drugs detected by en_ner_bc5cdr_md:", drugs_bc5cdr)

# BioBERT using Hugging Face
tokenizer_biobert = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
model_biobert = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
ner_pipeline_biobert = pipeline("ner", model=model_biobert, tokenizer=tokenizer_biobert)


# Extract entities using BioBERT
def extract_biobert_entities(text_file, chunk_size=1000):
    entities = []
    # Process the text in chunks
    for chunk in process_text_in_chunks(text_file, chunk_size=chunk_size):
        for token_chunk in split_into_token_chunks(chunk, tokenizer_biobert, max_length=512):
            text_chunk = tokenizer_biobert.convert_tokens_to_string(token_chunk)
            entities.extend(ner_pipeline_biobert(text_chunk))

    return entities


# Extract entities with BioBERT
biobert_entities = extract_biobert_entities('combined_text.txt')

# Print BioBERT entities
print("Entities detected by BioBERT:", biobert_entities)
