import ast

_IW_TIME_PATCH_CALL_ERROR_MSG = "IW02 unsafe time patch call"


class ForbiddenTimePatchFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []
        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        if isinstance(node.func, ast.Name) and len(node.args) == 1 and node.func.id == "patch":
            patch_target = node.args[0]

            if isinstance(patch_target, ast.Constant) and patch_target.value == "django.utils.timezone.now":
                self.issues.append((node.func.lineno, node.func.col_offset, _IW_TIME_PATCH_CALL_ERROR_MSG))

        if isinstance(node.func, ast.Attribute) and len(node.args) == 1 and node.func.attr == "patch":
            patch_target = node.args[0]

            if isinstance(patch_target, ast.Constant) and patch_target.value == "django.utils.timezone.now":
                self.issues.append((node.func.value.lineno, node.func.value.col_offset, _IW_TIME_PATCH_CALL_ERROR_MSG))

        self.generic_visit(node)
        return node
