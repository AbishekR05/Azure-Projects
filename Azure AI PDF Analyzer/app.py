"""
Streamlit app for PDF upload, image and text extraction using Azure AI (Computer Vision & Document Intelligence)
"""

import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.ai.formrecognizer import DocumentAnalysisClient
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile

# Page config
st.set_page_config(
    page_title="c",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Azure AI PDF Analyzer")
st.markdown("Upload a PDF file. Extracted images and text will be displayed using Azure AI!")


# Sidebar for credentials
st.sidebar.header("⚙️ Azure Settings")
st.sidebar.markdown("**Document Intelligence**")
doc_endpoint = st.sidebar.text_input("Doc Intelligence Endpoint", value="YOUR_DOC_ENDPOINT_HERE", type="default")
doc_api_key = st.sidebar.text_input("Doc Intelligence API Key", value="YOUR_DOC_API_KEY_HERE", type="password")
st.sidebar.markdown("**Computer Vision**")
vision_endpoint = st.sidebar.text_input("Vision Endpoint", value="YOUR_VISION_ENDPOINT_HERE", type="default")
vision_api_key = st.sidebar.text_input("Vision API Key", value="YOUR_VISION_API_KEY_HERE", type="password")
# Main content
st.header("📤 Upload PDF File")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded! Extracting content...")
    # Save PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name

    # Extract images from PDF
    st.subheader("🖼️ Extracted Images from PDF")
    doc = fitz.open(pdf_path)
    image_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Page {page_num+1} - Image {img_index+1}", width=600)
            image_count += 1
            # Optionally: Analyze image with Azure Computer Vision
            if vision_endpoint and vision_api_key:
                try:
                    client = ImageAnalysisClient(endpoint=vision_endpoint, credential=AzureKeyCredential(vision_api_key))
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format or "PNG")
                    image_data = img_byte_arr.getvalue()
                    result = client.analyze(
                        image_data=image_data,
                        visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.OBJECTS]
                    )
                    st.markdown("**Azure Vision Analysis:**")
                    if result.caption:
                        st.info(f"Caption: {result.caption.text} (Confidence: {result.caption.confidence:.1%})")
                    if result.tags:
                        tags_text = ", ".join([f"{tag.name} ({tag.confidence:.0%})" for tag in result.tags.list[:8]])
                        st.write(f"Tags: {tags_text}")
                    if result.objects:
                        st.write("Objects:")
                        for obj in result.objects.list[:5]:
                            st.write(f"- {obj.tags[0].name} ({obj.tags[0].confidence:.0%})")
                except Exception as e:
                    st.warning(f"Azure Vision error: {str(e)}")
    if image_count == 0:
        st.info("No images found in PDF.")

    # Extract text from PDF using Azure Document Intelligence
    st.subheader("📄 Extracted Text from PDF (Azure Document Intelligence)")
    extracted_text = ""
    if doc_endpoint and doc_api_key:
        try:
            form_client = DocumentAnalysisClient(endpoint=doc_endpoint, credential=AzureKeyCredential(doc_api_key))
            with open(pdf_path, "rb") as f:
                poller = form_client.begin_analyze_document("prebuilt-document", document=f)
                result = poller.result()
            for page_idx, page in enumerate(result.pages):
                st.markdown(f"**Page {page_idx+1}:**")
                page_text = " ".join([line.content for line in page.lines])
                st.write(page_text)
                extracted_text += " " + page_text
        except Exception as e:
            st.error(f"Azure Document Intelligence error: {str(e)}")
    else:
        st.warning("Please enter your Azure credentials in the sidebar.")

    # Word count feature
    st.subheader("🔎 Word Occurrence Counter")
    word_query = st.text_input("Enter a word to count in the document:")
    if word_query:
        import re
        # Remove punctuation and special characters for word matching
        words = re.findall(r'\b\w+\b', extracted_text.lower())
        count = sum(1 for w in words if w == word_query.lower())
        st.info(f"The word '{word_query}' occurs {count} times in the document.")

else:
    st.info("👈 Upload a PDF file to get started.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 How to Use")
st.sidebar.markdown("""
1. Enter your Azure AI credentials
2. Upload a PDF file
3. See extracted images and text!
""")
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit & Azure AI")
