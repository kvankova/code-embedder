from src.script_metadata import ScriptMetadata


def create_script_metadata(
    start: int, end: int, path: str, extraction_part: str | None = None
) -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content="",
    )
