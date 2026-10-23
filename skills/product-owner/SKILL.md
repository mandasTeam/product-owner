---
name: product-owner
description: "Use ao planejar um projeto ou feature a partir de enunciado, rubrica, issue, repo herdado ou ideia; ao montar repositório GitHub com issues e Project a partir de um plano; ou ao limpar escopo e planejamento inchados. Extrai requisitos rastreáveis, registra decisões e corta tudo o que nenhum requisito pede."
license: MIT
---

# Product Owner

Fontes → requisitos rastreáveis → decisões registradas → plano mínimo → repositório.
A regra que sustenta tudo: **todo artefato aponta para um requisito (R#) ou uma decisão
(D#); o que não aponta para nada não entra.** É assim que o plano sai preciso (nada
inventado) e enxuto (nada sobrando).

Escreva no idioma do usuário, direto.

## Quando usar

- Planejar projeto, trabalho ou feature grande a partir de enunciado, rubrica, issue, repo
  herdado ou ideia solta.
- Transformar um plano em repo com issues, Project e templates.
- Limpar escopo ou planejamento que já existe (**modo limpeza**, abaixo).

Não use quando o diff cabe numa frase: faça direto e diga o que fez.

## Cinco palavras que guiam

- **Rastreável** — cada tarefa, arquivo, seção, label e campo cita o R#/D# que atende.
- **Executado** — número, nome, conta e comando saem de saída real ou de cópia literal da
  fonte, com o comando ao lado. O que não foi conferido é marcado como hipótese.
- **Necessário** — passa no teste das três perguntas (passo 7).
- **Fonte única** — cada informação mora num lugar só; os outros apontam para ele.
- **Proporção** — o plano carrega decisões, não o programa. Plano maior que o código que
  descreve já escreveu o código.

## Procedimento

0. **Dimensionar.** Pequeno (1 entrega, 1 pessoa): plano curto num arquivo ou direto na issue.
   Projeto: plano completo. Vários subsistemas independentes: um plano por subsistema.
   Cresceu no meio: pare e suba de tamanho. *Pronto quando:* o tamanho está dito em uma linha.
1. **Inventário de fontes.** Ler cada fonte inteira (PDF com OCR se preciso, repo, rubrica,
   repo de referência, conversa anterior). Pessoas e contas saem do GitHub, nunca de memória.
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
   *Pronto quando:* nenhuma decisão aberta e cada D tem motivo.
4. **Verificar fatos e viabilidade.** Rodar o que der: baixar e contar dados, medir cobertura,
   listar colaboradores e e-mails atribuídos, prototipar em rascunho a parte arriscada. Toda
   **regra de processo** passa pelo teste "a plataforma deixa?" (ver Armadilhas).
   *Pronto quando:* todo número do plano tem comando de origem.
5. **Escopo negativo.** "Fora do escopo": o que um builder razoável acrescentaria e não vamos
   fazer, com motivo. Inclui os itens de `references/catalogo-de-lixo.md` que não se aplicam.
   *Pronto quando:* cada exclusão tem uma linha de motivo.
6. **Plano mínimo.** Modelo em `references/modelos.md`.
   - `docs/plano/00-visao-geral.md`: fontes, R → onde é atendido, D, fora do escopo, tarefas,
     contratos entre tarefas, definição de pronto com comandos.
   - Arquivo por responsável só com mais de uma pessoa; senão a tarefa vive na issue.
   - **Tarefa** = menor unidade com verificação própria que um revisor aprovaria ou
     rejeitaria sozinha. Setup, config e docs entram na tarefa que precisa deles.
   - Ordem por **grafo de dependências** (`bloqueada por`). Data só quando a fonte fixa
     prazo, e aí só o prazo.
   - Cada passo diz o que o implementador não decide sozinho: arquivo, assinatura, valores
     exatos da fonte, asserções do teste, comando de verificação e saída esperada. Corpo de
     código só para algoritmo que assinatura + teste não determinam, ou texto literal exigido.
   *Pronto quando:* toda tarefa cita R/D e termina num comando que passa ou falha.
7. **Teste de necessidade** em cada arquivo, seção, issue, label, campo do Project, workflow,
   template, agente e skill do repo:
   1. qual R/D atende?
   2. quem lê ou usa, e quando?
   3. o que quebra se não existir?

   Qualquer resposta vazia → corta. Confira contra `references/catalogo-de-lixo.md`.
   *Pronto quando:* a tabela de artefatos não tem célula vazia.
8. **Olhos frescos.** Um subagente recebe só as fontes e o plano, em dois papéis: *builder*
   (que perguntas precisaria fazer para implementar?) e *refutador* (afirmação sem fonte,
   regra impossível, nome/conta/§ inconsistente). Peça para reportar **só** lacuna que afeta
   correção ou requisito declarado — revisor caçando "melhorias" gera over-engineering.
   Triagem: já respondido → entra no doc; menor → decisão do agente; do usuário → uma mensagem.
   *Pronto quando:* cada achado foi para uma das três pilhas.
9. **Materializar no GitHub** (se pedido), com `gh`. Repo → arquivos do commit inicial (lint
   e testes locais verdes; config de lint exclui os blocos de código do plano) → labels
   (apagar as padrão que nada usa) → issues em ordem de dependência → Project → convites →
   proteção da `main` por último. Issue = o que entregar + critérios de aceite em checkbox +
   `bloqueada por` + link para a seção do plano; o *como* fica no plano, não duplicado na issue.
   *Pronto quando:* CI do último commit verde.
10. **Auditar.** `python <pasta-desta-skill>/scripts/auditar_escopo.py <repo> --gh dono/repo`.
    Cada ERRO corrigido; cada AVISO cortado ou justificado por R/D no plano.
    *Pronto quando:* 0 erro e nenhum aviso sem justificativa.

## Modo limpeza (o escopo já existe)

1. Rode o auditor e inventarie os artefatos do repo (`git ls-files`, labels, issues, campos).
2. Teste de necessidade em cada um; liste os cortes com motivo.
3. Antes do início do desenvolvimento, limpeza vai direto na `main` em commits `cleanup:`,
   sem issue nem branch, a menos que a `main` já esteja protegida ou o usuário peça PR.
4. Depois de cortar: renumere seções, busque cada termo removido até dar zero, e apague cópias
   antigas do plano fora do repo (ou declare qual é a fonte única).
5. Rode o auditor de novo e reporte o antes/depois.

## Relatório final

Curto: o que existe (links), cobertura `R atendidos/R total`, **decisões do agente** para o
usuário conferir, fora do escopo, saída do auditor, pendências que são do usuário.

## Armadilhas

- **Regra que a plataforma não executa.** "O QA aprova todos os PRs" quando o QA também é
  autor: o GitHub não deixa aprovar o próprio PR, e esses PRs acabam mergeados sem revisão.
  Toda regra de revisão/aprovação precisa de um caminho válido para *cada* autor.
- **Plano que virou o programa.** Uma spec por issue com o código inteiro produz dez vezes
  mais linhas de plano que de código. Ninguém lê, e desatualiza no primeiro commit.
- **Conta e nome deduzidos.** Pessoa com duas contas no GitHub: use a que tem commits
  atribuídos recentes. Nome de disciplina, produto ou cliente: copie da fonte, não deduza.
- **Padrão de produto em projeto que não é produto.** Trabalho de uma entrega não precisa de
  LICENSE, cronograma, `requirements-dev.txt` nem ambientes. Molde e repo de referência passam
  pelo teste de necessidade como qualquer artefato.
- **Duas cópias do plano.** A cópia fora do repo não recebe as correções. Fonte única.
- **Lint no plano.** Formatador que alcança os blocos de código do plano quebra o CI.
- **Renumerar quebra §.** Depois de cortar seção, procure toda `§N` (o auditor acusa).
- **Siglas do time.** "TBD" pode ser Trunk-Based Development, não "a definir". Leia o glossário
  do projeto antes de chamar algo de pendência.
- **Assignee com convite pendente** não pega, e o `gh` não reclama: leia de volta.
- **Entrevista longa não é qualidade.** Conte rodadas, não perguntas; muitas perguntas = escopo
  grande demais, quebre em partes.

## Verificação

- [ ] Toda tarefa e todo artefato do repo cita R# ou D#
- [ ] Todo número do plano tem comando de origem; nomes próprios copiados da fonte
- [ ] Toda regra de processo tem caminho válido na plataforma para cada autor
- [ ] "Fora do escopo" existe e tem motivo por linha
- [ ] Plano menor que o código esperado; blocos de código só onde decidem algo
- [ ] Auditor: 0 erro, avisos justificados
- [ ] Revisão de olhos frescos feita e triada
