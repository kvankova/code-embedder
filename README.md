<div align="center">

<img src="assets/front.png" alt="Image" />

## **Code Embedder**
Seamlessly update code snippets in your **README** files! 🔄📝🚀

[Description](#-description) • [How it works](#-how-it-works) • [Examples](#-examples) • [Setup](#-setup) • [Under the hood](#-under-the-hood)
</div>


## 📚 Description

**Code Embedder** is a GitHub Action that automatically updates code snippets in your markdown (`README`) files. It finds code blocks in your `README` that reference specific scripts, then replaces these blocks with the current content of those scripts. This keeps your documentation in sync with your code.

✨ **Key features**
- 🔄 **Automatic synchronization**: Keep your `README` code examples up-to-date without manual intervention.
- 📝 **Section support**: Update specific sections of the script in the `README`.
- 🛠️ **Easy setup**: Simply add the action to your GitHub workflow and format your `README` code blocks.
- 🌐 **Language agnostic**: Works with any programming language or file type.

By using **Code Embedder**, you can focus on writing and updating your actual code 💻, while letting the action take care of keeping your documentation current 📚🔄. This reduces the risk of outdated or incorrect code examples in your project documentation.

## 🔍 How it works

The action looks for specific tags in all markdown (`README`) files, which indicate the script file path (and optionally the section to update), then it updates the code block sections in the `README` files with the content. The changes are then pushed to the repository 🚀.

### 📄 **Full script** updates
In the `README` (or other markdown) file, the full script is marked with the following tag:
````md
 ```language:path/to/script
 ```
````
### 📂 **Section** updates
In the `README` (or other markdown) file, the section of the script is marked with the following tag:
````md
 ```language:path/to/script:section_name
 ```
````
You must also add the following comment tags in the script file `path/to/script`, where the section is located:
```
[Comment sign] code_embedder:section_name start
...
[Comment sign] code_embedder:section_name end
```
The comment sign is the one that is used in the script file, e.g. `#` for Python, or `//` for JavaScript. The `section_name` must be unique in the file, otherwise the action will not be able to identify the section.



## 💡 Examples

### 📄 Full script update

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
With any changes to `main.py`, the code block section is updated in the `README` file with the next workflow run.

### 📂 Section update

Now we have the following `README` file:
````md
# README

This is a readme.

```python:main.py:A
```
````
The `main.py` file contains the following code:
```python
print("Hello, world!")

# code_embedder:A start
print("Embedding successful")
# code_embedder:A end
```

Once the workflow runs, the code block section will be updated in the `README` file with the content of the section `A` from the script located at `main.py` and pushed to the repository 🚀.

````md
# README

This is a readme.

```python:main.py:A
print("Embedding successful")
```
````

With any changes to the section `A` in `main.py`, the code block section is updated in the `README` file with the next workflow run.

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

      - name: Run code embedder
        uses: kvankova/code-embedder@v0.4.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
You need to create a secret with write and repo permissions in the repository settings to pass it as `GITHUB_TOKEN` in the workflow. 🔑 **Fine-grained tokens** are preferred, and you need to set repository permissions to obtain:
- **Read** access to actions variables, metadata and secrets.
- **Read** and **Write** access to actions, contents (code), commit statuses, pull requests, and workflows.

Also you need to add read and write permissions to workflows in your repository. You can find it under `Settings > Action > General > Workflow permissions`.

## 🔬 Under the hood
This action performs the following steps:
1. 🔎 Scans through the markdown (`README`) files to identify referenced script files (full script or section).
1. 📝 Extracts the contents from those script files and updates the corresponding code blocks in the markdown (`README`) files.
1. 🚀 Commits and pushes the updated documentation back to the repository.
