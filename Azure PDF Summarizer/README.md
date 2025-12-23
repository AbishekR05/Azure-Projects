# Azure PDF Summarizer

This Streamlit app allows you to upload PDF files, extract text using Azure Document Intelligence (with OCR support), and summarize the document using the Azure Language service (Text Analytics SDK). The summary is provided as a downloadable PDF.

## Features
- Upload PDF files
- Extract text from all pages (including scanned/image-based PDFs)
- Summarize the document using Azure Language (Text Analytics SDK)
- Download the summary as a PDF file

## How to Use
1. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Enter your Azure endpoints and API keys for Document Intelligence and Language services in the sidebar.
4. Upload a PDF file.
5. View extracted text and summary. Download the summary as a PDF.

## Required Azure Services
- **Azure Document Intelligence**: For extracting text from PDFs (supports OCR for scanned/image-based documents)
- **Azure Language Service (Text Analytics SDK)**: For document summarization

## Dependencies
See `requirements.txt` for all required Python modules:
- streamlit
- azure-core
- azure-ai-formrecognizer
- azure-ai-textanalytics
- fpdf
- fitz
- PyMuPDF

## Output
- Extracted text from all PDF pages
- Abstractive summary of the document
- Downloadable PDF containing the summary

## Author
This project was generated with GitHub Copilot (GPT-4.1).
