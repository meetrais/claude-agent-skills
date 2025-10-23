import os
from pathlib import Path
from anthropic import Anthropic
from anthropic_client_init import client
from file_utils import (
    download_all_files,
    extract_file_ids,
    get_file_info,
    print_download_summary,
)

# Get configuration from environment
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

# Create outputs directory if it doesn't exist
OUTPUT_DIR = Path.cwd().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Create a PDF receipt
pdf_response = client.beta.messages.create(
    model=MODEL,
    max_tokens=4096,
    container={
        "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": """Create a simple receipt PDF:

RECEIPT

Acme Corporation
Date: January 15, 2025
Receipt #: RCT-2025-001

Customer: Jane Smith

Items:
- Product A: $50.00
- Product B: $75.00
- Product C: $25.00

Subtotal: $150.00
Tax (8%): $12.00
Total: $162.00

Thank you for your business!

Use simple, clean formatting with clear sections.
""",
        }
    ],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)

print("PDF Response:")
print("=" * 80)
for content in pdf_response.content:
    if content.type == "text":
        print(content.text)

print("\n\n📊 Token Usage:")
print(f"   Input: {pdf_response.usage.input_tokens}")
print(f"   Output: {pdf_response.usage.output_tokens}")

# Download the PDF file
file_ids = extract_file_ids(pdf_response)

if file_ids:
    results = download_all_files(
        client, pdf_response, output_dir=str(OUTPUT_DIR), prefix="receipt_"
    )

    print_download_summary(results)

    # Verify PDF integrity
    for result in results:
        if result["success"]:
            file_path = result["output_path"]
            file_size = result["size"]

            # Basic PDF validation
            with open(file_path, "rb") as f:
                header = f.read(5)
                if header == b"%PDF-":
                    print(f"\n✅ PDF file is valid: {file_path}")
                    print(f"   File size: {file_size / 1024:.1f} KB")
                else:
                    print(f"\n⚠️ File may not be a valid PDF: {file_path}")
else:
    print("❌ No files found in response")