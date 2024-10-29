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
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
            ],
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="",
                    readme_start=0,
                    readme_end=0,
                    content='print("Hello, World! from script")\n',
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    readme_start=0,
                    readme_end=0,
                    content=(
                        'print("Hello, World!")\n'
                        "# code_embedder:A start\n"
                        'print("Printing only section A")\n'
                        "# code_embedder:A end\n"
                    ),
                ),
            ],
            id="one_full_script_one_script_with_section",
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
                    readme_start=0,
                    readme_end=0,
                    content='print("Hello, World! from script")\n',
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    readme_start=0,
                    readme_end=0,
                    content=(
                        'print("Hello, World!")\n'
                        "# code_embedder:A start\n"
                        'print("Printing only section A")\n'
                        "# code_embedder:A end\n"
                    ),
                ),
            ],
            [
                ScriptMetadata(
                    path="tests/data/example.py",
                    extraction_part="no_section",
                    readme_start=0,
                    readme_end=0,
                    content="",
                ),
                ScriptMetadata(
                    path="tests/data/example_section.py",
                    extraction_part="A",
                    readme_start=0,
                    readme_end=0,
                    content='print("Printing only section A")',
                ),
            ],
            id="one_full_script_one_script_with_section",
        ),
    ],
)
def test_read_script_section(
    scripts: list[ScriptMetadata], expected_scripts: list[ScriptMetadata]
):
    script_content_reader = ScriptContentReader()

    assert script_content_reader._read_script_section(scripts) == expected_scripts
