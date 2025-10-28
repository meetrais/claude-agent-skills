import anthropic
import os
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
SKILLS_STORAGE_PATH = os.getenv("SKILLS_STORAGE_PATH", "./skills")

# Validate API key before initializing client
if not ANTHROPIC_API_KEY:
    print("Error: The ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
    print("Please set it in the .env file or as an environment variable.", file=sys.stderr)
    sys.exit(1)

try:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
except anthropic.APIStatusError as e:
    print("--- Anthropic API Error ---", file=sys.stderr)
    print(f"Error initializing Anthropic client: {e.message}", file=sys.stderr)
    print("Please ensure your ANTHROPIC_API_KEY is set correctly.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during client initialization: {e}", file=sys.stderr)
    sys.exit(1)


def load_all_skills(skills_base_dir: str = None) -> dict:
    """
    Loads all available custom skills from the skills directory.
    
    Args:
        skills_base_dir (str): The base directory where all skill folders are stored.
        
    Returns:
        dict: A dictionary mapping skill names to their full instructions.
    """
    if skills_base_dir is None:
        skills_base_dir = SKILLS_STORAGE_PATH
    
    skills = {}
    skills_path = Path(skills_base_dir)
    
    if not skills_path.exists():
        print(f"Error: Skills directory not found at '{skills_path}'", file=sys.stderr)
        return skills
    
    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir():
            skill_md_path = skill_dir / "SKILL.md"
            if skill_md_path.is_file():
                try:
                    with open(skill_md_path, "r", encoding="utf-8") as f:
                        skills[skill_dir.name] = f.read()
                except IOError as e:
                    print(f"Warning: Could not read skill '{skill_dir.name}': {e}", file=sys.stderr)
    
    return skills


def run_all_skills(user_prompt: str, skills_base_dir: str = None) -> None:
    """
    Loads all available custom skills and lets Claude automatically select
    which one(s) to use based on the user's prompt.
    
    Args:
        user_prompt (str): The user's prompt/request.
        skills_base_dir (str): The base directory where all skill folders are stored.
    """
    if skills_base_dir is None:
        skills_base_dir = SKILLS_STORAGE_PATH
    
    # Load all available skills
    available_skills = load_all_skills(skills_base_dir)
    
    if not available_skills:
        print("Error: No skills found in the skills directory.", file=sys.stderr)
        return
    
    # Build the combined prompt with all skills
    skills_section = "\n\n".join([
        f"=== SKILL: {skill_name} ===\n{instructions}"
        for skill_name, instructions in available_skills.items()
    ])
    
    combined_prompt = f"""You have access to the following custom skills. Based on the user's request, automatically select and use the most appropriate skill(s).

{skills_section}

---
User Request: "{user_prompt}"

Based on the user's request above, identify which skill is most appropriate and follow its instructions to complete the task."""

    try:
        print(f"\n{'=' * 80}")
        print("CUSTOM CLAUDE SKILLS - INTELLIGENT SKILL SELECTION")
        print('=' * 80)
        print(f"\nAvailable skills: {', '.join(available_skills.keys())}")
        print("\nProcessing your request...")
        print("   Claude will automatically select the appropriate skill(s)")
        print('=' * 80 + "\n")
        
        # Initialize conversation history
        messages = [
            {
                "role": "user",
                "content": combined_prompt
            }
        ]
        
        # Tool execution loop
        while True:
            message = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                tools=[{"type": "bash_20250124", "name": "bash"}],
                messages=messages
            )
            
            # Check if we need to execute tools
            tool_uses = [block for block in message.content if block.type == "tool_use"]
            
            if not tool_uses:
                # No more tools to execute, print final response
                print("Claude's Response:")
                print('=' * 80)
                for content in message.content:
                    if content.type == "text":
                        print(content.text)
                
                print(f"\n\nToken Usage:")
                print(f"   Input: {message.usage.input_tokens}")
                print(f"   Output: {message.usage.output_tokens}")
                print("\n" + '=' * 80)
                print("Process complete!")
                print('=' * 80 + "\n")
                break
            
            # Execute tools and collect results
            tool_results = []
            for tool_use in tool_uses:
                if tool_use.name == "bash":
                    print(f"\n🔧 Executing: {tool_use.input['command']}")
                    print("-" * 80)
                    
                    import subprocess
                    try:
                        # Execute the bash command
                        result = subprocess.run(
                            tool_use.input["command"],
                            shell=True,
                            capture_output=True,
                            text=True,
                            cwd=os.getcwd()
                        )
                        output = result.stdout if result.returncode == 0 else result.stderr
                        print(output)
                        print("-" * 80)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": output
                        })
                    except Exception as e:
                        error_msg = f"Error executing command: {str(e)}"
                        print(error_msg)
                        print("-" * 80)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": error_msg,
                            "is_error": True
                        })
            
            # Add assistant's response and tool results to conversation
            messages.append({
                "role": "assistant",
                "content": message.content
            })
            messages.append({
                "role": "user",
                "content": tool_results
            })

    except anthropic.APIStatusError as e:
        print("\n--- Anthropic API Error ---", file=sys.stderr)
        print(f"An error occurred while communicating with the Claude API: {e.message}", file=sys.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)


def main():
    """
    Main function to parse command-line arguments and orchestrate the skill execution.
    """
    parser = argparse.ArgumentParser(
        description="Run custom Claude Skills with intelligent skill selection. Claude will automatically choose the best skill for your request.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "prompt",
        help="Your request/prompt (e.g., 'Summarize the repo at C:\\Code\\my-project')."
    )
    args = parser.parse_args()

    run_all_skills(args.prompt)


if __name__ == "__main__":
    main()
