#!/usr/bin/env python3
"""Audita o escopo e o planejamento de um repositório: procura lixo e delírio.

Só biblioteca padrão. Heurístico de propósito: cada achado é uma pergunta
("isto atende a qual requisito?"), não uma condenação. ERRO = quase sempre bug
(referência quebrada, caminho local, regra de plataforma); AVISO = justificar
ou cortar; INFO = conferir.

Uso:
    python auditar_escopo.py <pasta-do-repo> [--gh dono/repo] [--plano docs/plano]

Sai com código 1 se houver ERRO.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

IGNORAR_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
                ".pytest_cache", ".ruff_cache", ".ipynb_checkpoints", "data"}
EXT_CODIGO = {".py", ".js", ".jsx", ".ts", ".tsx", ".prw", ".tlpp", ".prx", ".go", ".rs",
              ".java", ".cs", ".rb", ".php", ".sql", ".css", ".scss", ".vue", ".svelte",
              ".kt", ".swift", ".dart", ".c", ".cpp", ".h", ".sh", ".ps1"}
DIRS_PLANO_PADRAO = ("docs/plano", "docs/specs", "docs/plans", "plano", "specs")

# Arquivos que costumam entrar "porque todo repo tem". Cada um precisa de um R/D.
SUSPEITOS = {
    "LICENSE": "licença: só se o código for distribuído para reuso por terceiros",
    "CONTRIBUTING.md": "guia de contribuição: só com contribuidores externos",
    "CODE_OF_CONDUCT.md": "código de conduta: só em comunidade aberta",
    "SECURITY.md": "política de segurança: só em software publicado/mantido",
    "CHANGELOG.md": "changelog: só com releases versionadas para usuários",
    ".env.example": "variáveis de ambiente: confirmar que o código lê cada uma",
    "docker-compose.yml": "compose: confirmar que algum requisito exige ambiente reproduzível",
    "Dockerfile": "imagem: confirmar requisito de deploy/ambiente",
    "SUPPORT.md": "suporte: só em produto com usuários externos",
    "FUNDING.yml": "patrocínio: quase nunca em projeto de trabalho/cliente",
}

RE_DATA = re.compile(r"\b(\d{1,2}/\d{1,2}/20\d\d|20\d\d-\d\d-\d\d)\b")
RE_CRONO = re.compile(r"\b(cronograma|D0|sprint \d|semana \d|deadline|data limite)\b",
                      re.IGNORECASE)
RE_AMBIENTE = re.compile(r"\b(homologa[çc][ãa]o|staging|ambiente de produ[çc][ãa]o|"
                         r"ambiente de desenvolvimento)\b", re.IGNORECASE)
# "TBD" fica de fora: muitos times usam para Trunk-Based Development, não "a definir".
# Marca de lacuna da spec (SDD): decisão em aberto até virar D. Só a marca ignora caixa:
# "todo" minúsculo é português ("todo requisito"), não placeholder.
RE_PLACEHOLDER = re.compile(r"\b(TODO|FIXME|A DEFINIR|a definir)\b|\[PREENCHER\]|<a definir>|"
                            r"(?i:\[(?:PRECISA ESCLARECER|NEEDS CLARIFICATION)\b[^\]]*\])")
RE_CAMINHO_LOCAL = re.compile(r"([A-Za-z]:\\Users\\[^\s`'\"]+|/home/[a-z0-9_-]+/|/Users/[A-Za-z0-9_-]+/)")
RE_USO_IA = re.compile(r"^#{1,6}\s*uso de (ia|intelig[êe]ncia artificial)\b", re.IGNORECASE | re.M)
RE_SECAO_REF = re.compile(r"§\s?(\d+(?:\.\d+)*)")
RE_TITULO_NUM = re.compile(r"^#{1,6}\s+(\d+(?:\.\d+)*)[.)]?\s", re.M)
RE_FENCE = re.compile(r"^(```|~~~)", re.M)
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_FORA_ESCOPO = re.compile(r"fora d[oe] (escopo|mvp)|n[ãa]o[- ]escopo|out of scope|non-goals",
                            re.IGNORECASE)
# Decisão registrada que aceita plano maior que o código (plano "mastigado" com código de referência).
RE_D_PROPORCAO = re.compile(r"^\|?\s*\**(D\d+)\b.*plano (?:é |fica |sai )?maior que o código",
                            re.IGNORECASE | re.M)


class Achados:
    def __init__(self) -> None:
        self.itens: list[tuple[str, str, str]] = []

    def add(self, nivel: str, onde: str, msg: str) -> None:
        self.itens.append((nivel, onde, msg))

    def tem_erro(self) -> bool:
        return any(n == "ERRO" for n, _, _ in self.itens)


def arquivos(raiz: Path):
    for p in sorted(raiz.rglob("*")):
        if p.is_file() and not any(part in IGNORAR_DIRS for part in p.relative_to(raiz).parts[:-1]):
            yield p


def ler(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def rel(raiz: Path, p: Path) -> str:
    return p.relative_to(raiz).as_posix()


def sem_codigo(texto: str) -> str:
    """Texto do markdown sem os blocos cercados: datas e TODO de exemplo não contam."""
    dentro, saida = False, []
    for linha in texto.splitlines():
        if RE_FENCE.match(linha.strip()):
            dentro = not dentro
            continue
        if not dentro:
            saida.append(re.sub(r"`[^`]*`", "", linha))
    return "\n".join(saida)


def sem_fora_do_escopo(texto: str) -> str:
    """Remove as seções "Fora do escopo": ali o plano *nomeia* o que exclui (cronograma, ambientes)."""
    saida, corte = [], None
    for linha in texto.splitlines():
        m = RE_TITULO.match(linha)
        if m:
            nivel = len(m.group(1))
            if corte is not None and nivel <= corte:
                corte = None
            if corte is None and RE_FORA_ESCOPO.search(m.group(2)):
                corte = nivel
                continue
        if corte is None:
            saida.append(linha)
    return "\n".join(saida)


def no_plano(caminho: str, alvo: str) -> bool:
    """`alvo` é pasta ou arquivo do plano, relativo à raiz; "." vale o repo inteiro."""
    alvo = alvo.replace("\\", "/").strip("/")
    alvo = alvo[2:] if alvo.startswith("./") else alvo
    return alvo in ("", ".") or caminho == alvo or caminho.startswith(alvo + "/")


def linhas_de_codigo_em_md(texto: str) -> int:
    dentro, n = False, 0
    for linha in texto.splitlines():
        if RE_FENCE.match(linha.strip()):
            dentro = not dentro
            continue
        n += dentro
    return n


def auditar(raiz: Path, dirs_plano: list[str], gh_repo: str | None) -> Achados:
    a = Achados()
    todos = list(arquivos(raiz))
    mds = [p for p in todos if p.suffix.lower() == ".md"]
    planos = [p for p in mds if any(no_plano(rel(raiz, p), d) for d in dirs_plano)]

    # 1. Arquivos suspeitos na raiz e em .github/
    for p in todos:
        nome = p.name
        if nome in SUSPEITOS and p.parent in (raiz, raiz / ".github"):
            a.add("AVISO", rel(raiz, p), f"justificar com R/D ou cortar ({SUSPEITOS[nome]})")
    reqs = [p for p in todos if p.parent == raiz and re.fullmatch(r"requirements.*\.txt", p.name)]
    if len(reqs) > 1:
        a.add("AVISO", ", ".join(rel(raiz, p) for p in reqs),
              "mais de um requirements: existe mesmo ambiente de produção separado?")
    gitkeeps = [p for p in todos if p.name == ".gitkeep"]
    if len(gitkeeps) > 3:
        a.add("INFO", f"{len(gitkeeps)} .gitkeep",
              "pastas vazias versionadas: crie a pasta quando a tarefa que a usa chegar")

    # 2. Conteúdo dos markdown
    for p in mds:
        t, r = sem_codigo(ler(p)), rel(raiz, p)
        em_plano = p in planos
        if em_plano:
            t = sem_codigo(sem_fora_do_escopo(ler(p)))
        if em_plano:
            datas = RE_DATA.findall(t)
            if datas:
                a.add("AVISO", r, f"{len(datas)} data(s) no plano ({', '.join(sorted(set(datas))[:3])}): "
                                  "planeje por dependência; data só se a fonte fixar prazo")
            if RE_CRONO.search(t):
                a.add("AVISO", r, "cronograma/sprint/D0 no plano: troque por grafo de dependências")
            if RE_AMBIENTE.search(t):
                a.add("AVISO", r, "fala de ambientes (prod/homolog/staging): algum requisito exige?")
            ph = RE_PLACEHOLDER.findall(t)
            if ph:
                a.add("AVISO", r, f"{len(ph)} placeholder(s) TODO/a definir/[PREENCHER]: decisão em aberto")
        for m in RE_CAMINHO_LOCAL.finditer(t):
            a.add("ERRO", r, f"caminho de máquina local no repo: {m.group(1)[:60]}")
            break
        if RE_USO_IA.search(t):
            a.add("AVISO", r, "seção 'Uso de IA': algum requisito pede? (não é conteúdo do projeto)")

    # 3. Referências § quebradas (só dentro do mesmo arquivo ou do conjunto do plano)
    titulos_plano = set()
    for p in planos:
        titulos_plano |= set(RE_TITULO_NUM.findall(ler(p)))
    for p in mds:
        t = sem_codigo(ler(p))
        proprios = set(RE_TITULO_NUM.findall(t))
        if not proprios and p not in planos:
            continue  # sem seções numeradas próprias: o § aponta para outro doc, não dá para checar
        validos = proprios | titulos_plano
        quebradas = sorted({s for s in RE_SECAO_REF.findall(t) if s not in validos
                            and s.split(".")[0] not in validos})
        if quebradas:
            a.add("ERRO", rel(raiz, p), f"§ sem título correspondente: {', '.join(quebradas[:8])}")

    # 4. Proporção plano × código
    loc = 0
    for p in todos:
        if p.suffix.lower() in EXT_CODIGO and not any(no_plano(rel(raiz, p), d) for d in dirs_plano
                                                      if d.strip("./")):
            loc += sum(1 for linha in ler(p).splitlines() if linha.strip())
    lp = sum(len(ler(p).splitlines()) for p in planos)
    lc = sum(linhas_de_codigo_em_md(ler(p)) for p in planos)
    if planos:
        msg = f"plano {lp} linhas ({lc} em blocos de código) × código do repo {loc} linhas"
        just = next((m.group(1) for p in planos for m in RE_D_PROPORCAO.finditer(ler(p))), None)
        if just and (lp > loc or (lp and lc / lp > 0.5)):
            a.add("INFO", "proporção", msg + f": plano maior que o código, justificado por {just}")
        elif loc and lp > loc:
            a.add("AVISO", "proporção", msg + ": plano maior que o código = escreveu o código no plano")
        elif lp and lc / lp > 0.5:
            a.add("AVISO", "proporção", msg + ": mais da metade do plano é código; troque corpos por "
                                              "assinaturas, valores e asserções")
        else:
            a.add("INFO", "proporção", msg)

    # 5. Fonte única: parágrafos longos repetidos entre arquivos
    vistos: dict[str, set[str]] = defaultdict(set)
    for p in mds:
        for linha in ler(p).splitlines():
            s = linha.strip()
            if len(s) >= 120 and not s.startswith(("|", "```", "http")):
                vistos[hashlib.sha1(s.encode()).hexdigest()].add(rel(raiz, p))
    pares: dict[tuple[str, ...], int] = defaultdict(int)
    for fs in vistos.values():
        if len(fs) > 1:
            pares[tuple(sorted(fs))] += 1
    for fs, n in sorted(pares.items(), key=lambda x: -x[1])[:5]:
        if n >= 3:
            a.add("AVISO", " ↔ ".join(fs), f"{n} linhas longas idênticas: escolha uma fonte única e aponte")

    # 6. GitHub (opcional)
    if gh_repo:
        auditar_github(gh_repo, raiz, a)
    return a


def gh(*args: str):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return json.loads(r.stdout) if r.stdout.strip() else None


def auditar_github(repo: str, raiz: Path, a: Achados) -> None:
    try:
        labels = gh("label", "list", "-R", repo, "--limit", "200", "--json", "name")
        issues = gh("issue", "list", "-R", repo, "--state", "all", "--limit", "500",
                    "--json", "number,title,body,labels")
        prs = gh("pr", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "labels")
    except (RuntimeError, FileNotFoundError) as e:
        a.add("INFO", "github", f"não consultado: {e}")
        return
    usados = {lb["name"] for i in issues + prs for lb in i["labels"]}
    texto_repo = "\n".join(ler(p) for p in (raiz / ".github").rglob("*") if p.is_file()) \
        if (raiz / ".github").exists() else ""
    for lb in labels:
        if lb["name"] not in usados and lb["name"] not in texto_repo:
            a.add("AVISO", f"label '{lb['name']}'", "nenhuma issue nem template usa: apague")
    for i in issues:
        corpo = i.get("body") or ""
        onde = f"issue #{i['number']}"
        if not re.search(r"- \[[ xX]\]", corpo):
            a.add("AVISO", onde, "sem critério de aceite verificável (checkbox)")
        if not re.search(r"\b(R\d+|D\d+|requisito|atende|rubrica|enunciado)", corpo, re.IGNORECASE):
            a.add("INFO", onde, "não aponta o requisito/decisão que atende (rastreabilidade)")
        n = len(corpo.splitlines())
        if n > 120:
            a.add("AVISO", onde, f"corpo com {n} linhas: issue diz o quê e o aceite; o como vai no plano")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo", type=Path)
    ap.add_argument("--gh", metavar="DONO/REPO", help="também audita labels e issues no GitHub")
    ap.add_argument("--plano", action="append", metavar="DIR",
                    help=f"pasta ou arquivo de planejamento, relativo ao repo; '.' = todos os .md "
                         f"(padrão: {', '.join(DIRS_PLANO_PADRAO)})")
    args = ap.parse_args()
    raiz = args.repo.resolve()
    if not raiz.is_dir():
        print(f"pasta não encontrada: {raiz}", file=sys.stderr)
        return 2
    a = auditar(raiz, args.plano or list(DIRS_PLANO_PADRAO), args.gh)
    ordem = {"ERRO": 0, "AVISO": 1, "INFO": 2}
    print(f"# Auditoria de escopo: {raiz.name}\n")
    if not a.itens:
        print("Nenhum achado.")
    else:
        print("| Nível | Onde | Achado |\n|---|---|---|")
        for nivel, onde, msg in sorted(a.itens, key=lambda x: (ordem[x[0]], x[1])):
            print(f"| {nivel} | `{onde}` | {msg} |")
    cont = {n: sum(1 for x in a.itens if x[0] == n) for n in ordem}
    print(f"\n{cont['ERRO']} erro(s), {cont['AVISO']} aviso(s), {cont['INFO']} info.")
    return 1 if a.tem_erro() else 0


if __name__ == "__main__":
    sys.exit(main())
