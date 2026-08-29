from ast_nodes import *

class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    """Basic semantic analysis for BanglaCode v1.0.

    v1.0 uses one global scope. Types are inferred from literal/expression values.
    inputNao() has type 'unknown' because input conversion is not implemented yet.
    """

    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, program):
        for stmt in program.statements:
            self.visit_statement(stmt)
        if self.errors:
            raise SemanticError("\n".join(self.errors))
        return self.symbol_table

    def error(self, message):
        self.errors.append(message)

    def visit_statement(self, node):
        if isinstance(node, VariableDeclaration):
            if node.name in self.symbol_table:
                self.error(f"Duplicate declaration: variable '{node.name}' is already declared.")
                # Still analyze RHS so we can discover other errors.
                self.infer_type(node.value)
                return
            value_type = self.infer_type(node.value)
            self.symbol_table[node.name] = value_type
            return

        if isinstance(node, Assignment):
            if node.name not in self.symbol_table:
                self.error(f"Undeclared variable: '{node.name}' must be declared with 'dhori' before assignment.")
                self.infer_type(node.value)
                return
            rhs_type = self.infer_type(node.value)
            old_type = self.symbol_table[node.name]
            if old_type == "unknown" and rhs_type != "unknown":
                self.symbol_table[node.name] = rhs_type
            elif rhs_type != "unknown" and old_type != rhs_type:
                self.error(
                    f"Type mismatch: variable '{node.name}' has type {old_type} "
                    f"but assignment has type {rhs_type}."
                )
            return

        if isinstance(node, PrintStatement):
            self.infer_type(node.expression)
            return

        if isinstance(node, IfStatement):
            condition_type = self.infer_type(node.condition)
            if condition_type not in ("boolean", "unknown"):
                self.error("If condition must evaluate to boolean.")
            for stmt in node.then_block:
                self.visit_statement(stmt)
            if node.else_block is not None:
                for stmt in node.else_block:
                    self.visit_statement(stmt)
            return

        if isinstance(node, WhileStatement):
            condition_type = self.infer_type(node.condition)
            if condition_type not in ("boolean", "unknown"):
                self.error("While condition must evaluate to boolean.")
            for stmt in node.body:
                self.visit_statement(stmt)
            return

        self.error(f"Unsupported AST statement: {type(node).__name__}")

    def infer_type(self, node):
        if isinstance(node, NumberLiteral):
            return "number"
        if isinstance(node, StringLiteral):
            return "string"
        if isinstance(node, BooleanLiteral):
            return "boolean"
        if isinstance(node, InputExpression):
            return "unknown"

        if isinstance(node, Identifier):
            if node.name not in self.symbol_table:
                self.error(f"Undeclared variable: '{node.name}' is used before declaration.")
                return "unknown"
            return self.symbol_table[node.name]

        if isinstance(node, BinaryExpression):
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)
            op = node.operator

            if op in ("+", "-", "*", "/", "%"):
                if left_type == "unknown" or right_type == "unknown":
                    return "unknown"
                if left_type != "number" or right_type != "number":
                    self.error(
                        f"Invalid arithmetic: operator '{op}' requires number operands, "
                        f"got {left_type} and {right_type}."
                    )
                    return "unknown"
                return "number"

            if op in (">", "<", ">=", "<="):
                if left_type == "unknown" or right_type == "unknown":
                    return "boolean"
                if left_type != "number" or right_type != "number":
                    self.error(
                        f"Invalid comparison: operator '{op}' requires number operands, "
                        f"got {left_type} and {right_type}."
                    )
                return "boolean"

            if op in ("==", "!="):
                if left_type != "unknown" and right_type != "unknown" and left_type != right_type:
                    self.error(
                        f"Type mismatch in comparison '{op}': got {left_type} and {right_type}."
                    )
                return "boolean"

            self.error(f"Unsupported operator '{op}'.")
            return "unknown"

        self.error(f"Unsupported expression node: {type(node).__name__}")
        return "unknown"


def analyze_ast(ast):
    analyzer = SemanticAnalyzer()
    symbols = analyzer.analyze(ast)
    return symbols
