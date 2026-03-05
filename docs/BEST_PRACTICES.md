# Best Practices

## Research Workflow

| Best Practice | Description |
| ------------- | ----------- |
| Optimize for reproducibility first. | Every key result should be reproducible from code + config + seed + data snapshot. Prefer deterministic pipelines where feasible, and always store the exact command used to launch an experiment. |
| Treat experiments as versioned artifacts. | Track metrics, checkpoints, and config files per run. A result is only useful if you can trace it back to the code commit and dataset version that produced it. |
| Keep exploratory and production-like code separated. | Use notebooks for exploration, then migrate stable logic into `src/` modules used by both training and evaluation scripts. |
| Make ablations cheap to run. | Keep experiments modular so swapping model blocks, datasets, or hyperparameters does not require major refactors. |
| Write publication-ready outputs continuously. | Save plots/tables and experiment metadata in a consistent structure so paper/report generation does not become a last-minute manual step. |

## Project Bootstrap (Cookiecutter)

| Best Practice | Description |
| ------------- | ----------- |
| Create an empty remote repository first. | Create the GitHub repository before generating the project, and keep it empty (no README, no `.gitignore`, no license) to avoid merge friction in the first push. |
| Use a valid `repo_url` format. | Use one of: `git@host:org/repo.git`, `ssh://git@host/org/repo.git`, or `https://host/org/repo.git`. The post-generation hook validates the format before attempting `git remote add origin`. |
| Let post-gen run, then verify state. | The hook performs git/bootstrap actions and `uv sync` on a best-effort basis. After generation, verify that `origin` exists and that `main` was pushed successfully. |
| Keep a manual fallback path. | If push/auth/network fails, run the git and `uv sync` commands manually from the generated project directory. This keeps onboarding robust across different machine/network setups. |
| Keep generated history clean. | After bootstrap, ensure `main` is the working branch and remove the temporary `cookiecutter` branch remotely and locally when no longer needed. |

## Dependency and Platform Management

| Best Practice | Description |
| ------------- | ----------- |
| Pin Python baseline per project. | Set `minimal_python_version` intentionally and use the same value for local development and CI jobs to reduce environment drift. |
| Use platform-specific torch sources deliberately. | Linux uses CUDA source, Windows uses CUDA only when `enable_cuda=True`, otherwise CPU source, and macOS uses default PyPI source. This avoids accidental CUDA installs where unsupported. |
| Prefer declarative dependency management. | Keep dependencies in `pyproject.toml` and avoid ad-hoc installs that are not represented in versioned project metadata. |

## Training and Evaluation Pipeline

| Best Practice                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Separate pipeline definition from execution.                                   | Keep configuration, orchestration, and model code separated. This allows researchers to iterate quickly while keeping runs consistent across local machines and shared compute. |
| Use the same code for pre-processing in training and inference                 | The majority of time in most ML projects is allocated to data collection, data engineering, label and feature engineering. It is vital to ensure that the same code/logic is used by both the training and inference pipeline so that there are no opportunities for human errors and inconsistencies.                                                                                                                                                                                                                                                                                      |
| Maintain traceability across all experiment components.                        | Record which data, preprocessing, model architecture, and hyperparameters were used for each run. Keep this lineage in version control and experiment logs. |
| Ensure code gives consistent results across environments.                      | Code should behave similarly on laptop, workstation, and cluster. Use pinned dependencies and fixed seeds, and document known sources of non-determinism (for example, some GPU kernels). |
| Promote modularity in the development of Training and Inference solutions.     | Training and inference pipelines can be broken down into several components such as data validation, data preprocessing, data combination, etc.... When designing training and inference pipelines it is important that these components are created such that they can be developed, tested, and maintained independently from one another.                                                                                                                                                                                                                                                |
| Automate reporting for model and hyperparameter search.                        | Automatically log metrics and export result summaries so comparisons are transparent and easy to share within the lab/team. |
| Provision infrastructure and jobs as code.                                     | Define compute jobs and environments declaratively to reduce setup drift and speed up onboarding for new researchers. |

## Developer Environment

| Best Practice                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Support multiple research workflows.                                           | Researchers should be able to work from VS Code, notebooks, and remote servers without changing project structure. Avoid enforcing a single IDE workflow. |
| Utilize basic software development best practices.                            | Having a branching/collaboration strategy, using semantic versioning, using PRs, organizing the code repository, working effectively with notebooks, writing code that works on dummy data for testing as well as in pipeline, consistent formatting, type-checking, are some of the techniques that Data Scientists can borrow from software developers.                                            |
| Standardize dependency access patterns.                                        | Reduce one-off setup issues by documenting package/index policies and providing a stable default environment for common research stacks. |
| Keep model ownership close to domain experts.                                  | The people defining hypotheses and modeling choices should own experiment interpretation, while still using shared engineering standards for reproducibility. |
| Utilize automation and integrated version control for documentation.          | How many disparate sources of information would it take to review before a model could be transferred from one data scientist to another (e.g., confluence, GitHub, word document, etc...). Documentation should be semi-automated from the code itself, and should be contained in a single repository to ensure that it is always up-to-date.                                                      |
| Make dataset permissions and provenance explicit.                              | Document where data came from, what processing was applied, and what usage restrictions exist before experiments are shared or published. |
| Provision environments as code.                                                | Keep environment setup scripted (`uv`, lockfiles, task scripts) so collaborators can reproduce results without manual machine-specific setup. |
| Use secure and auditable storage for data and artifacts.                       | Protect sensitive data and maintain an audit trail for dataset access, model artifacts, and experiment outputs. |

## Monitoring and Validation

| Best Practice                                     | Description                                                                                                                                     |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Check train/validation/test consistency.          | Ensure preprocessing and evaluation logic are identical across splits and reruns to avoid hidden leakage and inflated metrics. |
| Monitor data drift for long-running studies.      | Track feature distribution changes over time when experiments are repeated on newly collected data. |
| Monitor metric stability across reruns.           | Re-run key experiments with multiple seeds and report variance, not only best-run performance. |
| Define retraining and re-evaluation triggers.     | Set explicit criteria for when new data or model changes require rerunning baselines and refreshing reported results. |
