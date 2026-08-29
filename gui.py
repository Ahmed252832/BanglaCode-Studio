
import re
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "BanglaCode Studio"
BASE_DIR = Path(__file__).resolve().parent
COMPILER = BASE_DIR / "compiler.py"

SAMPLES = {
    "Hello": 'dekhao("Hello BanglaCode");',
    "If Else": 'dhori marks = 75;\n\njodi marks >= 40 {\n    dekhao("Pass");\n}\nnahole {\n    dekhao("Fail");\n}',
    "Loop": 'dhori x = 1;\n\njotokkhon x <= 5 {\n    dekhao(x);\n    x = x + 1;\n}',
    "Full Demo": '// BanglaCode Studio Demo\ndhori marks = 75;\ndhori bonus = 5;\ndhori finalMarks = marks + bonus;\n\ndekhao("BanglaCode Demo");\ndekhao(finalMarks);\n\njodi finalMarks >= 40 {\n    dekhao("Pass");\n}\nnahole {\n    dekhao("Fail");\n}\n\ndhori count = 1;\njotokkhon count <= 3 {\n    dekhao(count);\n    count = count + 1;\n}'
}

KEYWORDS = ["dhori", "jodi", "nahole", "jotokkhon", "dekhao", "inputNao", "shotto", "mittha"]

class BanglaCodeStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x680")
        self.minsize(760, 520)
        self.configure(bg="#08111f")
        self.current_file = None
        self._setup_style()
        self._build_ui()
        self.editor.insert("1.0", SAMPLES["Full Demo"])
        self._highlight()
        self._refresh_lines()
        self._set_status("Ready", "●")

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Root.TFrame", background="#08111f")
        style.configure("Top.TFrame", background="#0b1526")
        style.configure("Side.TFrame", background="#0f1b2e")
        style.configure("Card.TFrame", background="#111f33")
        style.configure("TButton", font=("Segoe UI", 10), padding=(11, 7))
        style.configure("Run.TButton", font=("Segoe UI Semibold", 10), padding=(14, 8))
        style.configure("Title.TLabel", background="#0b1526", foreground="#f8fafc",
                        font=("Segoe UI Semibold", 17))
        style.configure("Sub.TLabel", background="#0b1526", foreground="#7dd3fc",
                        font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#0b1526", foreground="#cbd5e1",
                        font=("Segoe UI", 9))

    def _build_ui(self):
        top = ttk.Frame(self, style="Top.TFrame")
        top.pack(fill="x")
        brand = ttk.Frame(top, style="Top.TFrame")
        brand.pack(side="left", padx=16, pady=10)
        ttk.Label(brand, text="BanglaCode Studio", style="Title.TLabel").pack(anchor="w")
        ttk.Label(brand, text="Bengali-friendly mini compiler IDE", style="Sub.TLabel").pack(anchor="w")

        actions = ttk.Frame(top, style="Top.TFrame")
        actions.pack(side="right", padx=12, pady=12)
        ttk.Button(actions, text="New", command=self.new_file).pack(side="left", padx=3)
        ttk.Button(actions, text="Open", command=self.open_file).pack(side="left", padx=3)
        ttk.Button(actions, text="Save", command=self.save_file).pack(side="left", padx=3)
        ttk.Button(actions, text="▶ Run", style="Run.TButton", command=self.run_code).pack(side="left", padx=3)
        ttk.Button(actions, text="Build EXE", command=self.build_exe).pack(side="left", padx=3)

        # Scrollable application workspace
        workspace = ttk.Frame(self, style="Root.TFrame")
        workspace.pack(fill="both", expand=True)

        self.workspace_canvas = tk.Canvas(
            workspace,
            bg="#08111f",
            highlightthickness=0,
            bd=0
        )
        self.workspace_canvas.pack(side="left", fill="both", expand=True)

        global_vscroll = ttk.Scrollbar(
            workspace,
            orient="vertical",
            command=self.workspace_canvas.yview
        )
        global_vscroll.pack(side="right", fill="y")

        global_hscroll = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.workspace_canvas.xview
        )
        global_hscroll.pack(fill="x")

        self.workspace_canvas.configure(
            yscrollcommand=global_vscroll.set,
            xscrollcommand=global_hscroll.set
        )

        main = ttk.Frame(self.workspace_canvas, style="Root.TFrame")
        self.workspace_window = self.workspace_canvas.create_window(
            (0, 0),
            window=main,
            anchor="nw"
        )

        # Keep scroll region updated as widgets change size.
        main.bind(
            "<Configure>",
            lambda event: self.workspace_canvas.configure(
                scrollregion=self.workspace_canvas.bbox("all")
            )
        )

        # Expand the inner frame to the visible width when there is enough space.
        self.workspace_canvas.bind("<Configure>", self._resize_workspace)

        # Mouse wheel scrolls the whole interface when pointer is outside editor.
        self.bind_all("<Shift-MouseWheel>", self._global_horizontal_scroll)

        side = ttk.Frame(main, style="Side.TFrame", width=190)
        side.pack(side="left", fill="y", padx=(10, 6), pady=10)
        side.pack_propagate(False)

        tk.Label(side, text="QUICK SAMPLES", bg="#0f1b2e", fg="#93c5fd",
                 font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=12, pady=(14, 8))
        for name in SAMPLES:
            tk.Button(side, text=name, command=lambda n=name: self.load_sample(n),
                      bg="#17243a", fg="#e5e7eb", activebackground="#243b5a",
                      activeforeground="#ffffff", relief="flat", bd=0,
                      font=("Segoe UI", 9), padx=10, pady=7, anchor="w").pack(
                          fill="x", padx=10, pady=3)

        tk.Label(side, text="LANGUAGE", bg="#0f1b2e", fg="#93c5fd",
                 font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=12, pady=(18, 6))
        help_text = "dhori      variable\njodi       if\nnahole     else\njotokkhon  while\ndekhao     print\nshotto     true\nmittha     false"
        tk.Label(side, text=help_text, justify="left", bg="#0f1b2e", fg="#94a3b8",
                 font=("Consolas", 9)).pack(anchor="w", padx=12)

        content = ttk.Frame(main, style="Root.TFrame")
        content.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        upper = ttk.Frame(content, style="Card.TFrame")
        upper.pack(fill="both", expand=True)

        editor_header = tk.Frame(upper, bg="#111f33")
        editor_header.pack(fill="x")
        tk.Label(editor_header, text="SOURCE EDITOR", bg="#111f33", fg="#7dd3fc",
                 font=("Segoe UI Semibold", 10)).pack(side="left", padx=12, pady=8)
        self.file_label = tk.Label(editor_header, text="untitled.bncode", bg="#111f33",
                                   fg="#64748b", font=("Segoe UI", 9))
        self.file_label.pack(side="right", padx=12)

        editwrap = tk.Frame(upper, bg="#0a1220")
        editwrap.pack(fill="both", expand=True, padx=10, pady=(0,10))

        self.lines = tk.Text(editwrap, width=4, bg="#07101c", fg="#475569", bd=0,
                             padx=4, pady=10, state="disabled", takefocus=0,
                             font=("Consolas", 11))
        self.lines.pack(side="left", fill="y")

        self.editor = tk.Text(editwrap, bg="#0a1220", fg="#e2e8f0", insertbackground="#ffffff",
                              selectbackground="#244664", bd=0, undo=True, wrap="none",
                              padx=12, pady=10, font=("Consolas", 11))
        self.editor.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(editwrap, orient="vertical", command=self._scroll)
        sb.pack(side="right", fill="y")

        editor_hscroll = ttk.Scrollbar(
            upper,
            orient="horizontal",
            command=self.editor.xview
        )
        editor_hscroll.pack(fill="x", padx=10, pady=(0, 8))

        self.editor.configure(
            yscrollcommand=lambda *a: self._sync_scroll(sb,*a),
            xscrollcommand=editor_hscroll.set
        )

        self.editor.tag_config("keyword", foreground="#7dd3fc", font=("Consolas", 11, "bold"))
        self.editor.tag_config("string", foreground="#86efac")
        self.editor.tag_config("number", foreground="#fbbf24")
        self.editor.tag_config("comment", foreground="#64748b", font=("Consolas", 11, "italic"))
        self.editor.tag_config("operator", foreground="#f9a8d4")
        self.editor.tag_config("paren", foreground="#c4b5fd")

        self.editor.bind("<KeyRelease>", self._on_edit)
        self.editor.bind("<ButtonRelease-1>", self._refresh_lines)
        self.editor.bind("<MouseWheel>", self._refresh_lines)

        lower = ttk.Frame(content, style="Card.TFrame", height=240)
        lower.pack(fill="both", expand=False, pady=(8,0))
        lower.pack_propagate(False)

        self.tabs = ttk.Notebook(lower)
        self.tabs.pack(fill="both", expand=True, padx=8, pady=8)
        self.output = self._make_text_tab("Console", "#d1fae5")
        self.ast_view = self._make_text_tab("AST", "#dbeafe")
        self.tac_view = self._make_text_tab("TAC / IR", "#fde68a")
        self.c_view = self._make_text_tab("Generated C", "#e9d5ff")

        statusbar = ttk.Frame(self, style="Top.TFrame")
        statusbar.pack(fill="x")
        self.status = ttk.Label(statusbar, style="Status.TLabel")
        self.status.pack(side="left", padx=12, pady=5)
        ttk.Label(statusbar, text="BanglaCode v1.0 • Python + GCC", style="Status.TLabel").pack(
            side="right", padx=12)

    def _resize_workspace(self, event):
        """Make the workspace responsive while preserving horizontal scrolling."""
        required = 940
        width = max(event.width, required)
        self.workspace_canvas.itemconfigure(self.workspace_window, width=width)

    def _global_horizontal_scroll(self, event):
        direction = -1 if event.delta > 0 else 1
        self.workspace_canvas.xview_scroll(direction, "units")

    def _make_text_tab(self, name, fg):
        frame = tk.Frame(self.tabs, bg="#050b14")
        self.tabs.add(frame, text=name)
        box = tk.Text(frame, bg="#050b14", fg=fg, insertbackground="#fff", bd=0,
                      padx=12, pady=10, wrap="word", font=("Consolas", 10), state="disabled")
        box.pack(fill="both", expand=True)
        return box

    def _set_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0","end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def _set_status(self, text, dot="●"):
        self.status.config(text=f"{dot}  {text}")

    def _scroll(self,*a):
        self.editor.yview(*a)
        self.lines.yview(*a)

    def _sync_scroll(self, sb, *a):
        sb.set(*a)
        self.lines.yview_moveto(a[0])

    def _on_edit(self,event=None):
        self._refresh_lines()
        self._highlight()

    def _refresh_lines(self,event=None):
        count = int(self.editor.index("end-1c").split(".")[0])
        data = "\n".join(str(i) for i in range(1,count+1))
        self.lines.config(state="normal")
        self.lines.delete("1.0","end")
        self.lines.insert("1.0",data)
        self.lines.config(state="disabled")

    def _highlight(self):
        text = self.editor.get("1.0","end-1c")
        for tag in ["keyword","string","number","comment","operator","paren"]:
            self.editor.tag_remove(tag,"1.0","end")

        def apply(pattern, tag, flags=0):
            for m in re.finditer(pattern, text, flags):
                self.editor.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

        apply(r'//.*$', "comment", re.M)
        apply(r'"(?:\\.|[^"\\])*"', "string")
        apply(r'\b\d+\b', "number")
        apply(r'\b(?:' + "|".join(map(re.escape,KEYWORDS)) + r')\b', "keyword")
        apply(r'==|!=|>=|<=|[+\-*/%=<>]', "operator")
        apply(r'[(){}]', "paren")

    def new_file(self):
        self.current_file=None
        self.editor.delete("1.0","end")
        self.file_label.config(text="untitled.bncode")
        self._set_text(self.output,"")
        self._set_status("New file")

    def open_file(self):
        p=filedialog.askopenfilename(filetypes=[("BanglaCode","*.bncode"),("All files","*.*")])
        if not p: return
        try:
            self.current_file=Path(p)
            self.editor.delete("1.0","end")
            self.editor.insert("1.0",self.current_file.read_text(encoding="utf-8"))
            self.file_label.config(text=self.current_file.name)
            self._highlight(); self._refresh_lines()
            self._set_status(f"Opened {self.current_file.name}")
        except Exception as e:
            messagebox.showerror("Open Error",str(e))

    def save_file(self):
        if self.current_file is None:
            p=filedialog.asksaveasfilename(defaultextension=".bncode",
                filetypes=[("BanglaCode","*.bncode"),("All files","*.*")])
            if not p: return False
            self.current_file=Path(p)
        self.current_file.write_text(self.editor.get("1.0","end-1c"),encoding="utf-8")
        self.file_label.config(text=self.current_file.name)
        self._set_status(f"Saved {self.current_file.name}")
        return True

    def load_sample(self,name):
        self.editor.delete("1.0","end")
        self.editor.insert("1.0",SAMPLES[name])
        self.current_file=None
        self.file_label.config(text=f"{name.lower().replace(' ','_')}.bncode")
        self._highlight(); self._refresh_lines()
        self._set_status(f"Loaded sample: {name}")

    def _temp_source(self):
        p=BASE_DIR/"_studio_temp.bncode"
        p.write_text(self.editor.get("1.0","end-1c"),encoding="utf-8")
        return p

    def _compile(self, build=True):
        source=self._temp_source()
        cmd=[sys.executable,str(COMPILER),str(source)]
        if build: cmd.append("--build")
        return subprocess.run(cmd,cwd=BASE_DIR,capture_output=True,text=True),source

    def _split_sections(self, text):
        ast=tac=""
        if "AST:\n" in text:
            rest=text.split("AST:\n",1)[1]
            if "\nSymbol Table:" in rest:
                ast=rest.split("\nSymbol Table:",1)[0].strip()
        if "Three-Address Code (TAC):" in text:
            tac=text.split("Three-Address Code (TAC):",1)[1]
            if "\nGCC build:" in tac:
                tac=tac.split("\nGCC build:",1)[0]
            tac=tac.strip()
        return ast,tac

    def run_code(self):
        self._set_status("Compiling...", "◉")
        self._set_text(self.output,"Compiling BanglaCode source...\n\n")
        self._set_text(self.ast_view,"")
        self._set_text(self.tac_view,"")
        self._set_text(self.c_view,"")
        try:
            result,source=self._compile(True)
        except Exception as e:
            self._set_text(self.output,f"IDE Error: {e}")
            self._set_status("Failed","✖")
            return

        text=(result.stdout or "") + (("\n"+result.stderr) if result.stderr else "")
        ast,tac=self._split_sections(result.stdout or "")
        self._set_text(self.ast_view,ast or "No AST generated.")
        self._set_text(self.tac_view,tac or "No TAC generated.")

        cfile=source.with_suffix(".c")
        if cfile.exists():
            self._set_text(self.c_view,cfile.read_text(encoding="utf-8",errors="replace"))

        if result.returncode!=0:
            self._set_text(self.output,text)
            self.tabs.select(0)
            self._set_status("Compilation error","✖")
            return

        exe=source.with_suffix(".exe" if sys.platform.startswith("win") else "")
        console = "COMPILER STATUS\n------------------------------\n"
        for line in (result.stdout or "").splitlines():
            if "PASS" in line or "Generated C file:" in line or "GCC build:" in line or "Executable:" in line:
                console += line + "\n"

        console += "\nPROGRAM OUTPUT\n------------------------------\n"
        try:
            rr=subprocess.run([str(exe)],cwd=BASE_DIR,capture_output=True,text=True,timeout=10)
            console += rr.stdout or "(no output)\n"
            if rr.stderr:
                console += "\n" + rr.stderr
            console += "\n✓ Program finished successfully."
            self._set_status("Run completed","✓")
        except subprocess.TimeoutExpired:
            console += "\n✖ Timed out. Possible infinite loop."
            self._set_status("Timed out","✖")
        except Exception as e:
            console += f"\n✖ Run error: {e}"
            self._set_status("Run failed","✖")

        self._set_text(self.output,console)
        self.tabs.select(0)

    def build_exe(self):
        self._set_status("Building executable...","◉")
        try:
            result,source=self._compile(True)
            self._set_text(self.output,result.stdout + ("\n"+result.stderr if result.stderr else ""))
            if result.returncode==0:
                self._set_status("Executable built","✓")
            else:
                self._set_status("Build failed","✖")
        except Exception as e:
            self._set_text(self.output,str(e))
            self._set_status("Build failed","✖")

if __name__=="__main__":
    BanglaCodeStudio().mainloop()
