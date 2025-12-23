"""
Streamlit app for PDF upload, text extraction using Azure Document Intelligence, and summarization using Azure Language service.
"""

import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import fitz  # PyMuPDF
import io
import tempfile
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Page config
st.set_page_config(
    page_title="Azure PDF Summarizer",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Azure PDF Summarizer")
st.markdown("Upload a PDF file. Extracted text and summary will be displayed using Azure AI!")

# Sidebar for credentials
st.sidebar.header("⚙️ Azure Settings")
st.sidebar.markdown("**Document Intelligence**")
doc_endpoint = st.sidebar.text_input("Doc Intelligence Endpoint", value="<YOUR_DOC_ENDPOINT_HERE>", type="default")
doc_api_key = st.sidebar.text_input("Doc Intelligence API Key", value="<YOUR_DOC_API_KEY_HERE>", type="password")
st.sidebar.markdown("**Language Service**")
language_endpoint = st.sidebar.text_input("Language Endpoint", value="<YOUR_LANGUAGE_ENDPOINT_HERE>", type="default")
language_api_key = st.sidebar.text_input("Language API Key", value="<YOUR_LANGUAGE_API_KEY_HERE>", type="password")

# Main content
st.header("📤 Upload PDF File")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

extracted_text = ""

if uploaded_file:
    st.success("PDF uploaded! Extracting content...")
    # Save PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name

    # Extract text from PDF using Azure Document Intelligence
    st.subheader("📄 Extracted Text from PDF")
    if doc_endpoint and doc_api_key:
        try:
            form_client = DocumentAnalysisClient(endpoint=doc_endpoint, credential=AzureKeyCredential(doc_api_key))
            with open(pdf_path, "rb") as f:
                poller = form_client.begin_analyze_document("prebuilt-read", document=f)
                result = poller.result()
            st.info(f"Total pages detected: {len(result.pages)}")
            for page_idx, page in enumerate(result.pages):
                st.markdown(f"**Page {page_idx+1}:**")
                if page.lines:
                    page_text = " ".join([line.content for line in page.lines])
                    st.write(page_text)
                    extracted_text += " " + page_text
                else:
                    st.warning("No text extracted from this page.")
        except Exception as e:
            st.error(f"Azure Document Intelligence error: {str(e)}")
    else:
        st.warning("Please enter your Document Intelligence credentials in the sidebar.")

    # Summarize extracted text using Azure Language service (Text Analytics SDK)
    st.subheader("📝 Document Summary (Azure Language)")
    if language_endpoint and language_api_key and extracted_text.strip():
        try:
            # Use Azure Text Analytics SDK for summarization
            text_analytics_client = TextAnalyticsClient(endpoint=language_endpoint, credential=AzureKeyCredential(language_api_key))
            documents = [extracted_text[:4000]]
            poller = text_analytics_client.begin_abstract_summary(documents, model_version="latest")
            result = list(poller.result())
            if result and result[0].summaries:
                summary = " ".join([s.text for s in result[0].summaries])
                st.success(summary)
                # Create a new PDF with the summary
                from fpdf import FPDF
                pdf_summary_path = tempfile.NamedTemporaryFile(delete=False, suffix="_summary.pdf").name
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in summary.split('\n'):
                    pdf.multi_cell(0, 10, line)
                pdf.output(pdf_summary_path)
                with open(pdf_summary_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Summary PDF",
                        data=pdf_file.read(),
                        file_name="document_summary.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("No summary generated.")
        except Exception as e:
            st.error(f"Azure Language error: {str(e)}")
    elif not (language_endpoint and language_api_key):
        st.info("Enter your Language API credentials to get a summary.")
    elif not extracted_text.strip():
        st.info("No text extracted to summarize.")
else:
    st.info("👈 Upload a PDF file to get started.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 How to Use")
st.sidebar.markdown("""
1. Enter your Azure AI credentials
2. Upload a PDF file
3. See extracted text and summary!
""")
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit & Azure AI")
