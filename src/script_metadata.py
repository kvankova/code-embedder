from dataclasses import dataclass


@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    extraction_part: str | None = None  # None for full script, section_name for section
    content: str = ""
