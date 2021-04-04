cf-search
==================

Query CF API and submission ASTs using [tree-sitter](https://github.com/tree-sitter/tree-sitter) and [graphql-compiler](https://github.com/kensho-technologies/graphql-compiler).

## Setup
TODO

## Examples

Query all accepted Haskell submissions that import modules containing the substring "array".

```python
query = """
{
    Contest {
        id 
            @filter(op_name: ">=", value: ["$min_id"]) 
            @filter(op_name: "<=", value: ["$max_id"]) 
        
        out_Contest_Submission {
            id @output(out_name: "submission_id")
            programming_language 
                @filter(op_name: "=", value: ["$lang_name"])
                @output(out_name: "language")
            verdict 
                @filter(op_name: "=", value: ["$verdict"])
                @output(out_name: "verdict")
                
            out_Submission_Source {
                out_Source_Children {
                    out_Node_Children @recurse(depth: 3) {
                        type @filter(op_name: "in_collection", value: ["$node_types"])
                        content
                            @filter(op_name: "has_substring", value: ["$node_content_str"])
                            @output(out_name: "node_content")
                    }
                }
            }
        }
    }
}
"""

args = {
    "min_id": 1470,
    "max_id": 1500,
    "lang_name": "Haskell",
    "verdict": "OK",
    "node_types": ['qualified_module'],
    "node_content_str": 'Array',
}
```
