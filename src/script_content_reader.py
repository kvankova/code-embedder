import ast
import re
from typing import Protocol

from loguru import logger

from src.script_metadata import ScriptMetadata


class ScriptContentReaderInterface(Protocol):
    def read(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]: ...


class ScriptContentReader:
    def __init__(self) -> None:
        self._section_start_regex = r".*code_embedder:.*start"
        self._section_end_regex = r".*code_embedder:.*end"

    def read(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        scripts_with_full_contents = self._read_full_script(scripts)
        return self._process_scripts(scripts_with_full_contents)

    def _read_full_script(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        scripts_with_full_contents: list[ScriptMetadata] = []

        for script in scripts:
            try:
                with open(script.path) as script_file:
                    script.content = script_file.read()

                scripts_with_full_contents.append(script)

            except FileNotFoundError:
                logger.error(f"Error: {script.path} not found. Skipping.")

        return scripts_with_full_contents

    def _process_scripts(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        full_scripts = [script for script in scripts if not script.extraction_part]
        scripts_with_extraction = [script for script in scripts if script.extraction_part]

        if scripts_with_extraction:
            scripts_with_extraction = self._update_script_content_with_extraction_part(
                scripts_with_extraction
            )

        return full_scripts + scripts_with_extraction

    def _update_script_content_with_extraction_part(
        self, scripts: list[ScriptMetadata]
    ) -> list[ScriptMetadata]:
        return [
            ScriptMetadata(
                path=script.path,
                extraction_part=script.extraction_part,
                extraction_type=script.extraction_type,
                readme_start=script.readme_start,
                readme_end=script.readme_end,
                content=self._extract_part(script),
            )
            for script in scripts
        ]

    def _extract_part(self, script: ScriptMetadata) -> str:
        lines = script.content.split("\n")

        if script.extraction_type == "object":
            start, end = self._extract_object_part(script)

        elif script.extraction_type == "section":
            start, end = self._extract_section_part(lines)
            if not self._validate_section_bounds(start, end, script):
                return ""

        if not start and not end:
            logger.error(
                f"Part {script.extraction_part} not found in {script.path}. Skipping."
            )
            return ""

        return "\n".join(lines[start:end])

    def _extract_object_part(self, script: ScriptMetadata) -> tuple[int | None, int | None]:
        tree = ast.parse(script.content)

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.FunctionDef)
                | isinstance(node, ast.AsyncFunctionDef)
                | isinstance(node, ast.ClassDef)
            ):
                if script.extraction_part == getattr(node, "name", None):
                    start = getattr(node, "lineno", None)
                    end = getattr(node, "end_lineno", None)
                    return start - 1 if start else None, end

        return None, None

    def _extract_section_part(self, lines: list[str]) -> tuple[int | None, int | None]:
        for i, line in enumerate(lines):
            if re.search(self._section_start_regex, line):
                start = i + 1
            elif re.search(self._section_end_regex, line):
                return start, i

        return None, None

    def _validate_section_bounds(
        self, start: int | None, end: int | None, script: ScriptMetadata
    ) -> bool:
        if not start:
            logger.error(
                f"Start of section {script.extraction_part} not found in {script.path}. "
                "Skipping."
            )
            return False

        if not end:
            logger.error(
                f"End of section {script.extraction_part} not found in {script.path}. "
                "Skipping."
            )
            return False

        return True
