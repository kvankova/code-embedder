import glob
import sys

import typer
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor

app = typer.Typer()

# Setup logging for the script running as pre-commit hook
logger.remove()
logger.add(sys.stderr, level="ERROR")


@app.command(help="Embed code from scripts to markdown files.")
def run(
    changed_files: list[str] = typer.Argument(None, help="List of changed files to process."),
):
    readme_paths = glob.glob("**/*.md", recursive=True)

    if not readme_paths:
        logger.info("No markdown files found in the current repository.")
        exit(0)

    logger.info(f"Found {len(readme_paths)} markdown files in the current repository.")

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    code_embedder = CodeEmbedder(
        readme_paths=readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    code_embedder()

    logger.info("Code Embedder finished successfully.")


if __name__ == "__main__":
    # Update logging for the script running as github action
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    typer.run(run)
