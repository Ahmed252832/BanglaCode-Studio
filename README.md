# BanglaCode v1.0

## Project Title
**BanglaCode: Design of a Bengali-Friendly Mini Programming Language and Compiler**

BanglaCode is an educational mini programming language that uses simple Banglish keywords.
The compiler demonstrates the major stages of compilation and can generate C code and a
native executable through GCC.

## Main Language Keywords

| BanglaCode | Meaning |
|---|---|
| `dhori` | variable declaration |
| `jodi` | if |
| `nahole` | else |
| `jotokkhon` | while |
| `dekhao` | print/output |
| `inputNao` | input |
| `shotto` | true |
| `mittha` | false |

## Supported Features

- Variable declaration and assignment
- Number, string, and boolean values
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- `jodi` / `nahole` conditional statements
- `jotokkhon` loops
- `dekhao()` output
- Lexical, syntax, and semantic error detection
- AST construction
- Symbol table
- Three-Address Code (TAC)
- C code generation
- GCC executable generation

## Compiler Architecture

```text
BanglaCode Source (.bncode)
          |
          v
        Lexer
          |
          v
        Tokens
          |
          v
        Parser
          |
          v
          AST
          |
          v
   Semantic Analyzer
          |
          +----> Symbol Table
          |
          v
      IR / TAC
          |
          v
   C Code Generator
          |
          v
         GCC
          |
          v
      Executable
```

## Important Files

- `lexer.py` — converts source characters into tokens
- `parser.py` — checks grammar and creates the AST
- `ast_nodes.py` — defines AST node classes
- `semantic.py` — performs semantic checks and creates the symbol table
- `ir.py` — generates Three-Address Code
- `codegen.py` — generates C source code
- `compiler.py` — integrates the complete compiler pipeline
- `final_demo.bncode` — recommended final demonstration program
- `tests/` — functional and error-handling test cases
- `FINAL_TEST_REPORT.md` — final testing summary

## How to Run

Open CMD/Terminal in this project folder.

### Compile and build the final demo

```bash
python compiler.py final_demo.bncode --build
```

On Windows, a successful build creates:

```text
final_demo.c
final_demo.exe
```

Run it with:

```bash
final_demo.exe
```

Expected output:

```text
BanglaCode Demo
80
Pass
1
2
3
```

### Generate C without building

```bash
python compiler.py final_demo.bncode
```

## Example BanglaCode Program

```text
dhori marks = 75;
dhori bonus = 5;
dhori finalMarks = marks + bonus;

jodi finalMarks >= 40 {
    dekhao("Pass");
}
nahole {
    dekhao("Fail");
}
```

## Error Handling Examples

Undeclared variable:
```text
x = 10;
```

Missing semicolon:
```text
dhori x = 10
dekhao(x);
```

Type mismatch:
```text
dhori x = 10;
x = "hello";
```

## Testing

The prepared final test suite contains 10 test cases covering normal execution and
compiler errors. All 10 prepared tests passed in the final test run.

## Current Limitations

BanglaCode v1.0 intentionally keeps the language small. It does not currently include:

- User-defined functions
- Arrays
- Classes / object-oriented programming
- Full Bengali Unicode syntax or Bengali identifiers
- File handling
- Networking
- Advanced standard libraries
- Optimization passes
- Direct machine-code generation

The current compiler generates C as its target language and uses GCC to create the executable.

## Demo Flow for Defense

1. Open `final_demo.bncode`.
2. Briefly explain the Banglish keywords.
3. Run `python compiler.py final_demo.bncode --build`.
4. Show PASS results for compiler stages.
5. Show the AST and symbol table.
6. Show the generated TAC.
7. Open `final_demo.c` to show generated target code.
8. Run `final_demo.exe`.
9. Show one invalid test to demonstrate error detection.

## Version

BanglaCode v1.0 — Mini Compiler Project


## BanglaCode IDE — Graphical User Interface

BanglaCode now includes a desktop IDE-style graphical interface.

Start it on Windows by double-clicking:

```text
Start_BanglaCode_IDE.bat
```

Or from CMD:

```bash
python gui.py
```

The interface includes:

- BanglaCode source-code editor
- Line numbers
- New / Open / Save buttons
- Run button
- Build EXE button
- Compiler output panel
- Program output panel
- Syntax / semantic error display
- Dark IDE-style interface

### Recommended Demo

1. Start `Start_BanglaCode_IDE.bat`.
2. Write or paste BanglaCode code in the editor.
3. Click **Run**.
4. The IDE compiles the program, generates C, builds it with GCC, runs the executable,
   and displays the compiler output and program output in the lower panel.

This UI is an additional usability layer. The original compiler pipeline remains unchanged.


## BanglaCode Studio — Enhanced IDE

Launch on Windows by double-clicking `Start_BanglaCode_Studio.bat`, or run:

```bash
python gui.py
```

Enhanced IDE features:
- Live syntax highlighting
- Line numbers
- Quick sample programs
- New / Open / Save
- Run and Build EXE
- Console tab
- AST tab
- TAC / IR tab
- Generated C tab
- Compiler stage status
- Program output and error display


## Responsive / Scrollable Interface Update

The BanglaCode Studio window now starts at a smaller `1100x680` size and can be freely resized.
The main IDE workspace has vertical and horizontal scrolling for smaller displays.
The source editor also has its own horizontal and vertical scrolling.
