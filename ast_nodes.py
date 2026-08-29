from dataclasses import dataclass
from typing import Any, List, Optional
@dataclass
class Program: statements: List[Any]
@dataclass
class VariableDeclaration: name: str; value: Any
@dataclass
class Assignment: name: str; value: Any
@dataclass
class PrintStatement: expression: Any
@dataclass
class IfStatement: condition: Any; then_block: List[Any]; else_block: Optional[List[Any]]=None
@dataclass
class WhileStatement: condition: Any; body: List[Any]
@dataclass
class InputExpression: pass
@dataclass
class BinaryExpression: left: Any; operator: str; right: Any
@dataclass
class Identifier: name: str
@dataclass
class NumberLiteral: value: int
@dataclass
class StringLiteral: value: str
@dataclass
class BooleanLiteral: value: bool
