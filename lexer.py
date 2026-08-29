import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.column})"

RESERVED = {
    "dhori": "DHORI", "jodi": "JODI", "nahole": "NAHOLE",
    "jotokkhon": "JOTOKKHON", "dekhao": "DEKHAO",
    "inputNao": "INPUT_NAO", "shotto": "TRUE", "mittha": "FALSE",
}

TOKEN_SPEC = [
    ("COMMENT", r"//[^\n]*"), ("STRING", r'"([^"\\]|\\.)*"'),
    ("NUMBER", r"\d+"),
    ("GE", r">="), ("LE", r"<="), ("EQ", r"=="), ("NE", r"!="),
    ("GT", r">"), ("LT", r"<"), ("ASSIGN", r"="),
    ("PLUS", r"\+"), ("MINUS", r"-"), ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"), ("MOD", r"%"),
    ("LPAREN", r"\("), ("RPAREN", r"\)"),
    ("LBRACE", r"\{"), ("RBRACE", r"\}"), ("SEMICOLON", r";"),
    ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("NEWLINE", r"\n"), ("SKIP", r"[ \t\r]+"), ("MISMATCH", r"."),
]
MASTER_RE = re.compile("|".join(f"(?P<{n}>{p})" for n,p in TOKEN_SPEC))

class LexerError(Exception): pass

def tokenize(source: str):
    tokens=[]; line=1; line_start=0
    for m in MASTER_RE.finditer(source):
        kind=m.lastgroup; value=m.group(); column=m.start()-line_start+1
        if kind=="NEWLINE": line+=1; line_start=m.end(); continue
        if kind in ("SKIP","COMMENT"): continue
        if kind=="MISMATCH":
            raise LexerError(f"Illegal character {value!r} at line {line}, column {column}")
        if kind=="IDENTIFIER": kind=RESERVED.get(value,"IDENTIFIER")
        if kind=="NUMBER": value=int(value)
        elif kind=="STRING": value=value[1:-1]
        elif kind=="TRUE": value=True
        elif kind=="FALSE": value=False
        tokens.append(Token(kind,value,line,column))
    tokens.append(Token("EOF",None,line,1))
    return tokens

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], encoding="utf-8") as f: src=f.read()
    try:
        for t in tokenize(src): print(t)
    except LexerError as e: print("Lexical Error:", e)
