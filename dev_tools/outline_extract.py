import ast

def extract_classes_and_functions(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    class ClassAndFunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.classes = []
            self.functions = []

        def visit_ClassDef(self, node):
            self.classes.append(node.name)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            self.functions.append(node.name)
            self.generic_visit(node)
    
    visitor = ClassAndFunctionVisitor()
    visitor.visit(tree)
    
    return visitor.classes, visitor.functions

if __name__ == "__main__":
    # Replace 'your_file.py' with the path to your Python file
    filename = 'data.py'
    
    classes, functions = extract_classes_and_functions(filename)
    
    print("Classes found:")
    for cls in classes:
        print(f' - {cls}')
    
    print("\nFunctions found:")
    for func in functions:
        print(f' - {func}')