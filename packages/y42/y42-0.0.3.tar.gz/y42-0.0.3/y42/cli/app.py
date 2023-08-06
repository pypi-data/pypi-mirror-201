import asyncio
import os
from typing import Literal, cast

import typer

from y42.cli.client import reinit_client, y42_client
from y42.cli.settings import cli_settings
from y42.cli.state import get_state
from y42.cli.util import (
    _get_space_and_company_from_cwd,
    print_shell_output,
    refresh_known_companies,
    refresh_known_spaces_for_company,
    require_active_company,
    require_space_from_cwd,
    resolve_company_slug_or_index,
    resolve_space_name_or_index,
)
from y42.clients.space import SpaceClient, is_clone
from y42.models.company import Company
from y42.models.space import Space

app = typer.Typer(
    no_args_is_help=True,
)


@app.callback()
def callback(
    environment: str = typer.Option(
        None, help="Override for Y42_ENVIRONMENT ('prod' or 'dev')"
    ),
    api_key: str = typer.Option(None, help="Override for Y42_API_KEY"),
):
    environment = cast(Literal["dev", "prod"], environment)
    if environment is not None:
        cli_settings.Y42_ENVIRONMENT = environment
    if api_key is not None:
        cli_settings.Y42_API_KEY = api_key

    if not cli_settings.Y42_API_KEY:
        print("Y42_API_KEY is not set, and --api-key was not specified. Exiting.")
        exit(0)

    reinit_client()


company_app = typer.Typer()
app.add_typer(company_app, name="company", help="List/activate companies")
space_app = typer.Typer()
app.add_typer(space_app, name="space", help="Manage spaces in Y42")


def require_choice(prompt, deny_prompt: str = "Cancelling."):
    # TODO Typer actually has a util for this already
    choice = input(f"{prompt} [Y/n]")
    if not (choice.strip() == "" or choice.lower().strip() == "y"):
        print(deny_prompt)
        exit(0)


# ###### GENERAL UTILS ######


@app.command(
    help="Reset the local Y42 state. This does not delete your cloned repositories,"
    " (but will unlink them from the Y42 CLI)."
)
def reset():
    print("After reset, the following repos will be untracked, but not deleted:")
    repos()
    require_choice("Continue?")
    get_state().reset()


@app.command(help="Show currently active company and space, if any.")
def status():
    state = get_state()
    cwd_space, cwd_slug, reason = _get_space_and_company_from_cwd()
    print(f"Configured Y42 root directory: {cli_settings.Y42_ROOT_DIR}")
    suffix = ""
    if cwd_slug != state.active_company:
        suffix = f" (Current directory belongs to space of company {cwd_slug}!)"

    if state.active_company:
        print(f"Active company: {state.active_company}{suffix}")
    else:
        print(f"No active company{suffix}")

    if cwd_space:
        print(f"Space in current directory: {cwd_space.repo_name}")
    else:
        print("No space found in current directory.")


@app.command(name="state", help="Prints the current Y42 CLI app state in JSON format.")
def print_state():
    state = get_state()
    print(state.json(indent=4))


# ###### COMPANIES ######


@company_app.command(
    name="ls",
    help="Refresh and print the list of known Y42 companies for your current credentials.",
)
def company_ls():
    state = get_state()
    refresh_known_companies()
    for i, company_slug in enumerate(state.known_companies):
        # TODO best practices for output to make this play nicely with other CLI tools?
        print(f"{i}: {company_slug}")


@company_app.command(
    name="info",
    help="Print information about the specified (or only known) company in JSON format.",
)
def company_info(
    company_slug_or_index: str = typer.Argument(None), refresh: bool = False
):
    state = get_state()
    if refresh:
        # we could refresh only one, but no point for now as all API keys have only 1 company
        refresh_known_companies()

    if company_slug_or_index is None:
        require_active_company()
        company_slug_or_index = state.active_company

    company = resolve_company_slug_or_index(company_slug_or_index)
    print(company.json(indent=4, by_alias=True))


@company_app.command(
    name="activate",
    help="Activate company. Only needed if the specified Y42_API_KEY allows access to multiple companies.",
)
def activate_company(company_slug_or_index: str = typer.Argument(None)):
    state = get_state()
    company = resolve_company_slug_or_index(company_slug_or_index)
    if state.active_company != company.slug:
        state.active_company = company.slug
        state.persist()
        print(f"Activated company {company.slug}")
    else:
        print(f"Company {company.slug} is already active.")


# ###### SPACES ######


@space_app.command(name="ls", help="List known spaces")
def space_ls():
    state = get_state()
    company = require_active_company()
    refresh_known_spaces_for_company(company)
    for i, space_name in enumerate(state.known_spaces[company.slug]):
        # TODO best practices for output to make this play nicely with other CLI tools?
        print(f"{i}: {space_name}")


