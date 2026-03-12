#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration tasks to be run after the template has been generated."""

import logging
import os
import shutil
import subprocess
import re
import sys
from typing import Sequence

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("post_gen_project")

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

REPO_URL_PATTERNS = (
    r"^git@[^:\s]+:[^\s]+(?:\.git)?$",
    r"^ssh://git@[^/\s]+/.+(?:\.git)?$",
    r"^https://[^/\s]+/.+(?:\.git)?$",
)


def run_command(command: Sequence[str], *, check: bool = False) -> int:
    logger.info(INFO + f"Running: {' '.join(command)}" + TERMINATOR)
    try:
        completed_process = subprocess.run(command, check=check)
    except FileNotFoundError:
        logger.warning(WARNING + f"Command not found: {command[0]}" + TERMINATOR)
        return 127
    except subprocess.CalledProcessError as error:
        logger.warning(WARNING + f"Command failed ({error.returncode}): {' '.join(command)}" + TERMINATOR)
        return error.returncode

    if completed_process.returncode != 0:
        logger.warning(
            WARNING + f"Command failed ({completed_process.returncode}): {' '.join(command)}" + TERMINATOR,
        )
    return completed_process.returncode


def remove_cli_script(cli_enable: str, project_slug: str) -> None:
    cli_path = f"src/{project_slug}/cli.py"
    if cli_enable == "none" and os.path.exists(cli_path):
        os.remove(cli_path)


def is_valid_repo_url(repo_url: str) -> bool:
    return any(re.match(pattern, repo_url) for pattern in REPO_URL_PATTERNS)


def parse_repo_slug(repo_url: str) -> str | None:
    """Extract owner/repo from SSH/HTTPS git URLs."""
    patterns = (
        r"^git@[^:\s]+:(?P<slug>[^\s]+?)(?:\.git)?$",
        r"^ssh://git@[^/\s]+/(?P<slug>.+?)(?:\.git)?$",
        r"^https://[^/\s]+/(?P<slug>.+?)(?:\.git)?$",
    )
    for pattern in patterns:
        match = re.match(pattern, repo_url)
        if match:
            return match.group("slug")
    return None


def switch_remote_default_branch_to_main(repo_url: str) -> bool:
    """Try to set GitHub default branch to main using gh CLI."""
    repo_slug = parse_repo_slug(repo_url)
    if not repo_slug:
        logger.warning(WARNING + "Could not parse owner/repo from repo_url; cannot switch default branch automatically." + TERMINATOR)
        return False

    logger.info(INFO + f"Attempting to set default branch to main via gh for {repo_slug}" + TERMINATOR)
    rc = run_command(["gh", "repo", "edit", repo_slug, "--default-branch", "main"])
    if rc != 0:
        logger.warning(
            WARNING
            + "Failed to switch default branch using gh. Ensure gh is installed/authenticated or change default branch in GitHub settings."
            + TERMINATOR,
        )
        return False
    return True


def setup_git_repo() -> None:
    # Create git repo
    run_command(["git", "init", "-q"])
    # Setup empty main and dev
    run_command(["git", "checkout", "--orphan", "main", "-q"])
    run_command(["git", "commit", "--allow-empty", "-m", "Initial commit.", "-q"])
    run_command(["git", "checkout", "--orphan", "dev", "-q"])
    run_command(["git", "commit", "--allow-empty", "-m", "Initial commit.", "-q"])
    # Add cookiecutter on new branch
    run_command(["git", "checkout", "-b", "cookiecutter", "-q"])
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-am", "Setup cookiecutter", "-q"])
    run_command(["git", "tag", "-a", "v0.0.0", "-m", "Release tag for version 0.0.0"])


def setup_remote_and_push(repo_url: str) -> None:
    if "should look like:" in repo_url:
        logger.warning(WARNING + "repo_url is placeholder text; skipping remote setup/push." + TERMINATOR)
        return
    if not is_valid_repo_url(repo_url):
        logger.warning(
            WARNING
            + "repo_url format is invalid; expected SSH/HTTPS git URL (e.g. git@host:org/repo.git). Skipping remote setup/push."
            + TERMINATOR,
        )
        return

    run_command(["git", "remote", "add", "origin", repo_url])
    run_command(["git", "push", "--all"])
    run_command(["git", "push", "origin", "--tags"])
    run_command(["git", "checkout", "main"])
    run_command(["git", "merge", "cookiecutter"])
    run_command(["git", "push", "--set-upstream", "origin", "main"])
    run_command(["git", "branch", "-d", "cookiecutter"])
    delete_rc = run_command(["git", "push", "origin", "--delete", "cookiecutter"])
    if delete_rc != 0:
        logger.warning(
            WARNING
            + "Remote rejected deleting 'cookiecutter'. Trying to switch remote default branch to 'main' and retry."
            + TERMINATOR,
        )
        switched = switch_remote_default_branch_to_main(repo_url)
        if switched:
            delete_rc = run_command(["git", "push", "origin", "--delete", "cookiecutter"])

    if delete_rc != 0:
        logger.error(
            "[ERROR] Mandatory cleanup failed: remote branch 'cookiecutter' could not be deleted. "
            "Set default branch to 'main' in GitHub, then run: git push origin --delete cookiecutter",
        )
        sys.exit(1)

    run_command(["git", "checkout", "dev"])
    run_command(["git", "merge", "main"])
    run_command(["git", "push", "--set-upstream", "origin", "dev"])


def setup_env(minimal_python_version: str) -> None:
    logger.info(INFO + "Create your uv environment..." + TERMINATOR)
    if not os.path.exists("pyproject.toml"):
        run_command(["uv", "init", "--bare", "--python", minimal_python_version])
    else:
        logger.info(INFO + "Skipping uv init; pyproject.toml already exists." + TERMINATOR)
    run_command(["uv", "sync", "--python", minimal_python_version])


def main() -> None:

    project_slug = "{{ cookiecutter.project_slug }}"
    repo_url = "{{ cookiecutter.repo_url }}"
    minimal_python_version = "{{ cookiecutter.minimal_python_version }}"

    remove_cli_script("{{ cookiecutter.command_line_interface | default('none') }}", project_slug)
    logger.info(
        SUCCESS + "Project initialized successfully! You can now jump to {} folder".format(project_slug) + TERMINATOR,
    )
    logger.info(INFO + "{}/README.md contains instructions on how to proceed.".format(project_slug) + TERMINATOR)
    setup_git_repo()
    setup_remote_and_push(repo_url)
    setup_env(minimal_python_version)
    logger.info(
        SUCCESS + "Environment setup completed successfully!" + TERMINATOR,
    )
    


if __name__ == "__main__":
    main()

# EOF
