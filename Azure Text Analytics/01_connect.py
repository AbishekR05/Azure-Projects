from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

endpoint = "<YOUR_ENDPOINT_HERE>"
key = "<YOUR_API_KEY_HERE>"

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

print("Connected to Text Analytics service.")
print("Client successfully created:", client)

documents = [
    "I had a wonderful experience! The rooms were clean and the staff was helpful.","The food was terrible and the waiter was rude."]
response = client.recognize_entities(documents=documents)

for idx, doc in enumerate(response):
    print(f"\nDocument {idx + 1} entities:")
    for entity in doc.entities:
        print(f" - Entity: {entity.text}, Category: {entity.category}, Confidence Score: {entity.confidence_score}")