from typing import Any, Dict, Iterable, Set, Tuple

from graphql_compiler.interpreter import DataContext, InterpreterAdapter
from graphql_compiler.interpreter.typedefs import EdgeInfo

from .data_manager import (
    CfDataManager,
    get_submissions_for_contest,
)
from .tokens import CfToken

class CfDataAdapter(InterpreterAdapter[CfToken]):
    data_manager: CfDataManager

    def __init__(self) -> None:
        self.data_manager = CfDataManager()

    def get_tokens_of_type(self, type_name: str, **hints: Dict[str, Any]) -> Iterable[CfToken]:
        if type_name == "Contest":
            return self.data_manager.contests
        else:
            raise NotImplementedError()

    def project_property(
        self,
        data_contexts: Iterable[DataContext[CfToken]],
        current_type_name: str,
        field_name: str,
        **hints: Dict[str, Any],
    ) -> Iterable[Tuple[DataContext[CfToken], Any]]:
        for data_context in data_contexts:
            token = data_context.current_token
            current_value = None
            if token is not None:
                current_value = token.content[field_name]

            yield (data_context, current_value)

    def project_neighbors(
        self,
        data_contexts: Iterable[DataContext[CfToken]],
        current_type_name: str,
        edge_info: EdgeInfo,
        **hints: Dict[str, Any],
    ) -> Iterable[Tuple[DataContext[CfToken], Iterable[CfToken]]]:
        edge_handlers = {
            ("Contest", ("out", "Contest_Submission")): get_submissions_for_contest,
        }

        handler_key = (current_type_name, edge_info)
        handler_for_edge = edge_handlers.get(handler_key, None)
        if handler_for_edge is None:
            raise NotImplementedError(handler_key)
        else:
            for data_context in data_contexts:
                token = data_context.current_token

                neighbors = []
                if token is not None:
                    neighbors = handler_for_edge(self.data_manager, token)

                yield (data_context, neighbors)

    def can_coerce_to_type(
        self,
        data_contexts: Iterable[DataContext[CfToken]],
        current_type_name: str,
        coerce_to_type_name: str,
        **hints: Dict[str, Any],
    ) -> Iterable[Tuple[DataContext[CfToken], bool]]:
        # Tuple (current_known_type, attempted_coercion_type) -> set of concrete types for which
        # the coercion is successful. The attempted coercion type may be concrete or abstract;
        # if abstract then all concrete types that are descended from it are in the value set.
        coercion_table: Dict[Tuple[str, str], Set[str]] = {
        }

        for data_context in data_contexts:
            token = data_context.current_token

            can_coerce = False
            if token is not None:
                # Getting a KeyError here means that the coercion table needs to be updated
                # to account for more type conversions that the schema allows to occur.
                allowed_types = coercion_table[(current_type_name, coerce_to_type_name)]
                can_coerce = token.type_name in allowed_types

            yield (data_context, can_coerce)
