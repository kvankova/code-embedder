<div align="center">

<img src="assets/front.png" alt="Image" />

## **Code Embedder**
Seamlessly update code snippets in your **README** files! 🔄📝🚀

[Description](#-description) • [Example](#-example) • [Setup](#-setup) • [Under the hood](#-under-the-hood)
</div>


## 📚 Description

**Code Embedder** is a GitHub Action that automatically updates code snippets in your markdown (`README`) files. It finds code blocks in your `README` that reference specific scripts, then replaces these blocks with the current content of those scripts. This keeps your documentation in sync with your code.

✨ **Key features**
- 🔄 **Automatic synchronization**: Keep your `README` code examples up-to-date without manual intervention.
- 🛠️ **Easy setup**: Simply add the action to your GitHub workflow and format your `README` code blocks.
- 🌐 **Language agnostic**: Works with any programming language or file type.

By using **Code Embedder**, you can focus on writing and updating your actual code 💻, while letting the action take care of keeping your documentation current 📚🔄. This reduces the risk of outdated or incorrect code examples in your project documentation.

## 🔍 How it works

The action looks for the following sections in the all markdown (`README`) files:
````md
 ```language:path/to/script
 ```
````
It updates the code snippets in `README` files with the content of the script located at `path/to/script` and pushes the changes to the repository 🚀.

## 💡 Example

Let's say you have the following `README` file:
````md
# README

This is a readme.

```python:main.py
```
````
The `main.py` file contains the following code:
```python
print("Embedding successful")
```

Once the workflow runs, the code block sections are filled with the content of the script located at `main.py` and updated in the `README` file.

````md
# README

This is a readme.

```python:main.py
print("Embedding successful")
```
````
Once the content of the script located at `main.py` changes, the code block section will be updated in the `README` file with the next workflow run.

## 🔧 Setup
To use this action, you need to configure a yaml workflow file in `.github/workflows` folder (e.g. `.github/workflows/code-embedder.yaml`) with the following content:

```yaml
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
        uses: kvankova/code-embedder@v0.3.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
You need to create a secret with write and repo permissions in the repository settings to pass it as `GITHUB_TOKEN` in the workflow. 🔑 **Fine-grained tokens** are preferred, and you need to set repository permissions to obtain:
- **Read** access to actions variables, metadata and secrets.
- **Read** and **Write** access to actions, contents (code), commit statuses, pull requests, and workflows.

Also you need to add read and write permissions to workflows in your repository. You can find it under `Settings > Action > General > Workflow permissions`. 

## 🔬 Under the hood
This action performs the following steps:
1. 🔎 Scans through the markdown (`README`) files to identify referenced script files.
1. 📝 Extracts the contents from those script files and updates the corresponding code blocks in the markdown (`README`) files.
1. 🚀 Commits and pushes the updated documentation back to the repository.
