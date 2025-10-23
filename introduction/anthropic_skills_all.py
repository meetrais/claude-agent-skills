import os
import sys
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

print("\n" + "=" * 80)
print("ANTHROPIC CLAUDE SKILLS - INTELLIGENT SKILL SELECTION")
print("=" * 80)
print("\nClaude will automatically select the best skill(s) for your request:")
print("  📊 Excel (xlsx) - Spreadsheets, data tables, charts")
print("  📽️ PowerPoint (pptx) - Presentations, slides")
print("  📄 PDF - Documents, forms, reports")
print("  📝 Word (docx) - Documents, letters, proposals")
print("\n" + "=" * 80)

# Get user's prompt
user_prompt = input("\nEnter your request (what you want Claude to create): ").strip()

if not user_prompt:
    print("❌ No prompt provided!")
    sys.exit(1)

print("\n" + "=" * 80)
print("🚀 Processing your request...")
print("   Claude will automatically select the appropriate skill(s)")
print("=" * 80)

# Make the API call with ALL skills available
# Claude will intelligently choose which skill(s) to use based on the user's prompt
response = client.beta.messages.create(
    model=MODEL,
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"},
            {"type": "anthropic", "skill_id": "pdf", "version": "latest"},
            {"type": "anthropic", "skill_id": "docx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)

print("\n🤖 Claude's Response:")
print("=" * 80)
for content in response.content:
    if content.type == "text":
        print(content.text)
    elif content.type == "tool_use":
        print(f"\n🔧 Tool Used: {content.name}")

print("\n\n📊 Token Usage:")
print(f"   Input: {response.usage.input_tokens}")
print(f"   Output: {response.usage.output_tokens}")

# Download generated file(s)
file_ids = extract_file_ids(response)

if file_ids:
    print(f"\n✓ Found {len(file_ids)} file(s)\n")

    # Download all files with blank prefix
    results = download_all_files(
        client, response, output_dir=str(OUTPUT_DIR), prefix=""
    )

    # Print summary
    print_download_summary(results)

    # Show file details
    for file_id in file_ids:
        info = get_file_info(client, file_id)
        if info:
            print(f"\n📄 File Details:")
            print(f"   Filename: {info['filename']}")
            print(f"   Size: {info['size'] / 1024:.1f} KB")
            print(f"   Created: {info['created_at']}")
            print(f"   Location: {OUTPUT_DIR}")
else:
    print("\n❌ No files found in response")
    print("\nDebug: Response content types:")
    for i, content in enumerate(response.content):
        print(f"  {i}. {content.type}")

print("\n" + "=" * 80)
print("✅ Process complete!")
print("=" * 80 + "\n")
