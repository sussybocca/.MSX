import os
import subprocess
import sys

# List of suspicious keywords to scan for in extension files
SUSPICIOUS_KEYWORDS = ["os.system", "subprocess.Popen", "eval", "exec", "open(", "requests"]

def scan_for_malicious_code(extension_path):
    print(f"Scanning '{extension_path}' for potentially malicious code...")
    issues_found = False

    for root, _, files in os.walk(extension_path):
        for file in files:
            if file.endswith((".py", ".msx", ".js")):  # adjust extensions as needed
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for keyword in SUSPICIOUS_KEYWORDS:
                            if keyword in content:
                                print(f"⚠ Suspicious keyword '{keyword}' found in {file_path}")
                                issues_found = True
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

    if issues_found:
        print("Warning: Potentially unsafe code detected. Review before publishing.")
    else:
        print("No obvious malicious code found.")

def publish_extension(extension_path, repo_url):
    if not os.path.exists(extension_path):
        print(f"Error: Extension folder '{extension_path}' not found.")
        return

    # Scan extension for suspicious code
    scan_for_malicious_code(extension_path)

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
