"""Testes do auditor com repositórios sintéticos (stdlib: python -m unittest)."""

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "product-owner" / "scripts" / "auditar_escopo.py"


def rodar(arquivos: dict[str, str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as d:
        for nome, conteudo in arquivos.items():
            p = Path(d, nome)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(textwrap.dedent(conteudo), encoding="utf-8")
        r = subprocess.run([sys.executable, str(SCRIPT), d], capture_output=True, text=True,
                           encoding="utf-8")
        return r.returncode, r.stdout


class TestAuditor(unittest.TestCase):
    def test_repo_enxuto_nao_tem_achado(self):
        codigo, saida = rodar({
            "src/app.py": "\n".join(f"x{i} = {i}" for i in range(40)),
            "docs/plano/00-visao-geral.md": "# Plano\n\n## 1. Requisitos\n\nR1 atendido (§1).\n",
        })
        self.assertEqual(codigo, 0)
        self.assertNotIn("AVISO", saida)
        self.assertNotIn("ERRO", saida)

    def test_lixo_classico_vira_aviso(self):
        _, saida = rodar({
            "LICENSE": "MIT",
            "requirements.txt": "", "requirements-dev.txt": "",
            "docs/plano/00.md": "## Cronograma\n\nEntrega em 23/10/2026.\n\n## Uso de IA\n",
        })
        for trecho in ("`LICENSE`", "mais de um requirements", "data(s) no plano",
                       "cronograma", "Uso de IA"):
            self.assertIn(trecho, saida)

    def test_exemplo_em_bloco_de_codigo_nao_conta(self):
        _, saida = rodar({"docs/plano/00.md": "```\nstart = '2026-10-21'  # TODO\n```\n"
                                              "Exemplo `21/10/2026` inline.\n"})
        self.assertNotIn("data(s)", saida)
        self.assertNotIn("placeholder", saida)

    def test_tbd_e_trunk_based_nao_placeholder(self):
        _, saida = rodar({"docs/plano/00.md": "Fluxo TBD: branch curta a partir da main.\n"})
        self.assertNotIn("placeholder", saida)

    def test_secao_inexistente_e_caminho_local_sao_erro(self):
        codigo, saida = rodar({"docs/plano/00.md": "## 1. Escopo\n\nVer §9. Clone em C:\\Users\\fulano\\repo\n"})
        self.assertEqual(codigo, 1)
        self.assertIn("§ sem título correspondente: 9", saida)
        self.assertIn("caminho de máquina local", saida)

    def test_plano_maior_que_codigo(self):
        _, saida = rodar({
            "src/a.py": "a = 1\n",
            "docs/plano/00.md": "```python\n" + "x = 1\n" * 30 + "```\n",
        })
        self.assertIn("plano maior que o código", saida)


if __name__ == "__main__":
    unittest.main()
