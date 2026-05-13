import subprocess
import sys
import time

def run_command(command, check=True):
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}:\n{e.stderr}")
        if check:
            sys.exit(1)
        return None

def autopush(commit_message="Auto-update"):
    print("Adding changes...")
    run_command(["git", "add", "."])
    
    status = run_command(["git", "status", "--porcelain"])
    if not status:
        print("No changes to commit. Working tree clean.")
        return
        
    print("Committing changes...")
    run_command(["git", "commit", "-m", commit_message], check=False)
    
    print("Pushing to GitHub...")
    run_command(["git", "push"])
    print("Successfully pushed changes to GitHub.")

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Auto-commit from autopush.py"
    autopush(message)
