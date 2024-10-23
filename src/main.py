import argparse

from loguru import logger

from src import job

parser = argparse.ArgumentParser()
parser.add_argument("--readme-path", type=str, help="Path to Readme", default="README.md")
args = parser.parse_args()

lookup_string = "```python:"


def main(readme_path: str) -> None:
    script_to_embed = job.find_embed_lines(
        readme_path=readme_path, lookup_string=lookup_string
    )

    logger.info(
        f"Found {len(script_to_embed)} script paths in {readme_path}: {script_to_embed}"
    )

    embed_dict = job.read_embeds_from_readme(
        embed_lines=script_to_embed, lookup_string=lookup_string
    )

    job.replace_embeds_in_readme(
        readme_path=readme_path, embed_dict=embed_dict, lookup_string=lookup_string
    )

    logger.info(f"Scripts were successfully updated in {readme_path}.")


if __name__ == "__main__":
    main(args.readme_path)
