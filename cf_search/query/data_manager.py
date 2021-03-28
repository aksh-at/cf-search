import requests

from .tokens import make_contest_token

class CfDataManager:
    def __init__(self) -> None:
        self.contests = _get_contests()

def _get_contests():
    response = requests.get("https://codeforces.com/api/contest.list").json()
    return list(map(make_contest_token, response["result"]))
