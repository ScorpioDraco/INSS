'''
Retorna a seleção de fragmentos com base nos cenários apresentados
Diaut 04/2026
'''
import os
import ctypes
import tkinter as tk
from tkinter import ttk

# ── Ícone da aplicação ───────────────────────────────────────────────────────
_ICO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fragmentos.ico")

def _aplicar_icone(janela):
    """Aplica o ícone .ico à janela informada, se o arquivo existir."""
    if os.path.exists(_ICO_PATH):
        janela.iconbitmap(_ICO_PATH)

def _configurar_taskbar():
    """
    Define um AppUserModelID único para que o Windows 11 exiba o ícone
    correto na barra de tarefas (sem agrupar com o ícone genérico do Python).
    Deve ser chamado ANTES de criar a janela Tk.
    """
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "diaut.fragmentos.app.1"
        )
    except AttributeError:
        pass  # Não está no Windows — ignora silenciosamente

# ── Paleta de cores ──────────────────────────────────────────────────────────
BG        = "#1e1e2e"
BG_CARD   = "#2a2a3e"
BG_HOVER  = "#32324a"
ACCENT    = "#4937bb"
ACCENT2   = "#c7b8f1"
TEXT      = "#e2e0f0"
TEXT_DIM  = "#8884aa"
BORDER    = "#3d3d5c"

# ── Dados do cenário ─────────────────────────────────────────────────────────
cenario_def = {
    "servico": {
        "nome": "Serviço",
        "opcoes": None,
        "tipo": "texto",
        "default": "TPU"
    },
    "canal": {
        "nome": "Canal",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Todos exceto SEC"},
            {"opcao": "2", "texto": "SEC"},
        ]
    },
    "requerente": {
        "nome": "Requerente",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Titular"},
            {"opcao": "2", "texto": "Procurador"},
            {"opcao": "3", "texto": "RL"}
        ]
    },
    "motivo": {
        "nome": "Motivo",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Óbito"}
        ]
    },
    "precedido": {
        "nome": "Precedido",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Sim"},
            {"opcao": "2", "texto": "Não"}
        ]
    },
    "relacao": {
        "nome": "Relação",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Casado"},
            {"opcao": "2", "texto": "Companheiro"},
            {"opcao": "3", "texto": "Filho menor"},
            {"opcao": "4", "texto": "Filho maior com deficiência"},
            {"opcao": "5", "texto": "Filho maior com invalidez"},
            {"opcao": "6", "texto": "Pais"},
            {"opcao": "7", "texto": "Outros"}
        ]
    },
    "situacao": {
        "nome": "Situação",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Há mais de 2 anos"},
            {"opcao": "4", "texto": "Há menos de 2 anos"},
            {"opcao": "2", "texto": "Há menos de 2 anos com UE anterior"},
            {"opcao": "3", "texto": "Há menos de 2 anos sem UE anterior"}
        ]
    },
    "sem_outros_dependentes": {
        "nome": "Outros Dependentes",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Sem outros dependentes"}
        ]
    },
    "acumula": {
        "nome": "Acumula",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Sim"},
            {"opcao": "2", "texto": "Não"},
            {"opcao": "3", "texto": "Sim/Não"}
        ]
    },
    "morte_por_acidente": {
        "nome": "Morte por acidente",
        "tipo": "radio",
        "opcoes": [
            {"opcao": "1", "texto": "Sim"},
            {"opcao": "2", "texto": "Não"}
        ]
    },
    "divergencias": {
        "nome": "Divergências",
        "tipo": "checkbox",
        "mostrar_codigo": False,          # exibe apenas o texto
        "opcoes": [
            {"opcao": "118", "texto": "118"}
        ]
    },
    "anexos": {
        "nome": "Anexos",
        "tipo": "checkbox",
        "mostrar_codigo": True,           # exibe "código - texto"
        "opcoes": [
#            {"opcao": "1",    "texto": "Documentos titular"},
#            {"opcao": "2",    "texto": "Documentos RL"},
#            {"opcao": "3",    "texto": "Tutela/Curatela/Guarda"},
#            {"opcao": "4",    "texto": "Documentos procurador"},
            {"opcao": "5",    "texto": "Documentos dependentes"},
            {"opcao": "6",    "texto": "Certidão de óbito"},
            {"opcao": "7",    "texto": "Certidão de casamento"},
#            {"opcao": "8",    "texto": "Certidão de nascimento"},
            {"opcao": "9",    "texto": "Comprovantes de união estável"},
#            {"opcao": "10",   "texto": "Declaração acumulação RPPS"},
#            {"opcao": "11",   "texto": "CTPS"},
#            {"opcao": "12",   "texto": "Comprovante serviço público"},
#            {"opcao": "13",   "texto": "Carnês"},
#            {"opcao": "15",   "texto": "Outros documentos"},
#            {"opcao": "1480", "texto": "Documentos interessado"},
#            {"opcao": "1482", "texto": "Documentos grupo familiar"}
        ]
    }
}

