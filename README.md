# 🤖 Bot STEM GIRL

Bot Discord para a comunidade STEM GIRL com sistema de eventos e boas-vindas.

## 🚀 Funcionalidades

- **📅 Sistema de Eventos**: Adicionar e listar eventos da semana
- **👋 Sistema de Boas-vindas**: Mensagens personalizadas para novos membros
- **📊 Logs de Saída**: Informações detalhadas para moderação
- **⚙️ Arquitetura Modular**: Código organizado e escalável

## 🛠️ Tecnologias

- **Python 3.8+**
- **Discord.py 2.0+**
- **SQLite** (banco de dados)
- **Arquitetura Modular** (Cogs + Services)

## 📁 Estrutura do Projeto

```
stem-bot/
├── 📁 cogs/           # Comandos e interface do usuário
├── 📁 services/       # Lógica de negócio e operações
├── 📁 components/     # Componentes reutilizáveis
├── 📁 dados/          # Camada de dados
├── 📁 orientacoes/    # Documentação
├── 📁 logs/           # Logs do sistema
├── bot.py             # Arquivo principal
├── logging_config.py  # Configuração de logs
├── requirements.txt   # Dependências
├── .env               # Variáveis de ambiente
├── Dockerfile         # Configuração Docker
└── docker-compose.yml # Orquestração Docker
```

## 🚀 Como Executar

### 1. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 2. **Configurar Token**
Crie um arquivo `.env` com:
```
TOKEN=seu_token_do_bot
```
### 3. **Executar o Bot**
```bash
python bot.py
```

## 📚 Documentação

### **Para Desenvolvedores:**
- [📋 Arquitetura do Projeto](orientacoes/ARQUITETURA.md)
- [🔧 Guia de Desenvolvimento](orientacoes/DESENVOLVIMENTO.md)

### **Para Administradores:**
- [⚙️ Configuração Inicial](orientacoes/CONFIGURACAO.md)
- [🔧 Configurar Canais](orientacoes/CONFIGURAR_CANAIS.md)
- [🚨 Solução de Problemas](orientacoes/SOLUCAO_PROBLEMAS.md)
- [🛡️ Guia de Segurança](orientacoes/SEGURANCA.md)
- [📅 Sistema de Eventos](orientacoes/EVENTOS.md)

## 🎯 Comandos Disponíveis

### **📅 Eventos (Usuários):**
- `/eventos` - Listar eventos ativos da semana atual

### **📅 Eventos (Administradores):**
- `/addevento` - Adicionar evento (único ou recorrente) com seleção de frequência
- `/alterarevento` - Alterar detalhes de evento (com seleção de frequência, detalhes e status)
- `/modeventos` - Listar eventos com filtros (ativos, concluídos, cancelados, etc.)
- `/concluirevento` - Marcar evento como concluído

### **🔧 Administração:**
- `/sync` - Sincronizar comandos (apenas administradores)
- `/ping` - Testar latência do bot
- `/help` - Mostrar todos os comandos

### **👋 Sistema de Boas-vindas:**
- **Automático**: Mensagens de boas-vindas para novos membros
- **Automático**: Logs de saída para moderação

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação na pasta `orientacoes/`.

