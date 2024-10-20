#!/bin/sh -l
set -xe 
git config --global --add safe.directory /github/workspace
git update-index --chmod=+x entrypoint.sh
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git remote set-url origin https://x-access-token:$EMBED_TOKEN@github.com/$GITHUB_REPOSITORY.git
git fetch origin 

README_PATH=${1:-README.md}
BRANCH_NAME=${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."

python3 main.py 

git checkout $BRANCH_NAME
git pull

# Check if there are changes to commit
if [ -n "$(git status -s)" ]; then  
    git add "$README_PATH"    
    git diff --staged

    echo "Pushing changes..."
    
    git commit -m "Update $README_PATH"
    git push
else
    echo "No changes to commit."
fi