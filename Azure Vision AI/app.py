# Azure Vision AI Streamlit Demo
import streamlit as st
from PIL import Image
import requests
import io

st.set_page_config(page_title="Azure Vision AI Demo", layout="centered")
st.title("Azure Vision AI Demo")
st.write("""
This app demonstrates Azure's Vision AI capabilities. Upload an image to analyze it using Azure's Vision AI service.
""")

# Azure Vision AI endpoint and key (replace with your own)
AZURE_VISION_ENDPOINT = st.secrets["AZURE_VISION_ENDPOINT"] if "AZURE_VISION_ENDPOINT" in st.secrets else "https://<your-endpoint>.cognitiveservices.azure.com/"
AZURE_VISION_KEY = st.secrets["AZURE_VISION_KEY"] if "AZURE_VISION_KEY" in st.secrets else "<your-key>"

def analyze_image(image_bytes):
	url = AZURE_VISION_ENDPOINT + "/vision/v3.2/analyze?visualFeatures=Description,Tags,Objects,Categories,Color"
	headers = {
		"Ocp-Apim-Subscription-Key": AZURE_VISION_KEY,
		"Content-Type": "application/octet-stream"
	}
	response = requests.post(url, headers=headers, data=image_bytes)
	if response.status_code == 200:
		return response.json()
	else:
		st.error(f"Error: {response.status_code} - {response.text}")
		return None

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
	image = Image.open(uploaded_file)
	st.image(image, caption="Uploaded Image", use_column_width=True)
	st.write("Analyzing image...")
	image_bytes = uploaded_file.read()
	result = analyze_image(image_bytes)
	if result:
		st.subheader("Analysis Results")
		if "description" in result and "captions" in result["description"]:
			captions = result["description"]["captions"]
			if captions:
				st.write(f"**Description:** {captions[0]['text']} (Confidence: {captions[0]['confidence']:.2f})")
		if "tags" in result:
			st.write(f"**Tags:** {', '.join(result['tags'])}")
		if "objects" in result:
			st.write(f"**Objects Detected:** {', '.join([obj['object'] for obj in result['objects']])}")
		if "categories" in result:
			st.write(f"**Categories:** {', '.join([cat['name'] for cat in result['categories']])}")
		if "color" in result:
			st.write(f"**Dominant Colors:** {', '.join(result['color']['dominantColors'])}")
