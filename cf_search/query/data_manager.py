import requests

from typing import List
from .tokens import make_contest_token, make_submission_token, CfToken

class CfDataManager:
    def __init__(self) -> None:
        self.contests = _get_contests()

def _get_contests():
    response = requests.get("https://codeforces.com/api/contest.list").json()
    return list(map(make_contest_token, response["result"]))

def get_submissions_for_contest(
    data_manager: CfDataManager, token: CfToken
) -> List[CfToken]:
    assert token.type_name == "Contest"

    results: List[CfToken] = []

    response = requests.get("https://codeforces.com/api/contest.status?contestId=%d&from=1&count=10000" % token.content["id"]).json()

    if response["status"] != "OK":
        return []

    return list(map(make_submission_token, response["result"]))
