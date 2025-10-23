# Claude Agent Skills

Repository for Anthropic Claude Skills examples demonstrating how to use Claude's Skills API to generate Excel spreadsheets, PowerPoint presentations, PDF documents, and Word documents.

## Overview

This project provides Python examples for using Anthropic's Skills API to programmatically generate various document types:

- 📊 **Excel (xlsx)** - Spreadsheets, data tables, charts
- 📽️ **PowerPoint (pptx)** - Presentations, slides
- 📄 **PDF** - Documents, forms, reports
- 📝 **Word (docx)** - Documents, letters, proposals

## Prerequisites

### Required

1. **Anthropic API Key** (required for all examples)
   - Visit [console.anthropic.com](https://console.anthropic.com/)
   - Create an account or log in
   - Navigate to "API Keys" section
   - Generate a new API key
   - Ensure your account has access to Skills beta features
   - **Note**: This is separate from Claude Code/Cline subscriptions

2. **Python 3.7+**

### Important Note About Claude Code Pro

Having a Claude Code Pro subscription does **NOT** provide access to the Anthropic Skills API. These are separate services:

- **Claude Code Pro** = VS Code extension subscription (interactive development)
- **Anthropic API Key** = Programmatic API access (separate service, separate billing)

You need an Anthropic API key to run the code in this repository, regardless of your Claude Code subscription.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/meetrais/claude-agent-skills.git
   cd claude-agent-skills
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd introduction
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
   ```

## Project Structure

```
claude-agent-skills/
├── introduction/
│   ├── anthropic_client_init.py    # Centralized client initialization
│   ├── anthropic_skills_all.py     # Intelligent skill selection (recommended)
│   ├── anthropic_skill_xlsx.py     # Excel-specific example
│   ├── anthropic_skill_pptx.py     # PowerPoint-specific example
│   ├── anthropic_skill_pdf.py      # PDF-specific example
│   ├── anthropic_skill_docx.py     # Word-specific example
│   ├── file_utils.py               # File download utilities
│   └── requirements.txt            # Python dependencies
├── outputs/                         # Generated files directory
├── .env                            # Environment variables (create this)
└── README.md                       # This file
```

## Usage

### Option 1: Intelligent Skill Selection (Recommended)

Use `anthropic_skills_all.py` - Claude automatically selects the appropriate skill based on your request:

```bash
cd introduction
python anthropic_skills_all.py
```

**Example interaction:**
```
Enter your request: Create a quarterly sales report spreadsheet

🚀 Processing your request...
   Claude will automatically select the appropriate skill(s)
```

Claude will intelligently choose the xlsx skill and create your spreadsheet.

**Features:**
- All 4 skills available in one script
- Claude automatically selects the right skill
- Single-line input (press Enter once)
- Files saved with original names (no prefix)
- Automatic file download to `outputs/` directory

### Option 2: Skill-Specific Scripts

Run individual skill examples:

**Excel Spreadsheet:**
```bash
python anthropic_skill_xlsx.py
```

**PowerPoint Presentation:**
```bash
python anthropic_skill_pptx.py
```

**PDF Document:**
```bash
python anthropic_skill_pdf.py
```

**Word Document:**
```bash
python anthropic_skill_docx.py
```

## How It Works

### Client Initialization

All scripts import a shared client from `anthropic_client_init.py`:

```python
from anthropic_client_init import client
```

This centralized initialization:
- Loads environment variables
- Creates authenticated Anthropic client
- Tests API connection
- Lists available skills

### Skills API Call

The intelligent skill selector (`anthropic_skills_all.py`) provides all skills to Claude:

```python
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
    messages=[{"role": "user", "content": user_prompt}],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

Claude intelligently selects which skill to use based on the context of your request.

## Features

✅ **Intelligent Skill Selection** - Claude chooses the right tool for the job  
✅ **Automatic File Download** - Generated files saved to outputs directory  
✅ **Comprehensive Output** - See Claude's reasoning and token usage  
✅ **Shared Client** - Centralized initialization for all scripts  
✅ **File Details** - View filename, size, and creation date  
✅ **Error Handling** - Debug information when files aren't generated  

## Output Files

All generated files are saved to the `outputs/` directory with their original names:

```
outputs/
├── monthly_budget.xlsx
├── presentation.pptx
├── report.pdf
└── proposal.docx
```

## Dependencies

- `anthropic` - Official Anthropic Python SDK
- `python-dotenv` - Environment variable management

See `introduction/requirements.txt` for version details.

## API Costs

The Skills API is a **paid service**. You'll be charged based on:
- Token usage (input and output)
- Model used (claude-sonnet-4-5-20250929)

Monitor your usage at [console.anthropic.com](https://console.anthropic.com/)

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify the API key is correctly formatted
- Check that `python-dotenv` is installed

### "500 Internal Server Error"
- This is an Anthropic API server-side issue
- Try again later
- Check Anthropic status page
- Report persistent issues to Anthropic support

### Skills not working
- Verify your account has beta access to Skills features
- Ensure you're using the correct model version
- Check that all beta flags are included in the API call

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Links

- [Anthropic Console](https://console.anthropic.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Skills API Documentation](https://docs.anthropic.com/en/docs/agents/skills)

## Acknowledgments

This project demonstrates the capabilities of Anthropic's Claude Skills API for programmatic document generation.
