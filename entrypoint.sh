#!/bin/sh -l
git add entrypoint.sh
git update-index --chmod=+x entrypoint.sh

README_PATH=${1:-README.md}

# Update the README file as needed
echo "Updating $README_PATH with code snippets..."

python3 main.py 

# Check if there are changes to commit
if [ -n "$(git status -s)" ]; then  # Use [ ] instead of [[ ]]
    git config --global user.name "github-actions"
    git config --global user.email "github-actions@github.com"

    # Ensure we're in the correct directory
    cd "$GITHUB_WORKSPACE"  # This is the default location for the checked out repo

    git add "$README_PATH"

    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD --; then
        git commit -m "Update $README_PATH"
        git push origin HEAD:${GITHUB_REF}  # Push changes to the current branch
    else
        echo "No changes to commit."
    fi
else
    echo "No changes to commit."
fi