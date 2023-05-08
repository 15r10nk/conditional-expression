import sys
from pathlib import Path
import ast

import textwrap

from typing import List, Tuple, Literal, NamedTuple


class Result(NamedTuple):
    file: Path
    line: int
    current_code: str
    new_code: str
    elements: int
    if_count: int


def add_to(node, var_name) -> Tuple[str, ast.expr] | Literal[False]:
    match node:
        case ast.AugAssign(
            target=ast.Name(id),
            op=ast.Add(),
            value=(ast.List() | ast.ListComp() as value),
        ) if id == var_name:
            return ("add", value)

        case ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id), attr="append"), args=[value]
            )
        ) if id == var_name:
            return ("append", value)

        case _:
            return False


def combine_parts(items):
    parts = []
    for kind, value in items:
        if kind == "add":
            if isinstance(value, ast.List):
                parts += value.elts
            else:
                parts.append(ast.Starred(value))

        elif kind == "append":
            parts.append(value)

    if len(parts) == 1:
        return ("append", parts[0])
    else:
        return ("add", ast.List(parts))


results = []
list_comprehensions=0
for file in Path(sys.base_prefix).rglob("*.py"):
    # for file in [Path("example.py")]:
    try:
        code = file.read_text()
        code_lines = code.splitlines()
        tree = ast.parse(code, str(file))
    except:
        continue

    for node in ast.walk(tree):
        if isinstance(node,ast.ListComp):
            list_comprehensions+=1

        for name, child in ast.iter_fields(node):
            if isinstance(child, list):
                for i in range(len(child)):
                    first = child[i]
                    if (
                        isinstance(first, ast.Assign)
                        and isinstance(first.value, (ast.List, ast.ListComp))
                        and len(first.targets) == 1
                        and isinstance(first.targets[0], ast.Name)
                    ):
                        var_name = first.targets[0].id
                        parts: List[Tuple[None | ast.expr, Tuple[str, ast.expr]]] = [
                            (None, ("add", first.value))
                        ]

                        for extra in child[i + 1 :]:
                            if (
                                isinstance(extra, ast.If)
                                and extra.orelse == []
                                and all(
                                    items := [add_to(n, var_name) for n in extra.body]
                                )
                            ):
                                parts.append((extra.test, combine_parts(items)))

                            # exit(0)
                            elif add_type := add_to(extra, var_name):
                                parts.append((None, add_type))
                            else:
                                break

                        if any(p[0] is not None for p in parts):
                            new_parts = []
                            lines = set()
                            for condition, (op, value) in parts:
                                for v in ast.walk(value):
                                    if hasattr(v, "lineno"):
                                        lines.add(v.lineno)
                                        lines.add(v.end_lineno)

                                if op == "add":
                                    match (condition, value):
                                        case None, ast.List(elts):
                                            new_parts += [ast.unparse(e) for e in elts]

                                        case ast.expr() as cond, ast.List(elts=[e]):
                                            new_parts.append(
                                                f"{ast.unparse(e)} if {ast.unparse(cond)}"
                                            )
                                        case _:
                                            new_part = "*" + ast.unparse(value)
                                            if condition is not None:
                                                new_part += " if " + ast.unparse(
                                                    condition
                                                )
                                            new_parts.append(new_part)

                                elif op == "append":
                                    new_part = ast.unparse(value)

                                    if condition is not None:
                                        new_part += " if " + ast.unparse(condition)
                                    new_parts.append(new_part)
                                else:
                                    assert False

                            line_start = min(lines)
                            line_end = max(lines)

                            nl = ",\n    "

                            results.append(
                                Result(
                                    file=file,
                                    line=line_start,
                                    elements=len(new_parts),
                                    if_count=len([part for part in parts if part[0] is not None]),
                                    current_code=textwrap.dedent(
                                        "\n".join(code_lines[line_start - 1 : line_end])
                                    ),
                                    new_code=f"{var_name}=[\n    {nl.join(new_parts)},\n]",
                                )
                            )
results.sort(key=lambda e: e.if_count,reverse=True)
print(
f"""

This is an analsis about some source code which creates lists and a possible alternative syntax. 
You can find [here](https://discuss.python.org/t/conditional-elements-arguments/26567/1) more information.

The source files for this analysis where taken from `sys.base_prefix`.

{len(results)} pattern can be transformed to the new syntax.

for reference: there are {list_comprehensions} list comprehensions in the code.

The following transformations are sorted by the number of conditions.

"""

    )

for result in results:


    file=str(result.file).partition("/lib/")[2]
    print()
    print()
    print(f"## {file}:{result.line}")
    print("current syntax:")
    print("``` python")
    print(result.current_code)
    print("```")

    print()
    print("new syntax:")

    print("``` python")
    print(result.new_code)
    print("```")
