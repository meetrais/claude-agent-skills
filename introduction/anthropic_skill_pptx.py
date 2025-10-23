import os
from pathlib import Path
from anthropic import Anthropic
from anthropic_client_init import client
from file_utils import (
    download_all_files,
    extract_file_ids,
    print_download_summary,
)

# Get configuration from environment
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

# Create outputs directory if it doesn't exist
OUTPUT_DIR = Path.cwd().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Create a PowerPoint presentation
pptx_response = client.beta.messages.create(
    model=MODEL,
    max_tokens=4096,
    container={
        "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": """Create a simple 2-slide PowerPoint presentation:

Slide 1: Title slide
- Title: "Q3 2025 Results"
- Subtitle: "Acme Corporation"

Slide 2: Revenue Overview
- Title: "Quarterly Revenue"
- Add a simple column chart showing:
  - Q1: $12M
  - Q2: $13M
  - Q3: $14M

Use clean, professional formatting.
""",
        }
    ],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)

print("PowerPoint Response:")
print("=" * 80)
for content in pptx_response.content:
    if content.type == "text":
        print(content.text)

print("\n\n📊 Token Usage:")
print(f"   Input: {pptx_response.usage.input_tokens}")
print(f"   Output: {pptx_response.usage.output_tokens}")

# Download the PowerPoint file
file_ids = extract_file_ids(pptx_response)

if file_ids:
    results = download_all_files(
        client, pptx_response, output_dir=str(OUTPUT_DIR), prefix="q3_review_"
    )

    print_download_summary(results)

    print("\n✅ Open the presentation in PowerPoint or Google Slides to view!")
else:
    print("❌ No files found in response")