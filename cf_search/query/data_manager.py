import requests
from lxml import html

from typing import List, Dict, Tuple, Any
from .tokens import (
    make_contest_token,
    make_node_token,
    make_problem_token,
    make_source_token,
    make_submission_token,
    CfToken,
)

from .tree_sitter import TreeSitter


class CfDataManager:
    contests: List[CfToken]
    problems: List[CfToken]
    contest_submissions: Dict[str, List[CfToken]]
    submission_source: Dict[str, List[CfToken]]
    tree_sitter: TreeSitter

    def __init__(self) -> None:
        self.contests = _fetch_contests()
        self.problems = _fetch_problems()
        self.contest_submissions = {}
        self.submission_source = {}
        self.tree_sitter = TreeSitter()

    def get_submissions_for_contest(self, token: CfToken):
        assert token.type_name == "Contest"

        contest_id = token.content["id"]

        if contest_id not in self.contest_submissions:
            self.contest_submissions[contest_id] = _fetch_submissions_for_contest(
                contest_id
            )

        return self.contest_submissions[contest_id]

    def get_source_for_submission(self, token: CfToken):
        assert token.type_name == "Submission"

        submission_id = token.content["id"]

        if submission_id not in self.submission_source:
            contest_id = token.content["contest_id"]
            lang = token.content["programming_language"]

            src = _fetch_source_for_submission(contest_id, submission_id)
            root = self.tree_sitter.get_tree_for_source(src, lang).root_node
            self.submission_source[submission_id] = [make_source_token(src, root)]

        return self.submission_source[submission_id]

    def get_problem_for_submission(self, token: CfToken):
        assert token.type_name == "Submission"

        index = token.content["index"]
        contest_id = token.content["contest_id"]

        def filter_fn(p):
            return p.content["index"] == index and p.content["contest_id"] == contest_id

        return filter(filter_fn, self.problems)

    def get_children_for_source(self, token: CfToken):
        assert token.type_name == "Source"
        return _get_children_for_node(
            token.content["root_node"], token.content["source_code"]
        )

    def get_children_for_node(self, token: CfToken):
        assert token.type_name == "Node"
        return _get_children_for_node(token.content["node"], token.content["src"])


def _fetch_contests() -> List[CfToken]:
    response = requests.get("https://codeforces.com/api/contest.list").json()
    return list(map(make_contest_token, response["result"]))


def _fetch_problems() -> List[CfToken]:
    response = requests.get("https://codeforces.com/api/problemset.problems").json()

    zipped = zip(
        response["result"]["problems"], response["result"]["problemStatistics"]
    )

    return list(map(make_problem_token, zipped))


def _fetch_submissions_for_contest(contest_id: int) -> List[CfToken]:
    response = requests.get(
        "https://codeforces.com/api/contest.status?contestId=%d&from=1&count=100000"
        % contest_id
    ).json()

    if response["status"] != "OK":
        return []

    return list(map(make_submission_token, response["result"]))


def _fetch_source_for_submission(contest_id: int, submission_id: int) -> str:
    response = requests.get(
        "https://codeforces.com/contest/%d/submission/%d" % (contest_id, submission_id)
    )

    if not response.ok:
        pass

    tree = html.fromstring(response.text)
    source_code = tree.xpath('//*[@id="pageContent"]/div[3]/pre/text()')[0]

    return source_code


def _get_children_for_node(node: Any, src: str) -> List[CfToken]:
    return [make_node_token(n, src) for n in node.children]
