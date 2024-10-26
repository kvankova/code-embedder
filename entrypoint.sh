#!/bin/sh -l
git config --global --add safe.directory /github/workspace
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git

# Read the JSON array of readme paths from the first argument
README_PATHS=$(echo $1 | jq -r '.[]')

# If no paths are provided, default to README.md
if [ -z "$README_PATHS" ]; then
    README_PATHS="README.md"
fi

BRANCH_NAME=${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}

git pull origin ${BRANCH_NAME}

echo "Updating $README_PATHS with code snippets..."

poetry run python /app/src/main.py --readme-paths "$README_PATHS"

if [ -n "$(git status -s)" ]; then

    echo "Changes to commit..."
    git add "$README_PATHS"
    git diff --staged
    git commit -m "Update $README_PATHS"
    git push origin ${BRANCH_NAME}
else
    echo "No changes to commit."
fi
