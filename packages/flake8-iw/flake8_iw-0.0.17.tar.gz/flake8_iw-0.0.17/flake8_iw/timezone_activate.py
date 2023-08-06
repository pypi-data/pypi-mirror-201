import ast

_IW_ERROR_TIMEZONE_ACTIVATE_MSG = ("IW08 use of timezone.activate or timezome.deactivate, "
                                   "use with timezone.override instead")


class TimezoneActivateNowFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []

        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        # from django.utils import timezone
        # timezone.activate()
        # timezone.deactivate()
        if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "timezone"
                and node.func.attr in ["activate", "deactivate"]
        ):
            self.issues.append(
                (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_TIMEZONE_ACTIVATE_MSG)
            )

        # from django import utils
        # utils.timezone.activate()
        # utils.timezone.deactivate()
        if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Attribute)
                and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == "utils"
                and node.func.value.attr == "timezone"
                and node.func.attr in ["activate", "deactivate"]
        ):
            self.issues.append(
                (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_TIMEZONE_ACTIVATE_MSG)
            )

        self.generic_visit(node)
        return node
