# Modelos

Esqueletos mínimos. Seção que não tem conteúdo real no projeto não entra — não deixe título
vazio "para depois".

## `docs/plano/00-visao-geral.md`

```markdown
# <Projeto> · Plano

## 0. Hipótese (só no modo MVP)
H1: Para <segmento>, que <dor>, <solução> faz <resultado>.
Métrica: <comportamento> ≥ <limiar> em <janela>, medido por <como>. Parada: <resultado>.
Jornada: <passo> → <passo> → <resultado visível>

## 1. Fontes
| Fonte | O que fixa |
|---|---|
| <enunciado.pdf> | requisitos R1–R9, formato de entrega |

## 2. Requisitos
| R | Trecho literal (local) | Onde é atendido |
|---|---|---|
| R1 | "Descrição dos dados (fontes, tipos, volume)" (p.1, §2) | T1 · README §2.1 |

## 3. Decisões
| D | Decisão | Quem | Motivo | Descartado |
|---|---|---|---|---|
| D1 | README é o relatório | agente | a fonte aceita "notebook ou markdown" | PDF separado |

## 4. Fora do escopo
- <item> — <motivo em uma linha>

## 5. Fatos verificados
| Fato | Valor | Comando |
|---|---|---|

## 6. Tarefas
| T | Entrega | Atende | Responsável | Revisor | Bloqueada por |
|---|---|---|---|---|---|
| T1 | <entregável verificável> | R1, R2, D3 | @login | @login | — |

## 7. Contratos entre tarefas
<só o que uma tarefa consome de outra: assinaturas, nomes de arquivo, colunas>

## 8. Pronto
- [ ] <comando> → <saída esperada>
```

Grafo de dependências em texto (`T0 → T1 → {T2, T3}`) quando a tabela não deixar óbvio.

## Tarefa dentro do plano

```markdown
### T2 · <entrega>
Atende: R4, D7 · Fecha: US1.2 · Bloqueada por: T1

Arquivos: `src/pkg/modulo.py` (novo), `tests/test_modulo.py` (novo)
Interface: `funcao(df: DataFrame, limiar: float = 0.5) -> DataFrame`
Valores da fonte: <exatos>
Teste: `test_funcao_rejeita_vazamento` — `funcao(df_com_alvo)` levanta `ValueError`
Verificação: `pytest -q tests/test_modulo.py` → `N passed`
```

## Corpo de issue

```markdown
Atende: R4, D7 · Plano: docs/plano/00-visao-geral.md §6 (T2)
Bloqueada por: #1

## O que entregar
<comportamento de ponta a ponta, do ponto de vista de quem usa>

## Critérios de aceite
- [ ] <verificável por comando ou observação objetiva>
```

## `specs/<nnn-slug>/spec.md` (SDD)

Só quando há mais de uma feature especificada; senão histórias e critérios ficam nas tarefas.
Sem tecnologia: o como vai na tarefa. Formato dos critérios em `sdd.md`.

```markdown
# <nnn> · <feature>
Atende: R2, R5 · Plano: docs/plano/00-visao-geral.md

## Histórias
### US1 · <título> (P1)
<jornada em linguagem de quem usa>. Teste independente: <como provar só esta história>.
- US1.1 — Dado <estado>, quando <ação>, então <resultado com valor exato>.
- US1.2 — Se <erro>, então o sistema deve <resposta>.

## Casos de borda
- <vazio / duplicado / limite / permissão / falha externa> → <resultado esperado>

## Entidades
- <Entidade>: <o que representa, atributos que importam>

## Sucesso
- <resultado mensurável, sem tecnologia>
```

## Tabela do teste de necessidade (modo limpeza)

```markdown
| Artefato | Atende | Quem usa / quando | Sem ele quebra | Decisão |
|---|---|---|---|---|
| LICENSE | — | ninguém | nada | cortar |
```
