from pathlib import Path

import pytest

from src.code_embedding import CodeEmbedder
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor


@pytest.mark.parametrize(
    "before_code_embedding_path, after_code_embedding_path",
    [
        # Full path and missing path
        (
            "tests/data/readme0.md",
            "tests/data/expected_readme0.md",
        ),
        # Section
        (
            "tests/data/readme1.md",
            "tests/data/expected_readme1.md",
        ),
        # Empty readme
        (
            "tests/data/readme2.md",
            "tests/data/expected_readme2.md",
        ),
        # Objects
        (
            "tests/data/readme3.md",
            "tests/data/expected_readme3.md",
        ),
    ],
    ids=[
        "full_path_missing_path",
        "section",
        "empty_readme",
        "objects",
    ],
)
def test_code_embedder(
    before_code_embedding_path: str, after_code_embedding_path: str, tmp_path: Path
) -> None:
    # Create a temporary copy of the original file
    temp_readme_path = tmp_path / "readme.md"
    with open(before_code_embedding_path) as readme_file:
        temp_readme_path.write_text(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path)],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    code_embedder()

    with open(after_code_embedding_path) as expected_file:
        expected_readme_content = expected_file.readlines()

    with open(temp_readme_path) as updated_file:
        updated_readme_content = updated_file.readlines()

    assert updated_readme_content == expected_readme_content
