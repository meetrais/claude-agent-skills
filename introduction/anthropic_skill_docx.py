
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

# Create a Word document report
docx_response = client.beta.messages.create(
    model=MODEL,
    max_tokens=4096,
    container={
        "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": "Write a one page report on the benefits of renewable energy"
        }
    ],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)

print("Word Document Response:")
print("=" * 80)
for content in docx_response.content:
    if content.type == "text":
        print(content.text)

print("\n\n📊 Token Usage:")
print(f"   Input: {docx_response.usage.input_tokens}")
print(f"   Output: {docx_response.usage.output_tokens}")

# Download the Word document
file_ids = extract_file_ids(docx_response)

if file_ids:
    print(f"\n✓ Found {len(file_ids)} file(s)\n")

    results = download_all_files(
        client, docx_response, output_dir=str(OUTPUT_DIR), prefix="report_"
    )

    print_download_summary(results)

    # Show file details
    for file_id in file_ids:
        info = get_file_info(client, file_id)
        if info:
            print("\n📄 File Details:")
            print(f"   Filename: {info['filename']}")
            print(f"   Size: {info['size'] / 1024:.1f} KB")
            print(f"   Created: {info['created_at']}")
else:
    print("❌ No files found in response")
