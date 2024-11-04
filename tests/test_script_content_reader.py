import pytest

from src.script_content_reader import ScriptContentReader
from src.script_metadata import ScriptMetadata


@pytest.mark.parametrize(
    "scripts, expected_scripts",
    [
        pytest.param(
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="",
                    extraction_type="full",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="",
                    extraction_type="full",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
            ],
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="",
                    extraction_type="full",
                    readme_start=0,
                    readme_end=0,
                    content='print("Hello, World! from script")\n',
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content=(
                        'print("Hello, World!")\n'
                        "# code_embedder:A start\n"
                        'print("Printing only section A")\n'
                        "# code_embedder:A end\n"
                    ),
                ),
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="",
                    extraction_type="full",
                    readme_start=0,
                    readme_end=0,
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
            ],
        ),
    ],
)
def test_read_full_script(
    scripts: list[ScriptMetadata], expected_scripts: list[ScriptMetadata]
):
    script_content_reader = ScriptContentReader()

    assert script_content_reader._read_full_script(scripts) == expected_scripts


@pytest.mark.parametrize(
    "scripts, expected_scripts",
    [
        pytest.param(
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="no_section",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content='print("Hello, World! from script")\n',
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content=(
                        'print("Hello, World!")\n'
                        "# code_embedder:A start\n"
                        'print("Printing only section A")\n'
                        "# code_embedder:A end\n"
                    ),
                ),
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="verify_email",
                    extraction_type="object",
                    readme_start=0,
                    readme_end=0,
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
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="Person",
                    extraction_type="object",
                    readme_start=0,
                    readme_end=0,
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
            ],
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="no_section",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    extraction_type="section",
                    readme_start=0,
                    readme_end=0,
                    content='print("Printing only section A")',
                ),
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="verify_email",
                    extraction_type="object",
                    readme_start=0,
                    readme_end=0,
                    content=(
                        "def verify_email(email: str) -> bool:\n"
                        '    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                        '$", email) is not None'
                    ),
                ),
                ScriptMetadata(
                    path="tests/data/example_python_objects.py",
                    extraction_part="Person",
                    extraction_type="object",
                    readme_start=0,
                    readme_end=0,
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
            ],
        ),
    ],
)
def test_read_script_section(
    scripts: list[ScriptMetadata], expected_scripts: list[ScriptMetadata]
):
    script_content_reader = ScriptContentReader()

    assert (
        script_content_reader._update_script_content_with_extraction_part(scripts)
        == expected_scripts
    )
