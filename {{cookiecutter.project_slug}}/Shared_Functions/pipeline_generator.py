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

PIPELINE_MAIN_TEXT = (f'\
    """ Main script for the {folder_name} pipeline.
    
        To run this script, please use this command in the terminal,
        from the project root:
            uv run python -m Pipelines.{folder_name}.{file_name}"""\
    \n\
    \n## IMPORTS ##\
    \n# Internal\
    \nfrom Shared_Functions.logger_functionality import *\
    \nfrom .Functions.example_functions_script import example_function\
    \n## _______ ##\
    \n\
    \n## STATIC VARIABLES ##\
    \n# Directories - input\
    \n#INPUT_DIR_AAA = "xxx/yyy.zzz"\
    \n\
    \n# Directories - internal output\
    \n#OUTPUT_DIR_AAA = "Pipelines/{folder_name}/Data/xxx.zzz"\
    \n\
    \n# Directories - global output\
    \n#OUTPUT_DIR_AAA = "./Data/{folder_name}/xxx.zzz"\
    \n\
    \n# Directories - logs\
    \nOUTPUT_DIR_LOG_FULL_PIPELINE = "./Pipelines/{folder_name}/Logs/full_pipeline.log"\
    \nOUTPUT_DIR_LOG_1 = "./Pipelines/{folder_name}/Logs/example_1.log"\
    \nOUTPUT_DIR_LOG_2 = "./Pipelines/{folder_name}/Logs/example_2.log"\
    \n\
    \n# Other\
    \n## _______________________ ##\
    \n\
    \n## HELPER FUNCTIONS ##\
    \n## ________________ ##\
    \n\
    \n## MAIN FUNCTION ##\
    \ndef main() -> None:\ 
    \n    """Run the full ACT {folder_name.lower()} pipeline.\
    \n       Executes step 1 and step 2, and rebuilding of the combined pipeline log.\
    \n    """\
    \n    example_function(\
    \n        input_str="Hello",\
    \n        logger=setup_logger(\
    \n            output_dir_log=OUTPUT_DIR_LOG_1,\
    \n            logger_name="{folder_name.lower()}.step_1",\
    \n        ),\
    \n    )\
    \n\
    \n    example_function(\
    \n        input_str="world!",\
    \n        logger=setup_logger(\
    \n            output_dir_log=OUTPUT_DIR_LOG_2,\
    \n            logger_name="{folder_name.lower()}.step_2",\
    \n        ),\
    \n\
    \n    rebuild_pipeline_log(\
    \n        step_log_paths=[\
    \n            OUTPUT_DIR_LOG_1,\
    \n            OUTPUT_DIR_LOG_2,\
    \n        ],\
    \n        output_dir_log=OUTPUT_DIR_LOG_FULL_PIPELINE,\
    \n    )\
    \n\
    \n## _____________ ##\
    \n\
    \n## CALL OF MAIN FUNCTION ##\
    \nif __name__ == "__main__":\
    \n    main()')

PIPELINE_EXAMPLE_FUNCTIONS_SCRIPT_TEXT = (f'\
    """Generate additional working datasets from cleaned ACT message data.
    The module creates alternative representations of the cleaned message
        dataset for downstream analyses. It generates a dataset with
        consecutive messages collapsed by sender and a conversation-level
        dataset where all messages are combined into a single row.
    """\
    \n\
    \n## IMPORTS ##\
    \n# Standard\
    \nimport logging\
    \n\
    \n# External\
    \n## _______ ##\
    \n\
    \n## HELPER FUNCTIONS ##\
    \ndef _print_str(\
    \n    input_str: str,\
    \n    logger: logging.Logger,\
    \n) -> None:\
    \n    """Prints a given string to the terminal."""\
    \n\
    \n    print(input_str)\
    \n\
    \n    logger.info(f"{input_str} has been printed in the terminal.")
    \n## ________________ ##\
    \n\
    \n## MAIN FUNCTIONALITY ##\
    \ndef combine_example_functions(\
    \n    input_str: str,\
    \n    logger: logging.Logger,\
    \n) -> None:\
    \n    """Combines all helper functions within this script.\
    \n\
    \n    Args:\
    \n        input_str: String to be printed.\
    \n        logger: Logger used to write processing information.\
    \n    """\
    \n    _print_str(input_str, logger)\
    \n## __________________ ##')
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
    script_path.write_text(PIPELINE_MAIN_TEXT)

    functions_script_path = pipeline_path / "Functions" / "example_functions_script"
    functions_script_path.write_text(PIPELINE_EXAMPLE_FUNCTIONS_SCRIPT_TEXT)

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