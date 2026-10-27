# Modo MVP: da ideia ao escopo

MVP é o menor produto que **testa a hipótese** com usuários reais, não a versão 1.0 com
menos telas. O critério de corte é aprendizado: entra o que a hipótese precisa para ser
confirmada ou derrubada.

## Despejar e consolidar

- Fontes de ideia: conversa, áudio transcrito, notas, issues soltas, mensagens dos colegas.
  Leia tudo antes de agrupar; ideia que só aparece uma vez também entra.
- Uma linha por ideia, no formato `I#: <verbo + objeto> — <quem trouxe>`. Ideia que é solução
  ("usar IA para…") e ideia que é dor ("perco tempo com…") ficam na mesma lista.
- Agrupe por dor atendida, não por tela ou tecnologia. Duas ideias que resolvem a mesma dor de
  jeitos diferentes viram uma ideia com variantes; a escolha da variante é um D.
- Conflito entre pessoas (cada um quer uma coisa) não se resolve com "faz as duas": vira
  pergunta na rodada ou duas hipóteses, e o MVP testa uma.

## Rodada de perguntas (só o que o agente não levanta sozinho)

| Pergunta | Por que importa |
|---|---|
| Quem exatamente usa? (um segmento, não "todo mundo") | define a jornada e quem testa |
| Que dor ele tem hoje e como resolve agora? | sem dor real, não há o que validar |
| O que tem que acontecer para você dizer "funcionou"? | vira a métrica com limiar |
| O que faria você desistir ou mudar de rumo? | vira o critério de parada |

Restrição dada pela fonte (prazo da disciplina, stack obrigatória, tamanho do time) não é
pergunta: é R. Se o usuário pediu para não perguntar, proponha cada resposta como decisão do
agente e liste no relatório.

## Hipótese e métrica

```text
H1: Para <segmento>, que <dor>, <solução> faz <resultado>.
Métrica: <comportamento observável> ≥ <limiar> em <janela>, medido por <como>.
Parada: <resultado> → desistir ou mudar de rumo.
```

- Métrica é comportamento (concluiu, voltou, pagou, indicou), não opinião ("gostou").
- O limiar vem do usuário ou da fonte. Sem base, marque como hipótese do agente; não invente
  benchmark de mercado.
- Projeto acadêmico sem usuário real: a métrica é a demonstração da jornada para quem avalia
  (o professor, a banca), e a rubrica continua sendo fonte de R.

## Jornada crítica

Os passos que o usuário faz para sentir o valor uma vez: `entrar → <ação central> → <resultado
visível>`. Teste de cada passo: tirando este, a hipótese ainda pode ser testada? Se pode, ele
sai do MVP. Cadastro, perfil, configurações e painel administrativo quase sempre saem:
substitua por usuário fixo, dado semeado ou operação manual feita pelo time.

## Corte

| Ideia | Destino | Motivo |
|---|---|---|
| I3 enviar lembrete por e-mail | MVP | sem ele a métrica "voltou em 7 dias" não acontece |
| I5 login com Google | Depois | conveniência; usuário fixo basta para testar H1 |
| I7 app mobile nativo | Descartada | web responsiva cobre a jornada |

- **MVP** vira R com fonte `H1` na tabela de requisitos.
- **Depois** e **Descartada** vão para o "Fora do escopo" com o motivo. Não viram issue nem
  backlog; quando a métrica confirmar H1, o próximo ciclo reabre a lista.
- Faça manual o que puder ser manual (o time envia o relatório, cadastra o cliente): o MVP
  testa a dor, não a automação.

## Riscos

Para cada suposição que mata a ideia se for falsa: como o MVP a testa e o que observar. Risco
técnico desconhecido (a API existe? o dado está disponível?) é fato levantável: protótipo
descartável no passo 4 do procedimento, antes de fechar o escopo.

## Sinais de MVP inchado

- Mais de 5 passos na jornada, ou passos que não levam à métrica.
- Coluna "Depois" vazia: nada foi cortado.
- Feature para "parecer produto" (landing page, onboarding, temas, notificações configuráveis).
- Infra de escala antes de existir usuário (filas, microsserviços, cache).
- Pontuação de priorização com números chutados no lugar do teste "a hipótese cai sem isso?".
