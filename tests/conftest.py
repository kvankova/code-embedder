from typing import Literal

from src.script_metadata import ScriptMetadata


def create_script_metadata(
    start: int,
    end: int,
    path: str,
    extraction_type: Literal["section", "object", "full"] = "full",
    extraction_part: str | None = None,
    content: str = "",
) -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_type=extraction_type,
        extraction_part=extraction_part,
        content=content,
    )
