import pytest

from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from tests.conftest import create_script_metadata

test_cases = [
    pytest.param(
        ["```python:main.py", "print('Hello, World!')", "```"],
        [create_script_metadata(0, 2, "main.py")],
        id="one_tagged_script",
    ),
    pytest.param(["```", "print('Hello, World!')", "```"], [], id="one_untagged_script"),
    pytest.param([], [], id="empty_readme"),
    pytest.param(
        ["```javascript", "console.log('Hello, World!');", "```"],
        [],
        id="one_untagged_script_language_specified",
    ),
    pytest.param(
        [
            "```python:example.py",
            "import os",
            "print('Hello, World!')",
            "```",
            "```",
            "print('Do not replace')",
            "```",
        ],
        [create_script_metadata(0, 3, "example.py")],
        id="one_tagged_script_one_untagged_script",
    ),
    pytest.param(
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
            create_script_metadata(0, 2, "main.py"),
            create_script_metadata(3, 6, "example.py"),
        ],
        id="two_tagged_scripts_one_untagged_script",
    ),
    pytest.param(
        ["```python:main.py:section_name", "print('Hello, World!')", "```"],
        [create_script_metadata(0, 2, "main.py", "section_name")],
        id="one_tagged_script_with_section_name",
    ),
    pytest.param(
        [
            "```python:main.py:section_name",
            "print('Hello, World!')",
            "```",
            "```python:example.py",
            "print('Hello, World!')",
            "```",
        ],
        [
            create_script_metadata(0, 2, "main.py", "section_name"),
            create_script_metadata(3, 5, "example.py"),
        ],
        id="one_tagged_script_with_section_name_one_tagged_script",
    ),
    pytest.param(
        [
            "```python:main.py:A",
            "print('Hello, World!')",
            "```",
            "```python:example.py:B",
            "print('Hello, World!')",
            "```",
        ],
        [
            create_script_metadata(0, 2, "main.py", "A"),
            create_script_metadata(3, 5, "example.py", "B"),
        ],
        id="two_tagged_scripts_with_section_names",
    ),
]


@pytest.mark.parametrize("readme_content, expected", test_cases)
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    result = script_metadata_extractor.extract(readme_content=readme_content)
    assert result == expected
