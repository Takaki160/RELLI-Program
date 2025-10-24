import os
import types
import fitz  # Import the PyMuPDF library
from google.genai import Client as GenAIClient # Renamed to avoid confusion

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Opens and reads a PDF file, extracting all its text content.

    Args:
        pdf_path: The file path to the PDF document.

    Returns:
        A string containing the text content of all pages, or an empty string if an error occurs.
    """
    text_content = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text()
                text_content += str(page_text) if page_text else ""
        print(f"✅ Successfully extracted PDF text")
        return text_content
    except FileNotFoundError:
        print(f"❌ ERROR: File path not found: {pdf_path}")
        return ""
    except Exception as e:
        print(f"❌ Error reading PDF with PyMuPDF: {e}")
        return ""

def call_gemini_model(prompt_content: str, model_name: str) -> str:
    """
    Sends a prompt to the Google Gemini API using the Client object and returns its response.

    Args:
        prompt_content: The full prompt string to send to the model.
        model_name: The name of the Gemini model to use (e.g., "gemini-1.5-flash").

    Returns:
        The model's response text, or an error message if the call fails.
    """
    try:
        # Initialize the GenAI Client with the API key
        client = GenAIClient(api_key="your google gemini api key")

        # Define generation config for deterministic output
        generation_config = {
            "temperature": 0.0,
            "top_p": 0.1
        }

        print(f"📡 Calling Google Gemini API ({model_name}), please wait...")

        # Send the request using the client
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_content,
            config=generation_config
        )

        # Return the model's text response
        return response.text.strip()

    except Exception as e:
        return f"❌ An error occurred while calling the Gemini API: {e}"

def main():
    """
    Main function to orchestrate the entire PDF extraction and model query process.
    """
    # === 1. Configuration ===
    pdf_path = r"D:/UCLA/Quarter 1/RELLI-Program/data/SIG III Brochure.pdf"
    model_name = "gemini-2.5-flash"
    max_content_length = 15000

    # === 2. Extract Text from PDF ===
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        return

    # === 3. Define Question and Construct Prompt (This part remains the same) ===
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
    prompt_content = f"{question}\n\n--- PDF Content Follows (Truncated to first {max_content_length} characters):---\n{pdf_text[:max_content_length]}"

    # === 4. Call the Google Gemini Model ===
    result = call_gemini_model(prompt_content, model_name)

    # === 5. Output the Result ===
    print("=============================================")
    print("✅ Model Extraction Result (Using Google Gemini):")
    print(result)
    print("=============================================")

if __name__ == "__main__":
    main()