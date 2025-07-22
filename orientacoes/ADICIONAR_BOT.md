# 🔗 Adicionar Bot ao Servidor

## 📋 Link de Convite

### **Como Gerar o Link:**

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

## 🚀 Como Adicionar

### **1. Usar o Link de Convite**
1. **Copie o link acima**
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
- **Canal de Boas-vindas**: ID configurável (veja configuração)
- **Canal de Saídas**: ID configurável (veja configuração)
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

## 🔧 Configuração de Canais

### **Canais Específicos do Bot:**

#### **1. Canal de Boas-vindas**
- **ID**: Configurável no código
- **Função**: Mensagens de boas-vindas para novos membros
- **Permissões**: Bot deve poder enviar mensagens

#### **2. Canal de Saídas**
- **ID**: Configurável no código
- **Função**: Logs de saída para moderação
- **Permissões**: Bot deve poder enviar mensagens

### **Como Configurar IDs de Canais:**

#### **Para Desenvolvedores:**
1. Ative o **Modo Desenvolvedor** no Discord
2. Clique com botão direito no canal
3. Selecione **"Copiar ID"**
4. Atualize o ID no código

## 🚨 Solução de Problemas

### **Se o bot não responde:**
1. Verifique se está online
2. Verifique permissões no canal
3. Use `/sync` para sincronizar comandos
4. Consulte [SOLUCAO_PROBLEMAS.md](SOLUCAO_PROBLEMAS.md)

### **Se comandos slash não aparecem:**
1. Aguarde até 1 hora para sincronização global
2. Use `/sync` para sincronização imediata
3. Verifique permissão "Use Application Commands"
4. Verifique permissão "Manage Server" (obrigatória para sincronizar)

## 📞 Suporte

Para problemas específicos, consulte:
- [SOLUCAO_PROBLEMAS.md](SOLUCAO_PROBLEMAS.md)
- [CONFIGURACAO.md](CONFIGURACAO.md)

Bot adicionado com sucesso! 🎉 