from typing import Literal

import pytest

from src.script_content_reader import ScriptContentReader
from src.script_metadata import ScriptMetadata


def create_script_metadata(
    path: str,
    extraction_type: Literal["full", "section", "object"] = "full",
    extraction_part: str | None = None,
    content: str = "",
) -> ScriptMetadata:
    return ScriptMetadata(
        path=path,
        extraction_part=extraction_part,
        extraction_type=extraction_type,
        readme_start=0,
        readme_end=0,
        content=content,
    )


@pytest.mark.parametrize(
    "script, expected_script",
    [
        # Full script
        (
            create_script_metadata(path="tests/data/example.py"),
            create_script_metadata(
                path="tests/data/example.py", content='print("Hello, World! from script")\n'
            ),
        ),
        # Section
        (
            create_script_metadata(
                path="tests/data/example_section.py",
                extraction_part="A",
                extraction_type="section",
            ),
            create_script_metadata(
                path="tests/data/example_section.py",
                extraction_part="A",
                extraction_type="section",
                content=(
                    'print("Hello, World!")\n'
                    "# code_embedder:A start\n"
                    'print("Printing only section A")\n'
                    "# code_embedder:A end\n"
                    "\n"
                    "# code_embedder:B start\n"
                    'print("Printing only section B")\n'
                    "# code_embedder:B end\n"
                ),
            ),
        ),
        # Full script with python objects
        (
            create_script_metadata(
                path="tests/data/example_python_objects.py",
            ),
            create_script_metadata(
                path="tests/data/example_python_objects.py",
                content=(
                    "import re\n"
                    "\n"
                    "\n"
                    "# Function verifying an email is valid\n"
                    "def verify_email(email: str) -> bool:\n"
                    '    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                    '$", email) is not None\n'
                    "\n"
                    "\n"
                    "class Person:\n"
                    "    def __init__(self, name: str, age: int):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "    # String representation of the class\n"
                    "    def __str__(self) -> str:\n"
                    '        return f"Person(name={self.name}, age={self.age})"\n'
                ),
            ),
        ),
    ],
    ids=["full_script", "section_script", "full_script_with_python_objects"],
)
def test_read_full_script(script: ScriptMetadata, expected_script: ScriptMetadata):
    script_content_reader = ScriptContentReader()
    assert script_content_reader._read_full_script([script]) == [expected_script]


def test_read_full_script_unknown_path() -> None:
    script_content_reader = ScriptContentReader()
    with pytest.raises(FileNotFoundError):
        script_content_reader._read_full_script(
            [create_script_metadata(path="unknown_path.py")]
        )


@pytest.mark.parametrize(
    "script_metadata, expected_script_metadata",
    [
        # Section
        (
            create_script_metadata(
                path="tests/data/example_section.py",
                extraction_part="A",
                extraction_type="section",
                content=(
                    'print("Hello, World!")\n'
                    "# code_embedder:A start\n"
                    'print("Printing only section A")\n'
                    "# code_embedder:A end\n"
                ),
            ),
            create_script_metadata(
                path="tests/data/example_section.py",
                extraction_part="A",
                extraction_type="section",
                content='print("Printing only section A")',
            ),
        ),
        # Object
        (
            create_script_metadata(
                path="tests/data/example_python_objects.py",
                extraction_part="verify_email",
                extraction_type="object",
                content=(
                    "import re\n"
                    "# Function verifying an email is valid\n"
                    "def verify_email(email: str) -> bool:\n"
                    '    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                    '$", email) is not None\n'
                    "\n"
                    "class Person:\n"
                    "    def __init__(self, name: str, age: int):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "    # String representation of the class\n"
                    "    def __str__(self) -> str:\n"
                    '        return f"Person(name={self.name}, age={self.age})"\n'
                ),
            ),
            create_script_metadata(
                path="tests/data/example_python_objects.py",
                extraction_part="verify_email",
                extraction_type="object",
                content=(
                    "def verify_email(email: str) -> bool:\n"
                    '    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                    '$", email) is not None'
                ),
            ),
        ),
        # Object class
        (
            create_script_metadata(
                path="tests/data/example_python_objects.py",
                extraction_part="Person",
                extraction_type="object",
                content=(
                    "import re\n"
                    "# Function verifying an email is valid\n"
                    "def verify_email(email: str) -> bool:\n"
                    '    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                    '$", email) is not None\n'
                    "\n"
                    "class Person:\n"
                    "    def __init__(self, name: str, age: int):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "    # String representation of the class\n"
                    "    def __str__(self) -> str:\n"
                    '        return f"Person(name={self.name}, age={self.age})"\n'
                ),
            ),
            create_script_metadata(
                path="tests/data/example_python_objects.py",
                extraction_part="Person",
                extraction_type="object",
                content=(
                    "class Person:\n"
                    "    def __init__(self, name: str, age: int):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "    # String representation of the class\n"
                    "    def __str__(self) -> str:\n"
                    '        return f"Person(name={self.name}, age={self.age})"'
                ),
            ),
        ),
    ],
    ids=["section", "object", "object_class"],
)
def test_read_script_section(
    script_metadata: ScriptMetadata, expected_script_metadata: ScriptMetadata
):
    script_content_reader = ScriptContentReader()

    assert script_content_reader._update_script_content_with_extraction_part(
        [script_metadata]
    ) == [expected_script_metadata]


@pytest.mark.parametrize(
    "script_metadata, error_message",
    [
        # Unknown section
        (
            create_script_metadata(
                path="tests/data/example.py",
                extraction_part="no_section",
                extraction_type="section",
                content='print("Hello, World! from script")\n',
            ),
            "Part no_section not found in tests/data/example.py. "
            "Either start and/or end of the section is missing.",
        ),
        # Unknown object
        (
            create_script_metadata(
                path="tests/data/example.py",
                extraction_part="no_object",
                extraction_type="object",
            ),
            "Object no_object not found in tests/data/example.py. ",
        ),
    ],
    ids=["unknown_section", "unknown_object"],
)
def test_read_script_unknown_extraction_part(
    script_metadata: ScriptMetadata, error_message: str
) -> None:
    script_content_reader = ScriptContentReader()
    with pytest.raises(ValueError, match=error_message):
        script_content_reader._update_script_content_with_extraction_part([script_metadata])
