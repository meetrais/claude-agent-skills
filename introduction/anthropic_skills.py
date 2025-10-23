import os
import sys
import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Import our file utilities
from file_utils import (
    download_all_files,
    download_file,
    extract_file_ids,
    get_file_info,
    print_download_summary,
)

# Load environment variables from parent directory
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found.")

# Initialize client
# Note: We'll add beta headers per-request when using Skills
client = Anthropic(api_key=API_KEY)

# Create outputs directory if it doesn't exist
OUTPUT_DIR = Path.cwd().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

print("✓ API key loaded")
print(f"✓ Using model: {MODEL}")
print(f"✓ Output directory: {OUTPUT_DIR}")
print("\n📝 Note: Beta headers will be added per-request when using Skills")

# Simple test to verify API connection
test_response = client.messages.create(
    model=MODEL,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Say 'Connection successful!' if you can read this.",
        }
    ],
)

print("API Test Response:")
print(test_response.content[0].text)
print(
    f"\n✓ Token usage: {test_response.usage.input_tokens} in, {test_response.usage.output_tokens} out"
)

### How Skills Work with Code Execution
#Skills require the **code execution** tool to be enabled. Here's the typical workflow:
# Use client.beta.messages.create() for Skills support
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Create an Excel file..."}],
    # Use betas parameter instead of extra_headers
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# List all available Anthropic skills
# Note: Skills API requires the skills beta header
client_with_skills_beta = Anthropic(
    api_key=API_KEY, default_headers={"anthropic-beta": "skills-2025-10-02"}
)

skills_response = client_with_skills_beta.beta.skills.list(source="anthropic")

print("Available Anthropic-Managed Skills:")
print("=" * 80)

for skill in skills_response.data:
    print(f"\n📦 Skill ID: {skill.id}")
    print(f"   Title: {skill.display_title}")
    print(f"   Latest Version: {skill.latest_version}")
    print(f"   Created: {skill.created_at}")

    # Get version details
    try:
        version_info = client_with_skills_beta.beta.skills.versions.retrieve(
            skill_id=skill.id, version=skill.latest_version
        )
        print(f"   Name: {version_info.name}")
        print(f"   Description: {version_info.description}")
    except Exception as e:
        print(f"   (Unable to fetch version details: {e})")

print(f"\n\n✓ Found {len(skills_response.data)} Anthropic-managed skills")

# Create an Excel budget spreadsheet
excel_response = client.beta.messages.create(  # Note: Using beta.messages for Skills support
    model=MODEL,
    max_tokens=4096,
    container={
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": """Create a monthly budget Excel spreadsheet with the following:

Income:
- Salary: $5,000
- Freelance: $1,200
- Investments: $300

Expenses:
- Rent: $1,500
- Utilities: $200
- Groceries: $600
- Transportation: $300
- Entertainment: $400
- Savings: $1,000

Include:
1. Formulas to calculate total income and total expenses
2. A formula for net savings (income - expenses)
3. Format currency values properly
4. Add a simple column chart showing income vs expenses
5. Use professional formatting with headers
""",
        }
    ],
    # Use betas parameter for beta features
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)

print("Excel Response:")
print("=" * 80)
for content in excel_response.content:
    if content.type == "text":
        print(content.text)
    elif content.type == "tool_use":
        print(f"\n🔧 Tool: {content.name}")
        if hasattr(content, "input"):
            print(f"   Input preview: {str(content.input)[:200]}...")

print("\n\n📊 Token Usage:")
print(f"   Input: {excel_response.usage.input_tokens}")
print(f"   Output: {excel_response.usage.output_tokens}")


#Download excel file

# Extract file IDs from the response
file_ids = extract_file_ids(excel_response)

if file_ids:
    print(f"✓ Found {len(file_ids)} file(s)\n")

    # Download all files
    results = download_all_files(
        client, excel_response, output_dir=str(OUTPUT_DIR), prefix="budget_"
    )

    # Print summary
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
    print("\nDebug: Response content types:")
    for i, content in enumerate(excel_response.content):
        print(f"  {i}. {content.type}")