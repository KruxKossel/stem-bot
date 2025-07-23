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
- Mensagem "Sincronizados 0 comandos no servidor: [Nome]"

#### **Soluções:**

##### **A. Sincronização Automática**
O bot sincroniza automaticamente:
- **Globalmente** (pode demorar até 1 hora)
- **Por servidor** (mais rápido para desenvolvimento)

##### **B. Comando Manual de Sincronização**
Use `/sync` (apenas administradores) para forçar sincronização.

##### **C. Verificar Permissões do Bot**
**Permissões OBRIGATÓRIAS:**
- ✅ **Manage Server** (para sincronizar comandos)
- ✅ **Use Application Commands** (para usar comandos slash)
- ✅ **Send Messages** (para responder)
- ✅ **View Channels** (para acessar canais)

##### **D. Problema de Sincronização por Servidor**
Se aparecer "⚠️ Bot sem permissão 'Manage Server' em [Servidor]":
1. **Vá para Configurações do Servidor** > **Integrações** > **Stem-bot**
2. **Ative a permissão "Manage Server"**
3. **Ou remova o bot do servidor** se não for necessário
4. **Reinicie o bot** para tentar sincronizar novamente

##### **E. Verificar Logs de Sincronização**
O bot mostra informações detalhadas:
```
📋 Sincronizando comandos nos servidores:
  - Servidor: [Nome] (ID: [ID])
    ✅ Sincronizados X comandos
    ⚠️  Bot sem permissão 'Manage Server'
    ❌ Sem permissão para sincronizar
```

### **3. Comandos Slash (/) Não Funcionam**

#### **Sintomas:**
- Comandos `/ping`, `/eventos`, `/addevento_unico` não aparecem
- Bot não responde a comandos slash

#### **Soluções:**

##### **A. Verificar Permissões do Bot**
- **Usar Comandos de Aplicação**
- **Enviar Mensagens**
- **Ver Canais**

##### **B. Sincronizar Comandos**
- Use `/sync` (apenas administradores)
- Aguarde até 1 hora para sincronização global

##### **C. Verificar Canal**
- Bot deve ter permissões no canal específico
- Teste em diferentes canais

### **4. Problema com Sincronização de Comandos (`/sync`)**

#### **Sintomas:**
- Comando `/sync` não funciona como esperado
- Comandos não aparecem imediatamente após sincronização
- Novos parâmetros não são reconhecidos
- Novas choices não são atualizadas

#### **Causas:**
- **Limitações da API do Discord**: Sincronização global pode demorar até 1 hora
- **Rate Limiting**: Discord limita quantas sincronizações podem ser feitas
- **Cache do Discord**: Comandos podem ficar em cache por até 1 hora
- **Permissões**: Bot precisa de permissão "Manage Server"

#### **Soluções:**

##### **A. Remover e Adicionar Bot Novamente (Mais Confiável)**
```bash
# 1. Remover o bot do servidor
# 2. Aguardar 5-10 minutos
# 3. Adicionar o bot novamente com as mesmas permissões
# 4. Executar /sync
```

**Vantagens:**
- ✅ Força atualização completa
- ✅ Resolve problemas de cache
- ✅ Garante sincronização imediata

**Desvantagens:**
- ❌ Perde configurações do servidor
- ❌ Pode perder permissões personalizadas
- ❌ Processo demorado

##### **B. Aguardar Propagação Natural**
```bash
# 1. Executar /sync
# 2. Aguardar até 1 hora
# 3. Comandos aparecerão automaticamente
```

**Vantagens:**
- ✅ Não perde configurações
- ✅ Processo automático
- ✅ Sem intervenção manual

**Desvantagens:**
- ❌ Pode demorar muito
- ❌ Não garante sincronização
- ❌ Pode falhar silenciosamente

##### **C. Comando `/sync` Melhorado**
O comando agora fornece informações detalhadas:

```
🔄 Sincronizando Comandos
Iniciando sincronização...

📡 Sincronização Local
Sincronizando comandos no servidor atual...

✅ Servidor Atual
Sincronizados 8 comandos no servidor!

🌐 Sincronização Global
Sincronizando comandos globalmente...

✅ Global
Sincronizados 8 comandos globalmente!

ℹ️ Informações Importantes
• Sincronização local: Imediata
• Sincronização global: Pode demorar até 1 hora
• Novos comandos: Pode ser necessário remover e adicionar o bot novamente
```

#### **Erros Comuns do `/sync`:**

##### **Erro de Permissão:**
```
❌ Erro de Permissão
O bot não tem permissão para sincronizar comandos neste servidor.

🔧 Solução
• Verifique se o bot tem permissão 'Manage Server'
• Tente remover e adicionar o bot novamente
```

##### **Erro HTTP:**
```
❌ Erro HTTP
Erro ao sincronizar comandos: 429 Too Many Requests

🔧 Possíveis Soluções
• Aguarde alguns minutos e tente novamente
• Remova e adicione o bot novamente
• Verifique se há muitos comandos (máximo 100)
```

#### **Recomendações:**
- **Para Desenvolvimento**: Use sincronização local, teste em servidor de desenvolvimento
- **Para Produção**: Planeje atualizações com antecedência, monitore logs
- **Para Novos Comandos**: Desenvolva completamente, execute `/sync`, aguarde até 1 hora

### **5. Bot Não Inicia**

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

#### **Comandos Slash Disponíveis:**
```
/ping
/addevento
/eventos
/help
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