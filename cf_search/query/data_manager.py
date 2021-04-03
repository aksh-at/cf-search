import requests
from lxml import html

from typing import List, Dict
from .tokens import (
    make_contest_token,
    make_submission_token,
    make_source_token,
    CfToken,
)


class CfDataManager:
    contests: List[CfToken]
    contest_submissions: Dict[str, List[CfToken]]
    submission_source: Dict[str, List[CfToken]]

    def __init__(self) -> None:
        self.contests = _fetch_contests()
        self.contest_submissions = {}
        self.submission_source = {}

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
        contest_id = token.content["contest_id"]

        if submission_id not in self.submission_source:
            self.submission_source[submission_id] = _fetch_source_for_submission(
                contest_id, submission_id
            )

        return self.submission_source[submission_id]


def _fetch_contests():
    response = requests.get("https://codeforces.com/api/contest.list").json()
    return list(map(make_contest_token, response["result"]))


def _fetch_submissions_for_contest(contest_id: int) -> List[CfToken]:
    response = requests.get(
        "https://codeforces.com/api/contest.status?contestId=%d&from=1&count=100000"
        % contest_id
    ).json()

    if response["status"] != "OK":
        return []

    return list(map(make_submission_token, response["result"]))


def _fetch_source_for_submission(contest_id: int, submission_id: int) -> List[CfToken]:
    response = requests.get(
        "https://codeforces.com/contest/%d/submission/%d" % (contest_id, submission_id)
    )

    if not response.ok:
        return []

    tree = html.fromstring(response.text)
    source_code = tree.xpath('//*[@id="pageContent"]/div[3]/pre/text()')[0]

    return [make_source_token(source_code)]
