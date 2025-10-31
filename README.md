# Claude Agent Skills

Repository for Anthropic Claude Skills examples demonstrating how to use Claude's Skills API with both **default skills** (document generation) and **custom skills** (extensible functionality).

## Overview

This project provides two categories of examples:

### Default Anthropic Skills (Document Generation)
Python examples for using Anthropic's built-in Skills API to programmatically generate various document types:

- 📊 **Excel (xlsx)** - Spreadsheets, data tables, charts
- 📽️ **PowerPoint (pptx)** - Presentations, slides
- 📄 **PDF** - Documents, forms, reports
- 📝 **Word (docx)** - Documents, letters, proposals

### Custom Skills Framework
A flexible framework for creating and running your own custom skills:

- 🔧 **Extensible Architecture** - Create custom skills with simple markdown instructions
- 🤖 **Intelligent Selection** - Claude automatically chooses the right skill for the task
- 🔍 **Git Analyzer** - Example custom skill for analyzing Git repositories
- 🛠️ **Tool Integration** - Uses bash tool execution for maximum flexibility

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
   
   Create a `.env` file in the `introduction/` directory:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
   ```
   
   For custom skills, create a `.env` file in the `custom_skills/` directory:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
   SKILLS_STORAGE_PATH=./skills
   ```

## Project Structure

```
claude-agent-skills/
├── introduction/                    # Default Anthropic Skills examples
│   ├── anthropic_client_init.py    # Centralized client initialization
│   ├── anthropic_skills_all.py     # Intelligent skill selection (recommended)
│   ├── anthropic_skill_xlsx.py     # Excel-specific example
│   ├── anthropic_skill_pptx.py     # PowerPoint-specific example
│   ├── anthropic_skill_pdf.py      # PDF-specific example
│   ├── anthropic_skill_docx.py     # Word-specific example
│   ├── file_utils.py               # File download utilities
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # Environment variables (create this)
├── custom_skills/                   # Custom Skills framework
│   ├── run_skill.py                # Custom skill runner
│   ├── .env                        # Environment variables (create this)
│   └── skills/                     # Custom skill definitions
│       └── git-analyzer/           # Example: Git repository analyzer
│           ├── SKILL.md            # Skill instructions
│           └── scripts/            # Skill implementation scripts
│               ├── analyze_repo.py
│               └── get_changed_files.py
├── outputs/                         # Generated files directory
└── README.md                       # This file
```

## Usage

### Part 1: Default Anthropic Skills (Document Generation)

#### Option 1: Intelligent Skill Selection (Recommended)

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

#### Option 2: Skill-Specific Scripts

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

### Part 2: Custom Skills Framework

The custom skills framework allows you to create and run your own skills with custom logic and tools.

#### Running Custom Skills

```bash
cd custom_skills
python run_skill.py "Your request here"
```

**Example with git-analyzer skill:**
```bash
python run_skill.py "Analyze the git repository at C:\Code\my-project"
```

**Features:**
- Automatically loads all skills from the `skills/` directory
- Claude intelligently selects the appropriate skill based on your request
- Each skill is defined by a simple `SKILL.md` markdown file
- Skills can execute bash commands and Python scripts
- Extensible architecture for adding new skills

#### Example: Git Analyzer Skill

The included `git-analyzer` skill demonstrates custom skill capabilities:

**Capabilities:**
- 📊 **Repository Summary** - Recent commits, top contributors, file counts
- 🔍 **Status Check** - Staged, unstaged, and untracked files
- 📈 **Git History** - Analyze commit history and patterns

**Example Usage:**
```bash
# Get repository summary
python run_skill.py "Summarize the git repo at C:\Code\my-project"

# Check uncommitted changes
python run_skill.py "What files have changed in C:\Code\my-project?"

# View recent activity
python run_skill.py "Show me recent commits in C:\Code\my-project"
```

**How It Works:**
1. Claude reads the skill instructions from `SKILL.md`
2. Based on your request, selects appropriate Python scripts
3. Executes scripts via bash tool: `python scripts/analyze_repo.py` or `python scripts/get_changed_files.py`
4. Parses JSON output and presents results in natural language

#### Creating Your Own Custom Skills

To create a new custom skill:

1. **Create a skill directory:**
   ```bash
   mkdir custom_skills/skills/my-skill
   ```

2. **Create a SKILL.md file:**
   ```markdown
   ---
   name: my-skill
   description: Brief description of what your skill does
   ---
   
   # My Custom Skill
   
   [Instructions for Claude on how to use your skill]
   
   ## Instructions
   
   1. Explain when to use this skill
   2. Describe available tools/scripts
   3. Show how to execute commands
   4. Explain how to format responses
   ```

3. **Add implementation scripts (optional):**
   ```bash
   mkdir custom_skills/skills/my-skill/scripts
   # Add your Python scripts, bash scripts, etc.
   ```

4. **Test your skill:**
   ```bash
   python run_skill.py "Request that uses your skill"
   ```

**Skill Structure:**
- `SKILL.md` - Required. Contains instructions for Claude
- `scripts/` - Optional. Contains implementation scripts
- Any other files/directories your skill needs

The custom skill framework automatically loads all skills and lets Claude choose the right one for each request.

## How It Works (Default Skills)

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
✅ **Custom Skills Framework** - Extend Claude with your own capabilities  
✅ **Bash Tool Integration** - Execute commands and scripts dynamically  

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

### Introduction (Default Skills)
- `anthropic` - Official Anthropic Python SDK
- `python-dotenv` - Environment variable management

See `introduction/requirements.txt` for version details.

### Custom Skills
- `anthropic` - Official Anthropic Python SDK
- `python-dotenv` - Environment variable management

Custom skills require only these base dependencies. Individual skills may have additional requirements depending on their implementation.

## API Costs

The Skills API is a **paid service**. You'll be charged based on:
- Token usage (input and output)
- Model used (claude-sonnet-4-5-20250929)

Monitor your usage at [console.anthropic.com](https://console.anthropic.com/)

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure `.env` file exists in the appropriate directory (`introduction/` or `custom_skills/`)
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

### Custom Skills Issues
- Ensure `SKILL.md` file exists in each skill directory
- Verify scripts have proper execution permissions
- Check that required tools (e.g., git) are installed and in PATH
- Review the skill's SKILL.md for specific requirements

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Links

- [Anthropic Console](https://console.anthropic.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Skills API Documentation](https://docs.anthropic.com/en/docs/agents/skills)

## Acknowledgments

This project demonstrates:
- The capabilities of Anthropic's Claude Skills API for programmatic document generation
- A flexible framework for extending Claude with custom skills and tools
- How to combine Claude's intelligence with custom scripts and commands for specialized tasks
