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
        raise RuntimeError(f"Error executing command {' '.join(command)}: {e.stderr.strip()}")

def get_changed_files(repo_path: str) -> dict:
    """
    Checks the status of a Git repository, including uncommitted and staged files.
    """
    if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, '.git')):
        return {"error": f"The provided path '{repo_path}' is not a valid Git repository."}

    try:
        # Get staged files (for commit)
        staged_files_raw = run_git_command(['git', 'diff', '--name-only', '--cached'], repo_path)
        staged_files = staged_files_raw.splitlines()

        # Get unstaged files (not yet added)
        unstaged_files_raw = run_git_command(['git', 'diff', '--name-only'], repo_path)
        unstaged_files = unstaged_files_raw.splitlines()
        
        # Get untracked files
        untracked_files_raw = run_git_command(['git', 'ls-files', '--others', '--exclude-standard'], repo_path)
        untracked_files = untracked_files_raw.splitlines()

        return {
            "repo_path": repo_path,
            "staged_files": staged_files,
            "unstaged_files": unstaged_files,
            "untracked_files": untracked_files
        }

    except RuntimeError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the status of a local Git repository.")
    parser.add_argument("repo_path", help="The local file path to the Git repository.")
    args = parser.parse_args()

    status_result = get_changed_files(args.repo_path)
    print(json.dumps(status_result, indent=2))
