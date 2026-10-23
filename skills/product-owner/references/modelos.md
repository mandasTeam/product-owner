# Modelos

Esqueletos mínimos. Seção que não tem conteúdo real no projeto não entra — não deixe título
vazio "para depois".

## `docs/plano/00-visao-geral.md`

```markdown
# <Projeto> · Plano

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
Atende: R4, D7 · Bloqueada por: T1

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

Branch: `<tipo>/<n>-<slug>`
```

## Tabela do teste de necessidade (modo limpeza)

```markdown
| Artefato | Atende | Quem usa / quando | Sem ele quebra | Decisão |
|---|---|---|---|---|
| LICENSE | — | ninguém | nada | cortar |
```
