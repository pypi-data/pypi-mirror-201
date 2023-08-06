import asyncio
import os
from typing import cast

from y42.cli.client import y42_client
from y42.cli.state import get_state
from y42.clients.company import CompanyClient
from y42.models.company import Company
from y42.models.space import Space


def print_shell_output(stdout, stderr):
    stdout_lines = stdout.decode("utf-8").strip().split("\n")
    stderr_lines = stderr.decode("utf-8").strip().split("\n")

    stdout_final = "\n".join(f"{line}" for line in stdout_lines).strip()
    stderr_final = "\n".join(f"{line}" for line in stderr_lines).strip()
    if stdout_final:
        print("[Shell stdout output]")
        print(stdout_final)
    if stderr_final:
        print("[Shell stderr output]")
        print(stderr_final)


def require_active_company() -> Company:
    state = get_state()
    if (
        state.active_company is not None
        and state.active_company not in state.known_companies
    ):
        print(
            f"Active company {state.active_company} is not in known companies - deactivating."
        )
        state.active_company = None
        state.persist()

    if state.active_company is None:
        if len(state.known_companies) == 0:
            print("No known companies, refreshing..")
            refresh_known_companies()

        if len(state.known_companies) == 1:
            slug = list(state.known_companies.keys())[0]
            state.active_company = slug
            state.persist()
            print(f"No active company, defaulting to only known company {slug}")
        elif len(state.known_companies) == 0:
            print(
                "No active company, and none are known! "
                "You can run `y42 company ls` to refresh, but it's looks like your API key does not have access to any."
            )
            exit(0)
        else:
            print("No active company! Run `y42 company activate` to choose one.")
            exit(0)

    slug = cast(str, state.active_company)
    company = state.known_companies[slug]
    return company


def find_git_root_from_cwd():
    checking_dir = os.getcwd()
    while checking_dir:
        files = os.listdir(checking_dir)
        if ".git" in files:
            return checking_dir
        parts = checking_dir.split(os.sep)
        if len(parts) <= 1:
            return None
        checking_dir = os.path.join(*parts[:-1])  # move up one level


def _get_space_and_company_from_cwd() -> tuple[Space | None, str | None, str | None]:
    state = get_state()
    git_root = find_git_root_from_cwd()
    if git_root is None:
        return (
            None,
            None,
            (
                "Your current working directory does not appear to be in a git repository. "
                "You can run `y42 space <name> cd` to navigate to the space you want to work on."
            ),
        )

    space_ids_by_dir = {
        _directory: _space_id for _space_id, _directory in state.space_dirs.items()
    }
    if (space_id := space_ids_by_dir.get(git_root)) is None:
        return (
            None,
            None,
            (
                "Your current working directory is in a git repository, but the repository is not a known Y42 space. "
                "You can run `y42 space ls` to refresh and list known spaces, "
                "`y42 space clone` to clone a space and "
                "`y42 space locate` to show the path to a space."
            ),
        )

    spaces_by_id = {
        str(space.space_id): (space, slug)
        for slug, spaces in state.known_spaces.items()
        for space in spaces.values()
    }
    space, slug = spaces_by_id[space_id]
    reason = None
    if slug != state.active_company:
        reason = f"Activated company {slug} as it contains the currently active space {space.repo_name}."

    return space, slug, reason


def require_space_from_cwd() -> Space:
    state = get_state()
    cwd_space, cwd_slug, reason = _get_space_and_company_from_cwd()
    if cwd_space is None:
        print(reason)
        exit(0)

    if cwd_slug != state.active_company:
        state.active_company = cwd_slug
        state.persist()
        print(reason)

    return cwd_space


def refresh_known_companies():
    state = get_state()
    companies: list[Company] = list(
        sorted(
            asyncio.get_event_loop().run_until_complete(y42_client.get_companies()),
            key=lambda c: c.slug,
        )
    )
    known_companies = {}
    for company in companies:
        known_companies[company.slug] = company
    state.known_companies = known_companies
    state.persist()


def refresh_known_spaces_for_company(company: Company):
    state = get_state()
    company_client = CompanyClient(company_id=company.company_id, init_from=y42_client)
    spaces: list[Space] = list(
        sorted(
            asyncio.get_event_loop().run_until_complete(company_client.get_spaces()),
            key=lambda c: c.repo_name,
        )
    )
    known_spaces = {}
    for space in spaces:
        known_spaces[space.repo_name] = space

    state.known_spaces[company.slug] = known_spaces
    state.persist()


def resolve_company_slug_or_index(company_slug_or_index: str | None):
    state = get_state()
    if company_slug_or_index is None:
        num_known = len(state.known_companies)
        if num_known == 1:
            company_slug_or_index = "0"
        else:
            print(
                f"COMPANY_SLUG_OR_INDEX argument was omitted but {num_known} companies are known. "
                "Please run `y42 company activate [COMPANY_SLUG_OR_INDEX]` to activate a company."
            )
            exit(0)

    company_slug_or_index = cast(str, company_slug_or_index)
    try:
        index = int(company_slug_or_index)  # type: ignore
        if len(state.known_companies) <= index:
            print(
                f"No company at index {index}. "
                f"You may need to run `y42 company ls` to refresh known companies locally."
            )
            exit(0)
        company_slug = list(state.known_companies)[index]
    except ValueError:
        company_slug = company_slug_or_index
    if company_slug not in state.known_companies:
        print(
            f"Company {company_slug} is unknown. "
            f"You may need to run `y42 company ls` to refresh known companies locally."
        )
        exit(0)
    return state.known_companies[company_slug]


def resolve_space_name_or_index(company_slug, space_name_or_index: str | None):
    state = get_state()
    known_spaces = state.known_spaces.get(company_slug, {})
    if space_name_or_index is None:
        num_known = len(known_spaces)
        if num_known == 1:
            space_name_or_index = "0"
        elif num_known == 0:
            print(
                f"No spaces known for company {company_slug}. "
                f"You may need to run `y42 company ls` to refresh known spaces locally"
            )
            exit(0)
        else:
            print(
                f"SPACE_NAME_OR_INDEX argument was omitted but "
                f"{num_known} spaces are known for company {company_slug}. "
                "Please run `y42 space activate [SPACE_NAME_OR_INDEX]` to activate a space."
            )
            exit(0)

    space_name_or_index = cast(str, space_name_or_index)
    try:
        index = int(space_name_or_index)
        if len(known_spaces) <= index:
            print(
                f"Index {index} is unknown, you may need to run `y42 company ls` to refresh known companies locally."
            )
            exit(0)
        space_name = list(known_spaces)[index]
    except ValueError:
        space_name = space_name_or_index
    space = known_spaces.get(space_name)
    if space is None:
        print(f"Space '{space_name}' not found for company {company_slug}.")
        exit(0)
    return space
