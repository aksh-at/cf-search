from graphql import build_ast_schema, parse


# TODO: Grab these definitions directly from the GraphQL compiler package instead.
SCHEMA_BASE = """
schema {
    query: RootSchemaQuery
}

directive @filter(
    \"\"\"Name of the filter operation to perform.\"\"\"
    op_name: String!
    \"\"\"List of string operands for the operator.\"\"\"
    value: [String!]
) repeatable on FIELD | INLINE_FRAGMENT

directive @tag(
    \"\"\"Name to apply to the given property field.\"\"\"
    tag_name: String!
) on FIELD

directive @output(
    \"\"\"What to designate the output field generated from this property field.\"\"\"
    out_name: String!
) on FIELD

directive @output_source on FIELD

directive @optional on FIELD

directive @recurse(
    \"\"\"
    Recurse up to this many times on this edge. A depth of 1 produces the current
    vertex and its immediate neighbors along the given edge.
    \"\"\"
    depth: Int!
) on FIELD

directive @fold on FIELD

directive @macro_edge on FIELD_DEFINITION

directive @stitch(source_field: String!, sink_field: String!) on FIELD_DEFINITION
"""

CF_SCHEMA_TEXT = (
    SCHEMA_BASE
    + """

type Contest {
    id: Int
    name: String
    phase: String

    out_Contest_Submission: [Submission]
}

type Problem {
    contest_id: Int
    index: String
    name: String
    rating: Int
    tags: [String]
    solved_count: Int
}

type Submission {
   id: Int
   contest_id: Int
   index: String
   programming_language: String
   verdict: String

   out_Submission_Source: [Source]
   in_Submission_Problem: [Problem]
}

type Source {
   source_code: String
}

type RootSchemaQuery {
    Contest: [Contest]
    Problem: [Problem]
}
"""
)

CF_SCHEMA = build_ast_schema(parse(CF_SCHEMA_TEXT))
