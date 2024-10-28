import pytest

from src.code_embedding import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor


@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (
            ["```python:main.py", "print('Hello, World!')", "```"],
            [
                ScriptMetadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_part=None,
                    content="",
                )
            ],
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
            [
                ScriptMetadata(
                    readme_start=0,
                    readme_end=3,
                    path="example.py",
                    extraction_part=None,
                    content="",
                )
            ],
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
                ScriptMetadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_part=None,
                    content="",
                ),
                ScriptMetadata(
                    readme_start=3,
                    readme_end=6,
                    path="example.py",
                    extraction_part=None,
                    content="",
                ),
            ],
        ),
        (
            ["```python:main.py:section_name", "print('Hello, World!')", "```"],
            [
                ScriptMetadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_part="section_name",
                    content="",
                )
            ],
        ),
        (
            [
                "```python:main.py:section_name",
                "print('Hello, World!')",
                "```",
                "```python:example.py",
                "print('Hello, World!')",
                "```",
            ],
            [
                ScriptMetadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_part="section_name",
                    content="",
                ),
                ScriptMetadata(
                    readme_start=3,
                    readme_end=5,
                    path="example.py",
                    extraction_part=None,
                    content="",
                ),
            ],
        ),
        (
            [
                "```python:main.py:A",
                "print('Hello, World!')",
                "```",
                "```python:example.py:B",
                "print('Hello, World!')",
                "```",
            ],
            [
                ScriptMetadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_part="A",
                    content="",
                ),
                ScriptMetadata(
                    readme_start=3,
                    readme_end=5,
                    path="example.py",
                    extraction_part="B",
                    content="",
                ),
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
        "one_tagged_script_with_section_name",
        "one_tagged_script_with_section_name_one_tagged_script",
        "two_tagged_scripts_with_section_names",
    ],
)
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    result = script_metadata_extractor.extract(readme_content=readme_content)
    assert result == expected
