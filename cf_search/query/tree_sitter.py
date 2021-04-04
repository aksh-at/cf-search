from tree_sitter import Language, Parser, Tree
from typing import Any, Dict, Tuple

# map CF lang to tree-sitter lang
CF_LANG_MAP = {
    "GNU C++11": "cpp",
    "GNU C++14": "cpp",
    "GNU C++17 (64)": "cpp",
    "GNU C++17": "cpp",
    "Clang++17 Diagnostics": "cpp",
    "MS C++ 2017": "cpp",
    "Python 3": "python",
    "Haskell": "haskell",
    # 'Java 8',
    # 'D',
    # 'Ocaml',
    # 'Rust',
    # 'MS C++',
    # 'GNU C11',
    # 'Java 11',
    # 'Kotlin',
    # 'Mono C#',
    # 'Node.js',
    # 'Perl',
    # 'PyPy 3',
    # 'Python 2',
    # 'Scala',
    # 'PyPy 2',
    # 'Delphi',
    # 'FPC',
    # 'Go',
    # 'Ruby 3',
    # 'JavaScript',
    # '.NET Core C#',
    # 'PHP',
    # 'Python 3 + libs'
}

TREE_SITTER_LANGS = list(set(CF_LANG_MAP.values()))

BUILD_PATH = "build/languages.so"


class TreeSitter:
    def __init__(self) -> None:
        # assume submodules exist
        vendor_dirs = ["vendor/tree-sitter-%s" % l for l in TREE_SITTER_LANGS]
        Language.build_library(BUILD_PATH, vendor_dirs)

        self.parsers = {}
        for l in TREE_SITTER_LANGS:
            parser = Parser()
            parser.set_language(Language(BUILD_PATH, "haskell"))
            self.parsers[l] = parser

    def get_tree_for_source(self, src: str, cf_lang: str) -> Tree:
        if cf_lang not in CF_LANG_MAP:
            return None

        ts_lang = CF_LANG_MAP[cf_lang]
        parser = self.parsers[ts_lang]
        return parser.parse(bytes(src, "utf8"))
