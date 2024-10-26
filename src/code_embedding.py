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
    def __init__(self) -> None:
        self._code_block_start_regex = r"^```.*?:"
        self._code_block_end = "```"
        self._path_separator = ":"

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

    def _start_new_block(self, line: str, row: int) -> dict:
        path = line.split(self._path_separator)[-1].strip()
        return {"start": row, "path": path}

    def _finish_current_block(self, block: dict, end_row: int) -> ScriptMetadata:
        return ScriptMetadata(
            readme_start=block["start"], readme_end=end_row, path=block["path"], content=""
        )


class CodeEmbedder:
    def __init__(
        self,
        readme_path: str,
        script_path_extractor: ScriptPathExtractor,
    ) -> None:
        self._readme_path = readme_path
        self._script_path_extractor = script_path_extractor

    def __call__(self) -> None:
        self._validate_and_read_readme()

        if not self.readme_content:
            logger.info("Empty README. Skipping.")
            return

        scripts = self._extract_and_validate_scripts()
        if not scripts:
            return

        script_contents = self._read_script_content(scripts=scripts)
        self._update_readme(script_contents=script_contents)

    def _validate_and_read_readme(self) -> None:
        if not self._readme_path.endswith(".md"):
            logger.error("README path must end with .md")
            raise ValueError("README path must end with .md")

        with open(self._readme_path) as readme_file:
            self.readme_content = readme_file.readlines()

    def _extract_and_validate_scripts(self) -> list[ScriptMetadata] | None:
        scripts = self._script_path_extractor.extract(readme_content=self.readme_content)

        if not scripts:
            logger.info("No script paths found in README. Skipping.")
            return None

        logger.info(f"Found script paths in README: {set(script.path for script in scripts)}")
        return scripts

    def _read_script_content(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        script_contents: list[ScriptMetadata] = []

        for script in scripts:
            try:
                with open(script.path) as script_file:
                    script.content = script_file.read()

                script_contents.append(script)

            except FileNotFoundError:
                logger.error(f"Error: {script.path} not found. Skipping.")

        return script_contents

    def _update_readme(self, script_contents: list[ScriptMetadata]) -> None:
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
