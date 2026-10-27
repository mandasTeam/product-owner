# Spec-driven development (SDD)

Com agente de IA implementando, a spec é o contrato: o agente lê a spec e a tarefa, não a
conversa. O que não está escrito ele inventa. Por isso a spec vem antes do código, descreve
comportamento verificável e muda **antes** do código quando o comportamento muda.

Ciclo: **especificar → esclarecer → planejar → quebrar em tarefas → conferir consistência →
implementar uma tarefa por vez → conferir código contra a spec.**

## Onde cada coisa mora

| Artefato | Conteúdo | Não contém |
|---|---|---|
| `specs/<nnn-slug>/spec.md` | o quê e por quê: histórias, critérios de aceite, casos de borda, entidades | tecnologia, arquivos, código |
| plano (`docs/plano/`) | R → onde é atendido, D, fora do escopo, tarefas, contratos | critérios repetidos da spec |
| tarefa (no plano ou na issue) | o como: arquivo, assinatura, teste, comando de verificação | justificativa de negócio |

- Projeto pequeno, uma feature: sem pasta `specs/`; as histórias e critérios ficam na seção de
  tarefas do plano. A pasta só existe quando há mais de uma feature especificada.
- Princípios que valem para toda feature (stack fixa, "sem dependência externa") são D no
  plano, ou ficam no `AGENTS.md`/`CLAUDE.md` que o repo já tiver. Não crie um arquivo de
  "constituição" separado: seria a segunda fonte.
- Não copie o andaime de ferramentas de SDD (pastas de scripts, templates, comandos): use só os
  arquivos que alguma feature preenche.

## Especificar

- **Histórias priorizadas** P1, P2…, cada uma testável sozinha. P1 implementada sozinha já é
  um incremento que entrega valor (no modo MVP, P1 é a jornada crítica).
- **Critérios de aceite** em *Dado / Quando / Então*, um comportamento por critério, com os
  valores exatos da fonte. Cada critério tem id (`US1.2`) para o teste citar.
- Regras do sistema que não são cenário usam a forma EARS:
  `Quando <gatilho>, o sistema deve <resposta>` · `Enquanto <estado>, …` · `Se <erro>, então …`.
- **Casos de borda** explícitos: vazio, duplicado, limite, permissão negada, falha externa.
- **Critério de sucesso** mensurável e sem tecnologia ("o usuário conclui X em até 3 passos"),
  não "a API responde em 200 ms com Redis".
- Cada história e critério cita o R que atende. Critério sem R é escopo inventado.

## Esclarecer

Lacuna vira marca `[PRECISA ESCLARECER: <pergunta>]` no ponto exato da spec, nunca uma
suposição silenciosa. Antes de planejar, as marcas viram perguntas da rodada única do passo 3
ou decisões do agente; cada resposta sai da spec como D. O auditor acusa marca que sobrou.

## Planejar e quebrar em tarefas

- Tarefas agrupadas por história, na ordem de prioridade: P1 inteira (com testes) antes de P2.
- Cada tarefa cita os critérios que fecha (`Fecha: US1.1, US1.2`) e o comando que prova.
- Contratos entre tarefas (assinatura, formato de arquivo, colunas) ficam escritos no plano;
  dois agentes em paralelo só se encontram pelo contrato.
- Tarefa que dois agentes podem fazer ao mesmo tempo não toca o mesmo arquivo.

## Conferir consistência (antes de implementar)

Matriz cruzada, feita pelo refutador do passo 8:

| Checagem | Falha típica |
|---|---|
| todo R tem história ou tarefa | requisito da rubrica esquecido |
| toda história tem critério de aceite | história que ninguém consegue aprovar |
| todo critério tem tarefa que o fecha | critério órfão |
| toda tarefa fecha critério ou atende D | tarefa inventada |
| termos iguais nos três artefatos | "cliente" na spec, "usuário" no plano |

## Implementar com o agente

1. Contexto mínimo por tarefa: a spec da feature, a tarefa e os contratos. A conversa de
   planejamento não vai junto; se algo dela importa, devia estar na spec.
2. Testes dos critérios primeiro, com o id do critério no nome ou na docstring; rode e veja
   falhar pelo motivo certo.
3. Implementação mínima até os testes passarem; nada que nenhum critério pede.
4. **Divergência:** o caso não cabe na spec, a interface não fecha, um critério contradiz
   outro → o agente para e relata. Decide-se o D, atualiza-se a spec e só então o código. Spec
   e código mudam no mesmo commit.
5. Fechamento: cada critério da tarefa aponta para o teste ou a saída que o prova. Critério
   sem evidência mantém a tarefa aberta.

## Conferir código contra a spec

Ao fim da feature, percorra a spec critério a critério: implementado e testado · implementado
sem teste · não implementado. Na direção inversa, comportamento no código que nenhuma spec
descreve é escopo inventado (corta) ou requisito esquecido (vira R e entra na spec).

## Repo herdado (brownfield)

Antes de especificar a mudança, extraia a spec do comportamento atual da parte que vai mudar:
cada regra observada com `arquivo:linha` como fonte, no mesmo formato EARS. O que o código faz
e ninguém explica vira pergunta, não requisito. A mudança é então um diff de spec (o que
passa a valer, o que deixa de valer) antes de ser um diff de código.
