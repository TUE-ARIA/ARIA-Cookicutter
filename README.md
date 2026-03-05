![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# ARIA Lab Cookiecutter

A practical cookiecutter template for starting our projects quickly with a consistent structure, `uv` dependency management, and sane defaults.

## What this gives you

- Project structure for data, docs, scripts, and source code
- `pyproject.toml` ready for `uv`
- Git bootstrap in the post-generation hook
- Optional CUDA-aware PyTorch source selection via `enable_cuda`

## Requirements

- Python 3.10+
- `uv` installed
- `cookiecutter` installed

Install cookiecutter from this repository root:

```bash
pip install -r requirements.txt
```

## Quickstart (recommended)

### 1) Create an empty GitHub repository

Create a new repository on GitHub first (no README, no `.gitignore`, no license).
Copy its SSH URL, for example:

```text
git@github.com:your-org/your-repo.git
```

### 2) Generate a project from this template

```bash
cookiecutter git@github.com:caetas/CookieCutter.git
```

During prompts:

- set `repo_name` to your GitHub repository name
- set `repo_url` to the SSH URL you copied above
- choose `enable_cuda` (`True` or `False`)

### 3) Let post-gen run

The hook automatically attempts to:

- initialize git branches/tags
- add `origin` from `repo_url`
- push branches/tags
- merge `cookiecutter` into `main`
- run `uv sync --python <minimal_python_version>`

### 4) If remote push was skipped or failed, run manually

If auth/network/permissions are not ready yet, run these in the generated project directory:

```bash
git remote add origin <repo_ssh>
git push --all
git push origin --tags
git checkout main
git merge cookiecutter
git push --set-upstream origin main
git branch -d cookiecutter
git push origin --delete cookiecutter
uv sync --python <min_version>
```

## Main template inputs

- `project_name`: Display/project name
- `repo_name`: Repository name (used for slug)
- `repo_url`: Remote git URL (validated in post-gen)
- `project_slug`: Python package/folder slug
- `organization`: Organization name
- `author_name`, `author_email`: Package metadata
- `description`: Short project description
- `license`: License selection
- `enable_cuda`: Controls Windows CUDA vs CPU PyTorch source in generated `pyproject.toml`
- `minimal_python_version`: Minimum Python version
- `line_length`: Formatting line length
- `version`: Initial package version

## Notes on platform behavior

- Linux: uses `pytorch-cu128` source in generated project
- Windows: uses CUDA source only when `enable_cuda=True`, otherwise CPU source
- macOS: falls back to default PyPI source

## Contributing

Pull requests are welcome, especially small and focused improvements to template usability.

## Inspired by

- [PyPackage](https://github.com/audreyr/cookiecutter-pypackage)
- [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)
- [python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter)
- [python-package-template](https://github.com/TezRomacH/python-package-template)
- [MLOpsPython](https://github.com/microsoft/MLOpsPython)
- [Kedro](https://github.com/kedro-org/kedro)
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup)

## License

See [LICENSE.md](LICENSE.md).
