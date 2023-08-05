from __future__ import annotations

import re


def find_github_details_from_url(text: str) -> str:
    """Find a GitHub url and gets its parts, from given text"""
    match = re.search(
        r"github.com/([^/]+)/([^/\s\r\n?#]+)(?:/tree/|)?([^/\s\r\n?#]+)?", text
    )
    if match:
        owner, repo, branch = match[1], match[2], match[3]
        return owner, repo, branch

    return None, None, None
