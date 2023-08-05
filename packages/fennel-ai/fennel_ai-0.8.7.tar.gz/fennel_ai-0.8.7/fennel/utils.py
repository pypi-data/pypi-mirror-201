from __future__ import annotations

import ast
import dataclasses
import datetime
import hashlib
import inspect
import json
import textwrap
from typing import Any
from typing import cast, Callable, Dict, List, Tuple, Union

import astunparse  # type: ignore
import cloudpickle
import requests  # type: ignore

Tags = Union[List[str], Tuple[str, ...], str]

FHASH_ATTR = "__fennel_fhash__"


def check_response(response: requests.Response):
    """Check the response from the server and raise an exception if the response is not OK"""
    if response.status_code != 200:
        raise Exception(
            "Server returned: {}, {}, {}".format(
                response.status_code,
                response.reason,
                response.text,
            )
        )


def del_namespace(obj, depth):
    if not hasattr(obj, "__dict__"):
        return
    if depth > 10:
        return
    if "namespace" in obj.__dict__:
        obj.__dict__.pop("namespace")

    for k, v in obj.__dict__.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                del_namespace(v1, depth + 1)
        elif isinstance(v, list):
            for v1 in v:
                del_namespace(v1, depth + 1)
        else:
            del_namespace(v, depth + 1)


def fennel_pickle(obj: Any) -> bytes:
    """Pickle an object using the Fennel protocol"""
    del_namespace(obj, 0)
    return cloudpickle.dumps(obj)


class RemoveOffsetsTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        if hasattr(node, "lineno"):
            node.lineno = 1
        if hasattr(node, "col_offset"):
            node.col_offset = 2
        if hasattr(node, "end_lineno"):
            node.end_lineno = 3
        if hasattr(node, "end_col_offset"):
            node.end_col_offset = 4
        return super().generic_visit(node)


def _fhash_callable(obj: Callable) -> str:
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    new_tree = RemoveOffsetsTransformer().visit(tree)
    ast_text = astunparse.unparse(new_tree)
    return fhash(ast_text)


def _json_default(item: Any):
    try:
        return dataclasses.asdict(item)
    except TypeError:
        pass
    if isinstance(item, datetime.datetime):
        return item.isoformat(timespec="microseconds")

    if hasattr(item, FHASH_ATTR):
        return getattr(item, FHASH_ATTR)(item)

    if isinstance(item, bytes):
        return item.hex()

    if callable(item) and not inspect.isclass(item):
        return _fhash_callable(item)

    if isinstance(item, datetime.timedelta):
        return str(item.total_seconds())

    raise TypeError(f"object of type {type(item).__name__} not hashable")


def _json_dumps(thing: Any):
    return json.dumps(
        thing,
        default=_json_default,
        ensure_ascii=False,
        sort_keys=True,
        indent=None,
        separators=(",", ":"),
    )


def fhash(*items: Any):
    """Fennel Hash that is used to uniquely identify any python object."""
    item_list = list(cast(List[Any], items))
    return hashlib.md5(_json_dumps(item_list).encode("utf-8")).hexdigest()


def parse_annotation_comments(cls: Any) -> Dict[str, str]:
    try:
        source = textwrap.dedent(inspect.getsource(cls))
        source_lines = source.splitlines()
        tree = ast.parse(source)
        if len(tree.body) != 1:
            return {}

        comments_for_annotations: Dict[str, str] = {}
        class_def = tree.body[0]
        if isinstance(class_def, ast.ClassDef):
            for stmt in class_def.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(
                    stmt.target, ast.Name
                ):
                    line = stmt.lineno - 2
                    comments: List[str] = []
                    while line >= 0 and source_lines[line].strip().startswith(
                        "#"
                    ):
                        comment = source_lines[line].strip().strip("#").strip()
                        comments.insert(0, comment)
                        line -= 1

                    if len(comments) > 0:
                        comments_for_annotations[
                            stmt.target.id
                        ] = textwrap.dedent("\n".join(comments))

        return comments_for_annotations
    except Exception:
        return {}


def propogate_fennel_attributes(src: Any, dest: Any):
    """Propogates any  fennel attributes from src to dest."""
    if not hasattr(src, "__dict__"):
        return

    for k, v in src.__dict__.items():
        if k.startswith("__fennel") and k.endswith("__"):
            setattr(dest, k, v)
