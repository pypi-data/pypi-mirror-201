import ast

_IW_BULK_UPDATE_WITHOUT_BATCH_SIZE_ERROR_MSG = "IW06 bulk update without batch_size"
_BULK_UPDATE_METHOD_CALLS = ["bulk_update", "bulk_create"]


class BulkUpdateFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []

        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        # bulk_create / bulk_update
        # Model.objects.bulk_update()
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Attribute)
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.attr == "objects"
            and node.func.attr in _BULK_UPDATE_METHOD_CALLS
        ):
            if not any([keywork.arg == "batch_size" for keywork in node.keywords]):
                self.issues.append(
                    (node.func.lineno, node.func.col_offset, _IW_BULK_UPDATE_WITHOUT_BATCH_SIZE_ERROR_MSG)
                )

        self.generic_visit(node)
        return node
