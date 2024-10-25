import re
from dataclasses import dataclass

from loguru import logger


@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    content: str


class ScriptPathExtractor:
    def __init__(self, readme_path: str, lookup_regex: str) -> None:
        self._readme_path = readme_path
        self._lookup_regex = lookup_regex

    def extract(self) -> list[ScriptMetadata]:
        with open(self._readme_path) as readme_file:
            readme_lines = readme_file.readlines()

        scripts = []
        inside_code_block = False

        for row, line in enumerate(readme_lines):
            if re.search(self._lookup_regex, line):
                inside_code_block = True
                path = line.split(":")[-1].strip()
                start = row
            if (line.strip() == ("```")) & inside_code_block:
                end = row
                scripts.append(
                    ScriptMetadata(readme_start=start, readme_end=end, path=path, content="")
                )
                inside_code_block = False

        return scripts


class CodeEmbedder:
    def __init__(
        self,
        readme_path: str,
        lookup_regex: str,
        script_path_extractor: ScriptPathExtractor,
    ) -> None:
        self._readme_path = readme_path
        self._lookup_regex = lookup_regex
        self._script_path_extractor = script_path_extractor

    def __call__(self) -> None:
        with open(self._readme_path) as readme_file:
            self.readme_content = readme_file.readlines()

        if len(self.readme_content) == 0:
            logger.info("Empty README. Skipping.")
            return

        scripts = self._script_path_extractor.extract()

        if len(scripts) == 0:
            logger.info("No script paths found in README. Skipping.")
            return

        logger.info(
            f"Found script paths in README: {set([script.path for script in scripts])}"
        )

        script_contents = self._read_script_content(scripts=scripts)

        self.update_readme(script_contents=script_contents)

    def _read_script_content(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        script_contents: list[ScriptMetadata] = []

        for script in scripts:
            try:
                with open(script.path) as script_file:
                    script.content = script_file.read()

                script_contents.append(script)

            except FileNotFoundError:
                print(f"Error: {script.path} not found. Skipping.")

        return script_contents

    def update_readme(self, script_contents: list[ScriptMetadata]) -> None:
        updated_readme = []
        readme_content_cursor = 0

        for script in script_contents:
            updated_readme += self.readme_content[
                readme_content_cursor : script.readme_start + 1
            ]
            updated_readme += script.content + "\n"

            readme_content_cursor = script.readme_end

        updated_readme += self.readme_content[readme_content_cursor:]

        with open(self._readme_path, "w") as readme_file:
            readme_file.writelines(updated_readme)
