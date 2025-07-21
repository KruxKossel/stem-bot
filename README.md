# 🤖 Bot STEM-GIRL

Bot Discord para a comunidade STEM-GIRL com sistema de eventos e boas-vindas.

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
├── 📁 cogs/           # Comandos do bot
├── 📁 services/       # Lógica de negócio
├── 📁 dados/          # Banco de dados
├── 📁 orientacoes/    # Documentação
├── bot.py             # Arquivo principal
└── requirements.txt   # Dependências
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
- [🔗 Adicionar Bot ao Servidor](orientacoes/ADICIONAR_BOT.md)
- [🔧 Configurar Canais](orientacoes/CONFIGURAR_CANAIS.md)
- [🚨 Solução de Problemas](orientacoes/SOLUCAO_PROBLEMAS.md)
- [🛡️ Guia de Segurança](orientacoes/SEGURANCA.md)

## 🎯 Comandos Disponíveis

### **Eventos:**
- `/addevento` - Adicionar novo evento
- `/eventos` - Listar eventos da semana

### **Administração:**
- `/welcome` - Testar mensagem de boas-vindas
- `/sync` - Sincronizar comandos (admin)

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação na pasta `orientacoes/`.