@space_app.command(
    name="locate", help="Print the directory that the space has been cloned to, if any."
)
def space_cd(
    space_name_or_index: str = typer.Argument(...),
):
    state = get_state()
    company = require_active_company()
    space = resolve_space_name_or_index(
        company_slug=company.slug, space_name_or_index=space_name_or_index
    )
    if (directory := state.space_dirs.get(str(space.space_id))) is None:
        print(f"Space {space.repo_name} does not appear to be cloned yet!")
        exit(0)
    print(directory)


@space_app.command(
    name="info",
    help="Print information about the specified space. "
    "If no space is specified, the current working directory must be a space.",
)
def space_info(
    space_name_or_index: str = typer.Argument(None),
    refresh: bool = False,
):
    company = require_active_company()
    if refresh:
        # TODO we could refresh only the selected space
        refresh_known_spaces_for_company(company)

    if space_name_or_index is None:
        space = require_space_from_cwd()
    else:
        space = resolve_space_name_or_index(company.slug, space_name_or_index)
    print(space.json(indent=4, by_alias=True))


# ###### REPOS ######


@app.command(
    name="repos",
    help="Print all currently cloned spaces and their local git repository directories.",
)
def repos():
    state = get_state()
    unknown_ids = []
    spaces_by_id: dict[str, Space] = {
        str(space.space_id): space
        for slug, spaces in state.known_spaces.items()
        for repo_name, space in spaces.items()
    }
    companies_by_id: dict[str, Company] = {
        company.company_id: company
        for company_slug, company in state.known_companies.items()
    }
    for space_id, repo_path in state.space_dirs.items():
        space = spaces_by_id.get(space_id)
        if space is None:
            unknown_ids.append(space_id)
        else:
            company = companies_by_id.get(space.company_id)
            company_slug = (
                f"Unknown company [ID: {space.company_id}]"
                if company is None
                else str(company.slug)
            )
            print(f"{company_slug}/{space.repo_name} -> {repo_path}")
    if unknown_ids:
        print(
            f"{len(unknown_ids)} locally tracked space repos are unknown (they may have been deleted on the remote):"
        )
        print("\n".join(unknown_ids))


# ###### GIT ######


@space_app.command(
    name="clone",
    help="Helper for running `git clone` against the specified space's git repository.",
)
def clone_space(
    space_name_or_index: str = typer.Argument(...),
    directory: str = typer.Argument(None),
    y: bool = typer.Option(False),
):
    state = get_state()
    company = require_active_company()
    space = resolve_space_name_or_index(
        company_slug=company.slug, space_name_or_index=space_name_or_index
    )
    if directory is None:
        directory = os.path.join(os.getcwd(), space.repo_name)
    elif directory.startswith("~"):
        directory = os.path.join(os.path.expanduser("~"), directory.removeprefix("~"))
    elif not directory.startswith("/"):
        directory = os.path.join(os.getcwd(), directory)

    if isinstance(directory, bytes):
        directory = directory.decode("utf-8")

    if not y:
        require_choice(f"Space will be cloned to {directory}. Proceed?")

    expected_dir = state.space_dirs.get(str(space.space_id))
    if expected_dir is not None:
        if expected_dir == directory:
            print(
                f"Space {space.repo_name} was already cloned to {expected_dir}, exiting."
            )
            exit(0)

        require_choice(
            f"Space {space.repo_name} was previously cloned to {expected_dir}. "
            f"Y42 CLI will no longer track the previous location if you clone this space to a new one. "
            f"Proceed anyway?"
        )

    space_client = SpaceClient(
        company_id=space.company_id,
        space_id=space.space_id,
        optional_repo_dir=directory,
        init_from=y42_client,
    )
    try:
        stdout, stderr = asyncio.get_event_loop().run_until_complete(
            space_client.clone()
        )
        print_shell_output(stdout, stderr)
    except Exception as e:
        print("Cloning failed:")
        raise e

    state.space_dirs[str(space.space_id)] = directory
    state.persist()


# wildcard for capturing git commands
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Helper alias for system's own `git` that applies Y42 authorization headers.",
    name="git",
)
def git(ctx: typer.Context, verbose: bool = typer.Option(False)):
    state = get_state()
    space = require_space_from_cwd()
    directory = state.space_dirs[str(space.space_id)]

    args_clean = []
    for c in ctx.args:
        if " " in c and not c.startswith('"'):
            args_clean.append(f'"{c}"')
        else:
            args_clean.append(c)

    if is_clone(args_clean):
        print(
            "Direct use of `git clone` is not supported - use `y42 space clone` to clone the active space."
        )

    space_client = SpaceClient(
        company_id=space.company_id,
        space_id=space.space_id,
        optional_repo_dir=directory,
        init_from=y42_client,
    )

    try:
        stdout, stderr = asyncio.get_event_loop().run_until_complete(
            space_client.git_cmd(args_clean)
        )
        print_shell_output(stdout, stderr)
    except Exception as e:
        print("Git command failed:")
        raise e
