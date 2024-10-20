#!/bin/sh -l
set -xe 

git add entrypoint.sh
git update-index --chmod=+x entrypoint.sh
git config --global --add safe.directory /github/workspace

README_PATH=${1:-README.md}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."

python3 main.py 

# Check if there are changes to commit
if [ -n "$(git status -s)" ]; then  # Use [ ] instead of [[ ]]
    git config --global user.name "github-actions"
    git config --global user.email "github-actions@github.com"
    echo "Changes to commit:"
    git add "$README_PATH"
    git remote set-url origin https://x-access-token:${{ secrets.EMBED_TOKEN }}@github.com/${{ github.repository }}
    echo "Pushing changes..."
    git commit -m "Update $README_PATH"
    git push origin HEAD 
else
    echo "No changes to commit."
fi