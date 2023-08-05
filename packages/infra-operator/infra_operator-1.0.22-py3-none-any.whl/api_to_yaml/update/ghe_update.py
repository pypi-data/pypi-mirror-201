#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api_to_yaml.layout.mod import parse as filename_parse
import os
from github import Github

from api_to_yaml.operators.mod import dict_matcher

github = Github(base_url="https://git.toolsfdg.net/api/v3",
                login_or_token=os.getenv('GITHUB_TOKEN'), retry=3)


def collaborator_update(content, current):
    repo = github.get_organization(current["metadata"]["Organization"]).get_repo(
        current["metadata"]["RepoName"])
    cols_target = content.get("spec", {}).get("collaborators", {})
    cols_current = current.get("spec", {}).get("collaborators", {})
    to_delete, to_create, to_update, unchanged = dict_matcher(
        cols_target, cols_current)
    for col in to_create + to_update:
        try:
            repo.add_to_collaborators(col, cols_target[col])
        except Exception as e:
            print("add_to_collaborators failed", col, e)
    for col in to_delete:
        try:
            repo.remove_from_collaborators(col)
        except Exception as e:
            print("remove_from_collaborators failed", col, e)


def update_repo(kind, content, info, current):
    check_list = [
        collaborator_update,
    ]
    for check in check_list:
        check(content, current)
