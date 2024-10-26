import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata, ScriptPathExtractor


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
    result = script_path_extractor.extract(readme_content=readme_content)
    assert result == expected


def test_code_embedder_read_script_content() -> None:
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_path_extractor=ScriptPathExtractor(),
    )

    scripts = code_embedder._read_script_content(
        scripts=[
            ScriptMetadata(
                readme_start=6, readme_end=7, path="tests/data/example.py", content=""
            )
        ]
    )
    assert scripts == [
        ScriptMetadata(
            readme_start=6,
            readme_end=7,
            path="tests/data/example.py",
            content='print("Hello, World! from script")\n',
        )
    ]


def test_code_embedder(tmp_path) -> None:
    original_paths = [
        "tests/data/readme0.md",
        "tests/data/readme1.md",
        "tests/data/readme2.md",
    ]
    expected_paths = [
        "tests/data/expected_readme0.md",
        "tests/data/expected_readme1.md",
        "tests/data/expected_readme2.md",
    ]

    # Create a temporary copy of the original file
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_path_extractor=ScriptPathExtractor(),
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content
