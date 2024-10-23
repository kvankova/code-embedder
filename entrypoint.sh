#!/bin/sh -l
git config --global --add safe.directory /github/workspace
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git

README_PATH=${1:-README.md}
BRANCH_NAME=${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}

git pull origin ${BRANCH_NAME}

echo "Updating $README_PATH with code snippets..."

poetry run python /app/src/main.py --readme-path "$README_PATH"

if [ -n "$(git status -s)" ]; then

    echo "Changes to commit..."
    git add "$README_PATH"
    git diff --staged
    git commit -m "Update $README_PATH"
    git push origin ${BRANCH_NAME}
else
    echo "No changes to commit."
fi
