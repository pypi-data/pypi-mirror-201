import ast

_IW_ERROR_LOG_WITHOUT_EXC_INFO_ERROR_MSG = "IW03 error log without exc_info"


class LoggerNameFinder(ast.NodeVisitor):
    def __init__(self, *args, **kwargs) -> None:
        self.logger_var_names: list[str] = []

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:

        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
        ):
            func_node: ast.Attribute = node.value.func

            if (
                func_node.attr == "getLogger"
                and isinstance(func_node.value, ast.Name)
                and func_node.value.id == "logging"
            ):
                self.logger_var_names.append(node.targets[0].id)
        self.generic_visit(node)
        return node


class ErrorLoggerFinder(ast.NodeVisitor):
    def __init__(self, tree, *args, **kwargs) -> None:
        self.tree = tree

        self.issues: list[tuple] = []

        logger_name_visitor = LoggerNameFinder()
        logger_name_visitor.visit(self.tree)

        self.logger_var_names = logger_name_visitor.logger_var_names

        super().__init__()

    def visit_Call(self, node: ast.Call) -> ast.Call:
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.attr == "error"
        ):
            if node.func.value.id in self.logger_var_names and not any(
                [keywork.arg == "exc_info" for keywork in node.keywords]
            ):
                self.issues.append(
                    (node.func.value.lineno, node.func.value.col_offset, _IW_ERROR_LOG_WITHOUT_EXC_INFO_ERROR_MSG)
                )

        self.generic_visit(node)
        return node
