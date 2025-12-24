# Azure Text Analytics

This project is a Streamlit web application that uses Azure AI services to analyze text. It provides features such as sentiment analysis, entity recognition, and key phrase extraction using Azure's Text Analytics API.

## Features
- Analyze text for sentiment (positive, negative, neutral)
- Extract key phrases from text
- Recognize named entities (people, organizations, locations, etc.)
- Simple and interactive web interface

## Setup
1. **Clone the repository**
2. **Install dependencies**
   - Navigate to the project folder and run:
     ```bash
     pip install -r requirements.txt
     ```
3. **Configure Azure Credentials**
   - Enter your Azure endpoint and API key in the sidebar fields when running the app.

## Running the App
```bash
streamlit run app/app.py
```

## Requirements
- Python 3.8+
- Streamlit
- Azure AI SDKs (see requirements.txt)

## Security
**Do not commit your API keys or endpoints to public repositories.** Use placeholders or environment variables for sensitive information.

## License
MIT
