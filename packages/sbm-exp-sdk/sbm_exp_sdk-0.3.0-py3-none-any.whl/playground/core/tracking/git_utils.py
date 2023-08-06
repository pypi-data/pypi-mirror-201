from typing import cast

from playground.constants import GITLAB_URL
from pygit2 import GIT_STATUS_WT_MODIFIED, Repository


def get_branch_name() -> str:
    return cast(str, Repository(".").head.shorthand)


def get_repo_name() -> str:
    return cast(str, Repository(".").remotes[0].url.split(".git")[0].split("/")[-1])


def get_gitlab_path() -> str:
    path = Repository(".").remotes[0].url.split(".git")[0].split(":")[1]
    return f"{GITLAB_URL}/{path}"


def check_uncommitted_changes() -> bool:
    status = Repository(".").status()
    for file, fstatus in status.items():
        if "notebooks" in file:
            continue
        if fstatus == GIT_STATUS_WT_MODIFIED:
            return True

    return False


def get_commit_hash() -> str:
    return cast(str, Repository(".").revparse_single("HEAD").hex)
