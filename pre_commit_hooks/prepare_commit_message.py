#!/usr/bin/env python

import argparse
import logging
import re
from subprocess import check_output
from typing import List, Optional, Sequence

GIT_MESSAGE_FORMAT = {"default": "[{}] {}", "jira": "[{}] {}"}
JIRA_PROJECT_BRANCH_REGEX = r"^(?P<gitflow>.*/)?(?P<jira_key>[A-Z]{2,10})-(?P<jira_ticket>[0-9]{1,10})(?=\s|-)(.+)$"
JIRA_PROJECT_COMMIT_REGEX = (
    r"^\[(?P<jira_key>[A-Z]{2,10})-(?P<jira_ticket>[0-9]{1,10})\](?=\s|-)(.+)$"
)

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.INFO, format="💭 prepare-commit-message - %(message)s",
)


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


def write_commit_message(filenames: Sequence[str], msg: str) -> int:
    for filename in filenames:
        with open(filename, "w") as f:
            f.writelines(msg)
    return 0


def extract_jira_identifier(regex, content, allowed):
    jira_match = None
    jira_prefix = None

    # Try to detect Jira project from content
    jira_match = re.match(regex, content)

    if jira_match is not None:
        jira_key = jira_match.group("jira_key")
        jira_ticket = jira_match.group("jira_ticket")
        jira_prefix = "{}-{}".format(jira_key, jira_ticket)

        if allowed is not None and jira_key not in allowed:
            logger.error(
                "Jira project '{}' found but is not allowed by the plugin."
                " Only the following projects are allowed {}".format(jira_key, allowed)
            )
            exit(2)

    return jira_prefix


def format_commit_message(
    msg: str, branch: str, fmt: str, exclude: List[str], allowed: List[str]
) -> str:

    new_commit_msg = msg
    logger.info("Prepare commit message for '{}' on branch '{}'".format(msg, branch))

    if branch in exclude:
        logger.info("Skipped formatting on branch {}".format(branch))
    else:
        if fmt == "default":
            # Simply append the branch name to the commit
            new_commit_msg = GIT_MESSAGE_FORMAT[fmt].format(branch, msg)

        elif fmt == "jira":
            # Try to detect jira project from commit msg
            jira_prefix = extract_jira_identifier(
                JIRA_PROJECT_COMMIT_REGEX, msg, allowed
            )

            if jira_prefix is None:
                # If not found in commit msg try in branch...
                logger.warning(
                    "Could not find Jira project in commit message"
                    " trying in branch name..."
                )
                jira_prefix = extract_jira_identifier(
                    JIRA_PROJECT_BRANCH_REGEX, branch, allowed
                )
            else:
                logger.info(
                    "Found Jira project in commit message {}".format(jira_prefix)
                )

            if jira_prefix is None:
                logger.error(
                    "Failed detecting Jira project / ticket number from branch"
                    " or commit message. You must use a valid pattern like '[MLE-123]'."
                    " Rejecting commit."
                )
                exit(1)

            if jira_prefix not in msg:
                new_commit_msg = GIT_MESSAGE_FORMAT[fmt].format(jira_prefix, msg)
            else:
                if "[{}]".format(jira_prefix) not in msg:
                    logger.info(
                        "Found Jira project in commit message {}"
                        " But the pattern is incorrect. You must use a valid"
                        " pattern like '[{}]'."
                        " Rejecting commit !".format(jira_prefix, jira_prefix)
                    )
                    exit(1)

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
    parser.add_argument(
        "--jira-projects",
        type=str,
        default=None,
        help="Comma separated list of jira projects allowed for this repository",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform dry-run and do write the commit message",
    )
    args = parser.parse_args(argv)

    branch = get_git_branch()
    commit_msg = get_commit_message(filenames=args.filenames)

    new_commit_msg = format_commit_message(
        msg=commit_msg,
        branch=branch,
        fmt=args.format,
        exclude=args.exclude,
        allowed=args.jira_projects.split(","),
    )

    logger.info("🔆Changing '{}' into '{}'".format(commit_msg, new_commit_msg))
    if not args.dry_run:
        write_commit_message(filenames=args.filenames, msg=new_commit_msg)
    else:
        logger.info("Dry-run mode enabled, commit message unchanged")

    return 0


if __name__ == "__main__":
    exit(main())
