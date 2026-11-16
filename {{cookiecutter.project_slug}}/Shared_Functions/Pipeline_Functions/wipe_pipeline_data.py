"""Clear generated data and log files from an exact pipeline folder.

This module provides the `clear-pipeline` command, which removes files
and subdirectories from a pipeline's Data and Logs directories.

The Data and Logs directories themselves are preserved, along with
their directly contained .gitkeep files.

Pipeline names must match the existing folder name exactly, including
casing and underscores. No name normalization is performed.

Usage
-----
    uv run clear-pipeline Data_Cleaning
    uv run clear-pipeline BERTopic

Run the command from the project root or an environment configured
for this project.

Contents are deleted without a confirmation prompt.
"""

# IMPORTS #
from pathlib import Path
import argparse
import shutil
# _______ #


# STATIC VARIABLES #
FOLDERS_TO_CLEAR = [
    "Data",
    "Logs",
]
# ________________ #


# HELPER FUNCTIONS #
def find_project_root() -> Path:
    """Find the nearest parent directory containing pyproject.toml."""
    current_path = Path.cwd()

    for path in [current_path, *current_path.parents]:
        if (path / "pyproject.toml").is_file():
            return path

    raise FileNotFoundError(
        "Could not find project root containing pyproject.toml."
    )


def clear_directory(directory_path: Path) -> None:
    """Remove all contents except directly contained .gitkeep files.

    Parameters
    ----------
    directory_path : Path
        Directory whose contents should be removed.
    """
    for item_path in directory_path.iterdir():
        if item_path.name == ".gitkeep":
            continue

        if item_path.is_symlink() or item_path.is_file():
            item_path.unlink()
        elif item_path.is_dir():
            shutil.rmtree(item_path)
# ________________ #


# MAIN FUNCTIONALITY #
def clear_pipeline(name: str) -> None:
    """Clear the Data and Logs directories for an exact pipeline name.

    Parameters
    ----------
    name : str
        Exact pipeline folder name, including casing and underscores.

    Raises
    ------
    FileNotFoundError
        If the project root, Pipelines directory, or exact pipeline
        directory cannot be found.
    NotADirectoryError
        If a pipeline's Data or Logs path is not a directory.
    ValueError
        If a selected pipeline or cleanup directory is a symbolic link.
    """
    project_root = find_project_root()
    pipelines_root = project_root / "Pipelines"

    if not pipelines_root.is_dir():
        raise FileNotFoundError(
            "Could not find the Pipelines directory."
        )

    # Compare actual directory names to enforce exact casing,
    # including on filesystems that normally ignore case.
    pipeline_path = next(
        (
            path
            for path in pipelines_root.iterdir()
            if path.name == name and path.is_dir()
        ),
        None,
    )

    if pipeline_path is None:
        raise FileNotFoundError(
            f"Pipeline does not exist with this exact name: {name}"
        )

    if pipeline_path.is_symlink():
        raise ValueError(
            f"Refusing to clear a symbolic-link pipeline: {name}"
        )

    # Validate all targets before deleting any contents.
    directories_to_clear: list[Path] = []

    for folder_name in FOLDERS_TO_CLEAR:
        folder_path = pipeline_path / folder_name

        if folder_path.is_symlink():
            raise ValueError(
                "Refusing to clear a symbolic-link directory: "
                f"{folder_path.relative_to(project_root)}"
            )

        if not folder_path.exists():
            print(
                "Skipped missing directory: "
                f"{folder_path.relative_to(project_root)}"
            )
            continue

        if not folder_path.is_dir():
            raise NotADirectoryError(
                f"Expected a directory: {folder_path}"
            )

        directories_to_clear.append(folder_path)

    for folder_path in directories_to_clear:
        clear_directory(folder_path)

    if directories_to_clear:
        folders_text = " and ".join(
            folder_path.name
            for folder_path in directories_to_clear
        )
        print(
            f"Cleared {folders_text} for pipeline: {pipeline_path.name}"
        )
    else:
        print(
            f"No directories were cleared for pipeline: "
            f"{pipeline_path.name}"
        )
# __________________ #


# COMMAND-LINE INTERFACE #
def main() -> None:
    """Run the pipeline-cleaning command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Remove contents from a pipeline's Data and Logs "
            "directories. The pipeline folder name must match exactly. "
            "Files are deleted without confirmation."
        )
    )

    parser.add_argument(
        "pipeline_name",
        help=(
            "Exact pipeline folder name, including casing "
            "and underscores."
        ),
    )

    args = parser.parse_args()

    try:
        clear_pipeline(name=args.pipeline_name)

    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")


if __name__ == "__main__":
    main()
# ______________________ #