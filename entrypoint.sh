#!/bin/sh -l
set -xe
git config --global --add safe.directory /github/workspace
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git
git fetch origin

README_PATH=${1:-README.md}
BRANCH_NAME=${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."

python3 /app/src/main.py

if [ -n "$(git status -s)" ]; then
    echo "Changes to commit..."
    git diff --stage
    git add "$README_PATH"
    git commit -m "Update $README_PATH"
    git push origin ${BRANCH_NAME}
else
    echo "No changes to commit."
fi
