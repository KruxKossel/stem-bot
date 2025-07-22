# 🏗️ Arquitetura do Projeto

## 📋 Visão Geral

O Bot STEM-GIRL foi desenvolvido seguindo uma **arquitetura modular** com separação clara de responsabilidades, facilitando manutenção, testes e escalabilidade.

## 🗂️ Estrutura de Arquivos

```
stem-bot/
├── 📁 cogs/           # Comandos e interface do usuário
│   ├── events.py      # Sistema de eventos
│   ├── welcome.py     # Sistema de boas-vindas
│   └── __init__.py
├── 📁 services/       # Lógica de negócio
│   ├── events_service.py      # Operações de eventos
│   ├── event_formatters.py    # Formatação de embeds
│   ├── event_handlers.py      # Handlers de comandos
│   ├── event_validators.py    # Validação de dados
│   ├── event_scheduler.py     # Agendador de eventos
│   ├── event_choices.py       # Opções de comandos
│   └── __init__.py
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

#### **Services Disponíveis:**
- **`events_service.py`**: Operações de eventos (CRUD)
- **`event_formatters.py`**: Formatação de embeds e mensagens
- **`event_handlers.py`**: Handlers de comandos e lógica de negócio
- **`event_validators.py`**: Validação de dados de entrada
- **`event_scheduler.py`**: Agendador de eventos recorrentes
- **`event_choices.py`**: Opções predefinidas para comandos slash

### 3. **Camada de Dados** (`dados/`)

#### **Responsabilidades:**
- ✅ Gerenciar conexão com SQLite
- ✅ Criar e manter estrutura do banco
- ✅ Fornecer interface de acesso aos dados

#### **Componentes:**
- **`database.py`**: Contexto e configuração do banco
- **`stem_bot.db`**: Arquivo do banco SQLite

### 4. **Aplicação Principal** (`bot.py`)

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
- **Services**: Apenas lógica de negócio
- **Database**: Apenas persistência de dados

### **2. Manutenibilidade**
- Mudanças no banco não afetam comandos
- Queries centralizadas nos services
- Fácil localizar e corrigir problemas

### **3. Testabilidade**
- Services podem ser testados isoladamente
- Mocks podem substituir banco de dados
- Comandos testáveis independentemente

### **4. Escalabilidade**
- Fácil adicionar novos Cogs
- Services reutilizáveis entre Cogs
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