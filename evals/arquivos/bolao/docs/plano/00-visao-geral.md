# Bolão da Copa · Plano

## Visão

Plataforma de bolão escalável para o escritório, com potencial para virar produto SaaS para
outras empresas. A expectativa é reduzir em 40% o tempo de apuração do bolão.

## Cronograma

| Sprint | Período | Entrega |
|---|---|---|
| Sprint 1 | 04/05/2026 a 15/05/2026 | setup, Docker, Kubernetes, CI/CD |
| Sprint 2 | 18/05/2026 a 29/05/2026 | login social (Google e Microsoft), cadastro de perfil com foto |
| Sprint 3 | 01/06/2026 a 05/06/2026 | palpites, ranking, chat entre participantes |
| Sprint 4 | 08/06/2026 a 10/06/2026 | app mobile, notificações push, dashboard de estatísticas |

## Ambientes

- Desenvolvimento: docker-compose local.
- Homologação: cluster Kubernetes na nuvem.
- Produção: cluster Kubernetes na nuvem com autoescala.

## Especificação

O frontend em React consome uma API REST em Node com PostgreSQL e cache Redis. A tabela
`palpites` guarda (usuario_id, jogo_id, gols_casa, gols_fora). O ranking é recalculado por um
worker em fila a cada palpite.

Pontuação: 3 pontos para placar exato, 1 ponto para vencedor.

## Tarefas

| T | Entrega | Responsável |
|---|---|---|
| T1 | Setup Docker, Kubernetes e pipeline CI/CD | Rafa |
| T2 | Login social e perfil com foto | Rafa |
| T3 | Tela de palpites | Rafa |
| T4 | Ranking com worker em fila | Rafa |
| T5 | Chat entre participantes | Rafa |
| T6 | App mobile e notificações push | Rafa |
| T7 | Dashboard de estatísticas | Rafa |
| T8 | TODO: definir como o RH lança o placar | Rafa |
