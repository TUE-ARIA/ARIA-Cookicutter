# {{ cookiecutter.project_name }}

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

{{cookiecutter.description}}

## Prerequisites

You will need:

- `python` (see `pyproject.toml` for full version)
- `Git`
- `uv`
- a `.secrets` file with the required secrets and credentials
- load environment variables from `.env`
- `Weights & Biases` account

## Installation

Clone this repository (requires git ssh keys)

    git clone {{cookiecutter.repo_url}}
    cd {{cookiecutter.project_slug}}

### Using uv

Create the environment and install the dependencies:

    uv sync --python {{cookiecutter.minimal_python_version}}

#### Activate the environment on Linux

You can activate the environment with:

    source .venv/bin/activate

You might be required to run the following command once to setup the automatic activation of the conda environment and the virtualenv:

    direnv allow

Feel free to edit the [`.envrc`](.envrc) file if you prefer to activate the environments manually.

#### Activate the environment on Windows

You can activate the environment with:

    .venv-dev/Scripts/Activate.ps1

### Using Docker or Apptainer

Create a `.secrets` file and add your Weights & Biases API Key:

    WANDB_API_KEY = <your-wandb-api-key>

#### Docker

Create the image using the provided [`Dockerfile`](Dockerfile)

    docker build --tag {{ cookiecutter.project_slug }} .

Or download it from the Hub:

    docker pull docker://ocaetas/{{ cookiecutter.project_slug }}

Then run the script [`job_docker.sh`](scripts/job_docker.sh) that will execute [`main.sh`](scripts/main.sh):

    cd scripts
    bash job_docker.sh

To access the shell, please run:

    docker run --rm -it --gpus all --ipc=host --env-file .env -v $(pwd)/:/app/ {{ cookiecutter.project_slug }} bash

#### Apptainer

Convert the Docker Image to a `.sif` file:

    apptainer pull {{ cookiecutter.project_slug }}.sif docker://ocaetas/{{ cookiecutter.project_slug }}

Then run the script [`job_apptainer.sh`](scripts/job_apptainer.sh) that will execute [`main.sh`](scripts/main.sh):
    
    cd scripts
    bash job_apptainer.sh

To access the shell, please run:

    apptainer shell --nv --env-file .env --bind $(pwd)/:/app/ {{ cookiecutter.project_slug }}.sif

**Add the flag `--nvccli` if you are using WSL.**

**Note: Edit the [`main.sh`](scripts/main.sh) script if you want to train a different model.**

## Documentation

Full documentation is available here: [`docs/`](docs).

## License

This project is licensed under the terms of the `{{ cookiecutter.license }}` license.
See [LICENSE](LICENSE) for more details.

## Citation

If you publish work that uses {{ cookiecutter.project_name }}, please cite {{ cookiecutter.project_name }} as follows:

```bibtex
{% raw %}@misc{{% endraw %}{{ cookiecutter.project_name }},
  author = {% raw %}{{% endraw %}{{ cookiecutter.organization }}{% raw %}}{% endraw %},
  title = {% raw %}{{% endraw %}{{ cookiecutter.description }}{% raw %}}{% endraw %},
  year = {% raw %}{{% endraw %}{% now 'utc', '%Y' %}{% raw %}}{% endraw %},
}
```
