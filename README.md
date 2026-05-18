# CALDISS Python Cookiecutter

Cookiecutter template for creating standardized Python projects at CALDISS.

---

## Requirements

Install Cookiecutter:

```bash
pip install cookiecutter
```

---

## Usage

Generate a new project:

```bash
cookiecutter https://github.com/CALDISS-AAU/CALDISS_cookiecutter.git
```

Create uv-environment within the new project:
```bash
cd {{ cookiecutter.project_name }}
uv sync
```

Make git compatible:
```bash
cd {{ cookiecutter.project_name }}
git init
```

---

## Template Variables

During setup you will be prompted for:

| Variable | Description |
|---|---|
| `project_name` | Project name / abbreviation |
| `project_slug` | Project folder + package name |
| `project_description` | Short project description |
| `author_name` | Author or organization |
| `author_email` | Contact email |
| `github_username` | GitHub organization/user |
| `package_name` | Python package name |

---

## Generated Structure

The template generates a Python project with:

- standardized folder structure
- Python package setup
- testing setup
- linting/formatting configuration
- Git initialization

---

## Example

```bash
project_name [PROJECT - preferably the project abreviation]: My Analysis Tool
project_slug [my_analysis_tool]:
project_description [Short project description]: Internal analytics toolkit
```

This generates:

```text
my_analysis_tool/
```