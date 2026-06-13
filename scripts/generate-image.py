#!/usr/bin/env python3
"""
Generate an image using Google's Gemini image generation API.

Usage:
    python3 generate-image.py "A retro-futuristic landing page mockup with neon accents" output.png

Requirements:
    - GEMINI_API_KEY environment variable set
    - Google AI Studio account with billing enabled
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3.1-flash-image-preview"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def generate_image(prompt: str, output_path: str):
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)

    url = f"{API_URL}?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error (HTTP {e.code}):")
        try:
            err_json = json.loads(error_body)
            print(json.dumps(err_json, indent=2))
        except json.JSONDecodeError:
            print(error_body)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    # Extract image data from response
    candidates = data.get("candidates", [])
    if not candidates:
        print("Error: No candidates in response.")
        print(json.dumps(data, indent=2))
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    image_data = None
    text_response = None

    for part in parts:
        if "inlineData" in part:
            image_data = part["inlineData"].get("data")
        elif "text" in part:
            text_response = part["text"]

    if image_data:
        image_bytes = base64.b64decode(image_data)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"Image saved to: {output_path}")
        if text_response:
            print(f"Model notes: {text_response}")
    else:
        print("Error: No image data found in response.")
        if text_response:
            print(f"Model response: {text_response}")
        print("Full response:")
        print(json.dumps(data, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate-image.py \"<prompt>\" <output.png>")
        print("Example: python3 generate-image.py \"A minimalist dashboard UI\" dashboard.png")
        sys.exit(1)

    prompt_text = sys.argv[1]
    output_file = sys.argv[2]
    generate_image(prompt_text, output_file)
