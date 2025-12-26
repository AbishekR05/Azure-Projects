# Azure Vision AI Streamlit Demo

This project demonstrates how to use Azure's Vision AI service to analyze images using a simple Streamlit web app.

## Features
- Upload an image and get:
  - Description
  - Tags
  - Detected objects
  - Categories
  - Dominant colors

## Setup
1. Install requirements:
	```bash
	pip install -r requirements.txt
	```
2. Set your Azure Vision endpoint and key in Streamlit secrets (or edit in code):
	- `.streamlit/secrets.toml`:
	  ```toml
	  AZURE_VISION_ENDPOINT = "https://<your-endpoint>.cognitiveservices.azure.com/"
	  AZURE_VISION_KEY = "<your-key>"
	  ```
3. Run the app:
	```bash
	streamlit run app.py
	```

## Requirements
- Streamlit
- requests
- Pillow

## Notes
- You need an Azure Vision AI resource and key. [Get started here.](https://portal.azure.com/)
