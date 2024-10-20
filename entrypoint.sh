#!/bin/sh -l
set -xe 
git config --global --add safe.directory /github/workspace

git update-index --chmod=+x entrypoint.sh

README_PATH=${1:-README.md}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."

python3 main.py 

git pull

# Check if there are changes to commit
if [ -n "$(git status -s)" ]; then  # Use [ ] instead of [[ ]]
    git config --global user.name "github-actions"
    git config --global user.email "github-actions@github.com"
    git add "$README_PATH"    
    git diff --staged
    echo "Pushing changes..."
    git remote set-url origin https://x-access-token:$EMBED_TOKEN@github.com/$GITHUB_REPOSITORY.git
    git commit -m "Update $README_PATH"
    git push origin HEAD:refs/heads/$GITHUB_REF_NAME
else
    echo "No changes to commit."
fi