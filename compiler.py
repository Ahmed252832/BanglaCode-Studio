import sys
import subprocess
from pathlib import Path

from lexer import LexerError
from parser import parse_source, ParserError, pretty
from semantic import analyze_ast, SemanticError
from ir import generate_ir, format_ir
from codegen import generate_c


def compile_file(filename, show_ast=True, show_ir=True, build_exe=False):
    path = Path(filename)

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    ast = parse_source(source)
    symbols = analyze_ast(ast)
    ir = generate_ir(ast)
    c_source = generate_c(ast, symbols)

    c_path = path.with_suffix(".c")
    c_path.write_text(c_source, encoding="utf-8")

    print("Lexical analysis:  PASS")
    print("Syntax analysis:   PASS")
    print("Semantic analysis: PASS")
    print("IR generation:     PASS")
    print("C code generation: PASS")
    print(f"Generated C file:  {c_path.name}")

    if show_ast:
        print("\nAST:\n")
        print(pretty(ast))

    print("\nSymbol Table:")
    if symbols:
        for name, typ in symbols.items():
            print(f"  {name:<15} : {typ}")
    else:
        print("  (empty)")

    if show_ir:
        print("\nThree-Address Code (TAC):\n")
        print(format_ir(ir))

    exe_path = None
    if build_exe:
        exe_name = path.stem + (".exe" if sys.platform.startswith("win") else "")
        exe_path = path.with_name(exe_name)
        try:
            subprocess.run(
                ["gcc", str(c_path), "-o", str(exe_path)],
                check=True
            )
            print(f"\nGCC build: PASS")
            print(f"Executable: {exe_path.name}")
        except FileNotFoundError:
            print("\nGCC build: SKIPPED (gcc not found on this computer)")
            print(f"Run manually: gcc {c_path.name} -o {exe_name}")
        except subprocess.CalledProcessError:
            print("\nGCC build: FAILED")
            raise

    return ast, symbols, ir, c_path, exe_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <file.bncode> [--build]")
        raise SystemExit(1)

    build = "--build" in sys.argv[2:]

    try:
        compile_file(sys.argv[1], build_exe=build)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        raise SystemExit(1)
    except LexerError as e:
        print(f"Lexical Error: {e}")
        raise SystemExit(1)
    except ParserError as e:
        print(f"Syntax Error: {e}")
        raise SystemExit(1)
    except SemanticError as e:
        print(f"Semantic Error:\n{e}")
        raise SystemExit(1)
