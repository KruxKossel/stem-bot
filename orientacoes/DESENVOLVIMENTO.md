# 🔧 Guia de Desenvolvimento

## 📋 Visão Geral

Este guia é para desenvolvedores que querem contribuir ou estender o Bot STEM-GIRL.

## 🛠️ Ambiente de Desenvolvimento

### **1. Configuração Inicial**
```bash
# Clonar repositório
git clone <url-do-repositorio>
cd stem-bot

# Instalar dependências
pip install -r requirements.txt

# Configurar token (NUNCA compartilhe seu token real)
echo "TOKEN=seu_token_aqui" > .env
```

### **2. Estrutura do Projeto**
```
stem-bot/
├── 📁 cogs/           # Comandos do bot
├── 📁 services/       # Lógica de negócio
├── 📁 dados/          # Banco de dados
├── 📁 orientacoes/    # Documentação
├── bot.py             # Arquivo principal
└── requirements.txt   # Dependências
```

## 🚀 Como Adicionar Novas Funcionalidades

### **1. Adicionar Novo Cog**

#### **Estrutura Básica:**
```python
import discord
from discord.ext import commands

class NovoCog(commands.Cog):
    """Descrição do Cog"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def comando(self, ctx):
        """Descrição do comando"""
        await ctx.send("Resposta do comando")
    
    @discord.app_commands.command(name="comando", description="Descrição")
    async def comando_slash(self, interaction: discord.Interaction):
        """Comando slash"""
        await interaction.response.send_message("Resposta")

async def setup(bot):
    """Função necessária para carregar o Cog"""
    await bot.add_cog(NovoCog(bot))
    print("Cog NovoCog carregado!")
```

#### **Passos:**
1. Criar `cogs/novo_cog.py`
2. Implementar comandos
3. O bot carrega automaticamente

### **2. Adicionar Novo Service**

#### **Estrutura Básica:**
```python
from dados.database import DatabaseContext

class NovoService:
    """Service para operações específicas"""
    
    @staticmethod
    def operacao():
        """Descrição da operação"""
        conn = DatabaseContext.get_connection()
        try:
            cursor = conn.cursor()
            # Sua lógica aqui
            return resultado
        finally:
            conn.close()
```

#### **Passos:**
1. Criar `services/novo_service.py`
2. Implementar lógica de negócio
3. Importar no Cog correspondente

### **3. Adicionar Nova Tabela**

#### **No arquivo `dados/database.py`:**
```python
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela existente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            link TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Nova tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nova_tabela (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campo1 TEXT NOT NULL,
            campo2 INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
```

## 📝 Padrões de Código

### **1. Nomenclatura**
- **Cogs**: PascalCase (`Events`, `Welcome`)
- **Services**: PascalCase + Service (`EventsService`)
- **Funções**: snake_case (`add_event`, `get_events`)
- **Variáveis**: snake_case (`event_name`, `user_id`)

### **2. Documentação**
```python
def funcao_complexa(parametro1, parametro2):
    """
    Descrição detalhada da função.
    
    Args:
        parametro1 (str): Descrição do parâmetro
        parametro2 (int): Descrição do parâmetro
    
    Returns:
        bool: Descrição do retorno
    
    Raises:
        ValueError: Quando o parâmetro é inválido
    """
    pass
```

### **3. Tratamento de Erros**
```python
try:
    # Operação que pode falhar
    resultado = operacao_risco()
except ValueError as e:
    await ctx.send(f"❌ Erro de validação: {e}")
except Exception as e:
    await ctx.send(f"❌ Erro inesperado: {e}")
    print(f"Erro detalhado: {e}")
```

## 🧪 Testes

### **1. Testes Manuais**
```bash
# Executar bot
python bot.py

# Testar comandos
!ping
/addevento "Teste" 25/12/2024 14:00
/eventos
```

### **2. Testes de Service**
```python
# Em um script separado
from services.events_service import EventsService

# Testar adicionar evento
success = EventsService.add_event("Teste", "25/12/2024", "14:00", None, 123456)
print(f"Evento adicionado: {success}")

# Testar listar eventos
events = EventsService.get_events_of_the_week()
print(f"Eventos: {events}")
```

## 🔄 Fluxo de Desenvolvimento

### **1. Desenvolvimento Local**
1. **Criar branch** para nova funcionalidade
2. **Implementar** mudanças
3. **Testar** localmente
4. **Commit** com mensagem descritiva

### **2. Commit Messages**
```
feat: adicionar sistema de XP
fix: corrigir validação de data
docs: atualizar documentação
refactor: reorganizar estrutura de services
```

### **3. Pull Request**
- **Descrição clara** da mudança
- **Testes incluídos**
- **Documentação atualizada**

## 📊 Banco de Dados

### **1. Estrutura Atual**
```sql
-- Tabela de eventos
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    link TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **2. Migrações**
Para alterar estrutura do banco:
1. **Backup** do banco atual
2. **Criar script** de migração
3. **Testar** em ambiente de desenvolvimento
4. **Aplicar** em produção

## 🚨 Boas Práticas

### **1. Segurança**
- **NUNCA** commitar tokens ou arquivos `.env`
- **NUNCA** compartilhar links específicos do seu bot
- **NUNCA** expor IDs de aplicação ou tokens
- **Validar** entrada do usuário
- **Usar** permissões mínimas necessárias

### **2. Performance**
- **Fechar** conexões do banco
- **Limitar** queries desnecessárias
- **Usar** índices no banco

### **3. Manutenibilidade**
- **Comentar** código complexo
- **Separar** responsabilidades
- **Reutilizar** código comum

## 📚 Recursos Úteis

### **Documentação:**
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Documentation](https://docs.python.org/)

### **Ferramentas:**
- **Discord Developer Portal**: Configurar bot
- **SQLite Browser**: Visualizar banco
- **Git**: Controle de versão

## 🎯 Próximos Passos

### **Funcionalidades Planejadas:**
- [ ] Sistema de XP
- [ ] Sistema de ranks
- [ ] Missões semanais
- [ ] Quiz técnico
- [ ] Ferramentas de moderação

### **Como Contribuir:**
1. **Escolha** uma funcionalidade
2. **Crie** branch para desenvolvimento
3. **Implemente** seguindo padrões
4. **Teste** completamente
5. **Submeta** pull request

Boa sorte no desenvolvimento! 🚀 