import requests
import fitz  # Import PyMuPDF library

# === 1. Read PDF ===
pdf_path = r"D:/UCLA/Quarter 1/RELLI-Program/Career Accelerator Program - Relli.pdf"
text_content = ""

try:
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            text_content += str(page_text) if page_text else ""
    print("✅ PDF text extraction with PyMuPDF complete.")

except FileNotFoundError:
    print(f"❌ ERROR: File path not found: {pdf_path}")
    exit()
except Exception as e:
    # This will catch PyMuPDF-specific errors as well
    print(f"❌ Error reading PDF with PyMuPDF: {e}")
    exit()

# === 2. Question (Prompt) ===
question = """
The following PDF content is in **English**.
Please extract and summarize the timeline information (Timeline) found in the English content.
The timeline typically includes start and end dates for semesters, event timings, and registration or exam deadlines.

**Please strictly follow the output requirements below. This is crucial for consistency:**
1. Output **only** a single line of content.
2. **Strictly** start the output with “Timeline: ”.
3. **Do not** output any extra explanations, greetings, or additional text.

**Example Output Format:**
Timeline: 09/2023-06/2024 (Fall)

**If no timeline is found, strictly respond with:**
Timeline: Unknown
"""

# Limit PDF content length to prevent token overflow
max_content_length = 15000  # Corresponds to 4096 tokens approximately
prompt_content = f"{question}\n\n--- PDF Content Follows (Truncated to first {max_content_length} characters):---\n{text_content[:max_content_length]}"


# === 3. Call Ollama Local Model ===
url = "http://localhost:11434/api/generate"
model_name = "llama3.1:latest"

payload = {
    "model": model_name,
    "prompt": prompt_content,
    "stream": False,
    # === Critical Consistency Configuration ===
    "options": {
        "temperature": 0.0, # Set to 0.0 to enforce the highest-probability token selection, eliminating randomness
        "top_p": 0.1,       # Restrict sampling range, helps stability (less impact when T=0)
        "num_ctx": 4096      # Assuming your model supports a 4k context size
    }
}

print(f"📡 Calling Ollama ({model_name}), please wait...")
print(f"📡 Using Temperature: {payload['options']['temperature']}")

try:
    response = requests.post(url, json=payload, timeout=120)

    # === 4. Output Result ===
    if response.status_code == 200:
        data = response.json()
        print("\n=============================================")
        print("✅ Model Extraction Result (Consistency Settings Applied):")
        # Extract and clean up model response
        response_text = data.get("response", "").strip()
        print(response_text)
        print("=============================================")
    else:
        print(f"\n❌ Call Failed: HTTP Status Code {response.status_code}")
        print(f"❌ Details: {response.text}")
        # Check for common error: model not found
        if "model '" in response.text and "' not found" in response.text:
            print("\n💡 TIP: Please check if the 'llama3.1:latest' model is installed and running in Ollama.")

except requests.exceptions.RequestException as e:
    print(f"\n❌ Failed to connect to Ollama. Please ensure:")
    print(f"1. The Ollama service is running at 'http://localhost:11434'.")
    print(f"2. Error details: {e}")