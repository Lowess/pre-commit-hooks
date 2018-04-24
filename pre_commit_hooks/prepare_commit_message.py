#!/usr/bin/env python

import argparse
import os
import re
import sys
from subprocess import check_output
from typing import List, Optional, Sequence

GIT_MESSAGE_FORMAT = {"default": "[{}] - {}", "jira": "[{}] - {}"}
JIRA_PROJECT_REGEX = r"^(?P<gitflow>.*/)?(?P<jira_key>[A-Z]{2,10})-(?P<jira_ticket>[0-9]{1,10})(?=\s|-)(.+)$"


def get_git_branch():
    branch = (
        check_output(["git", "symbolic-ref", "--short", "HEAD"]).strip().decode("utf-8")
    )
    return branch


def get_commit_message(filenames: Sequence[str]) -> str:
    for filename in filenames:
        with open(filename, "r") as f:
            lines = [line.rstrip() for line in f.readlines()]

    return " ".join(lines)


def write_commit_message(filenames: Sequence[str], msg: str) -> str:
    for filename in filenames:
        with open(filename, "w") as f:
            f.writelines(msg)


def format_commit_message(msg: str, branch: str, fmt: str, exclude: List[str]) -> str:

    new_commit_msg = msg
    print("prepare-commit-message: for '{}' On branch '{}'".format(msg, branch))

    if branch in exclude:
        print("Skipped formatting on branch {}".format(branch))
    else:
        if fmt == "default":
            # Simply append the branch name to the commit
            new_commit_msg = GIT_MESSAGE_FORMAT[format].format(branch, msg)

        elif fmt == "jira":
            jira_match = None
            jira_prefix = None
            # Try to detect Jira project from the branch name
            # if not present try in commit message
            for content in [branch, msg]:
                jira_match = re.match(JIRA_PROJECT_REGEX, content)

                if jira_match is not None:
                    jira_key = jira_match.group("jira_key")
                    jira_ticket = jira_match.group("jira_ticket")
                    jira_prefix = "{}-{}".format(jira_key, jira_ticket)
                    break

            if jira_prefix is None or jira_ticket is None:
                print(
                    "Failed detecting Jira project / ticket number from branch"
                    " or commit message. Rejecting commit."
                )
                return 1

            if jira_prefix not in msg:
                new_commit_msg = GIT_MESSAGE_FORMAT[fmt].format(jira_prefix, msg)

    return new_commit_msg


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--exclude",
        type=list,
        default=["master", "develop", "stage"],
        help="The list of branches to ignore formatting",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["default", "jira"],
        default="default",
        help="Format that should be use",
    )

    args = parser.parse_args(argv)

    branch = get_git_branch()
    commit_msg = get_commit_message(args.filenames)

    new_commit_msg = format_commit_message(
        msg=commit_msg, branch=branch, fmt=args.format, exclude=args.exclude
    )

    print("💬 > '{}'\n🔄 > '{}'".format(commit_msg, new_commit_msg))
    write_commit_message(args.filenames, msg=new_commit_msg)


if __name__ == "__main__":
    exit(main())
