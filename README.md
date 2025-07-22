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
- `/addevento_unico` - Adicionar evento único
- `/addrecorrente` - Adicionar evento recorrente
- `/eventos` - Listar eventos da semana
- `/modeventos` - Listar todos os eventos (admin)
- `/alterarevento` - Alterar evento (admin)
- `/concluirevento` - Marcar evento como concluído (admin)
- `/limpar_duplicatas` - Remover eventos duplicados (admin)

### **Administração:**
- `/welcome` - Testar mensagem de boas-vindas
- `/sync` - Sincronizar comandos (admin)
- `/ping` - Testar latência do bot
- `/help` - Mostrar todos os comandos

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação na pasta `orientacoes/`.