# ── Lógica de negócio ────────────────────────────────────────────────────────
def gerar_fragmentos(selecoes):
    requerente             = selecoes.get("requerente")
    motivo                 = selecoes.get("motivo")
    precedido              = selecoes.get("precedido")
    relacao                = selecoes.get("relacao")
    situacao               = selecoes.get("situacao")
    sem_outros_dependentes = selecoes.get("sem_outros_dependentes")
    acumula                = selecoes.get("acumula")
    morte_acidente         = selecoes.get("morte_por_acidente")
    divergencias           = selecoes.get("divergencias", [])
    anexos_cenario         = selecoes.get("anexos", [])

    fragmentos = ["INTROD_PADRAO"]

    if requerente == "1" and relacao == "3" and not sem_outros_dependentes:
        fragmentos.append("IDENT_INTER")
    if requerente == "2":
        fragmentos.append("PROCURACAO")
        fragmentos.append("IDENT_PROCUR")
        fragmentos.append("T_RESP_PROC")
    if requerente == "3":
        fragmentos.append("IDENT_RL")
        fragmentos.append("REPRES_LEGAL")
        fragmentos.append("TERMO_RESPONS")
    if relacao not in ["3", "4", "5", "6", "7"] and 5 not in anexos_cenario:
        fragmentos.append("IDENT_INTER")
    fragmentos.append("IDENT_INST_21")

    if motivo == "1":
        if 6 not in anexos_cenario:
            fragmentos.append("FG_OBITO")

    if relacao == "1":
        if 7 not in anexos_cenario:
            fragmentos.append("CERT_CASAM_21")
    if relacao == "2":
        if 9 not in anexos_cenario:
            fragmentos.append("PROVA_UE_21")
    if relacao == "3":
        if sem_outros_dependentes == "1":
            fragmentos.append("IDENT_OUTROS")
        else:
            fragmentos.append("IDENT_FILHOS")
    if relacao in ["4", "5"]:
        fragmentos.append("IDENT_FMI_FMD")
    if relacao == "6":
        fragmentos.append("IDENT_PAIS_21")
        fragmentos.append("DECL_INEX_DEP")
        fragmentos.append("DEPEND_ECON_21")
    if relacao == "7":
        fragmentos.append("IDENT_OUTROS")
        fragmentos.append("OUTROS_DEP_21")

    if situacao == "2":
        fragmentos.append("UE_ANTES_CAS_21")

    if precedido == "2":
        fragmentos.append("CTPS_INSTIT_21")
        fragmentos.append("VINCULOS")

    if 118 in divergencias:
        fragmentos.append("ACP_PQS")

    if acumula in ("1", "3"):
        fragmentos.append("DECL_RPPS2")

    if morte_acidente == "1":
        fragmentos.append("OBITO_ACIDENTE")

    fragmentos.append("CONC_PADRAO")
    return fragmentos


def montar_output(selecoes, fragmentos, opcoes_anexos):
    servico    = selecoes.get("servico", "TPU")
    anexos_sel = selecoes.get("anexos", [])

    max_len = max(len(f) for f in fragmentos) + 2
    linhas  = [f"{f:<{max_len}}\t{i+1}" for i, f in enumerate(fragmentos)]
    output  = "\n".join(linhas)

    if anexos_sel:
        output += "\n\nAnexos:\n"
        for num in anexos_sel:
            item_anexo = next((op for op in opcoes_anexos if op["opcao"] == str(num)), None)
            if item_anexo:
                output += f"  • {item_anexo['opcao']} - {item_anexo['texto']}\n"

    nome = servico + " - "
    for chave, item in cenario_def.items():
        if item["tipo"] not in ("texto", "checkbox"):
            val = selecoes.get(chave)
            if val:
                texto_op = next((op["texto"] for op in item["opcoes"] if op["opcao"] == val), "")
                nome += f"{item['nome']} {texto_op} - "
    divergencias_sel = selecoes.get("divergencias", [])
    for div in divergencias_sel:
        op_div = next((op for op in cenario_def["divergencias"]["opcoes"] if op["opcao"] == str(div)), None)
        if op_div:
            nome += f"Divergência {op_div['opcao']} - "

    anexos_str = "0" if not anexos_sel else ", ".join(map(str, anexos_sel))
    nome += f"Anexos {anexos_str}"

    output += f"\n\nNome do cenário gerado:\n{nome}"
    return output


