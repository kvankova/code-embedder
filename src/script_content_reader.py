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
        script_contents = self._read_full_script(scripts)
        return self._process_scripts(script_contents)

    def _read_full_script(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        script_contents: list[ScriptMetadata] = []

        for script in scripts:
            try:
                with open(script.path) as script_file:
                    script.content = script_file.read()

                script_contents.append(script)

            except FileNotFoundError:
                logger.error(f"Error: {script.path} not found. Skipping.")

        return script_contents

    def _process_scripts(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        full_scripts = [script for script in scripts if not script.extraction_part]
        scripts_with_extraction_part = [script for script in scripts if script.extraction_part]

        if scripts_with_extraction_part:
            scripts_with_extraction_part = self._read_script_part(scripts_with_extraction_part)

        return full_scripts + scripts_with_extraction_part

    def _read_script_part(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
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

        is_object, start, end = self._find_object_bounds(script)

        if is_object:
            return "\n".join(lines[start:end])

        # Else, it is a section
        section_bounds = self._find_section_bounds(lines)

        if not section_bounds:
            logger.error(f"Section {script.extraction_part} not found in {script.path}")
            return ""

        start, end = section_bounds
        return "\n".join(lines[start:end])

    def _find_section_bounds(self, lines: list[str]) -> tuple[int, int] | None:
        start = None
        end = None

        for i, line in enumerate(lines):
            if re.search(self._section_start_regex, line):
                start = i + 1
            elif re.search(self._section_end_regex, line):
                end = i
                break

        if start is None or end is None:
            return None

        return start, end

    def _find_object_bounds(
        self, script: ScriptMetadata
    ) -> tuple[bool, int | None, int | None]:
        tree = ast.parse(script.content)

        object_nodes = []

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.FunctionDef)
                | isinstance(node, ast.AsyncFunctionDef)
                | isinstance(node, ast.ClassDef)
            ):
                object_nodes.append(node)

        for node in object_nodes:
            if script.extraction_part == getattr(node, "name", None):
                start_lineno = getattr(node, "lineno", None)
                end_lineno = getattr(node, "end_lineno", None)
                return (True, start_lineno - 1 if start_lineno else None, end_lineno)

        return False, None, None
