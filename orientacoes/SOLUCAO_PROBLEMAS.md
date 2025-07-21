# 🚨 Solução de Problemas

## 📋 Problemas Comuns

### **1. "Integração Desconhecida"**

#### **Sintomas:**
- Bot responde "Integração desconhecida" para todos os comandos
- Comandos slash não funcionam

#### **Soluções:**

##### **A. Verificar Discord Developer Portal**
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione seu bot "Stem-bot"
3. Vá para **Bot** > **Privileged Gateway Intents**
4. **Ative TODOS os intents:**
   - ✅ **Presence Intent**
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent**

##### **B. Reinvitar o Bot**
Use o link correto do seu bot:
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione sua aplicação
3. Vá para **OAuth2** > **URL Generator**
4. Configure permissões e escopos
5. Use o link gerado automaticamente

##### **C. Verificar Token**
- Confirme que o arquivo `.env` existe
- Verifique se o token está correto
- Nunca compartilhe o token

### **2. Comandos Slash Não Aparecem**

#### **Sintomas:**
- Comandos `/` não aparecem ao digitar
- Bot não responde a comandos slash

#### **Soluções:**

##### **A. Sincronização Automática**
O bot sincroniza automaticamente:
- **Globalmente** (pode demorar até 1 hora)
- **Por servidor** (mais rápido para desenvolvimento)

##### **B. Comando Manual de Sincronização**
Use `/sync` (apenas administradores) para forçar sincronização.

##### **C. Verificar Permissões**
- **Usar Comandos de Aplicação** deve estar ativo
- Bot deve ter permissões no canal

### **3. Comandos de Prefixo (!) Não Funcionam**

#### **Sintomas:**
- Comandos `!ping`, `!eventos` não respondem
- Bot não reage a mensagens

#### **Soluções:**

##### **A. Verificar Permissões do Bot**
- **Enviar Mensagens**
- **Ler Histórico de Mensagens**
- **Ver Canais**

##### **B. Verificar Intents**
- **Message Content Intent** deve estar ativo
- Reinicie o bot após alterações

##### **C. Verificar Canal**
- Bot deve ter permissões no canal específico
- Teste em diferentes canais

### **4. Bot Não Inicia**

#### **Sintomas:**
- Erro ao executar `python bot.py`
- Bot não conecta ao Discord

#### **Soluções:**

##### **A. Verificar Dependências**
```bash
pip install -r requirements.txt
```

##### **B. Verificar Token**
- Arquivo `.env` existe?
- Token está correto?
- Token não expirou?

##### **C. Verificar Python**
```bash
python --version  # Deve ser 3.8+
```

## 🔍 Diagnóstico

### **Logs de Erro Comuns:**

#### **Token Inválido:**
```
discord.errors.LoginFailure: 401 Unauthorized (error code: 0): 401: Unauthorized
```
**Solução:** Verificar token no arquivo `.env`

#### **Intents Não Configurados:**
```
discord.errors.ClientException: Intents.message_content is not enabled.
```
**Solução:** Ativar Message Content Intent no Developer Portal

#### **Permissões Insuficientes:**
```
discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions
```
**Solução:** Verificar permissões do bot no servidor

### **Comandos para Testar:**

#### **Comandos de Prefixo:**
```
!ping
!addevento "Teste" 25/12/2024 14:00
!eventos
```

#### **Comandos Slash:**
```
/ping
/addevento
/eventos
/welcome
/sync
```

## ⚙️ Verificação de Configuração

### **Checklist Completo:**

#### **1. Discord Developer Portal:**
- ✅ Aplicação criada
- ✅ Bot adicionado
- ✅ Todos os intents ativos
- ✅ Token copiado

#### **2. Arquivo .env:**
- ✅ Arquivo existe
- ✅ Token correto
- ✅ Formato: `TOKEN=seu_token_aqui`

#### **3. Permissões do Bot:**
- ✅ Administrador (desenvolvimento)
- ✅ Enviar Mensagens
- ✅ Usar Comandos de Aplicação
- ✅ Ler Histórico de Mensagens

#### **4. Canais:**
- ✅ IDs configurados corretamente
- ✅ Bot tem permissões nos canais
- ✅ Canais existem no servidor

#### **5. Dependências:**
- ✅ Python 3.8+
- ✅ discord.py instalado
- ✅ Todas as dependências instaladas

## 🚀 Logs Esperados

### **Inicialização Bem-sucedida:**
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
Sincronizados 6 comandos slash globalmente
```

## 📞 Suporte Adicional

### **Se nada funcionar:**
1. **Remova o bot** do servidor
2. **Reinicie o bot** completamente
3. **Adicione novamente** usando o link correto
4. **Verifique logs** de erro detalhados

### **Recursos Úteis:**
- [CONFIGURACAO.md](CONFIGURACAO.md) - Configuração inicial
- [ADICIONAR_BOT.md](ADICIONAR_BOT.md) - Como adicionar o bot
- [ARQUITETURA.md](ARQUITETURA.md) - Entender a estrutura

Problemas resolvidos! 🎉 