# 🏗️ Arquitetura do Projeto

## 📋 Visão Geral

O Bot STEM GIRL foi desenvolvido seguindo uma **arquitetura modular** com separação clara de responsabilidades, facilitando manutenção, testes e escalabilidade.

## 🗂️ Estrutura de Arquivos

```
stem-bot/
├── 📁 cogs/           # Comandos e interface do usuário
│   ├── events.py      # Sistema de eventos
│   ├── welcome.py     # Sistema de boas-vindas
│   └── __init__.py
├── 📁 services/       # Lógica de negócio e operações
│   ├── events_service.py      # Operações de eventos (CRUD)
│   ├── event_scheduler.py     # Agendador de eventos recorrentes
│   └── __init__.py
├── 📁 components/     # Componentes reutilizáveis
│   ├── formatters/    # Formatação de embeds e mensagens
│   │   └── event_formatters.py
│   ├── validators/    # Validação de dados de entrada
│   │   └── event_validators.py
│   ├── handlers/      # Handlers de comandos e orquestração
│   │   └── event_handlers.py
│   └── choices/       # Opções predefinidas para comandos
│       └── event_choices.py
├── 📁 dados/          # Camada de dados
│   ├── database.py    # Contexto do banco
│   ├── stem_bot.db    # Banco SQLite
│   └── __init__.py
├── 📁 orientacoes/    # Documentação
├── bot.py             # Arquivo principal
└── requirements.txt   # Dependências
```

## 🔧 Componentes da Arquitetura

### 1. **Camada de Apresentação** (`cogs/`)

#### **Responsabilidades:**
- ✅ Definir comandos slash do bot
- ✅ Validar dados de entrada do usuário
- ✅ Construir respostas visuais (Embeds)
- ✅ Gerenciar interações com usuários

#### **Cogs Disponíveis:**
- **`events.py`**: Sistema de eventos (`/addevento_unico`, `/addrecorrente`, `/eventos`, `/modeventos`)
- **`welcome.py`**: Sistema de boas-vindas e logs de saída

### 2. **Camada de Serviços** (`services/`)

#### **Responsabilidades:**
- ✅ Encapsular lógica de negócio
- ✅ Executar operações no banco de dados
- ✅ Fornecer interface para Cogs
- ✅ Centralizar queries SQL
- ✅ Gerenciar tarefas agendadas

#### **Services Disponíveis:**
- **`events_service.py`**: Operações de eventos (CRUD)
- **`event_scheduler.py`**: Agendador de eventos recorrentes

### 3. **Camada de Componentes** (`components/`)

#### **Responsabilidades:**
- ✅ Fornecer componentes reutilizáveis
- ✅ Formatação de UI e mensagens
- ✅ Validação de dados
- ✅ Orquestração de comandos
- ✅ Configurações e constantes

#### **Componentes Disponíveis:**
- **`formatters/event_formatters.py`**: Formatação de embeds e mensagens
- **`validators/event_validators.py`**: Validação de dados de entrada
- **`handlers/event_handlers.py`**: Handlers de comandos e lógica de negócio
- **`choices/event_choices.py`**: Opções predefinidas para comandos slash

### 4. **Camada de Dados** (`dados/`)

#### **Responsabilidades:**
- ✅ Gerenciar conexão com SQLite
- ✅ Criar e manter estrutura do banco
- ✅ Fornecer interface de acesso aos dados

#### **Componentes:**
- **`database.py`**: Contexto e configuração do banco
- **`stem_bot.db`**: Arquivo do banco SQLite

### 5. **Aplicação Principal** (`bot.py`)

#### **Responsabilidades:**
- ✅ Configurar e inicializar o bot
- ✅ Carregar Cogs automaticamente
- ✅ Configurar intents e permissões
- ✅ Sincronizar comandos slash

## 🔄 Fluxo de Dados

### **Exemplo: Adicionar Evento**
```
1. Usuário: /addrecorrente "Workshop" 25/12/2024 14:00
2. Cog: Chama event_handlers.handle_add_recurring_event()
3. Handler: Valida dados via event_validators
4. Service: Executa operação no banco via events_service
5. Formatter: Constrói embed via event_formatters
6. Cog: Retorna embed de confirmação
```

### **Exemplo: Listar Eventos**
```
1. Usuário: /eventos
2. Cog: Chama event_handlers.handle_list_user_events()
3. Handler: Busca dados via events_service
4. Service: Executa query no banco
5. Formatter: Constrói embed via event_formatters
6. Cog: Retorna embed formatado
7. Usuário: Recebe lista formatada
```

## ✅ Benefícios da Arquitetura

### **1. Separação de Responsabilidades**
- **Cogs**: Apenas interface e comandos
- **Services**: Apenas lógica de negócio e operações
- **Components**: Apenas componentes reutilizáveis
- **Database**: Apenas persistência de dados

### **2. Manutenibilidade**
- Mudanças no banco não afetam comandos
- Queries centralizadas nos services
- Componentes isolados e testáveis
- Fácil localizar e corrigir problemas

### **3. Testabilidade**
- Services podem ser testados isoladamente
- Components podem ser testados independentemente
- Mocks podem substituir banco de dados
- Comandos testáveis independentemente

### **4. Escalabilidade**
- Fácil adicionar novos Cogs
- Services reutilizáveis entre Cogs
- Components reutilizáveis entre funcionalidades
- Estrutura preparada para crescimento

## 🚀 Como Estender

### **Adicionar Novo Cog:**
1. Criar `cogs/novo_cog.py`
2. Implementar comandos e validações
3. O bot carrega automaticamente

### **Adicionar Novo Service:**
1. Criar `services/novo_service.py`
2. Implementar lógica de negócio
3. Importar no Cog correspondente

### **Adicionar Novo Componente:**
1. Criar pasta apropriada em `components/`
2. Implementar funcionalidade específica
3. Importar onde necessário

### **Adicionar Nova Tabela:**
1. Atualizar `dados/database.py`
2. Criar service correspondente
3. Implementar operações CRUD

## 📊 Banco de Dados

### **Tabelas Atuais:**
- **`events`**: Eventos do servidor
  - `id` (INTEGER PRIMARY KEY)
  - `name` (TEXT)
  - `date` (TEXT)
  - `time` (TEXT)
  - `link` (TEXT)
  - `created_by` (INTEGER)
  - `type` (TEXT) - 'unico' ou 'recorrente'
  - `status` (TEXT) - 'ativo' ou 'concluido'
  - `frequency` (TEXT) - frequência para eventos recorrentes
  - `recurrence_details` (TEXT) - detalhes da recorrência
  - `created_at` (TIMESTAMP)

### **Próximas Tabelas Planejadas:**
- **`users`**: Informações dos usuários
- **`xp`**: Sistema de experiência
- **`missions`**: Missões semanais

Esta arquitetura torna o projeto profissional e fácil de manter! 🎉 