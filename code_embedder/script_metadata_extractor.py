import re
from typing import Optional, Protocol

from code_embedder.script_metadata import ScriptMetadata


class ScriptMetadataExtractorInterface(Protocol):
    def extract(self, readme_content: list[str]) -> list[ScriptMetadata]: ...


class ScriptMetadataExtractor:
    def __init__(self) -> None:
        self._code_block_start_regex = r"^```.*?:"
        self._code_block_end = "```"
        self._path_separator = ":"
        self._object_separator = "o"
        self._section_separator = "s"
        self.extraction_type_mapping = {
            self._object_separator: "object",
            self._section_separator: "section",
            "full": "full",
        }

    def extract(self, readme_content: list[str]) -> list[ScriptMetadata]:
        scripts = []
        current_block = None

        for row, line in enumerate(readme_content):
            if self._is_code_block_start(line):
                current_block = self._start_new_block(line, row)
            elif self._is_code_block_end(line) and current_block:
                scripts.append(self._finish_current_block(current_block, row))
                current_block = None

        return scripts

    def _is_code_block_start(self, line: str) -> bool:
        return re.search(self._code_block_start_regex, line) is not None

    def _is_code_block_end(self, line: str) -> bool:
        return line.strip() == self._code_block_end

    def _start_new_block(self, line: str, row: int) -> Optional[dict]:
        tag_items = line.split(self._path_separator)
        path = tag_items[1].strip()
        extraction_type = tag_items[2].strip() if len(tag_items) > 2 else "full"

        if extraction_type not in self.extraction_type_mapping.keys():
            raise ValueError(
                f"Unknown extraction type {extraction_type}. Allowed are only "
                f"`{self._object_separator}` for object and "
                f"`{self._section_separator}` for section."
            )

        extraction_part = tag_items[3].strip() if len(tag_items) > 3 else None

        if not extraction_part and extraction_type != "full":
            raise ValueError(
                f"Extraction part (section or object name) is not provided for "
                f"{extraction_type} extraction type."
            )

        return {
            "start": row,
            "path": path,
            "extraction_type": self.extraction_type_mapping[extraction_type],
            "extraction_part": extraction_part,
        }

    def _finish_current_block(self, block: dict, end_row: int) -> ScriptMetadata:
        return ScriptMetadata(
            readme_start=block["start"],
            readme_end=end_row,
            path=block["path"],
            extraction_type=block["extraction_type"],
            extraction_part=block["extraction_part"],
            content="",
        )
