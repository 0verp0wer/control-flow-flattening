import ast
import string
import random
import textwrap

class Flattening(ast.NodeTransformer):
    def __init__(self):
        self.max_steps = 3
        self.generated_names = []

    def generate_name(self) -> str:
        prefix = "Cyron__"
        chars = string.ascii_letters + string.digits
        type = random.randint(1, 2)

        if type == 1:
            while (name := prefix + "".join(random.choice(chars) for _ in range(4))) in self.generated_names:
                pass
        else:
            while (name := prefix + "v" + str(random.randint(1,9999))) in self.generated_names:
                pass

        self.generated_names.append(name)
        
        return name

    def add_flattening(self, value: ast.stmt) -> ast.stmt:   
        cases = []
        dict_values = {}

        number = random.randint(300, 500)
        original_value = number

        value_name = self.generate_name()
        dict_name = self.generate_name()
        inc_name = self.generate_name()
        dec_name = self.generate_name()

        numbers_used = [number]
        
        for stmt in value:
            n_steps = random.randint(1, self.max_steps)
            steps = ["assign", "decrement", "dict", "increment"]

            for _ in range(n_steps):
                step = random.choice(steps)
                match(step):
                    case "assign":
                        while(new_number := random.randint(300, 500)) in numbers_used:
                            pass
                        numbers_used.append(new_number)
                        body = self.set_ast_metadata(ast.match_case(
                            pattern=ast.MatchValue(value=ast.Constant(value=number)),
                            body=[
                                ast.Assign(
                                    targets=[ast.Name(id=value_name, ctx=ast.Store())],
                                    value=ast.Constant(value=new_number)
                                )
                            ]
                        ))
                        number = new_number
                    case "decrement":
                        dec_number = random.randint(1, 25)
                        while number - dec_number in numbers_used:
                            dec_number += 1
                        numbers_used.append(number - dec_number)
                        body = self.set_ast_metadata(ast.match_case(
                            pattern=ast.MatchValue(value=ast.Constant(value=number)),
                            body=[
                                ast.AugAssign(
                                    target=ast.Name(id=value_name, ctx=ast.Store()),
                                    op=ast.Sub(),
                                    value=ast.Constant(value=dec_number)
                                )
                            ]
                        ))
                        number -= dec_number
                    case "dict":
                        string_method = random.randint(0, 1)
                        if string_method == 0:
                            while(dict_number:=random.randint(300, 500)) in numbers_used:
                                pass
                            numbers_used.append(dict_number)
                            body = self.set_ast_metadata(ast.match_case(
                                pattern=ast.MatchValue(value=ast.Constant(value=number)),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=value_name, ctx=ast.Store())],
                                        value=ast.Subscript(
                                            value=ast.Name(id=dict_name, ctx=ast.Load()),
                                            slice=ast.Name(id=value_name, ctx=ast.Load()),
                                            ctx=ast.Load()
                                        )
                                    )
                                ]
                            ))
                            dict_values[number] = dict_number
                            number = dict_number
                        else:
                            while (new_number:=random.randint(300, 500)) in numbers_used:
                                pass
                            numbers_used.append(new_number)

                            inc_number = random.randint(1, 25)
                            while new_number + inc_number in numbers_used:
                                inc_number += 1
                            numbers_used.append(new_number + inc_number)

                            dec_number = random.randint(1, 25)
                            while new_number - dec_number in numbers_used:
                                dec_number += 1
                            numbers_used.append(new_number - dec_number)

                            body_1 = self.set_ast_metadata(ast.match_case(
                                pattern=ast.MatchValue(value=ast.Constant(value=number)),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=inc_name, ctx=ast.Store())],
                                        value=ast.Constant(value=inc_number)
                                    ),
                                    ast.Assign(
                                        targets=[ast.Name(id=dec_name, ctx=ast.Store())],
                                        value=ast.Constant(value=dec_number)
                                    ),
                                    ast.Assign(
                                        targets=[ast.Name(id=value_name, ctx=ast.Store())],
                                        value=ast.Constant(value=new_number)
                                    )
                                ]
                            ))

                            cases.append(body_1)

                            body_2 = self.set_ast_metadata(ast.match_case(
                                pattern=ast.MatchValue(value=ast.Constant(value=new_number - dec_number)),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=value_name, ctx=ast.Store())],
                                        value=ast.Subscript(
                                            value=ast.Name(id=dict_name, ctx=ast.Load()),
                                            slice=ast.Constant(value=str(new_number)),
                                            ctx=ast.Load()
                                        )
                                    )
                                ]
                            ))

                            cases.append(body_2)

                            old_number = new_number

                            while (new_number:=random.randint(300, 500)) in numbers_used:
                                pass
                            numbers_used.append(new_number)

                            body = self.set_ast_metadata(ast.match_case(
                                pattern=ast.MatchValue(value=ast.Constant(value=old_number + inc_number)),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=value_name, ctx=ast.Store())],
                                        value=ast.Constant(value=new_number)
                                    )
                                ]
                            ))

                            number = new_number

                    case "increment":
                        inc_number = random.randint(1, 25)
                        while number + inc_number in numbers_used:
                            inc_number += 1
                        numbers_used.append(number + inc_number)
                        body = self.set_ast_metadata(ast.match_case(
                            pattern=ast.MatchValue(value=ast.Constant(value=number)),
                            body=[
                                ast.AugAssign(
                                    target=ast.Name(id=value_name, ctx=ast.Store()),
                                    op=ast.Add(),
                                    value=ast.Constant(value=inc_number)
                                )
                            ]
                        ))
                        number += inc_number

                cases.append(body)
            if isinstance(stmt, ast.FunctionDef):
                cases[-1].body.insert(0, self.set_ast_metadata(ast.FunctionDef(
                    name=stmt.name,
                    args=stmt.args,
                    body=stmt.body,
                    decorator_list=stmt.decorator_list,
                    returns=stmt.returns
                )))
            elif hasattr(stmt, "body") and isinstance(stmt.body, list):
                cases[-1].body = stmt.body + cases[-1].body
            else:
                cases[-1].body.insert(0, stmt)

        random.shuffle(cases)

        default_case = self.set_ast_metadata(ast.match_case(
            pattern=ast.MatchAs(),
            body=[
                ast.Assign(
                    targets=[
                        ast.Subscript(
                            value=ast.Name(id=dict_name, ctx=ast.Load()),
                            slice=ast.Call(
                                func=ast.Name(id="str", ctx=ast.Load()),
                                args=[ast.Name(id=value_name, ctx=ast.Load())]
                            ),
                            ctx=ast.Store()
                        )
                    ],
                    value=ast.BinOp(
                        left=ast.Name(id=value_name, ctx=ast.Load()),
                        op=ast.Add(),
                        right=ast.Name(id=inc_name, ctx=ast.Load())
                    )
                ),
                ast.AugAssign(
                    target=ast.Name(id=value_name, ctx=ast.Store()),
                    op=ast.Sub(),
                    value=ast.Name(id=dec_name, ctx=ast.Load())
                )
            ]
        ))

        cases.append(default_case)
                
        cases_code = "\n".join([textwrap.indent(ast.unparse(case), "        ") for case in cases])

        code = f"""
{value_name} = {original_value}
{dict_name} = {dict_values}
{inc_name} = 0
{dec_name} = 0
while {value_name} != {number}: 
    match {value_name}:
{cases_code}
"""
        return ast.parse(code).body
    
    def set_ast_metadata(self, node: ast.stmt, lineno=1, col_offset=0) -> ast.stmt:
        if not isinstance(node, ast.AST):
            return node

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.set_ast_metadata(item, lineno, col_offset)
            elif isinstance(value, ast.AST):
                self.set_ast_metadata(value, lineno, col_offset)
                
        node.lineno = lineno
        node.col_offset = col_offset
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        node.body = self.add_flattening(node.body)
        return node

    def visit_Module(self, node: ast.Module) -> ast.Module:
        self.generic_visit(node)
        node.body = self.add_flattening(node.body)
        return node