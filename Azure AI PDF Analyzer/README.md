# Azure AI PDF Analyzer

This project is a Streamlit web application that leverages Azure AI services to analyze PDF documents. It extracts text from uploaded PDFs and provides insights such as sentiment analysis, entity recognition, and key phrase extraction using Azure's AI capabilities.

## Features
- Upload PDF files for analysis
- Extract text from PDFs using Azure Document Intelligence
- Analyze extracted text with Azure Language Service
- Display sentiment, entities, and key phrases

## Setup
1. **Clone the repository**
2. **Install dependencies**
   - Navigate to the project folder and run:
     ```bash
     pip install -r requirements.txt
     ```
3. **Configure Azure Credentials**
   - Add your Azure endpoints and API keys in the sidebar fields when running the app.

## Running the App
```bash
streamlit run app.py
```

## Requirements
- Python 3.8+
- Streamlit
- Azure AI SDKs (see requirements.txt)

## Security
**Do not commit your API keys or endpoints to public repositories.** Use placeholders or environment variables for sensitive information.

## License
MIT
