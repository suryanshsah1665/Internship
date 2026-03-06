import ast

def extract_features(code_text):
    tree = ast.parse(code_text)

    num_functions = 0
    num_loops = 0
    num_conditionals = 0
    function_lengths = []
    max_depth = 0

    class CodeVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_depth = 0
            self.max_depth = 0

        def visit_FunctionDef(self, node):
            nonlocal num_functions
            num_functions += 1
            function_lengths.append(len(node.body))
            self.generic_visit(node)

        def visit_For(self, node):
            nonlocal num_loops
            num_loops += 1
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_While(self, node):
            nonlocal num_loops
            num_loops += 1
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_If(self, node):
            nonlocal num_conditionals
            num_conditionals += 1
            self.generic_visit(node)

    visitor = CodeVisitor()
    visitor.visit(tree)
    max_depth = visitor.max_depth

    lines_of_code = len(code_text.split("\n"))

    avg_function_length = (
        sum(function_lengths) / len(function_lengths)
        if function_lengths else 0
    )

    cyclomatic_complexity = num_loops + num_conditionals + num_functions + 1

    features = {
        "lines_of_code": lines_of_code,
        "num_functions": num_functions,
        "num_loops": num_loops,
        "num_conditionals": num_conditionals,
        "nested_loop_depth": max_depth,
        "avg_function_length": round(avg_function_length, 2),
        "cyclomatic_complexity": cyclomatic_complexity
    }

    return features