import ast

from modules.transformers.flattening import Flattening

file_name = input("insert the file name:")

with open(file_name, "r") as f:
    content = f.read()

tree = ast.parse(content)
tree = Flattening().visit(tree)

with open("out.py", "w") as f:
    f.write(ast.unparse(tree))
