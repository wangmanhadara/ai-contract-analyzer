import os
import json
from google import genai

def get_client():
    project = os.environ["PROJECT_ID"]
    location = os.environ.get("VERTEX_LOCATION", "us-central1")
    return genai.Client(vertexai=True, project=project, location=location)

def generate_structured_json(prompt: str) -> dict:
    client = get_client()
    model = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    text = (resp.text or "").strip()

    # If the model still wraps JSON, attempt to strip it safely.
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        text = text.replace("json", "", 1).strip()

    return json.loads(text)
