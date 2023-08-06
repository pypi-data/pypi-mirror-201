import ast

_IW_ERROR_DATETIME_REPLACE_TZINFO_MSG = "IW05 use of datetime.replace(tzinfo=XXX)"


class DatetimeReplaceTzinfoFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []

        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        # dt.replace(tzinfo=X)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "replace":
            if any([keyword.arg == "tzinfo" for keyword in node.keywords]):
                self.issues.append(
                    (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_DATETIME_REPLACE_TZINFO_MSG)
                )

        self.generic_visit(node)
        return node
