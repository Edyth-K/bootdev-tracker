#!/usr/bin/env python3
"""
Auto Git Push Script
Automatically adds, commits, and pushes changes to a GitHub repository.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        # Handle command as list or string
        if isinstance(command, str):
            command_list = command.split()
        else:
            command_list = command
            
        result = subprocess.run(
            command_list,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Error output: {e.stderr}")
        return None, e.stderr

def check_git_repo(repo_path):
    """Check if the directory is a Git repository."""
    git_dir = os.path.join(repo_path, '.git')
    return os.path.exists(git_dir)

def auto_git_push(repo_path=".", commit_message=None, branch="main"):
    """
    Automatically add, commit, and push changes to GitHub.
    
    Args:
        repo_path (str): Path to the repository (default: current directory)
        commit_message (str): Custom commit message (default: auto-generated)
        branch (str): Branch to push to (default: main)
    """
    
    # Check if it's a git repository
    if not check_git_repo(repo_path):
        print(f"Error: {repo_path} is not a Git repository.")
        return False
    
    print(f"Working in repository: {os.path.abspath(repo_path)}")
    
    # Check if there are changes to commit
    stdout, stderr = run_command("git status --porcelain", cwd=repo_path)
    if stdout is None:
        return False
    
    if not stdout:
        print("No changes to commit.")
        return True
    
    print("Changes detected:")
    print(stdout)
    
    # Add all changes
    print("\n1. Adding all changes...")
    stdout, stderr = run_command("git add .", cwd=repo_path)
    if stdout is None:
        return False
    print("✓ Changes added")
    
    # Create commit message if not provided
    if not commit_message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-commit: {timestamp}"
    
    # Commit changes
    print(f"\n2. Committing with message: '{commit_message}'")
    stdout, stderr = run_command(['git', 'commit', '-m', commit_message], cwd=repo_path)
    if stdout is None:
        return False
    print("✓ Changes committed")
    
    # Push to remote repository
    print(f"\n3. Pushing to remote branch '{branch}'...")
    stdout, stderr = run_command(f"git push origin {branch}", cwd=repo_path)
    if stdout is None:
        return False
    print("✓ Changes pushed to GitHub")
    
    print(f"\n🎉 Successfully pushed changes to GitHub!")
    return True

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto Git Push Script")
    parser.add_argument(
        "--path", "-p", 
        default=".", 
        help="Path to the Git repository (default: current directory)"
    )
    parser.add_argument(
        "--message", "-m", 
        help="Custom commit message"
    )
    parser.add_argument(
        "--branch", "-b", 
        default="main", 
        help="Branch to push to (default: main)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be done without actually doing it"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        # Check status only
        if check_git_repo(args.path):
            stdout, stderr = run_command("git status --porcelain", cwd=args.path)
            if stdout:
                print("Changes that would be committed:")
                print(stdout)
            else:
                print("No changes to commit.")
        else:
            print(f"Error: {args.path} is not a Git repository.")
        return
    
    # Run the auto push
    success = auto_git_push(
        repo_path=args.path,
        commit_message=args.message,
        branch=args.branch
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()