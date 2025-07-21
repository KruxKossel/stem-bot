import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from dados import database

# Carregar variáveis de ambiente
load_dotenv()

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Criar bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Configurar banco de dados
def setup_database():
    """Configura o banco de dados usando o contexto"""
    database.setup_database()

# Carregar Cogs
async def load_cogs():
    """Carrega todos os Cogs da pasta cogs"""
    cogs_dir = 'cogs'
    
    if not os.path.exists(cogs_dir):
        print(f"Pasta {cogs_dir} não encontrada. Criando...")
        os.makedirs(cogs_dir)
        return
    
    # Lista de arquivos que são Cogs (não services)
    cog_files = ['events', 'welcome']
    
    for cog_name in cog_files:
        try:
            await bot.load_extension(f'cogs.{cog_name}')
            print(f"Cog carregado: {cog_name}")
        except Exception as e:
            print(f"Erro ao carregar cog {cog_name}: {e}")

@bot.event
async def on_ready():
    """Evento executado quando o bot está pronto"""
    print(f'{bot.user} está online!')
    print(f'ID do bot: {bot.user.id}')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')
    
    # Configurar banco de dados
    setup_database()
    
    # Carregar Cogs
    await load_cogs()
    
    # Sincronizar comandos slash
    try:
        # Sincronizar globalmente (pode demorar até 1 hora para aparecer)
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos slash globalmente")
        
        # Para desenvolvimento, também sincronizar por servidor (mais rápido)
        for guild in bot.guilds:
            try:
                synced_guild = await bot.tree.sync(guild=guild)
                print(f"Sincronizados {len(synced_guild)} comandos no servidor: {guild.name}")
            except Exception as e:
                print(f"Erro ao sincronizar no servidor {guild.name}: {e}")
                
    except Exception as e:
        print(f"Erro ao sincronizar comandos slash: {e}")

@bot.command()
async def ping(ctx):
    """Comando de teste para verificar se o bot está funcionando"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latência: {latency}ms')

@bot.command()
async def test(ctx):
    """Comando de teste simples"""
    await ctx.send('✅ Bot está funcionando! Comandos de prefixo ativos.')

@bot.command()
async def help(ctx):
    """Comando de ajuda simples"""
    embed = discord.Embed(
        title="🤖 Comandos do STEM-GIRL Bot",
        description="Lista de comandos disponíveis:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📅 Eventos",
        value="`!addevento` - Adicionar evento\n`!eventos` - Listar eventos da semana",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Geral",
        value="`!ping` - Testar latência\n`!test` - Teste simples\n`!help` - Mostrar esta ajuda",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.tree.command(name="ping", description="Testa a latência do bot")
async def ping_slash(interaction: discord.Interaction):
    """Comando slash para testar latência"""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'🏓 Pong! Latência: {latency}ms')

@bot.tree.command(name="help", description="Mostra todos os comandos disponíveis")
async def help_slash(interaction: discord.Interaction):
    """Comando slash para mostrar ajuda"""
    embed = discord.Embed(
        title="🤖 Comandos do STEM-GIRL Bot",
        description="Lista de todos os comandos disponíveis:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📅 Eventos",
        value="`/addevento` - Adicionar evento\n`/eventos` - Listar eventos da semana",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Geral",
        value="`/ping` - Testar latência\n`/help` - Mostrar esta ajuda\n`/sync` - Sincronizar comandos (admin)",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Evento para tratar erros de comandos"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Comando não encontrado: `{ctx.message.content}`\nUse `!help` para ver comandos disponíveis.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    else:
        await ctx.send(f"❌ Erro: {error}")

@bot.tree.command(name="sync", description="Sincroniza os comandos slash (apenas administradores)")
async def sync_slash(interaction: discord.Interaction):
    """Comando para sincronizar comandos slash"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Você precisa ser administrador para usar este comando.", ephemeral=True)
        return
    
    try:
        # Recarregar Cogs
        await load_cogs()
        
        # Sincronizar comandos globalmente
        synced = await bot.tree.sync()
        
        # Sincronizar no servidor atual (mais rápido para desenvolvimento)
        synced_guild = await bot.tree.sync(guild=interaction.guild)
        
        embed = discord.Embed(
            title="✅ Comandos Sincronizados",
            description=f"Foram sincronizados **{len(synced)}** comandos globalmente e **{len(synced_guild)}** no servidor!",
            color=discord.Color.green()
        )
        
        # Listar comandos sincronizados
        commands_list = []
        for cmd in bot.tree.get_commands():
            commands_list.append(f"`/{cmd.name}` - {cmd.description}")
        
        if commands_list:
            embed.add_field(
                name="📋 Comandos Disponíveis",
                value="\n".join(commands_list),
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao sincronizar: {e}", ephemeral=True)

# Executar o bot
if __name__ == '__main__':
    token = os.getenv('TOKEN')
    if not token:
        print("Erro: TOKEN não encontrado no arquivo .env")
        exit(1)
    
    bot.run(token) 