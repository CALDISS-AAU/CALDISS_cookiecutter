# CALDISS Python Cookiecutter

Cookiecutter template for standardized Python data processing and analysis
projects at CALDISS, Aalborg University.

Generated projects include an example pipeline, shared logging utilities,
commands for creating and clearing pipelines, and a project entry point for
combining pipeline workflows.

## Requirements

- Cookiecutter installed in your environment, for example with
  `pip install cookiecutter`.
- [uv](https://docs.astral.sh/uv/) for managing the generated project.
- Python 3.12 or newer for the generated project. uv can provision a compatible
  Python version if needed.
- Git if you want version control.

## Create a project

Run:

```bash
cookiecutter https://github.com/CALDISS-AAU/CALDISS_cookiecutter.git
```

Answer the prompts, then enter the generated directory using the value you
selected for `project_slug`. For example, if the slug is `my_analysis`:

```bash
cd my_analysis
uv sync
uv run python -m main
```

`uv sync` creates the project environment and installs the project, including
its command-line tools. The initial workflow runs the example pipeline, prints
`Hello` and `World!`, and writes step logs and a combined pipeline log.

To start version control, run this from the generated project root:

```bash
git init
```

## Template variables

| Variable | Purpose and default behavior |
| --- | --- |
| `project_name` | Display name or abbreviation used in project documentation. |
| `project_slug` | Generated directory and project distribution name. Defaults to `project_name` with spaces replaced by underscores; casing is preserved. |
| `project_description` | Description inserted into the generated README. |
| `author_name` | Author or organization prompt; currently not used in the supplied generated files. |
| `author_email` | Contact email prompt; currently not used in the supplied generated files. |
| `github_username` | GitHub user or organization prompt; currently not used in the supplied generated files. |
| `package_name` | Defaults to `project_slug`; currently not used to create a Python package or configure packaging. |

Choose a simple `project_slug`, such as `my_analysis`, suitable for a directory
and Python distribution name. The default only replaces spaces; it does not
validate or remove other special characters.

## Generated project

```text
my_analysis/
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

`Data/` holds project input data. `Output/` is intended for shared or deliverable
outputs. Each pipeline has its own intermediate data, helper functions, and logs.
`Shared_Functions/` holds functionality reused across pipelines.

Newly created pipelines currently include `Data/`, `Functions/`, and `Logs/`; 
add tests and testing tools as needed. The template currently has no configured 
test runner, Ruff configuration, or automatic Git initialization.

## Pipeline commands

From the generated project root:

```bash
uv run create-pipeline data cleaning
uv run create-pipeline BERTopic --preserve-case --include model
```

The first command creates `Pipelines/Data_Cleaning/`, with
`data_cleaning_main.py` and a `data_cleaning_main()` function. The second creates
`Pipelines/BERTopic/`, with `BERTopic_main.py`, a `BERTopic_main()` function,
and an additional `Modelling/` directory.

Names are split into ASCII alphanumeric words and joined with underscores.
Normalized names must start with a letter. By default, folders use
`Capital_Snake_Case`, while file and function names use lowercase. With
`--preserve-case`, supplied casing is kept in folder, file, and function names.

To clear a normally named pipeline's generated data and logs:

```bash
uv run clear-pipeline Data_Cleaning
```

This deletes the contents of that pipeline's `Data/` and `Logs/` directories,
except `.gitkeep` files directly inside those directories. It has no confirmation
prompt. Review the target before running it.

The pipeline folder name must match exactly, including casing and underscores.
For example, clear a preserved-case pipeline with:

```bash
uv run clear-pipeline BERTopic
```

There is no name normalization and no `--preserve-case` option for clearing.
If only `Pipelines/Abc/` exists, `clear-pipeline ABC` and `clear-pipeline abc`
both fail; use `clear-pipeline Abc`.

See the generated project's README for running pipelines, adding them to
`main.py`, and using the logging helpers.

## Maintaining the template

- Edit files under `{{cookiecutter.project_slug}}/` to change the initial contents
  of newly generated projects.
- Edit `PIPELINE_MAIN_TEXT` and `PIPELINE_EXAMPLE_FUNCTIONS_SCRIPT_TEXT` in
  `Shared_Functions/Pipeline_Functions/pipeline_generator.py` to change files
  created by `create-pipeline`.
- Keep the bundled example pipeline and the generator's templates aligned.
  Updating either does not rewrite existing projects or pipelines.

## Generated project license

Generated projects include an MIT `LICENSE` with `CALDISS AAU` as the copyright
holder. The year is inserted when Cookiecutter generates the project and then
remains fixed in that file. Changing `author_name` does not change the license
holder.
