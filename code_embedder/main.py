import glob
import sys

import typer
from loguru import logger

from code_embedder.code_embedding import CodeEmbedder
from code_embedder.script_content_reader import ScriptContentReader
from code_embedder.script_metadata_extractor import ScriptMetadataExtractor

logger.remove()
logger.add(sys.stderr, level="ERROR")

app = typer.Typer(rich_markup_mode=None)


@app.command(help="Embed code from scripts to markdown files.")
def run(
    all_files: bool = typer.Option(
        False, "--all-files", help="Process all files in the repository."
    ),
    changed_files: list[str] = typer.Argument(None, help="List of changed files to process."),
):
    readme_paths = glob.glob("**/*.md", recursive=True)

    if not readme_paths:
        logger.info("No markdown files found in the current repository.")
        exit(0)

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    files = changed_files if not all_files else None  # None for all files

    code_embedder = CodeEmbedder(
        readme_paths=readme_paths,
        changed_files=files,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )

    code_embedder()
    logger.info("Code Embedder finished successfully.")


if __name__ == "__main__":
    app()
