from dataclasses import dataclass
from typing import Literal


@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    extraction_type: Literal["section", "object", "full"] = "full"
    extraction_part: str | None = None
    content: str = ""
