# publish_extension.py
import os
import subprocess
import sys

def publish_extension(extension_path, repo_url):
    if not os.path.exists(extension_path):
        print(f"Error: Extension folder '{extension_path}' not found.")
        return

    # Change directory to the extension folder
    os.chdir(extension_path)

    # Initialize git repo if not already
    if not os.path.exists(os.path.join(extension_path, ".git")):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

    # Add all files
    subprocess.run(["git", "add", "."], check=True)

    # Commit changes
    commit_msg = f"Publish {os.path.basename(extension_path)}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    # Push to main branch
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

    print(f"Extension '{extension_path}' published to {repo_url} successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python publish_extension.py <extension_path> <repo_url>")
        sys.exit(1)
    
    ext_path = sys.argv[1]
    repo = sys.argv[2]
    publish_extension(ext_path, repo)
