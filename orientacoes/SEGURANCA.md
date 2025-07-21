# 🛡️ Guia de Segurança

## ⚠️ Informações Sensíveis

### **O que NUNCA compartilhar:**

#### **1. Token do Bot**
```env
# ❌ NUNCA faça isso:
TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.ABCDEF.GHIJKLMNOPQRSTUVWXYZabcdefghijklmnop
```

#### **2. Links Específicos do Bot**
```
# ❌ NUNCA compartilhe links como:
https://discord.com/oauth2/authorize?client_id=1234567890123456789&permissions=268511232&scope=bot+applications.commands
```

#### **3. IDs de Aplicação**
```
# ❌ NUNCA exponha IDs como:
Client ID: 1234567890123456789
```

## ✅ Como Compartilhar o Projeto

### **1. Para Desenvolvedores:**
- ✅ Compartilhe apenas o **código fonte**
- ✅ Use **variáveis de ambiente** para tokens
- ✅ Documente como **gerar links próprios**
- ✅ Mantenha `.env` no `.gitignore`

### **2. Para Administradores:**
- ✅ Forneça **instruções** para criar bot próprio
- ✅ Explique como **configurar permissões**
- ✅ Documente **processo de setup**

## 🔧 Configuração Segura

### **1. Arquivo .env**
```env
# ✅ Formato correto (sem token real):
TOKEN=seu_token_aqui
```

### **2. .gitignore**
```gitignore
# ✅ Sempre incluir:
.env
*.db
__pycache__/
```

### **3. Documentação Genérica**
```markdown
# ✅ Exemplo correto:
1. Acesse Discord Developer Portal
2. Crie sua aplicação
3. Configure OAuth2
4. Gere seu próprio link
```

## 🚨 Riscos de Segurança

### **1. Token Comprometido:**
- **Risco**: Bot pode ser controlado por terceiros
- **Solução**: Resetar token imediatamente
- **Prevenção**: Nunca compartilhar

### **2. Links Específicos:**
- **Risco**: Outros podem adicionar seu bot
- **Solução**: Gerar novos links
- **Prevenção**: Usar links genéricos

### **3. IDs Expostos:**
- **Risco**: Informações podem ser usadas maliciosamente
- **Solução**: Não é crítico, mas evite
- **Prevenção**: Usar IDs genéricos na documentação

## 📋 Checklist de Segurança

### **Antes de Compartilhar:**
- [ ] **Token removido** de todos os arquivos
- [ ] **Links específicos** substituídos por instruções
- [ ] **IDs reais** substituídos por placeholders
- [ ] **Arquivo .env** no .gitignore
- [ ] **Documentação** genérica e segura

### **Para Novos Desenvolvedores:**
- [ ] **Criar própria aplicação** no Discord
- [ ] **Gerar próprio token**
- [ ] **Configurar próprias permissões**
- [ ] **Usar próprio link de convite**

## 🎯 Boas Práticas

### **1. Desenvolvimento:**
```python
# ✅ Usar variáveis de ambiente
import os
TOKEN = os.getenv('TOKEN')
```

### **2. Documentação:**
```markdown
# ✅ Instruções genéricas
1. Configure seu próprio bot
2. Use seu próprio token
3. Gere seus próprios links
```

### **3. Compartilhamento:**
- ✅ **Código fonte** apenas
- ✅ **Instruções** de setup
- ✅ **Documentação** genérica
- ✅ **Exemplos** sem dados reais

## 🔄 Processo de Setup Seguro

### **Para Novos Contribuidores:**
1. **Clone** o repositório
2. **Crie** aplicação no Discord Developer Portal
3. **Configure** OAuth2 e permissões
4. **Gere** seu próprio token
5. **Configure** arquivo `.env`
6. **Execute** o bot

### **Para Administradores:**
1. **Siga** instruções de configuração
2. **Use** permissões mínimas necessárias
3. **Monitore** logs de segurança
4. **Mantenha** tokens seguros

## 📞 Suporte de Segurança

### **Se Token for Comprometido:**
1. **Acesse** Discord Developer Portal
2. **Vá para** sua aplicação
3. **Clique em** "Reset Token"
4. **Atualize** arquivo `.env`
5. **Reinicie** o bot

### **Se Link for Comprometido:**
1. **Gere** novo link no OAuth2
2. **Remova** bot do servidor
3. **Adicione** com novo link
4. **Verifique** permissões

Segurança em primeiro lugar! 🛡️ 