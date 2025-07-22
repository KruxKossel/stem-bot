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

# Criar bot (apenas slash commands, mas ainda precisa do prefixo para compatibilidade)
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
        print(f"\n📋 Sincronizando comandos nos servidores:")
        for guild in bot.guilds:
            print(f"  - Servidor: {guild.name} (ID: {guild.id})")
            try:
                # Verificar se o bot tem permissões no servidor
                if not guild.me.guild_permissions.manage_guild:
                    print(f"    ⚠️  Bot sem permissão 'Manage Server' em {guild.name}")
                    continue
                
                synced_guild = await bot.tree.sync(guild=guild)
                print(f"    ✅ Sincronizados {len(synced_guild)} comandos")
                
            except discord.Forbidden:
                print(f"    ❌ Sem permissão para sincronizar em {guild.name}")
            except discord.HTTPException as e:
                print(f"    ❌ Erro HTTP ao sincronizar em {guild.name}: {e}")
            except Exception as e:
                print(f"    ❌ Erro ao sincronizar em {guild.name}: {e}")
                
    except Exception as e:
        print(f"Erro ao sincronizar comandos slash: {e}")

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
        name="📅 Eventos (Usuários)",
        value="`/eventos` - Listar eventos ativos e futuros",
        inline=False
    )
    
    embed.add_field(
        name="📅 Eventos (Administradores)",
        value="`/addevento_unico` - Adicionar evento único\n`/addrecorrente` - Adicionar evento recorrente (com seleção de frequência e detalhes)\n`/alterarevento` - Alterar detalhes de evento (com seleção de frequência, detalhes e status)\n`/modeventos` - Listar todos os eventos\n`/concluirevento` - Marcar evento como concluído",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Geral",
        value="`/ping` - Testar latência\n`/help` - Mostrar esta ajuda\n`/sync` - Sincronizar comandos (admin)",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sync", description="Sincroniza os comandos slash (apenas administradores)")
async def sync_slash(interaction: discord.Interaction):
    """Comando para sincronizar comandos slash"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Você precisa ser administrador para usar este comando.", ephemeral=True)
        return
    
    # Responder imediatamente para evitar timeout
    await interaction.response.defer(ephemeral=True)
    
    try:
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
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Erro ao sincronizar: {e}", ephemeral=True)

# Executar o bot
if __name__ == '__main__':
    token = os.getenv('TOKEN')
    if not token:
        print("Erro: TOKEN não encontrado no arquivo .env")
        exit(1)
    
    bot.run(token) 