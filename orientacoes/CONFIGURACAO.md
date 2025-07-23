# ⚙️ Configuração Inicial

## 📋 Pré-requisitos

### **1. Python 3.8+**
```bash
python --version
```

### **2. Conta Discord Developer**
- Acesse [Discord Developer Portal](https://discord.com/developers/applications)
- Crie uma nova aplicação
- Configure o bot

### **3. Servidor Discord**
- Servidor onde o bot será adicionado
- Permissões de administrador para configurar

## 🔧 Configuração do Bot

### **1. Criar Aplicação no Discord**

#### **Passos:**
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em **"New Application"**
3. Digite o nome: **"Stem-bot"**
4. Clique em **"Create"**

### **2. Configurar o Bot**

#### **Passos:**
1. No menu lateral, clique em **"Bot"**
2. Clique em **"Add Bot"**
3. Configure as seguintes opções:

#### **Privileged Gateway Intents:**
- ✅ **Presence Intent**
- ✅ **Server Members Intent**
- ✅ **Message Content Intent**

#### **Bot Permissions:**
- ✅ **Administrator** (para desenvolvimento)
- ✅ **Manage Server** (OBRIGATÓRIO para sincronizar comandos)
- ✅ **Use Application Commands** (OBRIGATÓRIO para comandos slash)
- ✅ **Send Messages**
- ✅ **View Channels**
- ✅ **Read Message History**

### **3. Obter Token**

#### **Passos:**
1. Na seção **"Bot"**, clique em **"Reset Token"**
2. Copie o token gerado
3. **⚠️ Mantenha este token seguro!**

### **4. Configurar Arquivo .env**

#### **Criar arquivo `.env` na raiz do projeto:**
```env
TOKEN=seu_token_aqui
```

#### **⚠️ IMPORTANTE - Segurança:**
- **NUNCA** compartilhe seu token
- **NUNCA** commite o arquivo `.env` no Git
- **NUNCA** compartilhe links específicos do seu bot
- Mantenha essas informações privadas

## 🚀 Configuração do Projeto

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Verificar Estrutura**
```
stem-bot/
├── bot.py
├── .env                 # Seu token aqui
├── requirements.txt
├── cogs/
├── services/
└── dados/
```

### **3. Executar Bot**
```bash
python bot.py
```

## ✅ Verificação da Configuração

### **Logs Esperados:**
```
2025-07-21 15:00:00 INFO     discord.client logging in using static token
2025-07-21 15:00:01 INFO     discord.gateway Shard ID None has connected to Gateway
Stem-bot#7776 está online!
ID do bot: SEU_BOT_ID
Conectado a 1 servidor(es)
Banco de dados configurado: dados\stem_bot.db
Cog Events carregado e comandos registrados!
Cog carregado: events
Cog Welcome carregado e comandos registrados!
Cog carregado: welcome
Sincronizados 10 comandos slash globalmente
📋 Sincronizando comandos nos servidores:
  - Servidor: [Nome do Servidor] (ID: [ID])
    ✅ Sincronizados 10 comandos
```

### **⚠️ Logs de Problema (Permissões):**
```
📋 Sincronizando comandos nos servidores:
  - Servidor: [Nome] (ID: [ID])
    ⚠️  Bot sem permissão 'Manage Server' em [Nome]
```
**Solução:** Ative a permissão "Manage Server" nas configurações do servidor.

## 🔗 Adicionar Bot ao Servidor

### **Como Gerar o Link de Convite:**

#### **1. Acesse o Discord Developer Portal:**
- Vá para [Discord Developer Portal](https://discord.com/developers/applications)
- Selecione sua aplicação

#### **2. Configure OAuth2:**
- Vá para **OAuth2** > **URL Generator**
- Selecione os escopos:
  - ✅ **bot**
  - ✅ **applications.commands**

#### **3. Configure Permissões:**
- **Manage Server** (Gerenciar Servidor) - OBRIGATÓRIO
- **Use Application Commands** (Usar Comandos de Aplicação) - OBRIGATÓRIO
- **Send Messages** (Enviar Mensagens)
- **View Channels** (Ver Canais)
- **Read Message History** (Ler Histórico)
- **Manage Messages** (Gerenciar Mensagens)
- **Embed Links** (Incorporar Links)

#### **4. Copie o Link Gerado:**
O Discord gerará automaticamente um link como:
```
https://discord.com/oauth2/authorize?client_id=SEU_BOT_ID&permissions=PERMISSOES&scope=bot+applications.commands
```

### **Permissões Incluídas:**
- ✅ **Administrador** (permissions=8)
- ✅ **Bot** (scope=bot)
- ✅ **Comandos de Aplicação** (scope=applications.commands)

## 🚀 Como Adicionar o Bot

### **1. Usar o Link de Convite**
1. **Copie o link gerado acima**
2. **Cole no navegador**
3. **Selecione o servidor** onde quer adicionar o bot
4. **Autorize o bot**

### **2. Verificar Permissões**
Após adicionar, verifique se o bot tem as permissões necessárias:

#### **Permissões Essenciais:**
- ✅ **Manage Server** (OBRIGATÓRIO para sincronizar comandos)
- ✅ **Use Application Commands** (OBRIGATÓRIO para comandos slash)
- ✅ **Send Messages** (para responder comandos)
- ✅ **View Channels** (para acessar canais)
- ✅ **Read Message History** (para ler histórico)
- ✅ **Manage Messages** (para moderação)

### **3. Configurar Canais**
Configure os canais específicos para o bot:

#### **Canais Necessários:**
- **Canal de Boas-vindas**: ID configurável (veja [CONFIGURAR_CANAIS.md](CONFIGURAR_CANAIS.md))
- **Canal de Saídas**: ID configurável (veja [CONFIGURAR_CANAIS.md](CONFIGURAR_CANAIS.md))
- **Canal de Comandos**: Qualquer canal onde o bot tenha permissões

## ⚠️ Importante

### **Se o bot já está no servidor:**
1. **Remova o bot** do servidor
2. **Use o link acima** para adicionar novamente
3. **Isso garantirá** que o bot tenha todas as permissões necessárias

### **Após adicionar o bot:**
1. **Execute**: `python bot.py`
2. **Aguarde** a sincronização dos comandos
3. **Teste**: `/ping`

## 🎯 Resultado Esperado

Após usar o link correto, o bot deve:
- ✅ Responder a comandos slash (`/ping`)
- ✅ Não mostrar mais "Integração desconhecida"
- ✅ Aparecer online no servidor

## 🔗 Próximos Passos

1. **Configurar Canais**: Veja [CONFIGURAR_CANAIS.md](CONFIGURAR_CANAIS.md)
2. **Testar Comandos**: Veja [SOLUCAO_PROBLEMAS.md](SOLUCAO_PROBLEMAS.md)
3. **Desenvolver Novas Funcionalidades**: Veja [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md)

## ⚠️ Importante

- **Nunca compartilhe seu token**
- **Use permissões mínimas necessárias em produção**
- **Mantenha o bot atualizado**
- **Faça backup do banco de dados regularmente**

Configuração concluída! 🎉 