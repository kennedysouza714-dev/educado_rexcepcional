# Detran Quiz - Aplicativo de Teste de Habilitação

## Visão Geral
Aplicativo móvel para simulação do teste de habilitação do DETRAN, desenvolvido com Expo (React Native) e FastAPI.

## Funcionalidades Implementadas

### ✅ Autenticação
- Registro de usuário (nome, email, senha)
- Login com email e senha
- Persistência do token JWT
- Logout

### ✅ Simulado DETRAN
- 30 questões aleatórias por simulado
- Timer de 40 minutos
- Feedback imediato após cada resposta
- Resultado com percentual de acertos
- Aprovação com 70% (21 acertos)
- Revisão detalhada das respostas com comentários

### ✅ Estudo por Módulo
- 4 módulos disponíveis:
  - Módulo 1: Placas, Cores e Caminhos (fácil)
  - Módulo 2: Escolhas e Consequências (intermediário)
  - Módulo 3: Na Direção da Segurança (difícil)
  - Módulo 4: Cuidar, Agir e Preservar (fácil)
- Estudo individual de questões
- Verificação de resposta com comentário explicativo

### ✅ Histórico e Estatísticas
- Lista de simulados anteriores
- Taxa de aprovação
- Melhor pontuação
- Total de simulados realizados

### ✅ Perfil do Usuário
- Visualização de dados do usuário
- Opções de configuração
- Logout

## Estrutura de Dados

### Questões (45 questões populadas)
- Módulo 1: 15 questões
- Módulo 2: 10 questões  
- Módulo 3: 10 questões
- Módulo 4: 10 questões

## Tecnologias

### Frontend
- Expo / React Native
- expo-router (navegação)
- zustand (gerenciamento de estado)
- axios (requisições HTTP)
- AsyncStorage (persistência local)

### Backend
- FastAPI
- MongoDB (motor async)
- JWT (autenticação)
- bcrypt (hash de senhas)

## Endpoints da API

### Autenticação
- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Dados do usuário atual

### Módulos
- `GET /api/modules` - Lista módulos
- `GET /api/modules/{modulo}/questions` - Questões do módulo
- `GET /api/modules/{modulo}/question/{id}` - Questão com resposta

### Simulado
- `GET /api/simulation/new` - Iniciar simulado (30 questões)
- `POST /api/simulation/submit` - Enviar respostas
- `GET /api/simulation/{id}` - Resultado do simulado

### Histórico
- `GET /api/history` - Histórico de simulados
- `GET /api/stats` - Estatísticas do usuário

## Próximos Passos Sugeridos
1. Adicionar mais questões (1153 total conforme PDF)
2. Implementar imagens para placas de trânsito
3. Adicionar modo de estudo com questões por categoria
4. Notificações push para lembretes de estudo
5. Tema escuro