# ── Interface gráfica ────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seleção de Fragmentos")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(680, 820)

        self._vars   = {}
        self._checks = {}
        self._drag_x = 0
        self._drag_y = 0

        self.withdraw()          # Oculta antes de construir
        self._build()
        self._center(820, 720)
        _aplicar_icone(self)
        self._bind_drag(self)
        self.deiconify()         # Exibe já na posição correta

    # ── Arrastar janela por qualquer área ────────────────────────────────────
    _NAO_ARRASTAVEIS = (tk.Button, tk.Entry, tk.Radiobutton,
                        tk.Checkbutton, tk.Text, ttk.Scrollbar, tk.Scrollbar)

    def _bind_drag(self, widget):
        if not isinstance(widget, self._NAO_ARRASTAVEIS):
            widget.bind("<ButtonPress-1>", self._drag_start, add="+")
            widget.bind("<B1-Motion>",     self._drag_move,  add="+")
        for child in widget.winfo_children():
            self._bind_drag(child)

    def _drag_start(self, event):
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _drag_move(self, event):
        self.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    # ── Layout principal ─────────────────────────────────────────────────────
    def _build(self):
        tk.Frame(self, bg=ACCENT, height=4).pack(fill="x")

        title_frame = tk.Frame(self, bg=BG, pady=18)
        title_frame.pack(fill="x", padx=28)
        tk.Label(title_frame, text="Seleção de Fragmentos",
                 font=("Segoe UI", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(title_frame, text="Configure o cenário para gerar os fragmentos",
                 font=("Segoe UI", 10), fg=TEXT_DIM, bg=BG).pack(anchor="w")

        # Canvas scrollável
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20)

        self._canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar    = ttk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._scroll_frame = tk.Frame(self._canvas, bg=BG)

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )
        self._canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self._canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # MouseWheel — vinculado apenas ao canvas (não propaga pelo drag)
        self._canvas.bind("<Enter>", lambda e: self._canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self._canvas.bind("<Leave>", lambda e: self._canvas.unbind_all("<MouseWheel>"))

        # Colunas
        col_l = tk.Frame(self._scroll_frame, bg=BG)
        col_r = tk.Frame(self._scroll_frame, bg=BG)
        col_l.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        col_r.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self._scroll_frame.columnconfigure(0, weight=1)
        self._scroll_frame.columnconfigure(1, weight=1)

        campos = list(cenario_def.items())
        meio   = (len(campos) + 1) // 2
        for i, (chave, item) in enumerate(campos):
            self._add_campo(col_l if i < meio else col_r, chave, item)

        # Botões
        btn_frame = tk.Frame(self, bg=BG, pady=16)
        btn_frame.pack(fill="x", padx=28)

        tk.Button(btn_frame, text="⚡  Gerar Fragmentos",
                  font=("Segoe UI", 12, "bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  activebackground=ACCENT2, activeforeground="white",
                  cursor="hand2", padx=24, pady=10,
                  command=self._gerar).pack(side="right")

        tk.Button(btn_frame, text="Limpar",
                  font=("Segoe UI", 10),
                  bg=BG_CARD, fg=TEXT_DIM, relief="flat",
                  activebackground=BG_HOVER, activeforeground=TEXT,
                  cursor="hand2", padx=16, pady=10,
                  command=self._limpar).pack(side="right", padx=(0, 10))

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Card de campo ─────────────────────────────────────────────────────────
    def _add_campo(self, parent, chave, item):
        card = tk.Frame(parent, bg=BG_CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=6)

        tk.Label(card, text=item["nome"].upper(),
                 font=("Segoe UI", 8, "bold"),
                 fg=ACCENT2, bg=BG_CARD, pady=8, padx=14).pack(anchor="w")

        body = tk.Frame(card, bg=BG_CARD, padx=14, pady=10)
        body.pack(fill="x")

        if item["tipo"] == "texto":
            var = tk.StringVar(value=item.get("default", ""))
            tk.Entry(body, textvariable=var, font=("Segoe UI", 10),
                     bg=BG, fg=TEXT, relief="flat", insertbackground=TEXT,
                     highlightbackground=BORDER, highlightthickness=1
                     ).pack(fill="x", ipady=6)
            self._vars[chave] = var

        elif item["tipo"] == "radio":
            var = tk.StringVar(value="none")
            var._last_val = "none"
            self._vars[chave] = var
            for op in item["opcoes"]:
                val = op["opcao"]
                tk.Radiobutton(
                    body, text=op["texto"], variable=var, value=val,
                    font=("Segoe UI", 10), fg=TEXT, bg=BG_CARD,
                    selectcolor=BG, activebackground=BG_HOVER,
                    activeforeground=TEXT, relief="flat", cursor="hand2",
                    command=lambda v=var, vl=val: self._toggle_radio(v, vl)
                ).pack(anchor="w", pady=2)

        elif item["tipo"] == "checkbox":
            mostrar_codigo = item.get("mostrar_codigo", True)
            self._checks[chave] = {}
            for idx, op in enumerate(item["opcoes"]):
                bv    = tk.BooleanVar(value=False)
                label = f"{op['opcao']} - {op['texto']}" if mostrar_codigo else op["texto"]
                self._checks[chave][op["opcao"]] = bv
                row, col = divmod(idx, 2)
                tk.Checkbutton(
                    body, text=label, variable=bv,
                    font=("Segoe UI", 10), fg=TEXT, bg=BG_CARD,
                    selectcolor=BG, activebackground=BG_HOVER,
                    activeforeground=TEXT, relief="flat", cursor="hand2"
                ).grid(row=row, column=col, sticky="w", pady=2, padx=(0, 16))

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _toggle_radio(self, var, clicked_val):
        if getattr(var, "_last_val", "none") == clicked_val:
            var.set("none")
            var._last_val = "none"
        else:
            var._last_val = clicked_val

    def _coletar_selecoes(self):
        selecoes = {}
        for chave, var in self._vars.items():
            v = var.get().strip()
            selecoes[chave] = v if (v and v != "none") else None
        for chave, opcoes_vars in self._checks.items():
            selecoes[chave] = [int(op) for op, bv in opcoes_vars.items() if bv.get()]
        return selecoes

    def _limpar(self):
        for chave, var in self._vars.items():
            if cenario_def[chave]["tipo"] == "radio":
                var.set("none")
                var._last_val = "none"
            else:
                var.set(cenario_def[chave].get("default", ""))
        for opcoes_vars in self._checks.values():
            for bv in opcoes_vars.values():
                bv.set(False)

    def _gerar(self):
        selecoes   = self._coletar_selecoes()
        fragmentos = gerar_fragmentos(selecoes)
        output     = montar_output(selecoes, fragmentos, cenario_def["anexos"]["opcoes"])
        self._abrir_resultado(output)

    def _abrir_resultado(self, texto):
        win = tk.Toplevel(self)
        win.title("Resultado Gerado")
        win.configure(bg=BG)
        win.focus_set()
        _aplicar_icone(win)

        larg, alt = 620, 740
        cx = self.winfo_x() + (self.winfo_width()  - larg) // 2
        cy = self.winfo_y() + (self.winfo_height() - alt)  // 2
        win.geometry(f"{larg}x{alt}+{cx}+{cy}")

        tk.Label(win, text="Fragmentos Selecionados",
                 font=("Segoe UI", 14, "bold"),
                 fg=ACCENT2, bg=BG, pady=15).pack()

        text_frame = tk.Frame(win, bg=BG_CARD,
                              highlightbackground=BORDER, highlightthickness=1)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        txt = tk.Text(text_frame, font=("Consolas", 11),
                      bg=BG_CARD, fg=TEXT, relief="flat",
                      padx=15, pady=15, wrap="none")
        sy  = ttk.Scrollbar(text_frame, orient="vertical",   command=txt.yview)
        sx  = ttk.Scrollbar(text_frame, orient="horizontal", command=txt.xview)
        txt.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

        sy.pack(side="right",  fill="y")
        sx.pack(side="bottom", fill="x")
        txt.pack(side="left",  fill="both", expand=True)

        txt.insert("1.0", texto)
        txt.config(state="disabled")

        tk.Button(win, text="Fechar", font=("Segoe UI", 10, "bold"),
                  bg=BG_CARD, fg=TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=8, command=win.destroy).pack(pady=(0, 15))

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2 - 40
        self.geometry(f"{w}x{h}+{x}+{y}")


if __name__ == "__main__":
    _configurar_taskbar()
    app = App()
    app.mainloop()
