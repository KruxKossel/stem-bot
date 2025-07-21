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
│   ├── events_service.py  # Operações de eventos
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
- ✅ Definir comandos do bot (prefixo e slash)
- ✅ Validar dados de entrada do usuário
- ✅ Construir respostas visuais (Embeds)
- ✅ Gerenciar interações com usuários

#### **Cogs Disponíveis:**
- **`events.py`**: Sistema de eventos (`/addevento`, `/eventos`)
- **`welcome.py`**: Sistema de boas-vindas e logs de saída

### 2. **Camada de Serviços** (`services/`)

#### **Responsabilidades:**
- ✅ Encapsular lógica de negócio
- ✅ Executar operações no banco de dados
- ✅ Fornecer interface para Cogs
- ✅ Centralizar queries SQL

#### **Services Disponíveis:**
- **`events_service.py`**: Operações de eventos (CRUD)

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
1. Usuário: /addevento "Workshop" 25/12/2024 14:00
2. Cog: Valida formato da data/hora
3. Service: Executa operação no banco
4. Database: Persiste dados no SQLite
5. Cog: Retorna embed de confirmação
```

### **Exemplo: Listar Eventos**
```
1. Usuário: /eventos
2. Cog: Chama service para buscar dados
3. Service: Executa query no banco
4. Database: Retorna lista de eventos
5. Cog: Formata dados em embed
6. Usuário: Recebe lista formatada
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
  - `created_at` (TIMESTAMP)

### **Próximas Tabelas Planejadas:**
- **`users`**: Informações dos usuários
- **`xp`**: Sistema de experiência
- **`missions`**: Missões semanais

Esta arquitetura torna o projeto profissional e fácil de manter! 🎉 