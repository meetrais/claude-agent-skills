import subprocess
import argparse
import json
import os
import sys

def run_git_command(command: list, repo_path: str) -> str:
    """Runs a Git command in a specified repository path and returns its output."""
    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError(f"Error: 'git' command not found. Is Git installed and in your PATH?")
    except subprocess.CalledProcessError as e:
        # This error is common if the path is not a git repo
        raise RuntimeError(f"Error executing command {' '.join(command)}: {e.stderr.strip()}")

def analyze_repository(repo_path: str) -> dict:
    """
    Analyzes a Git repository and returns a dictionary of structured data.
    """
    if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, '.git')):
        return {"error": f"The provided path '{repo_path}' is not a valid Git repository."}

    try:
        # 1. Get top 5 recent commits
        commit_log_raw = run_git_command(
            ['git', 'log', '-n', '5', '--pretty=format:%h||%an||%ar||%s'],
            repo_path
        )
        recent_commits = []
        for line in commit_log_raw.splitlines():
            parts = line.split('||')
            if len(parts) == 4:
                recent_commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "date_relative": parts[2],
                    "message": parts[3]
                })

        # 2. Get top 3 contributors
        contributors_raw = run_git_command(
            ['git', 'shortlog', '-sn', '--all'],
            repo_path
        )
        top_contributors = []
        for line in contributors_raw.splitlines()[:3]:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                top_contributors.append({
                    "commits": int(parts[0]),
                    "name": parts[1]
                })

        # 3. Get total file count
        file_count_raw = run_git_command(['git', 'ls-files'], repo_path)
        file_count = len(file_count_raw.splitlines())

        return {
            "repo_path": repo_path,
            "file_count": file_count,
            "recent_commits": recent_commits,
            "top_contributors": top_contributors
        }

    except RuntimeError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a local Git repository.")
    parser.add_argument("repo_path", help="The local file path to the Git repository.")
    args = parser.parse_args()

    analysis_result = analyze_repository(args.repo_path)
    # Print the result as a single JSON string
    print(json.dumps(analysis_result, indent=2))
