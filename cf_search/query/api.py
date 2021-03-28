from typing import Any, Dict, Iterable

from graphql_compiler.compiler.compiler_frontend import graphql_to_ir
from graphql_compiler.interpreter import interpret_ir

from .interpreter import CfDataAdapter
from .schema import CF_SCHEMA

def get_default_adapter() -> CfDataAdapter:
    return CfDataAdapter()

def execute_query(
    adapter: CfDataAdapter, query: str, args: Dict[str, Any],
) -> Iterable[Dict[str, Any]]:
    ir_and_metadata = graphql_to_ir(CF_SCHEMA, query)
    return interpret_ir(adapter, ir_and_metadata, args)
