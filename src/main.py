import glob
import sys

import typer
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.log_level import LogLevel
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor

app = typer.Typer(rich_markup_mode="rich")


@app.command(help="Embed code from scripts to markdown files.")
def run(
    log_level: LogLevel = typer.Option(
        LogLevel.ERROR, "--log-level", help="Log level, use INFO, WARNING, or ERROR."
    ),
    changed_files: list[str] = typer.Argument(None, help="List of changed files to process."),
):
    logger.remove()
    print(log_level.value)
    logger.add(sys.stderr, level=log_level.value)

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
    typer.run(run)
