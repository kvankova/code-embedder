from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    extraction_type: Literal["section", "object", "full"] = "full"
    extraction_part: Optional[str] = None
    content: str = ""
