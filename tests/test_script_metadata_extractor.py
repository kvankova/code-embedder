from typing import Literal, Optional

import pytest

from code_embedder.script_metadata import ScriptMetadata
from code_embedder.script_metadata_extractor import ScriptMetadataExtractor


def create_script_metadata(
    readme_start: int,
    readme_end: int,
    path: str,
    extraction_type: Literal["section", "object", "full"] = "full",
    extraction_part: Optional[str] = None,
    content: str = "",
) -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=readme_start,
        readme_end=readme_end,
        path=path,
        extraction_type=extraction_type,
        extraction_part=extraction_part,
        content=content,
    )


@pytest.mark.parametrize(
    "readme_content, expected_script_metadata",
    [
        (
            ["```python:main.py", "print('Hello, World!')", "```"],
            [create_script_metadata(readme_start=0, readme_end=2, path="main.py")],
        ),
        (
            ["```", "print('Hello, World!')", "```"],
            [],
        ),
        ([], []),
        (
            ["```javascript", "console.log('Hello, World!');", "```"],
            [],
        ),
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
            [create_script_metadata(readme_start=0, readme_end=3, path="example.py")],
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
                create_script_metadata(readme_start=0, readme_end=2, path="main.py"),
                create_script_metadata(readme_start=3, readme_end=6, path="example.py"),
            ],
        ),
        (
            ["```python:main.py:s:section_name", "print('Hello, World!')", "```"],
            [
                create_script_metadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_type="section",
                    extraction_part="section_name",
                )
            ],
        ),
        (
            [
                "```python:main.py:s:section_name",
                "print('Hello, World!')",
                "```",
                "```python:example.py",
                "print('Hello, World!')",
                "```",
            ],
            [
                create_script_metadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_type="section",
                    extraction_part="section_name",
                ),
                create_script_metadata(readme_start=3, readme_end=5, path="example.py"),
            ],
        ),
        (
            [
                "```python:main.py:s:A",
                "print('Hello, World!')",
                "```",
                "```python:example.py:s:B",
                "print('Hello, World!')",
                "```",
            ],
            [
                create_script_metadata(
                    readme_start=0,
                    readme_end=2,
                    path="main.py",
                    extraction_type="section",
                    extraction_part="A",
                ),
                create_script_metadata(
                    readme_start=3,
                    readme_end=5,
                    path="example.py",
                    extraction_type="section",
                    extraction_part="B",
                ),
            ],
        ),
        (
            [
                "```python:main.py:o:print_hello",
                "def print_hello() -> None:",
                "    print('Hello, World!')",
                "```",
            ],
            [
                create_script_metadata(
                    readme_start=0,
                    readme_end=3,
                    path="main.py",
                    extraction_type="object",
                    extraction_part="print_hello",
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
        "one_tagged_script_with_object_name",
    ],
)
def test_script_path_extractor(
    readme_content: list[str], expected_script_metadata: list[ScriptMetadata]
) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    result = script_metadata_extractor.extract(readme_content=readme_content)
    assert result == expected_script_metadata
