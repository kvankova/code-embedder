<div align="center">

<img src="assets/front.png" alt="Image" />

## **Code Embedder**
Seamlessly update code snippets in your **README** files! 🔄📝🚀

[Description](#-description) • [How it works](#-how-it-works) • [Setup](#-setup) • [Examples](#-examples) • [Contributing](#-contributing) • [Development](#️-development)
</div>


## 📚 Description

**Code Embedder** is a GitHub Action that automatically updates code snippets in your markdown (`README`) files. It finds code blocks in your `README` that reference specific scripts, then replaces these blocks with the current content of those scripts. This keeps your documentation in sync with your code.

### ✨ Key features
- 🔄 **Automatic synchronization**: Keep your `README` code examples up-to-date without manual intervention.
- 🛠️ **Easy setup**: Simply add the action to your GitHub workflow and format your `README` code blocks.
- 📝 **Section support**: Update only specific sections of the script in the `README`.
- 🧩 **Object support**: Update only specific objects (functions, classes) in the `README`. *The latest version supports only 🐍 Python objects (other languages to be added soon).*


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
 ```language:path/to/script:s:section_name
 ```
````
> [!Note]
>Notice that the `path/to/script` is followed by `s:` in the tag to indicate that the section `section_name` is being updated.

You must also add the following comment tags in the script file `path/to/script`, where the section is located:
```
[Comment sign] code_embedder:section_name start
...
[Comment sign] code_embedder:section_name end
```
The comment sign is the one that is used in the script file, e.g. `#` for Python, or `//` for JavaScript. The `section_name` must be unique in the file, otherwise the action will use the first section found.

### 🧩 **Object** updates
In the `README` (or other markdown) file, the object of the script is marked with the following tag:
````md
 ```language:path/to/script:o:object_name
 ```
````
> [!Note]
> Notice that the `path/to/script` is followed by `o:` in the tag to indicate that the object `object_name` is being updated.

> [!Note]
> The object name must match exactly the name of the object (function, class) in the script file, including the case (e.g. `Person` not `person`). Currently, only 🐍 Python objects are supported.

## 🔧 Setup
To use this action, you need to configure a yaml workflow file in `.github/workflows` folder (e.g. `.github/workflows/code-embedder.yaml`) with the following content:

```yaml
name: Code Embedder

on: pull_request

permissions:
  contents: write

jobs:
  code_embedder:
    name: "Code embedder"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Run code embedder
        uses: kvankova/code-embedder@v0.5.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

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

```python:main.py:s:A
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

```python:main.py:s:A
print("Embedding successful")
```
````

With any changes to the section `A` in `main.py`, the code block section is updated in the `README` file with the next workflow run.

### 🧩 Object update
The tag used for object update follows the same convention as the tag for section update with the following changes:
- use `o:` instead of `s:`
- use `object_name`

> [!Note]
> The `object_name` must match exactly the name of the object (function, class) in the script file, including the case. If you define class `Person` in the script, you must use `Person` as the object name in the `README`, not lowercase `person`.

For example, let's say we have the following `README` file:
````md
# README

This is a readme.

Function `print_hello` is defined as follows:
```python:main.py:o:print_hello
```

Class `Person` is defined as follows:
```python:main.py:o:Person
```
````

The `main.py` file contains the following code:
```python
...
def print_hello():
    print("Hello, world!")
...

class Person:
    def __init__(self, name):
        self.name = name
    def say_hello(self):
        print(f"Hello, {self.name}!")
...
```

Once the workflow runs, the code block section will be updated in the `README` file with the content of the function `print_hello` and class `Person` from the script located at `main.py` and pushed to the repository 🚀.

````md
# README

This is a readme.

Function `print_hello` is defined as follows:
```python:main.py:o:print_hello
def print_hello():
    print("Hello, world!")
```

Class `Person` is defined as follows:
```python:main.py:o:Person
class Person:
    def __init__(self, name):
        self.name = name
    def say_hello(self):
        print(f"Hello, {self.name}!")
```
````

With any changes to the function `print_hello` or class `Person` in `main.py`, the code block sections are updated in the `README` file with the next workflow run.

## 🤝 Contributing
We welcome contributions to improve this tool!
- If you have an idea for a **new feature** ✨, open a [new feature request](https://github.com/kvankova/code-embedder/issues/new?labels=enhancement&template=feature_request.yaml) on GitHub.
- If you spot a **bug** 🐛, open a [new issue](https://github.com/kvankova/code-embedder/issues/new/choose) on GitHub.
- If you want to **contribute to the code**, please pick an issue that is not assigned to anyone and comment on it, so that we know you are working on it.

## 🛠️ Development
1. Fork this project
1. Install [poetry](https://python-poetry.org/docs/#installation)
1. Install the dependencies by using the following command:
    ```bash
    poetry install --with dev
    ```
1. Make changes to the code and run the tests to make sure everything works as expected. ✅
    ```bash
    poetry run pytest
    ```
1. Commit your changes, push them to the repository 🚀, and open a new pull request.
