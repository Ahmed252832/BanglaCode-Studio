from ast_nodes import *

class CCodeGenerator:
    def __init__(self, symbols):
        self.symbols = symbols
        self.lines = []
        self.indent = 1

    def emit(self, line=""):
        self.lines.append("    " * self.indent + line)

    def c_type(self, typ):
        if typ == "number":
            return "int"
        if typ == "string":
            return "char*"
        if typ == "boolean":
            return "int"
        if typ == "unknown":
            return "int"
        return "int"

    def generate(self, program):
        out = [
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "",
            "int main(void) {"
        ]

        self.lines = []
        self.indent = 1

        for stmt in program.statements:
            self.gen_statement(stmt)

        self.emit("return 0;")
        out.extend(self.lines)
        out.append("}")
        return "\n".join(out) + "\n"

    def gen_statement(self, node):
        if isinstance(node, VariableDeclaration):
            typ = self.symbols.get(node.name, "number")
            ctyp = self.c_type(typ)
            expr = self.gen_expression(node.value)
            self.emit(f"{ctyp} {node.name} = {expr};")
            return

        if isinstance(node, Assignment):
            expr = self.gen_expression(node.value)
            self.emit(f"{node.name} = {expr};")
            return

        if isinstance(node, PrintStatement):
            expr = self.gen_expression(node.expression)
            etype = self.infer_expr_type(node.expression)

            if etype == "string":
                self.emit(f'printf("%s\\n", {expr});')
            elif etype == "boolean":
                self.emit(f'printf("%s\\n", ({expr}) ? "shotto" : "mittha");')
            else:
                self.emit(f'printf("%d\\n", {expr});')
            return

        if isinstance(node, IfStatement):
            cond = self.gen_expression(node.condition)
            self.emit(f"if ({cond}) {{")
            self.indent += 1
            for stmt in node.then_block:
                self.gen_statement(stmt)
            self.indent -= 1

            if node.else_block is not None:
                self.emit("} else {")
                self.indent += 1
                for stmt in node.else_block:
                    self.gen_statement(stmt)
                self.indent -= 1
                self.emit("}")
            else:
                self.emit("}")
            return

        if isinstance(node, WhileStatement):
            cond = self.gen_expression(node.condition)
            self.emit(f"while ({cond}) {{")
            self.indent += 1
            for stmt in node.body:
                self.gen_statement(stmt)
            self.indent -= 1
            self.emit("}")
            return

        raise TypeError(f"Unsupported statement node: {type(node).__name__}")

    def gen_expression(self, node):
        if isinstance(node, NumberLiteral):
            return str(node.value)

        if isinstance(node, StringLiteral):
            escaped = (
                node.value
                .replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
            )
            return f'"{escaped}"'

        if isinstance(node, BooleanLiteral):
            return "1" if node.value else "0"

        if isinstance(node, Identifier):
            return node.name

        if isinstance(node, InputExpression):
            # Simple integer input for v1.0
            return "({ int _bc_input; scanf(\"%d\", &_bc_input); _bc_input; })"

        if isinstance(node, BinaryExpression):
            left = self.gen_expression(node.left)
            right = self.gen_expression(node.right)
            return f"({left} {node.operator} {right})"

        raise TypeError(f"Unsupported expression node: {type(node).__name__}")

    def infer_expr_type(self, node):
        if isinstance(node, NumberLiteral):
            return "number"
        if isinstance(node, StringLiteral):
            return "string"
        if isinstance(node, BooleanLiteral):
            return "boolean"
        if isinstance(node, Identifier):
            return self.symbols.get(node.name, "unknown")
        if isinstance(node, InputExpression):
            return "number"
        if isinstance(node, BinaryExpression):
            if node.operator in (">", "<", ">=", "<=", "==", "!="):
                return "boolean"
            return "number"
        return "unknown"


def generate_c(program, symbols):
    return CCodeGenerator(symbols).generate(program)
