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
        scripts_with_sections = [script for script in scripts if script.extraction_part]

        if scripts_with_sections:
            scripts_with_sections = self._read_script_section(scripts_with_sections)

        return full_scripts + scripts_with_sections

    def _read_script_section(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        return [
            ScriptMetadata(
                path=script.path,
                extraction_part=script.extraction_part,
                readme_start=script.readme_start,
                readme_end=script.readme_end,
                content=self._extract_section(script),
            )
            for script in scripts
        ]

    def _extract_section(self, script: ScriptMetadata) -> str:
        lines = script.content.split("\n")
        section_bounds = self._find_section_bounds(lines)

        if not section_bounds:
            logger.error(f"Section {script.extraction_part} not found in {script.path}")
            return ""

        start, end = section_bounds
        return "\n".join(lines[start:end])

    def _find_section_bounds(self, lines: list[str]) -> tuple[int, int] | None:
        section_start = None
        section_end = None

        for i, line in enumerate(lines):
            if re.search(self._section_start_regex, line):
                section_start = i + 1
            elif re.search(self._section_end_regex, line):
                section_end = i
                break

        if section_start is None or section_end is None:
            return None

        return section_start, section_end
