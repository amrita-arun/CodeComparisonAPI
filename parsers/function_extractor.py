import ast

class FunctionCallExtractor(ast.NodeVisitor):

    def __init__(self):
        self.function_calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute): # plt.imshow
            func_name = f"{node.func.value.id}.{node.func.attr}" if isinstance(node.func.value, ast.Name) else node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id
        else:
            func_name = "unknown"

        self.function_calls.append(func_name)
        self.generic_visit(node)

def parse_all_functions(file_path):
    with open(file_path, "r") as f:
        code = f.read()

    tree = ast.parse(code)
    extractor = FunctionCallExtractor()
    extractor.visit(tree)

    return extractor.function_calls

def get_code(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    return code
