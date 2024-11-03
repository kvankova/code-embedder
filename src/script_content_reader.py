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
        scripts_with_extraction_part = [script for script in scripts if script.extraction_part]

        if scripts_with_extraction_part:
            scripts_with_extraction_part = self._update_script_content_with_extraction_part(
                scripts_with_extraction_part
            )

        return full_scripts + scripts_with_extraction_part

    def _update_script_content_with_extraction_part(
        self, scripts: list[ScriptMetadata]
    ) -> list[ScriptMetadata]:
        return [
            ScriptMetadata(
                path=script.path,
                extraction_part=script.extraction_part,
                readme_start=script.readme_start,
                readme_end=script.readme_end,
                content=self._extract_part(script),
            )
            for script in scripts
        ]

    def _extract_part(self, script: ScriptMetadata) -> str:
        lines = script.content.split("\n")

        # Try extracting as object first, then fall back to section
        is_object, start, end = self._find_object_bounds(script)
        if is_object:
            return "\n".join(lines[start:end])

        # Extract section if not an object
        start, end = self._find_section_bounds(lines)
        if not self._validate_section_bounds(start, end, script):
            return ""

        return "\n".join(lines[start:end])

    def _validate_section_bounds(
        self, start: int | None, end: int | None, script: ScriptMetadata
    ) -> bool:
        if not start and not end:
            logger.error(
                f"Part {script.extraction_part} not found in {script.path}. Skipping."
            )
            return False

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

    def _find_section_bounds(self, lines: list[str]) -> tuple[int | None, int | None]:
        for i, line in enumerate(lines):
            if re.search(self._section_start_regex, line):
                start = i + 1
            elif re.search(self._section_end_regex, line):
                return start, i

        return None, None

    def _find_object_bounds(
        self, script: ScriptMetadata
    ) -> tuple[bool, int | None, int | None]:
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
                    return True, start - 1 if start else None, end

        return False, None, None
