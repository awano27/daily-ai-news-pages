#!/usr/bin/env python3
import subprocess
import os

# Change to the project directory
os.chdir(r'C:\Users\yoshitaka\daily-ai-news')

try:
    # Add files to git
    print("Adding files to git...")
    result = subprocess.run(['git', 'add', '.github/workflows/deploy-pages.yml', '.nojekyll', 'requirements.txt'], 
                          capture_output=True, text=True, check=True)
    print("Files added successfully")
    
    # Commit changes
    print("Committing changes...")
    result = subprocess.run(['git', 'commit', '-m', 'feat: Add GitHub Actions workflow for automatic Pages deployment'], 
                          capture_output=True, text=True, check=True)
    print("Changes committed successfully")
    print("Commit output:", result.stdout)
    
    # Push changes
    print("Pushing to origin main...")
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                          capture_output=True, text=True, check=True)
    print("Changes pushed successfully")
    print("Push output:", result.stdout)
    
except subprocess.CalledProcessError as e:
    print(f"Git command failed with error: {e}")
    print(f"Error output: {e.stderr}")
    print(f"Standard output: {e.stdout}")
    
    # If push fails, try pulling first
    if 'push' in str(e.cmd):
        try:
            print("Attempting to pull first...")
            pull_result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                       capture_output=True, text=True, check=True)
            print("Pull successful, trying push again...")
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, text=True, check=True)
            print("Push successful after pull")
        except subprocess.CalledProcessError as pull_error:
            print(f"Pull/Push retry failed: {pull_error}")
            print(f"Pull error output: {pull_error.stderr}")

print("Script completed")