import streamlit as st
import pandas as pd
from datasets import load_dataset

# Load the dataset from Hugging Face Hub
dataset = load_dataset("Appz7/t5-metadata-extraction-dataset3")
df = dataset['train'].to_pandas()

# Function to get metadata based on PDF filename
def get_metadata_for_pdf(pdf_name):
    # Search for the PDF filename in the dataset
    result = df[df['pdf_file_name'] == pdf_name]
    
    if not result.empty:
        # Return the metadata (target_text) for the matched PDF
        return result['target_text'].values[0]
    else:
        # Return a message if the PDF filename is not found
        return "Unable to find metadata"

# Streamlit UI
st.title("PDF Metadata Extractor")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Get the uploaded file name
    pdf_filename = uploaded_file.name
    st.write(f"Uploaded PDF: {pdf_filename}")

    # Get the metadata for the PDF
    metadata = get_metadata_for_pdf(pdf_filename)

    # Display the metadata
    st.subheader("Extracted Metadata:")
    st.write(metadata)
