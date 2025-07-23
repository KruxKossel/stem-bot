import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from dados import database
from logging_config import setup_logging, get_logger

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging estruturado
setup_logging()
logger = get_logger(__name__)

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
        logger.warning(f"Pasta {cogs_dir} não encontrada. Criando...")
        os.makedirs(cogs_dir)
        return
    
    # Lista de arquivos que são Cogs (não services)
    cog_files = ['events', 'welcome']
    
    for cog_name in cog_files:
        try:
            await bot.load_extension(f'cogs.{cog_name}')
            logger.info(f"Cog carregado: {cog_name}")
        except Exception as e:
            logger.error(f"Erro ao carregar cog {cog_name}: {e}")

@bot.event
async def on_ready():
    """Evento executado quando o bot está pronto"""
    logger.info(f"{bot.user} está online!")
    logger.info(f"ID do bot: {bot.user.id}")
    logger.info(f"Conectado a {len(bot.guilds)} servidor(es)")
    
    # Configurar banco de dados
    try:
        setup_database()
    except Exception as e:
        logger.error(f"Erro ao configurar banco de dados: {e}")
        return
    
    # Carregar Cogs
    await load_cogs()
    
    # Sincronizar comandos slash
    try:
        # Sincronizar globalmente (pode demorar até 1 hora para aparecer)
        synced = await bot.tree.sync()
        logger.info(f"Sincronizados {len(synced)} comandos slash globalmente")
        
        # Para desenvolvimento, também sincronizar por servidor (mais rápido)
        logger.info("📋 Sincronizando comandos nos servidores:")
        for guild in bot.guilds:
            logger.info(f"  - Servidor: {guild.name} (ID: {guild.id})")
            try:
                # Verificar se o bot tem permissões no servidor
                if not guild.me.guild_permissions.manage_guild:
                    logger.warning(f"    ⚠️  Bot sem permissão 'Manage Server' em {guild.name}")
                    continue
                
                synced_guild = await bot.tree.sync(guild=guild)
                logger.info(f"    ✅ Sincronizados {len(synced_guild)} comandos")
                
            except discord.Forbidden:
                logger.error(f"    ❌ Sem permissão para sincronizar em {guild.name}")
            except discord.HTTPException as e:
                logger.error(f"    ❌ Erro HTTP ao sincronizar em {guild.name}: {e}")
            except Exception as e:
                logger.error(f"    ❌ Erro ao sincronizar em {guild.name}: {e}")
                
    except Exception as e:
        logger.error(f"Erro ao sincronizar comandos slash: {e}")

@bot.tree.command(name="ping", description="Testa a latência do bot")
async def ping_slash(interaction: discord.Interaction):
    """Comando slash para testar latência"""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'🏓 Pong! Latência: {latency}ms')

@bot.tree.command(name="help", description="Mostra todos os comandos disponíveis")
async def help_slash(interaction: discord.Interaction):
    """Comando slash para mostrar ajuda"""
    embed = discord.Embed(
        title="🤖 Comandos do STEM GIRL Bot",
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
        value="`/addevento` - Adicionar evento (único ou recorrente) com seleção de frequência\n`/alterarevento` - Alterar detalhes de evento (com seleção de frequência, detalhes e status)\n`/modeventos` - Listar eventos com filtros\n`/concluirevento` - Marcar evento como concluído",
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
        embed = discord.Embed(
            title="🔄 Sincronizando Comandos",
            description="Iniciando sincronização...",
            color=discord.Color.blue()
        )
        
        # Primeiro, sincronizar apenas no servidor atual (mais rápido)
        embed.add_field(
            name="📡 Sincronização Local",
            value="Sincronizando comandos no servidor atual...",
            inline=False
        )
        
        synced_guild = await bot.tree.sync(guild=interaction.guild)
        
        embed.add_field(
            name="✅ Servidor Atual",
            value=f"Sincronizados **{len(synced_guild)}** comandos no servidor!",
            inline=False
        )
        
        # Tentar sincronização global (pode demorar até 1 hora para propagar)
        embed.add_field(
            name="🌐 Sincronização Global",
            value="Sincronizando comandos globalmente...",
            inline=False
        )
        
        synced_global = await bot.tree.sync()
        
        embed.add_field(
            name="✅ Global",
            value=f"Sincronizados **{len(synced_global)}** comandos globalmente!",
            inline=False
        )
        
        # Atualizar título e cor
        embed.title = "✅ Sincronização Concluída"
        embed.color = discord.Color.green()
        
        # Informações importantes sobre sincronização
        embed.add_field(
            name="ℹ️ Informações Importantes",
            value="• **Sincronização local**: Imediata\n• **Sincronização global**: Pode demorar até 1 hora\n• **Novos comandos**: Pode ser necessário remover e adicionar o bot novamente",
            inline=False
        )
        
        # Listar comandos disponíveis
        commands_list = []
        for cmd in bot.tree.get_commands():
            commands_list.append(f"`/{cmd.name}` - {cmd.description}")
        
        if commands_list:
            embed.add_field(
                name="📋 Comandos Disponíveis",
                value="\n".join(commands_list[:10]),  # Limitar a 10 comandos
                inline=False
            )
            
            if len(commands_list) > 10:
                embed.add_field(
                    name="📋 ...",
                    value=f"E mais {len(commands_list) - 10} comandos",
                    inline=False
                )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ Erro de Permissão",
            description="O bot não tem permissão para sincronizar comandos neste servidor.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🔧 Solução",
            value="• Verifique se o bot tem permissão 'Manage Server'\n• Tente remover e adicionar o bot novamente",
            inline=False
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except discord.HTTPException as e:
        embed = discord.Embed(
            title="❌ Erro HTTP",
            description=f"Erro ao sincronizar comandos: {e}",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🔧 Possíveis Soluções",
            value="• Aguarde alguns minutos e tente novamente\n• Remova e adicione o bot novamente\n• Verifique se há muitos comandos (máximo 100)",
            inline=False
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Erro Inesperado",
            description=f"Erro ao sincronizar: {e}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

# Executar o bot
if __name__ == '__main__':
    token = os.getenv('TOKEN')
    if not token:
        print("Erro: TOKEN não encontrado no arquivo .env")
        exit(1)
    
    bot.run(token) 