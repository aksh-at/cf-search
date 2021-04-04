from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass
class CfToken:
    type_name: str
    content: Dict[str, Any]  # field values
    # foreign_keys: Dict[str, List[Any]]  # values that help us look up neighbors


def make_contest_token(raw_data) -> CfToken:
    type_name = "Contest"

    content: Dict[str, Any] = {
        "id": raw_data["id"],
        "name": raw_data["name"],
    }

    return CfToken(type_name, content)


def make_problem_token(raw_inputs: Tuple[Any, Any]) -> CfToken:
    (problem_data, problem_stats) = raw_inputs

    assert problem_data["contestId"] == problem_stats["contestId"]
    assert problem_data["index"] == problem_stats["index"]

    type_name = "Problem"

    content: Dict[str, Any] = {
        "contest_id": problem_data["contestId"],
        "index": problem_data["index"],
        "name": problem_data["name"],
        "rating": problem_data.get("rating", None),
        "tags": problem_data["tags"],
        "solved_count": problem_stats["solvedCount"],
    }

    return CfToken(type_name, content)


def make_submission_token(raw_data) -> CfToken:
    type_name = "Submission"

    content: Dict[str, Any] = {
        "id": raw_data["id"],
        "contest_id": raw_data["contestId"],
        "index": raw_data["problem"]["index"],
        "verdict": raw_data["verdict"],
        "programming_language": raw_data["programmingLanguage"],
    }

    return CfToken(type_name, content)


def make_source_token(source_code, root_node) -> CfToken:
    type_name = "Source"

    content: Dict[str, Any] = {
        "source_code": source_code,
        # not exposed in the schema
        "root_node": root_node,
    }

    return CfToken(type_name, content)


def make_node_token(node, src) -> CfToken:
    type_name = "Node"

    node_content = src[node.start_byte:node.end_byte]

    content: Dict[str, Any] = {
        "type": node.type,
        "content": node_content,
        # not exposed in the schema
        "node": node,
        "src": src,
    }

    return CfToken(type_name, content)
