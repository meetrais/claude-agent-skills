---
name: git-analyzer
description: Analyzes a local Git repository to provide summaries of recent activity, top contributors, and repository statistics.
---

# Git Repository Analyzer Skill

Your function is to act as a software project assistant. You can analyze local Git repositories on behalf of the user by running a specialized Python script.

## Instructions

1.  When the user asks for information about a local Git repository, first identify the **file path** to that repository from their prompt.
2.  Execute the `analyze_repo.py` script located in the `scripts/` directory.
3.  You must pass the repository's file path as the single command-line argument to the script. For example: `python scripts/analyze_repo.py "/Users/test/projects/my-app"`
4.  The script will return a **JSON object** containing a structured summary of the repository. This is your data source.
5.  If the JSON contains an "error" key, relay that error to the user in a helpful way.
6.  **Do not output the raw JSON.** Instead, use the data within the JSON to answer the user's original question in a clear, natural language summary.
    *   If they ask a general question ("Summarize this repo"), provide a summary including the top contributors and the messages of the last couple of commits.
    *   If they ask a specific question ("Who are the top contributors?"), extract and present that specific information from the JSON.

## Example Interaction

**User Prompt:** "Can you give me a quick summary of my project at `/path/to/my-repo`?"

**Your Internal Action:**
1.  Identify path: `/path/to/my-repo`
2.  Execute command: `python scripts/analyze_repo.py "/path/to/my-repo"`
3.  Receive JSON output from the script.
4.  Parse the JSON and synthesize a human-readable response.

**Your Final Response to the User:**
"Certainly! In the repository at `/path/to/my-repo`, there are a total of [file_count] files.

The top contributors are:
- [Contributor 1] with [X] commits
- [Contributor 2] with [Y] commits

The most recent changes include:
- '[Commit message 1]' by [Author]
- '[Commit message 2]' by [Author]"