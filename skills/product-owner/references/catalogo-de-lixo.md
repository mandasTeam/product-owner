# Catálogo de lixo

Artefatos que entram "porque todo repo tem". Nenhum é proibido: cada um precisa de um R/D.
Se o caso não bate com a coluna *Quando é necessário*, corte e registre em "Fora do escopo".

| Artefato | Quando é necessário |
|---|---|
| `LICENSE` | código distribuído para terceiros reusarem (biblioteca, skill, ferramenta pública) |
| `CONTRIBUTING`, `CODE_OF_CONDUCT`, `SECURITY`, `SUPPORT` | há contribuidores ou usuários externos |
| `CHANGELOG`, releases, número de versão | alguém consome versões |
| Cronograma por data, sprints, D0–Dn | a fonte fixa prazos intermediários |
| `requirements-dev.txt`, ambientes prod/dev/homolog | existe deploy de produção |
| Docker/compose | um requisito pede ambiente reproduzível ou deploy |
| Seção "Uso de IA", log de prompts | a rubrica ou o cliente pede |
| Histórico de montagem no plano (origem de e-mails, caminho local, e-mail pessoal ou corporativo) | nunca no repo; vai no relatório ao usuário |
| Labels padrão do GitHub (`good first issue`, `help wanted`, `wontfix`…) | algum template ou issue usa |
| Templates de issue | o fluxo do time cria issues por eles |
| Campos do Project além de Status | alguma visão ou decisão filtra por ele |
| Spec por issue com o código inteiro | só com D do usuário pedindo plano "mastigado" para quem implementa; senão spec = decisões, interfaces, valores, testes |
| Arquivo de plano por integrante | mais de uma pessoa implementa |
| ADR | decisão difícil de reverter, com alternativa real descartada |
| `.gitkeep` em pastas futuras | nunca; a tarefa que usa a pasta cria a pasta |
| Badges | o badge informa estado (CI, versão, link executável) |
| Time de agentes / skills herdados de outro projeto | cada peça tem uso real neste repo; diga o que saiu e por quê |
| Agente revisor com permissão de escrita | nunca; revisor é só leitura |
| Issue + branch para limpeza antes do desenvolvimento | o usuário pede PR (`main` protegida não basta: o dono faz push como admin) |
| `CODEOWNERS` | a proteção exige *code owner review*; se o revisor vem de uma matriz no plano, é ruído |
| Template de issue "tarefa" | as tarefas ainda não existem como issues; senão duplica o template do agente |
| Template de PR em dois lugares (`.github/` e skill do agente) | nunca; a skill lê o de `.github/` |
| Suporte a Colab (badges, célula que clona o repo) | a fonte exige Colab, não "Colab ou GitHub" |
| Seções "Resumo", "Contribuições" no relatório | a fonte pede; autoria já está no git |
| `docs/` que repete seção do README | nunca; o README aponta para a tabela/figura gerada |
| Modelo serializado (`joblib`, `.pkl`) | algum notebook, seção ou deploy carrega o arquivo |
| "Roteiro de defesa", mínimo de commits por PR, prazo de PR em dias | a fonte ou o usuário pede |
| Cópia do plano fora do repo | nunca depois do commit inicial |

## Sinais de delírio (conteúdo inventado)

- Número sem comando de origem ("cobertura ~40%", "reduz 30% das falhas").
- Nome deduzido em vez de copiado (disciplina, produto, conta GitHub).
- Regra de processo que a plataforma não executa (autor aprovando o próprio PR, CODEOWNER sem
  permissão de escrita, assignee com convite pendente).
- Promessa da documentação sem código correspondente (perfil "Admin" num sistema sem login).
- Tarefa ou seção que nenhum R/D pede ("já que estamos aqui, vamos também…").
- Referência a arquivo, função ou seção que nenhuma tarefa cria.
