import pytest

from src.code_embedding import ScriptMetadata, ScriptPathExtractor


@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (
            ["```python:main.py", "print('Hello, World!')", "```"],
            [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="")],
        ),
        (["```", "print('Hello, World!')", "```"], []),
        ([], []),
        (["```python", "print('Hello, World!')", "```"], []),
        (
            [
                "```python:example.py",
                "import os",
                "print('Hello, World!')",
                "```",
                "```",
                "print('Do not replace')",
                "```",
            ],
            [ScriptMetadata(readme_start=0, readme_end=3, path="example.py", content="")],
        ),
        (
            [
                "```python:main.py",
                "print('Hello, World!')",
                "```",
                "```python:example.py",
                "import os",
                "print('Hello, World!')",
                "```",
                "```",
                "print('Do not replace')",
                "```",
            ],
            [
                ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content=""),
                ScriptMetadata(readme_start=3, readme_end=6, path="example.py", content=""),
            ],
        ),
    ],
    ids=[
        "one_tagged_script",
        "one_untagged_script",
        "empty_readme",
        "one_untagged_script_language_specified",
        "one_tagged_script_one_untagged_script",
        "two_tagged_scripts_one_untagged_script",
    ],
)
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_path_extractor = ScriptPathExtractor()
    assert script_path_extractor.extract(readme_content=readme_content) == expected
