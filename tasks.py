import os
import sys
#abc
from invoke import task

CURRENT_DIR = os.getcwd()
WINDOWS = os.name == "nt"


@task
def install(ctx) -> None:
    """Create the environment for course."""
    ctx.run("conda create -n dtumlops python=3.11 pip --no-default-packages -y", echo=True, pty=not WINDOWS)
    ctx.run("conda activate dtumlops", echo=True, pty=not WINDOWS)
    ctx.run("pip install -r requirements.txt", echo=True, pty=not WINDOWS)


@task
def requirements(ctx):
    """Install Python requirements."""
    ctx.run("pip install -r requirements.txt", echo=True, pty=not WINDOWS)


@task
def precommit(ctx) -> None:
    """Install and run pre-commit checks."""
    ctx.run("pre-commit install", echo=True, pty=not WINDOWS)
    ctx.run("pre-commit run --all-files", echo=True, pty=not WINDOWS)


@task(aliases=["mkdocs"])
def docs(ctx) -> None:
    """Build the documentation."""
    ctx.run("mkdocs serve --dirty", echo=True, pty=not WINDOWS)


@task
def lint(ctx) -> None:
    """Run linters."""
    ctx.run("ruff check . --fix", echo=True, pty=not WINDOWS, warn=True)
    ctx.run("ruff format .", echo=True, pty=not WINDOWS, warn=True)
    ctx.run("mypy .", echo=True, pty=not WINDOWS)


@task
def docker_running(ctx):
    """Check if Docker is running."""
    result = ctx.run("docker info", pty=not WINDOWS, hide=True, warn=True)

    if result.ok:
        print("Docker is running.")
    else:
        print("Docker is not running.")
        sys.exit(1)


@task(docker_running)
def linkcheck(ctx) -> None:
    """Check for broken links."""
    ctx.run(
        (
            "docker build "
            "https://github.com/gaurav-nelson/github-action-markdown-link-check.git#master -t linkcheck:latest"
        ),
        echo=True,
        pty=not WINDOWS,
    )
    ctx.run(
        (
            "docker run "
            "--rm "
            f"-v {CURRENT_DIR}:/github/workspace "
            "linkcheck "
            """no no /github/workspace/.github/linkcheck_config.json /github/workspace -1 no master .md " " """
        ),
        echo=True,
        pty=not WINDOWS,
    )
