import ast

_IW_ERROR_DATETIME_NOW_MSG = "IW04 use of datetime.now"


class DatetimeNowFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []

        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        # from datetime import datetime
        # datetime.now()
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "datetime"
            and node.func.attr == "now"
        ):
            self.issues.append(
                (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_DATETIME_NOW_MSG)
            )

        # import datetime
        # datetime.datetime.now()
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Attribute)
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.value.id == "datetime"
            and node.func.attr == "now"
        ):
            self.issues.append(
                (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_DATETIME_NOW_MSG)
            )

        self.generic_visit(node)
        return node
