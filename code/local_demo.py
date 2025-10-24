import requests
import fitz  # Import PyMuPDF library

# === 1. Read PDF ===
pdf_path = r"D:/UCLA/Quarter 1/RELLI-Program/data/Health Wealth Fund I Offering Memorandum.pdf"
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

# Optional: Save extracted text to a file for review
# try:
#     with open("extracted_text_output.txt", "w", encoding="utf-8") as f:
#         f.write(text_content)
#     print("💡 INFO: Extracted text has been saved to 'extracted_text_output.txt' for review.")
# except Exception as e:
#     print(f"⚠️ WARNING: Could not save extracted text to file. Error: {e}")

# === 2. Question (Prompt) ===
question = """
Your task is to act as a highly specialized data extraction robot. Your **only** function is to find four specific pieces of information from the provided text and format them into a single line. Ignore all other data points, no matter how relevant they seem.

**== ABSOLUTE OUTPUT REQUIREMENTS ==**

1.  Your entire response **MUST** be on a single line. There must be no newline characters.
2.  The response format **MUST** be exactly: `Target Return: [value], Minimum: [value], Hold Period: [value]`
3.  You **MUST NOT** include any keys other than the four specified above (e.g., no "Preferred Return", "Equity Required", etc.).
4.  If a value for any of the four required keys is not found, you **MUST** use the word `Unknown` in its place.
5.  Your response **MUST NOT** contain any explanations, apologies, or introductory text.

**== DATA EXTRACTION RULES ==**

* **"Target Return"**: Find the target return (often called IRR).
    * If it's a range (e.g., "16-20%"), extract **only the maximum value**.
    * The final output **MUST** be a string formatted as a percentage with two decimal places (e.g., "20.00%").

* **"Minimum"**: Find the minimum investment amount.
    * The final output **MUST** be a string starting with a dollar sign and using commas for thousands (e.g., "$100,000").

* **"Hold Period"**: Find the hold period.
    * You **MUST** convert this value to months.
    * If it is a range (e.g., "3-5 years"), take the **maximum value** (5 years) and then convert it to months (outputting "60 Months").

Your final output must be a single line that perfectly matches the required format.
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
    response = requests.post(url, json=payload, timeout=300)  # Increased timeout for large processing

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