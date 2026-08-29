from lexer import tokenize, LexerError
from ast_nodes import *

class ParserError(Exception): pass

class Parser:
    def __init__(self,tokens): self.tokens=tokens; self.pos=0
    @property
    def current(self): return self.tokens[self.pos]
    def match(self,*types): return self.current.type in types
    def consume(self,t, msg=None):
        tok=self.current
        if tok.type!=t:
            raise ParserError(f"{msg or 'Expected '+t} at line {tok.line}, column {tok.column}; found {tok.type} ({tok.value!r})")
        self.pos+=1; return tok
    def parse(self):
        stmts=[]
        while not self.match("EOF"): stmts.append(self.parse_statement())
        return Program(stmts)
    def parse_statement(self):
        if self.match("DHORI"): return self.parse_declaration()
        if self.match("IDENTIFIER"): return self.parse_assignment()
        if self.match("DEKHAO"): return self.parse_print()
        if self.match("JODI"): return self.parse_if()
        if self.match("JOTOKKHON"): return self.parse_while()
        t=self.current; raise ParserError(f"Unexpected token {t.type} ({t.value!r}) at line {t.line}, column {t.column}")
    def parse_declaration(self):
        self.consume("DHORI"); name=self.consume("IDENTIFIER","Expected identifier after 'dhori'").value
        self.consume("ASSIGN","Expected '=' after identifier"); val=self.parse_expression()
        self.consume("SEMICOLON","Expected ';' after declaration"); return VariableDeclaration(name,val)
    def parse_assignment(self):
        name=self.consume("IDENTIFIER").value; self.consume("ASSIGN","Expected '=' after identifier")
        val=self.parse_expression(); self.consume("SEMICOLON","Expected ';' after assignment"); return Assignment(name,val)
    def parse_print(self):
        self.consume("DEKHAO"); self.consume("LPAREN","Expected '(' after 'dekhao'")
        e=self.parse_expression(); self.consume("RPAREN","Expected ')' after expression")
        self.consume("SEMICOLON","Expected ';' after print statement"); return PrintStatement(e)
    def parse_if(self):
        self.consume("JODI"); c=self.parse_condition(); self.consume("LBRACE","Expected '{' after condition")
        then=self.parse_block(); other=None
        if self.match("NAHOLE"):
            self.consume("NAHOLE"); self.consume("LBRACE","Expected '{' after 'nahole'"); other=self.parse_block()
        return IfStatement(c,then,other)
    def parse_while(self):
        self.consume("JOTOKKHON"); c=self.parse_condition(); self.consume("LBRACE","Expected '{' after condition")
        return WhileStatement(c,self.parse_block())
    def parse_block(self):
        stmts=[]
        while not self.match("RBRACE"):
            if self.match("EOF"): raise ParserError("Expected '}' before end of file")
            stmts.append(self.parse_statement())
        self.consume("RBRACE"); return stmts
    def parse_condition(self):
        left=self.parse_expression()
        if not self.match("GT","LT","GE","LE","EQ","NE"):
            t=self.current; raise ParserError(f"Expected comparison operator at line {t.line}, column {t.column}")
        op=self.current.value; self.pos+=1; right=self.parse_expression(); return BinaryExpression(left,op,right)
    def parse_expression(self):
        e=self.parse_term()
        while self.match("PLUS","MINUS"):
            op=self.current.value; self.pos+=1; e=BinaryExpression(e,op,self.parse_term())
        return e
    def parse_term(self):
        e=self.parse_factor()
        while self.match("MULTIPLY","DIVIDE","MOD"):
            op=self.current.value; self.pos+=1; e=BinaryExpression(e,op,self.parse_factor())
        return e
    def parse_factor(self):
        t=self.current
        if self.match("NUMBER"): self.pos+=1; return NumberLiteral(t.value)
        if self.match("STRING"): self.pos+=1; return StringLiteral(t.value)
        if self.match("TRUE","FALSE"): self.pos+=1; return BooleanLiteral(t.value)
        if self.match("IDENTIFIER"): self.pos+=1; return Identifier(t.value)
        if self.match("INPUT_NAO"):
            self.consume("INPUT_NAO"); self.consume("LPAREN"); self.consume("RPAREN"); return InputExpression()
        if self.match("LPAREN"):
            self.consume("LPAREN"); e=self.parse_expression(); self.consume("RPAREN"); return e
        raise ParserError(f"Expected expression at line {t.line}, column {t.column}; found {t.type} ({t.value!r})")

def parse_source(source): return Parser(tokenize(source)).parse()

def pretty(node, indent=0):
    p="  "*indent
    if isinstance(node,Program): return "\n".join([p+"Program"]+[pretty(x,indent+1) for x in node.statements])
    if isinstance(node,VariableDeclaration): return p+f"VariableDeclaration({node.name})\n"+pretty(node.value,indent+1)
    if isinstance(node,Assignment): return p+f"Assignment({node.name})\n"+pretty(node.value,indent+1)
    if isinstance(node,PrintStatement): return p+"PrintStatement\n"+pretty(node.expression,indent+1)
    if isinstance(node,IfStatement):
        out=[p+"IfStatement",p+"  Condition",pretty(node.condition,indent+2),p+"  ThenBlock"]+[pretty(x,indent+2) for x in node.then_block]
        if node.else_block is not None: out += [p+"  ElseBlock"]+[pretty(x,indent+2) for x in node.else_block]
        return "\n".join(out)
    if isinstance(node,WhileStatement): return "\n".join([p+"WhileStatement",p+"  Condition",pretty(node.condition,indent+2),p+"  Body"]+[pretty(x,indent+2) for x in node.body])
    if isinstance(node,BinaryExpression): return p+f"BinaryExpression({node.operator})\n"+pretty(node.left,indent+1)+"\n"+pretty(node.right,indent+1)
    if isinstance(node,Identifier): return p+f"Identifier({node.name})"
    if isinstance(node,NumberLiteral): return p+f"NumberLiteral({node.value})"
    if isinstance(node,StringLiteral): return p+f"StringLiteral({node.value!r})"
    if isinstance(node,BooleanLiteral): return p+f"BooleanLiteral({node.value})"
    if isinstance(node,InputExpression): return p+"InputExpression"
    return p+repr(node)

if __name__=="__main__":
    import sys
    with open(sys.argv[1],encoding="utf-8") as f: src=f.read()
    try:
        ast=parse_source(src); print("Parse successful!\n"); print(pretty(ast))
    except LexerError as e: print("Lexical Error:",e)
    except ParserError as e: print("Syntax Error:",e)
