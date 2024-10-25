import argparse

from loguru import logger

from src.code_embedding import CodeEmbedder, ScriptPathExtractor

parser = argparse.ArgumentParser()
parser.add_argument("--readme-path", type=str, help="Path to Readme", default="README.md")
args = parser.parse_args()

lookup_regex = r"^```.*?:"

if __name__ == "__main__":
    script_path_extractor = ScriptPathExtractor(
        readme_path=args.readme_path, lookup_regex=lookup_regex
    )
    code_embedder = CodeEmbedder(
        readme_path=args.readme_path,
        lookup_regex=lookup_regex,
        script_path_extractor=script_path_extractor,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")
