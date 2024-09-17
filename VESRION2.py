import streamlit as st
import pandas as pd
from datasets import load_dataset
import requests
from bs4 import BeautifulSoup

# Load the dataset from Hugging Face Hub
dataset = load_dataset("Appz7/t5-metadata-extraction-dataset3")
df = dataset['train'].to_pandas()

# Function to extract metadata from DOI using requests and BeautifulSoup
def extract_metadata_from_doi(doi):
    try:
        # Send a GET request to the DOI page
        doi_link = f"https://doi.org/{doi}"
        response = requests.get(doi_link)

        # Parse the page source
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata from the page
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else "Title not found"

        # Extract abstract (can vary in location on the page)
        abstract_tag = soup.find('div', {'class': 'abstract'}) or soup.find('section', {'class': 'abstract'})
        abstract = abstract_tag.get_text().strip() if abstract_tag else "Abstract not found"

        # Attempt to extract authors, published date, and publisher
        authors_tag = soup.find('meta', {'name': 'citation_author'})
        authors = authors_tag['content'] if authors_tag else "Authors not found"

        published_date_tag = soup.find('meta', {'name': 'citation_publication_date'})
        published_date = published_date_tag['content'] if published_date_tag else "Publication date not found"

        publisher_tag = soup.find('meta', {'name': 'citation_publisher'})
        publisher = publisher_tag['content'] if publisher_tag else "Publisher not found"

        return f"Title: {title}\nAuthors: {authors}\nPublished Date: {published_date}\nPublisher: {publisher}\nAbstract: {abstract}"

    except Exception as e:
        return f"Error extracting metadata: {str(e)}"

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
st.set_page_config(page_title="Unified Information Retrieval from Diverse Publication Formats")

# Add custom styles for the background and text color
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;
    }
    .css-18e3th9 {
        padding: 20px 40px;
    }
    .stRadio > div {
        display: flex;
        flex-direction: row;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title with an icon at the top
icon_path = "https://as1.ftcdn.net/v2/jpg/04/03/43/28/1000_F_403432800_GB7ZccxkrSnqBHABDMVHfmBYFhM5mBBs.jpg" # Path to the uploaded icon file
st.image(icon_path, width=100)  # Display the icon with a specified width
st.title("Unified Information Retrieval from Diverse Publication Formats")

# Let the user choose between PDF or DOI (radio buttons side by side)
option = st.radio("Choose input method:", ("Upload a PDF", "Enter DOI"))

if option == "Upload a PDF":
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

elif option == "Enter DOI":
    # Text input for DOI
    doi = st.text_input("Enter the DOI for the PDF:")

    if doi:
        # Extract metadata from the DOI page
        doi_metadata = extract_metadata_from_doi(doi)

        # Display the extracted metadata
        st.subheader("Extracted Metadata:")
        st.write(doi_metadata)
