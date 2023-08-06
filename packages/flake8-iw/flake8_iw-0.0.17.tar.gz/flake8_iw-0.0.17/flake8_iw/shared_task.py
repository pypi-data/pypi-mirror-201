import ast

_IW_ERROR_SHARED_TASK_MSG = "IW07 use of celery.shared_task, use instawork.decorators.shared_task"


class SharedTaskFinder(ast.NodeVisitor):
    def __init__(self, _, *args, **kwargs) -> None:
        self.issues: list[tuple] = []

        super().__init__()

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        # from celery import shared_task
        if node.module == "celery":
            imports_shared_task = any(map(lambda x: x.name == "shared_task", node.names))
            if imports_shared_task:
                self.issues.append((node.lineno, node.col_offset, _IW_ERROR_SHARED_TASK_MSG))

        self.generic_visit(node)
        return node
