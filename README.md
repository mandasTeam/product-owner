<p align="center">
  <img src="assets/banner.svg" width="100%" alt="PRODUCT OWNER — skill para agentes. Do enunciado ao backlog no GitHub: só o que algum requisito pede. Requisitos rastreáveis, decisões registradas, zero lixo no repo.">
</p>

<p align="center">
  <a href="https://github.com/igorSeberino/product-owner-skill/actions/workflows/ci.yml"><img src="https://github.com/igorSeberino/product-owner-skill/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/github/license/igorSeberino/product-owner-skill" alt="Licença MIT">
</p>

**product-owner** é uma skill no formato `SKILL.md` que faz o agente de código trabalhar como um
PO antes de escrever código. Ele lê o enunciado, a rubrica, a issue ou o repo herdado. Depois transforma
isso em requisitos com a fonte citada, registra as decisões que faltam e monta no GitHub só o plano e as
issues de que o projeto precisa. Nada de licença, cronograma ou documento "porque todo repo tem".

<img src="assets/h-fluxo.svg" width="100%" alt="Como funciona">

1. **Fontes inteiras.** Lê tudo antes de planejar. Pessoas e contas são conferidas no GitHub.
2. **Requisitos R#.** Cada um com o trecho literal e onde ele está na fonte.
3. **Decisões D#.** O que a fonte não diz vira decisão com motivo. São no máximo 4 perguntas numa
   rodada só. Se você pedir para não perguntar, o agente decide e marca cada escolha para você conferir.
4. **Fatos executados.** Todo número do plano vem de um comando que rodou.
5. **Teste de necessidade.** Arquivo, seção, issue, label ou campo do Project só fica se responder:
   que requisito atende, quem usa, o que quebra sem ele.
6. **Plano em proporção.** O plano leva interfaces, valores exatos e testes, não o programa inteiro.
7. **Olhos frescos e auditoria.** Um subagente tenta refutar o plano. Um script acusa datas no plano,
   arquivos-padrão sem motivo, `§` quebrado, caminho local, labels sem uso e plano maior que o código.

Também tem um **modo limpeza** para repo que já nasceu inchado: faz o inventário, corta o que não tem
motivo em commits `cleanup:` e confere que não sobrou nenhuma referência ao que foi removido.

<img src="assets/h-instalar.svg" width="100%" alt="Instalação">

```bash
git clone https://github.com/igorSeberino/product-owner-skill.git
```

| Onde | Comando |
|---|---|
| Claude Code, para você em todos os projetos | `cp -r product-owner-skill/skills/product-owner ~/.claude/skills/` |
| Claude Code, só num projeto (vai junto no git) | `cp -r product-owner-skill/skills/product-owner <projeto>/.claude/skills/` |
| Outro agente com suporte a `SKILL.md` | copie `skills/product-owner/` para a pasta de skills dele |

No Windows (PowerShell), troque `cp -r` por `Copy-Item -Recurse` e `~` por `$HOME`.

O agente carrega a skill sozinho quando você pede para planejar um projeto, montar o repo ou limpar o
escopo. Para chamar direto no Claude Code, use `/product-owner`. A auditoria roda com o Python 3.10+
que já estiver instalado, sem nenhuma dependência.

<img src="assets/h-entrega.svg" width="100%" alt="O que sai no repo">

- `docs/plano/00-visao-geral.md` com fontes, requisitos e onde cada um é atendido, decisões, o que
  ficou fora do escopo e por quê, tarefas com dependências e a definição de pronto em comandos.
- Um arquivo de plano por responsável, só quando há mais de uma pessoa.
- Issues com o que entregar, critérios de aceite em checkbox, de quais issues dependem e o link para o
  plano, mais o Project com os campos que alguém de fato filtra.
- Um relatório curto com links, cobertura dos requisitos e a lista de decisões que o agente tomou
  sozinho.

Para desenvolver: `python -m unittest discover -s tests`. Commits seguem Conventional Commits.

### Licença

MIT, veja [LICENSE](LICENSE).
