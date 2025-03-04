import ast
import re
from typing import Optional, Protocol

from code_embedder.script_metadata import ScriptMetadata


class ScriptContentReaderInterface(Protocol):
    def read(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]: ...


class ScriptContentReader:
    def __init__(self) -> None:
        self._section_start_regex = r".*code_embedder:section_name start"
        self._section_end_regex = r".*code_embedder:section_name end"

    def read(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        scripts_with_full_contents = self._read_full_script(scripts)

        return self._process_scripts(scripts_with_full_contents)

    def _read_full_script(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        scripts_with_full_contents: list[ScriptMetadata] = []

        for script in scripts:
            try:
                with open(script.path, encoding="utf-8") as script_file:
                    script.content = script_file.read()
                    scripts_with_full_contents.append(script)

            except FileNotFoundError:
                raise FileNotFoundError(f"File {script.path} not found.")

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
            start, end = self._extract_section_part(
                lines=lines, section=script.extraction_part
            )

        if not start or not end:
            if script.extraction_type == "object":
                raise ValueError(
                    f"Object {script.extraction_part} not found in {script.path}. "
                )
            elif script.extraction_type == "section":
                raise ValueError(
                    f"Part {script.extraction_part} not found in {script.path}. "
                    "Either start and/or end of the section is missing."
                )

        return "\n".join(lines[start:end])

    def _extract_object_part(
        self, script: ScriptMetadata
    ) -> tuple[Optional[int], Optional[int]]:
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

    def _extract_section_part(
        self, lines: list[str], section: Optional[str] = None
    ) -> tuple[Optional[int], Optional[int]]:
        if not section:
            return None, None

        updated_section_start_regex = self._section_start_regex.replace(
            "section_name", section
        )
        updated_section_end_regex = self._section_end_regex.replace("section_name", section)

        for i, line in enumerate(lines):
            if re.search(updated_section_start_regex, line):
                start = i + 1
            elif re.search(updated_section_end_regex, line):
                return start, i

        return None, None
