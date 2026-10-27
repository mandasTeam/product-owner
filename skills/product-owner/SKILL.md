---
name: product-owner
description: "Use ao transformar ideia solta em MVP; ao planejar projeto ou feature a partir de enunciado, rubrica, issue ou repo herdado; ao escrever a spec antes de um agente de IA implementar (spec-driven development); ao montar backlog no GitHub (issues e Project); ou ao limpar escopo inchado. Extrai requisitos rastreáveis, registra decisões e corta tudo o que nenhum requisito pede."
license: MIT
---

# Product Owner

Ideia ou fontes → requisitos rastreáveis → decisões registradas → spec → tarefas → código
conferido contra a spec. A regra que sustenta tudo: **todo artefato aponta para um requisito
(R#) ou uma decisão (D#); o que não aponta para nada não entra.** É assim que o plano sai
preciso (nada inventado) e enxuto (nada sobrando).

Escreva no idioma do usuário, direto.

## Quando usar

- Ideia solta, várias ideias de pessoas diferentes, "quero fazer um app que…" → **modo MVP**.
- Planejar projeto, trabalho ou feature grande a partir de enunciado, rubrica, issue ou repo
  herdado → **procedimento**.
- Feature que um agente de IA vai implementar → spec antes do código (passos 6 e 10).
- Transformar o plano em backlog no GitHub: issues, labels, Project.
- Limpar escopo ou planejamento que já existe → **modo limpeza**.

Não use quando o diff cabe numa frase: faça direto e diga o que fez.

**Fora desta skill:** CI/CD, lint e formatação, proteção de branch, CODEOWNERS, fluxo de
branch e PR, Docker, ambientes e deploy. Se um R pede algo disso, vira tarefa do plano com o
R citado; a configuração fica com a skill de devops.

## Seis palavras que guiam

- **Rastreável** — cada tarefa, arquivo, seção, label e campo cita o R#/D# que atende.
- **Executado** — número, nome, conta e comando saem de saída real ou de cópia literal da
  fonte, com o comando ao lado. O que não foi conferido é marcado como hipótese.
- **Necessário** — passa no teste das três perguntas (passo 7).
- **Fonte única** — cada informação mora num lugar só; os outros apontam para ele.
- **Spec primeiro** — comportamento novo ou alterado muda na spec antes de mudar no código.
- **Proporção** — o plano carrega decisões, não o programa. Plano maior que o código que
  descreve já escreveu o código — exceto quando o usuário quer o plano "mastigado" com código
  de referência para quem implementa (ex.: colegas de faculdade): aí isso vira um D do usuário
  que justifica o aviso de proporção do auditor, e o código não se corta sem perguntar.

## Modo MVP (a ideia ainda não tem escopo)

Quando nenhuma fonte fixa o que construir, o escopo sai de uma hipótese, não de uma lista de
features. Perguntas, exemplos e sinais de MVP inchado em `references/mvp.md`.

1. **Despejar.** Todas as ideias (conversa, notas, colegas) numa lista só, uma linha cada, com
   quem trouxe. Sem julgar ainda.
2. **Consolidar.** Junte duplicatas e variações; cada grupo vira uma ideia com os autores.
3. **Hipótese.** Uma frase: *para <quem>, que <dor>, <solução> faz <resultado>; deu certo
   quando <métrica com limiar>.* Público, dor e métrica são do usuário: entram na rodada de
   perguntas do passo 3; se ele não souber, decisão do agente marcada.
4. **Jornada crítica.** Os poucos passos (3–5) que entregam o valor uma vez, de ponta a ponta.
5. **Corte.** Cada ideia ganha destino: **MVP** (sem ela a jornada ou a métrica quebra) ·
   **Depois** (melhora, não valida) · **Descartada** (não serve à hipótese). Sem pontuação
   inventada: RICE ou "impacto 1–10" sem dado fere o *Executado*.
6. **Risco.** As suposições que matam a ideia se forem falsas, como o MVP testa cada uma e o
   critério de parada (o resultado que faz desistir ou mudar de rumo).
7. **Saída.** O que ficou no MVP vira R# com fonte "hipótese H1"; Depois e Descartada vão para
   o "Fora do escopo" com motivo. Siga do passo 3 do procedimento.

*Pronto quando:* hipótese em uma frase com métrica, toda ideia tem destino e o MVP cabe numa
jornada. Ideia nova no meio do projeto passa pelo mesmo corte: entra só se a jornada ou a
métrica quebra sem ela.

## Procedimento

0. **Dimensionar.** Pequeno (1 entrega, 1 pessoa): plano curto num arquivo ou direto na issue.
   Projeto: plano completo. Vários subsistemas independentes: um plano por subsistema.
   Cresceu no meio: pare e suba de tamanho. Sem fonte que fixe escopo: modo MVP primeiro.
   *Pronto quando:* o tamanho está dito em uma linha.
1. **Inventário de fontes.** Ler cada fonte inteira (PDF com OCR se preciso, repo, rubrica,
   repo de referência, conversa anterior). Pessoas e contas saem do GitHub, nunca de memória.
   Enunciado que não está no repo: procure o arquivo na máquina (`Downloads`, por nome do
   trabalho) e extraia o texto antes de perguntar — é fato levantável, não pergunta.
   Repo herdado: o comportamento atual é fonte, citado por `arquivo:linha` (`references/sdd.md`).
   *Pronto quando:* a tabela de fontes lista cada uma com o que ela fixa.
2. **Extrair requisitos.** `R1..Rn`, cada um com trecho literal curto e localização
   (página/seção/linha). Nomes próprios (disciplina, produto, cliente) copiados exatamente.
   Termo ambíguo: liste as leituras; cobrir as duas só se custar pouco, senão vira decisão.
   *Pronto quando:* toda frase imperativa da fonte virou um R ou tem nota "não é requisito".
3. **Fechar decisões.** O que as fontes não fixam e muda o que se constrói vira `D#`:
   decisão · quem decidiu · motivo · alternativa descartada.
   - Usuário pediu para não perguntar, ou a decisão é barata de reverter → decida e marque
     **decisão do agente**.
   - Senão, **uma rodada** de perguntas (`AskUserQuestion` no Claude Code): só a fronteira,
     isto é, perguntas cujos pré-requisitos já estão fechados; até 4, recomendação primeiro.
     Fato que dá para levantar é seu, nunca do usuário. Pergunta que precisa de algo para
     reagir (layout, "como deve parecer") não se debate: faça um protótipo descartável e volte.
   - Lacuna num rascunho de spec fica marcada `[PRECISA ESCLARECER: …]` até virar D; o
     auditor acusa a marca que sobrar.
   *Pronto quando:* nenhuma decisão aberta e cada D tem motivo.
4. **Verificar fatos e viabilidade.** Rodar o que der: baixar e contar dados, medir cobertura,
   listar colaboradores e e-mails atribuídos, prototipar em rascunho a parte arriscada. Toda
   **regra de processo** passa pelo teste "a plataforma deixa?" (ver Armadilhas).
   *Pronto quando:* todo número do plano tem comando de origem.
5. **Escopo negativo.** "Fora do escopo": o que um builder razoável acrescentaria e não vamos
   fazer, com motivo. Inclui os itens de `references/catalogo-de-lixo.md` que não se aplicam.
   *Pronto quando:* cada exclusão tem uma linha de motivo.
6. **Plano mínimo e spec.** Modelos em `references/modelos.md`.
   - `docs/plano/00-visao-geral.md`: fontes, R → onde é atendido, D, fora do escopo, tarefas,
     contratos entre tarefas, definição de pronto com comandos.
   - **Spec** = o *quê* e o *porquê* de uma feature, sem tecnologia: histórias priorizadas
     (P1 sozinha já entrega valor) e critérios de aceite *Dado / Quando / Então* que viram
     testes. O *como* (arquivos, interfaces) fica na tarefa. Feature que um agente implementa
     ganha `specs/<nnn-slug>/spec.md`; projeto de uma feature só usa a seção de tarefas.
     Ciclo completo em `references/sdd.md`.
   - Arquivo por responsável só com mais de uma pessoa; senão a tarefa vive na issue.
   - **Tarefa** = menor unidade com verificação própria que um revisor aprovaria ou
     rejeitaria sozinha. Setup, config e docs entram na tarefa que precisa deles.
   - Ordem por **grafo de dependências** (`bloqueada por`). Data só quando a fonte fixa
     prazo, e aí só o prazo.
   - Cada passo diz o que o implementador não decide sozinho: arquivo, assinatura, valores
     exatos da fonte, asserções do teste, comando de verificação e saída esperada. Corpo de
     código só para algoritmo que assinatura + teste não determinam, ou texto literal exigido.
   *Pronto quando:* toda tarefa cita R/D e critério de aceite, e termina num comando que passa
   ou falha.
7. **Teste de necessidade** em cada arquivo, seção, issue, label, campo do Project, template,
   agente e skill do repo:
   1. qual R/D atende?
   2. quem lê ou usa, e quando?
   3. o que quebra se não existir?

   Qualquer resposta vazia → corta. Confira contra `references/catalogo-de-lixo.md`.
   *Pronto quando:* a tabela de artefatos não tem célula vazia.
8. **Olhos frescos.** Um subagente recebe só as fontes, a spec e o plano, em dois papéis:
   *builder* (que perguntas precisaria fazer para implementar?) e *refutador* (afirmação sem
   fonte, regra impossível, nome/conta/§ inconsistente, R sem tarefa, tarefa sem R, critério
   de aceite sem teste). Peça para reportar **só** lacuna que afeta correção ou requisito
   declarado — revisor caçando "melhorias" gera over-engineering.
   Triagem: já respondido → entra no doc; menor → decisão do agente; do usuário → uma mensagem.
   *Pronto quando:* cada achado foi para uma das três pilhas.
9. **Materializar o backlog no GitHub** (se pedido), com `gh`. Repo → arquivos do commit
   inicial → labels (apagar as padrão que nada usa) → issues em ordem de dependência →
   Project → convites para quem recebe issue. Issue = o que entregar + linha `Atende: R…· D…`
   + critérios de aceite em checkbox + `bloqueada por` + link para a seção do plano; o *como*
   fica no plano, não duplicado na issue. Issue-mãe também leva checkbox (o auditor acusa sem)
   e aponta para a tabela de tarefas em vez de copiá-la.
   *Pronto quando:* issues, labels e Project lidos de volta (`gh issue list`,
   `gh project item-list`) batem com a tabela de tarefas.
10. **Implementar guiado pela spec** (quando você ou outro agente implementa). Uma tarefa por
    vez, com contexto mínimo: spec, tarefa e contratos. Testes dos critérios de aceite antes
    do código. Divergiu da spec (o caso não cabe, a interface não fecha) → pare, registre o D
    e atualize a spec, depois o código. Ao fechar, cada critério aponta para a evidência.
    *Pronto quando:* todo critério de aceite da tarefa tem teste ou saída que passa.
11. **Auditar.** `python <pasta-desta-skill>/scripts/auditar_escopo.py <repo> --gh dono/repo`.
    Cada ERRO corrigido; cada AVISO cortado ou justificado por R/D no plano.
    *Pronto quando:* 0 erro e nenhum aviso sem justificativa.

## Modo limpeza (o escopo já existe)

1. Rode o auditor e inventarie os artefatos do repo (`git ls-files`, labels, issues e corpos,
   campos do Project, colaboradores **e convites pendentes**, cópias do plano fora do repo).
   Confira os requisitos contra a fonte original, não contra o plano.
2. Teste de necessidade em cada um; liste os cortes com motivo.
3. Pedido de "verificação": entregue o relatório (quebrado/inconsistente · cortes propostos ·
   o que fica e por quê) e **uma rodada** só com o que o usuário pode querer manter por motivo
   que o repo não mostra (plano didático, material de apresentação, cópia externa, nome da
   fonte). O resto dos cortes já vai aprovado junto.
4. Antes do início do desenvolvimento, limpeza vai direto na `main` em commits `cleanup:`,
   sem issue nem branch, a menos que o usuário peça PR.
5. Aplique por grupo de assunto, um commit por grupo: script de substituição que **exige a
   contagem exata** de cada trecho (falha em vez de editar errado) + `git rm` + ações no GitHub
   (`gh label delete`, `gh project field-delete --id`, `gh issue edit --body-file -`). Ao
   apagar label, campo ou template, procure referências também em `.claude/` (skills, scripts)
   e nos corpos das issues. Os testes que já existiam continuam passando.
6. Depois de cortar: renumere seções, busque cada termo removido até dar zero (só pode sobrar
   no "Fora do escopo"), e apague cópias antigas do plano fora do repo (ou declare a fonte
   única).
7. Rode o auditor de novo e reporte o antes/depois.

## Relatório final

Curto: o que existe (links), hipótese e métrica (modo MVP), cobertura `R atendidos/R total` e
`critérios com teste/critérios total`, **decisões do agente** para o usuário conferir, fora do
escopo, saída do auditor, pendências que são do usuário.

## Armadilhas

- **Regra que a plataforma não executa.** "O QA aprova todos os PRs" quando o QA também é
  autor: o GitHub não deixa aprovar o próprio PR, e esses PRs acabam mergeados sem revisão.
  Toda regra de revisão/aprovação precisa de um caminho válido para *cada* autor.
- **Plano que virou o programa.** Uma spec por issue com o código inteiro produz dez vezes
  mais linhas de plano que de código. Ninguém lê, e desatualiza no primeiro commit. Exceção
  registrada como D do usuário: plano "mastigado" para implementadores pouco autônomos (ver
  **Proporção**) — aí corte só o que nenhum R/D pede (roteiro de defesa, regras de processo
  inventadas), não o código de referência.
- **Spec que descreve a implementação.** Framework, tabela e endpoint na spec misturam o quê
  com o como; o primeiro refactor invalida a spec inteira. Quê na spec, como na tarefa.
- **Código que corrige a spec em silêncio.** O agente implementa diferente do especificado e
  ninguém atualiza: a spec morre e o próximo agente segue o texto errado. Divergência = D
  novo e spec atualizada no mesmo commit do código.
- **MVP que é a versão 1.0.** Jornada com muitos passos, métrica ausente ou "Depois" vazio:
  nada foi cortado. Volte ao corte.
- **Conta e nome deduzidos.** Pessoa com duas contas no GitHub: use a que tem commits
  atribuídos recentes. Nome de disciplina, produto ou cliente: copie da fonte, não deduza.
- **Padrão de produto em projeto que não é produto.** Trabalho de uma entrega não precisa de
  LICENSE, cronograma, `requirements-dev.txt` nem ambientes. Molde e repo de referência passam
  pelo teste de necessidade como qualquer artefato.
- **Duas cópias do plano.** A cópia fora do repo não recebe as correções. Fonte única.
- **Renumerar quebra §.** Depois de cortar seção, procure toda `§N` (o auditor acusa).
- **Siglas do time.** "TBD" pode ser Trunk-Based Development, não "a definir". Leia o glossário
  do projeto antes de chamar algo de pendência.
- **Convite pendente** (`gh api repos/O/R/invitations`): o assignee não pega e o `gh` não
  reclama. Leia de volta e reporte como pendência do usuário.
- **Proporção justificada.** O auditor rebaixa o aviso de proporção para INFO quando uma linha
  de decisão do plano (`| D# | ...`) diz que "o plano é maior que o código". Escreva o D com
  essa frase; sem ela o aviso continua. Seções "Fora do escopo" e "Fora do MVP" são ignoradas
  nas checagens de cronograma, ambientes e placeholders.
- **Entrevista longa não é qualidade.** Conte rodadas, não perguntas; muitas perguntas = escopo
  grande demais, quebre em partes.

## Verificação

- [ ] Modo MVP: hipótese com métrica, toda ideia com destino, MVP numa jornada
- [ ] Toda tarefa e todo artefato do repo cita R# ou D#
- [ ] Todo número do plano tem comando de origem; nomes próprios copiados da fonte
- [ ] Toda regra de processo tem caminho válido na plataforma para cada autor
- [ ] "Fora do escopo" existe e tem motivo por linha
- [ ] Spec sem tecnologia e sem marca de esclarecimento; todo critério de aceite vira teste
- [ ] Plano menor que o código esperado (ou um D do usuário pede plano com código de referência); blocos de código só onde decidem algo
- [ ] Auditor: 0 erro, avisos justificados
- [ ] Revisão de olhos frescos feita e triada
