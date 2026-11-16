# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

This repository organizes the project's data processing and analysis into
pipelines, with shared helpers and a central entry point for combining them.

## Setup

Install [uv](https://docs.astral.sh/uv/), then open a terminal in this directory,
which contains `pyproject.toml`, and run:

```bash
uv sync
```

The project requires Python 3.12 or newer. uv creates the project environment
and installs the project and its command-line tools. No manual environment
activation is needed when using `uv run`.

If this directory is not yet a Git repository, initialize it with:

```bash
git init
```

## Run the project

Run commands from the project root so relative data and log paths resolve
correctly:

```bash
uv run python -m main
```

Initially, `main.py` runs the example pipeline. It prints `Hello` and `World!`
and writes logs under `Pipelines/Example_Pipeline/Logs/`.

To run the example pipeline independently:

```bash
uv run python -m Pipelines.Example_Pipeline.example_pipeline_main
```

## Project structure

```text
.
├── Data/
├── Output/
├── Pipelines/
│   └── Example_Pipeline/
│       ├── Data/
│       ├── Functions/
│       │   └── example_functions_script.py
│       ├── Logs/
│       ├── example_pipeline_main.py
│       └── example_pipeline_README.md
├── Shared_Functions/
│   ├── __init__.py
│   ├── logger_functionality.py
│   └── Pipeline_Functions/
│       ├── pipeline_generator.py
│       └── wipe_pipeline_data.py
├── LICENSE
├── README.md
├── main.py
└── pyproject.toml
```

| Location | Purpose |
| --- | --- |
| `Data/` | Original project input data. |
| `Output/` | Shared outputs and deliverables produced by the project. |
| `Pipelines/<name>/Data/` | Intermediate data used within one pipeline. |
| `Pipelines/<name>/Functions/` | Helpers specific to one pipeline. |
| `Pipelines/<name>/Logs/` | Individual step logs and the combined pipeline log. |
| `Pipelines/<name>/<name>_main.py` | Pipeline entry script; exact casing follows the naming options below. |
| `Pipelines/<name>/<name>_README.md` | Pipeline documentation; initially contains a heading only. |
| `Shared_Functions/` | Helpers shared across pipelines. |
| `main.py` | Imports and runs selected pipeline entry functions. |

## Create a pipeline

From the project root:

```bash
uv run create-pipeline data cleaning
```

This creates:

```text
Pipelines/Data_Cleaning/
├── Data/
├── Functions/
│   └── example_functions_script.py
├── Logs/
├── data_cleaning_main.py
└── data_cleaning_README.md
```

The entry function is named `data_cleaning_main()`. Run the pipeline with:

```bash
uv run python -m Pipelines.Data_Cleaning.data_cleaning_main
```

The generator finds the project root by searching upward from the current
directory for the nearest `pyproject.toml`. The installed `create-pipeline`
command can therefore also be used from project subdirectories when the project
environment is activated.

### Naming and casing

By default, pipeline folders use `Capital_Snake_Case`, while filenames and
entry function names use lowercase. Use `--preserve-case` to retain the supplied
casing throughout:

```bash
uv run create-pipeline BERTopic --preserve-case
uv run create-pipeline 'ABC#1' --preserve-case
```

| Name | Option | Folder | Main script | Entry function |
| --- | --- | --- | --- | --- |
| `data cleaning` | Default | `Data_Cleaning` | `data_cleaning_main.py` | `data_cleaning_main()` |
| `BERTopic` | Default | `Bertopic` | `bertopic_main.py` | `bertopic_main()` |
| `BERTopic` | `--preserve-case` | `BERTopic` | `BERTopic_main.py` | `BERTopic_main()` |
| `ABC#1` | `--preserve-case` | `ABC_1` | `ABC_1_main.py` | `ABC_1_main()` |

Names are split into words containing only `A–Z`, `a–z`, and `0–9`. Spaces,
underscores, punctuation, and non-ASCII letters act as separators; repeated
separators become a single underscore between words. The normalized name must
start with a letter. Names containing no ASCII alphanumeric characters or
starting with a digit after normalization are rejected. Existing pipeline
directories are not overwritten.

Quote names containing special shell characters so they are passed literally.

### Optional folders

Include a `Modelling/` directory with `--include model` or `-i model`:

```bash
uv run create-pipeline topic modelling --include model
uv run create-pipeline BERTopic --preserve-case -i model
```

`model` is currently the only optional folder group. The `--include` option can
be repeated; duplicate folders are generated only once.

## Add a pipeline to the project workflow

Creating a pipeline does not automatically add it to `main.py`. Import its
entry function and call it in the order required by the workflow. For example,
after creating `data cleaning`, `main.py` could contain:

```python
from Pipelines.Data_Cleaning.data_cleaning_main import data_cleaning_main


def main() -> None:
    data_cleaning_main()


if __name__ == "__main__":
    main()
```

Run the combined workflow with `uv run python -m main`.

Replace the generated example functions with your processing steps and document
inputs, outputs, dependencies, and execution order in the pipeline README. Direct
shared or deliverable outputs to `Output/`; the commented global-output examples
in the supplied scripts currently point to `Data/` and should be adjusted when
used.

## Logging

`Shared_Functions/logger_functionality.py` provides:

- `setup_logger(output_dir_log, logger_name, overwrite=True)`: creates a file
  logger and its parent directory. The log file is overwritten by default; use
  `overwrite=False` to append.
- `rebuild_pipeline_log(step_log_paths, output_dir_log)`: overwrites a combined
  log with the current contents of existing step logs, in the supplied order.
  Missing step logs are skipped.

The generated pipeline demonstrates two step logs (`example_1.log` and
`example_2.log`) and combines them into `full_pipeline.log`. All are stored in
that pipeline's `Logs/` directory.

## Clear pipeline data and logs

Pass the exact existing pipeline folder name, including casing and underscores:

```bash
uv run clear-pipeline Data_Cleaning
```

**This command deletes files and subdirectories without a confirmation prompt.**
It clears only `Pipelines/Data_Cleaning/Data/` and
`Pipelines/Data_Cleaning/Logs/`, preserving those directories and their directly
contained `.gitkeep` files. It leaves pipeline code, `Modelling/`, project-level
`Data/`, and `Output/` untouched. Missing data or log directories are skipped.

The command does not normalize names or accept `--preserve-case`. For a
pipeline created with preserved casing, use its folder name directly:

```bash
uv run clear-pipeline BERTopic
uv run clear-pipeline ABC_1
```

For example, if only `Pipelines/Abc/` exists:

| Command | Result |
| --- | --- |
| `uv run clear-pipeline Abc` | Clears that pipeline's data and logs. |
| `uv run clear-pipeline ABC` | Error: no exact matching pipeline. |
| `uv run clear-pipeline abc` | Error: no exact matching pipeline. |

A pipeline created with `create-pipeline 'ABC#1' --preserve-case` is cleared
using `clear-pipeline ABC_1`, because `ABC_1` is the actual folder name.
Exact casing is checked even on filesystems that normally ignore case.

The cleaner validates both target directories before deleting contents and
rejects symbolic links used as the pipeline folder or its `Data/` or `Logs/`
directory. Missing directories are skipped.

## Add dependencies

Add runtime dependencies through uv, for example:

```bash
uv add pandas
```

Add development tools separately with `uv add --dev <tool>`. Formatting and
linting are not configured automatically in this project.

## License

See [LICENSE](LICENSE) for the MIT license. Its copyright year was set when the
project was generated, and its copyright holder is `CALDISS AAU`.
