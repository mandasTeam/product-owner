"""conta-horas: soma as horas trabalhadas por projeto a partir de um log em texto.

Formato do log (uma linha por apontamento):
    2026-10-01 | protheus-fat | 2.5 | ajuste do ponto de entrada
"""

import argparse
import sys
from collections import defaultdict


def ler_log(caminho):
    apontamentos = []
    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = [p.strip() for p in linha.split("|")]
            if len(partes) != 4:
                print(f"linha {n} ignorada: esperado 4 campos", file=sys.stderr)
                continue
            data, projeto, horas, descricao = partes
            apontamentos.append({"data": data, "projeto": projeto,
                                 "horas": float(horas), "descricao": descricao})
    return apontamentos


def somar_por_projeto(apontamentos, mes=None):
    total = defaultdict(float)
    for a in apontamentos:
        if mes and not a["data"].startswith(mes):
            continue
        total[a["projeto"]] += a["horas"]
    return dict(sorted(total.items()))


def imprimir(total):
    largura = max((len(p) for p in total), default=7)
    for projeto, horas in total.items():
        print(f"{projeto:<{largura}}  {horas:6.1f} h")
    print(f"{'TOTAL':<{largura}}  {sum(total.values()):6.1f} h")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Soma horas por projeto.")
    ap.add_argument("log")
    ap.add_argument("--mes", help="filtra por mês, formato AAAA-MM")
    args = ap.parse_args(argv)
    imprimir(somar_por_projeto(ler_log(args.log), args.mes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
