#!/bin/sh -l
git config --global --add safe.directory /github/workspace
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git

BRANCH_NAME=${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}

git pull origin ${BRANCH_NAME}

echo "Searching for code snippets in $README_PATHS..."

poetry run python /app/src/main.py

if [ $? -ne 0 ]; then
    exit 1
fi

if [ -n "$(git status -s)" ]; then

    echo "Changes to commit..."
    git add $README_PATHS
    git diff --staged
    git commit -m "docs: Apply Code Embedder"
    git push origin ${BRANCH_NAME}
else
    echo "No changes to commit."
fi
