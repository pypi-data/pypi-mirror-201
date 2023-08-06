import ast
from dataclasses import dataclass
from typing import Optional, Union

_IW_PATCH_CALL_ERROR_MSG = "IW01 unsafe patch call"


def _get_function_call_attribute(node: Union[ast.Attribute, ast.Name]):
    if isinstance(node, ast.Name):
        return node.id, node
    elif isinstance(node.value, ast.Attribute) or isinstance(node.value, ast.Name):
        res, name_node = _get_function_call_attribute(node.value)
        return f"{res}.{node.attr}", name_node
    else:
        return "-", None


def _find_patch_call(node, imports):
    # Check direct patch function calls and alias function calls. e.g. patch() or mock_patch()
    if (
        node.func
        and isinstance(node.func, ast.Name)
        and node.func.id in imports
        and imports[node.func.id].full_name == "unittest.mock.patch"
    ):
        yield node.func

    # Check patch calls made using full function reference. e.g. unittest.mock.patch()
    if node.func and isinstance(node.func, ast.Attribute) and node.func.attr == "patch":
        # Extract module path and original ast.Name node
        module_path_attr, name_node = _get_function_call_attribute(node.func.value)
        if name_node and module_path_attr == "unittest.mock":
            yield node.func


@dataclass
class ImportName:
    """Dataclass for representing an import"""

    _module: str
    _name: str
    _alias: Optional[str]

    @property
    def name(self) -> str:
        """
        Returns the name of the import.
        The name is
            import pandas
                     ^-- this
            from pandas import DataFrame
                                  ^--this
            from pandas import DataFrame as df
                                            ^-- or this
        depending on the type of import.
        """
        return self._alias or self._name

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the import.
        The full name is
            import pandas --> 'pandas'
            from pandas import DataFrame --> 'pandas.DataFrame'
            from pandas import DataFrame as df --> 'pandas.DataFrame'
        """
        return f"{self._module}{self._name}"


class Visitor(ast.NodeVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.imports: dict[str, ImportName] = {}
        self.safe_patch_nodes: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        self.add_import(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.add_import(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.find_patch_decorator_excludes(node)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.find_patch_decorator_excludes(node)
        self.generic_visit(node)
        return node

    def visit_withitem(self, node: ast.withitem) -> ast.withitem:
        if isinstance(node.context_expr, ast.Call):
            for func_node in _find_patch_call(node.context_expr, self.imports):
                self.safe_patch_nodes.append(f"{func_node.lineno}:{func_node.col_offset}")

        return node

    def add_import(self, node: Union[ast.Import, ast.ImportFrom]) -> None:
        """Add relevant ast imports to import lists."""
        for name_node in node.names:
            if name_node.name:
                imp = ImportName(
                    _module=(f"{node.module}." if isinstance(node, ast.ImportFrom) else ""),
                    _alias=name_node.asname,
                    _name=name_node.name,
                )

                self.imports[imp.name] = imp

    def find_patch_decorator_excludes(self, node) -> None:
        func_decorator_list: list[ast.Name] = []

        for decorator_node in node.decorator_list:
            if isinstance(decorator_node, ast.Call):
                for func_node in _find_patch_call(decorator_node, self.imports):
                    func_decorator_list.append(func_node)

        for decorator_name in func_decorator_list:
            self.safe_patch_nodes.append(f"{decorator_name.lineno}:{decorator_name.col_offset}")


class ForbiddenPatchCallFinder(ast.NodeVisitor):
    def __init__(self, tree, *args, **kwargs) -> None:
        self.tree = tree

        parser = Visitor()
        parser.visit(self.tree)

        self.issues: list[tuple] = []
        self.imports: dict[str, ImportName] = parser.imports if parser.imports else {}
        self.excludes: list[str] = parser.safe_patch_nodes if parser.safe_patch_nodes else []
        super().__init__()

    def find_patch_call_issues(self, node):
        # Check direct patch function calls and alias function calls. e.g. patch() or mock_patch()
        for func_node in _find_patch_call(node, self.imports):
            node_loc = f"{func_node.lineno}:{func_node.col_offset}"
            if node_loc not in self.excludes:
                self.issues.append((node.lineno, node.col_offset, _IW_PATCH_CALL_ERROR_MSG))

    def visit_Call(self, node: ast.Call) -> ast.Call:
        self.find_patch_call_issues(node)
        self.generic_visit(node)
        return node
