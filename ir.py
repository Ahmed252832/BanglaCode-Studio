from ast_nodes import *

class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, text):
        self.instructions.append(text)

    def generate(self, program):
        for stmt in program.statements:
            self.gen_statement(stmt)
        return self.instructions

    def gen_statement(self, node):
        if isinstance(node, VariableDeclaration):
            value = self.gen_expression(node.value)
            self.emit(f"{node.name} = {value}")
            return

        if isinstance(node, Assignment):
            value = self.gen_expression(node.value)
            self.emit(f"{node.name} = {value}")
            return

        if isinstance(node, PrintStatement):
            value = self.gen_expression(node.expression)
            self.emit(f"PRINT {value}")
            return

        if isinstance(node, IfStatement):
            cond = self.gen_expression(node.condition)
            else_label = self.new_label()
            end_label = self.new_label() if node.else_block is not None else else_label

            self.emit(f"IF_FALSE {cond} GOTO {else_label}")

            for stmt in node.then_block:
                self.gen_statement(stmt)

            if node.else_block is not None:
                self.emit(f"GOTO {end_label}")
                self.emit(f"{else_label}:")
                for stmt in node.else_block:
                    self.gen_statement(stmt)
                self.emit(f"{end_label}:")
            else:
                self.emit(f"{else_label}:")
            return

        if isinstance(node, WhileStatement):
            start_label = self.new_label()
            end_label = self.new_label()

            self.emit(f"{start_label}:")
            cond = self.gen_expression(node.condition)
            self.emit(f"IF_FALSE {cond} GOTO {end_label}")

            for stmt in node.body:
                self.gen_statement(stmt)

            self.emit(f"GOTO {start_label}")
            self.emit(f"{end_label}:")
            return

        raise TypeError(f"Unsupported statement node: {type(node).__name__}")

    def gen_expression(self, node):
        if isinstance(node, NumberLiteral):
            return str(node.value)

        if isinstance(node, StringLiteral):
            escaped = node.value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'

        if isinstance(node, BooleanLiteral):
            return "true" if node.value else "false"

        if isinstance(node, Identifier):
            return node.name

        if isinstance(node, InputExpression):
            temp = self.new_temp()
            self.emit(f"{temp} = INPUT")
            return temp

        if isinstance(node, BinaryExpression):
            left = self.gen_expression(node.left)
            right = self.gen_expression(node.right)
            temp = self.new_temp()
            self.emit(f"{temp} = {left} {node.operator} {right}")
            return temp

        raise TypeError(f"Unsupported expression node: {type(node).__name__}")


def generate_ir(program):
    generator = IRGenerator()
    return generator.generate(program)


def format_ir(instructions):
    return "\n".join(f"{i+1:03}: {inst}" for i, inst in enumerate(instructions))
