"""Helper functions for VCS analysis logic"""

import os

from dotenv import load_dotenv
from github import Github
from loguru import logger

load_dotenv()


def get_github():
    """
    Returns an authenticated GitHub object if env variable is defined
    """

    if "GITHUB_TOKEN" in os.environ:
        gh_token = os.environ.get("GITHUB_TOKEN")
        if not gh_token:
            gh_token = None
    else:
        gh_token = None
        logger.info("Proceeding without GitHub Authentication")
    github_object = Github(gh_token)

    return github_object
