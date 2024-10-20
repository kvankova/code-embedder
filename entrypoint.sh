#!/bin/sh -l
set -xe 
git config --global --add safe.directory /github/workspace

git update-index --chmod=+x entrypoint.sh

README_PATH=${1:-README.md}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."
echo "[*] GITHUB_TOKEN=${GITHUB_TOKEN}"
echo "[*] GITHUB_REPOSITORY=${GITHUB_REPOSITORY}"

python3 main.py 

# Check if there are changes to commit
if [ -n "$(git status -s)" ]; then  # Use [ ] instead of [[ ]]
    git config --global user.name "github-actions"
    git config --global user.email "github-actions@github.com"
    git add "$README_PATH"
    echo "Pushing changes..."
    git commit -m "Update $README_PATH"
    git push origin HEAD 
else
    echo "No changes to commit."
fi