"""Generate standardized pipeline folder structures for the project.

This module provides functionality for automatically generating new
pipeline directories within the project's Pipelines folder. Generated
pipelines follow the standardized project structure defined by the
CALDISS Python Cookiecutter template.

The module exposes a command-line interface through the
`create-pipeline` command.

Usage
-----
Create a new pipeline from the terminal:

    create-pipeline pipeline_name

Pipeline names may contain spaces, underscores, mixed casing, and
numbers. Only alphanumeric characters will be included in the final
pipeline name. Spaces and special characters are treated as word
separators and converted to underscores.

Example
-------
    create-pipeline data cleaning

This generates:

    Pipelines/
    └── Data_Cleaning/
        ├── Data/
        ├── Functions/
        ├── Logs/
        ├── Tests/
        ├── data_cleaning_main.py
        └── data_cleaning_README.md
"""

# IMPORTS #
from pathlib import Path
import argparse
import re
# _______ #

# STATIC VARIABLES #
FOLDERS_TO_GENERATE = [
    "Data", 
    "Functions", 
    "Logs", 
    "Tests"
]

PIPELINE_MAIN_TEXT = '''"""Main script for the {folder_name} pipeline.

To run this script, use the following command from the project root:
    uv run python -m Pipelines.{folder_name}.{file_name}_main
"""

## IMPORTS ##
# Internal
from Shared_Functions.logger_functionality import *
from .Functions.example_functions_script import example_function
## _______ ##


## STATIC VARIABLES ##
# Directories - input
# INPUT_DIR_AAA = "xxx/yyy.zzz"

# Directories - internal output
# OUTPUT_DIR_AAA = "Pipelines/{folder_name}/Data/xxx.zzz"

# Directories - global output
# OUTPUT_DIR_AAA = "./Data/{folder_name}/xxx.zzz"

# Directories - logs
OUTPUT_DIR_LOG_FULL_PIPELINE = "./Pipelines/{folder_name}/Logs/full_pipeline.log"
OUTPUT_DIR_LOG_1 = "./Pipelines/{folder_name}/Logs/example_1.log"
OUTPUT_DIR_LOG_2 = "./Pipelines/{folder_name}/Logs/example_2.log"

## _______________________ ##


## HELPER FUNCTIONS ##
## ________________ ##


## MAIN FUNCTION ##
def main() -> None:
    """Run the full {folder_name} pipeline."""

    example_function(
        input_str="Hello",
        logger=setup_logger(
            output_dir_log=OUTPUT_DIR_LOG_1,
            logger_name="{file_name}.step_1",
        ),
    )

    example_function(
        input_str="World!",
        logger=setup_logger(
            output_dir_log=OUTPUT_DIR_LOG_2,
            logger_name="{file_name}.step_2",
        ),
    )

    rebuild_pipeline_log(
        step_log_paths=[
            OUTPUT_DIR_LOG_1,
            OUTPUT_DIR_LOG_2,
        ],
        output_dir_log=OUTPUT_DIR_LOG_FULL_PIPELINE,
    )


## CALL OF MAIN FUNCTION ##
if __name__ == "__main__":
    main()
'''

PIPELINE_EXAMPLE_FUNCTIONS_SCRIPT_TEXT = '''"""Example helper functions for the pipeline."""

## IMPORTS ##
import logging
## _______ ##


## HELPER FUNCTIONS ##
def _print_str(
    input_str: str,
    logger: logging.Logger,
) -> None:
    """Print a string and log it."""

    print(input_str)
    logger.info("%s has been printed in the terminal.", input_str)


## MAIN FUNCTIONALITY ##
def example_function(
    input_str: str,
    logger: logging.Logger,
) -> None:
    """Example function for new pipelines."""

    _print_str(input_str, logger)
'''
# _________ #

# HELPER FUNCTIONS #
def split_words(text: str) -> list[str]:
    """Split text into alphanumeric words."""
    return re.findall(r"[A-Za-z0-9]+", text)


def to_capital_snake_case(text: str) -> str:
    """Convert text to Capital_Snake_Case."""
    words = split_words(text)
    return "_".join(word.lower().capitalize() for word in words)


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    words = split_words(text)
    return "_".join(word.lower() for word in words)

def find_project_root() -> Path:
    """Find the nearest parent directory containing pyproject.toml."""
    current_path = Path.cwd()

    for path in [current_path, *current_path.parents]:
        if (path / "pyproject.toml").exists():
            return path

    raise FileNotFoundError("Could not find project root with pyproject.toml.")
# ________________ #

# COMBINING ALL HELPERFUNTIONS #
def create_pipeline(name: str) -> None:
    """Create a standardized pipeline folder structure.

    Generate a new pipeline directory within the project's Pipelines
    folder, including the required subfolders and starter files.

    Parameters
    ----------
    name : str
        Name of the pipeline to create.

    Raises
    ------
    FileExistsError
        If the pipeline directory already exists.
    """
    folder_name = to_capital_snake_case(name)
    file_name = to_snake_case(name)

    project_root = find_project_root()
    pipeline_path = project_root / "Pipelines" / folder_name

    if pipeline_path.exists():
        raise FileExistsError(f"Pipeline already exists: {folder_name}")

    pipeline_path.mkdir(parents=True)

    for folder in FOLDERS_TO_GENERATE:
        folder_path = pipeline_path / folder
        folder_path.mkdir()
        (folder_path / ".gitkeep").touch()

    script_path = pipeline_path / f"{file_name}_main.py"
    script_path.write_text(
        PIPELINE_MAIN_TEXT.format(
            folder_name=folder_name,
            file_name=file_name,
        ),
        encoding="utf-8",
    )

    functions_script_path = (
        pipeline_path / "Functions" / "example_functions_script.py"
    )

    functions_script_path.write_text(
        PIPELINE_EXAMPLE_FUNCTIONS_SCRIPT_TEXT,
        encoding="utf-8",
    )

    readme_path = pipeline_path / f"{file_name}_README.md"
    readme_path.write_text(f"# {folder_name} README\n")

    print(f"Created pipeline: {folder_name}")
# ____________________________ #

# FUNCTION MAIN #
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pipeline_name", nargs="+")

    args = parser.parse_args()
    pipeline_name = " ".join(args.pipeline_name)

    try:
        create_pipeline(pipeline_name)

    except (FileExistsError, FileNotFoundError) as error:
        print(error)


if __name__ == "__main__":
    main()
# _____________ #