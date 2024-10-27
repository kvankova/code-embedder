# code-embedder
<p align="center">
  <img src="assets/front.png" alt="Image" width="600" />
</p>

Code embedder is a GitHub action that updates your README.md with up-to-date code snippets from your scripts.

## Description
This action:
1. reads one or more README files from `readme_paths` input,
1. looks for specific script tags in the READMEs,
1. reads the content of the scripts and embeds it in the READMEs at the corresponding tags,
1. pushes the changes to the repository.

## Workflow file structure
To use this action, you need to configure a yaml workflow file in `.github/workflows` folder (e.g. `.github/workflows/code-embedder.yaml`) with the following content:

```yaml:.github/workflows/code-embedder.yml
name: Code Embedder

on: pull_request

jobs:
  code_embedder:
    name: "Code embedder"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.ref }}

      - name: Run code embedder
        uses: kvankova/code-embedder@v0.2.0
        with:
          readme_paths: README.md README2.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
It requires a secret `GITHUB_TOKEN` with write and repo permission.

## README file configuration
You can specify which README files you want to update with `readme_paths` (paths to markdown files). If no README files are provided, it will by default look for it in the root `README.md`. Argument `readme_paths` accepts multiple paths separated by spaces, example: `README.md README2.md`.

The action looks for the following sections in the readme file based on which it will update the code snippets:
````md
 ```language:path/to/script
 ```
````
These sections will be filled in by content of path/to/script and updated with up-to-date content of the scripts.

## Example

You will add the code block sections with path to the scripts in the following format:
````md
# README

This is a readme.

```python:main.py
```
````
And once the worklow runs, the code block sections will be filled with the content of the script and updated in the readme file.

````md
# README

This is a readme.

```python:main.py
print("Embedding successful")
```
````
Once the content of the script changes, the code block sections will be updated in the readme file.
