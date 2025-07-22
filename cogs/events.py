import discord
from discord.ext import commands, tasks
from services import event_handlers
from services import event_scheduler
from services import event_choices
from services import events_service

class Events(commands.Cog):
    """Cog para gerenciar eventos do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
        # Verificar se a tarefa já está rodando antes de iniciar
        if not self.recurring_event_updater.is_running():
            self.recurring_event_updater.start()
    
    def cog_unload(self):
        """Para a tarefa quando o cog é descarregado"""
        self.recurring_event_updater.cancel()
    
    @tasks.loop(hours=1)  # Executar a cada hora
    async def recurring_event_updater(self):
        """Atualiza eventos recorrentes que já passaram"""
        print("Verificando eventos recorrentes vencidos...")
        result = event_scheduler.EventScheduler.update_recurring_events()
        if result['success']:
            print(result['message'])
        else:
            print(f"Erro: {result['error']}")
    
    @recurring_event_updater.before_loop
    async def before_recurring_event_updater(self):
        """Aguarda o bot estar pronto antes de iniciar a tarefa"""
        await self.bot.wait_until_ready()
    
    @discord.app_commands.command(name="addevento_unico", description="Adiciona um novo evento único (apenas administradores)")
    @discord.app_commands.describe(
        nome="Nome do evento",
        data="Data do evento (DD/MM/YYYY)",
        hora="Hora do evento (HH:MM)",
        link="Link do evento (opcional)"
    )
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def addevento_unico(self, interaction: discord.Interaction, nome: str, data: str, hora: str, link: str = None):
        """Adiciona um novo evento único ao calendário (apenas administradores)"""
        success, embed = await event_handlers.EventHandlers.handle_add_unique_event(
            interaction, nome, data, hora, link
        )
        await interaction.response.send_message(embed=embed, ephemeral=not success)
    
    @addevento_unico.error
    async def addevento_unico_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando addevento_unico"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="addrecorrente", description="Adiciona um novo evento recorrente (apenas administradores)")
    @discord.app_commands.describe(
        nome="Nome do evento",
        data_inicio="Data de início (DD/MM/YYYY)",
        hora="Hora do evento (HH:MM)",
        frequencia="Frequência do evento",
        detalhes="Detalhes da recorrência (opcional)",
        link="Link do evento (opcional)"
    )
    @discord.app_commands.choices(frequencia=event_choices.FREQUENCY_CHOICES)
    @discord.app_commands.choices(detalhes=event_choices.DETAILS_CHOICES)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def addrecorrente(self, interaction: discord.Interaction, nome: str, data_inicio: str, hora: str, 
                          frequencia: discord.app_commands.Choice[str], detalhes: discord.app_commands.Choice[str] = None, link: str = None):
        """Adiciona um novo evento recorrente ao calendário (apenas administradores)"""
        success, embed = await event_handlers.EventHandlers.handle_add_recurring_event(
            interaction, nome, data_inicio, hora, frequencia, detalhes, link
        )
        await interaction.response.send_message(embed=embed, ephemeral=not success)
    
    @addrecorrente.error
    async def addrecorrente_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando addrecorrente"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="alterarevento", description="Altera detalhes de um evento (apenas administradores)")
    @discord.app_commands.describe(
        id_evento="ID do evento a ser alterado",
        nome="Novo nome do evento (opcional)",
        data="Nova data (DD/MM/YYYY) (opcional)",
        hora="Nova hora (HH:MM) (opcional)",
        frequencia="Nova frequência (opcional)",
        detalhes="Novos detalhes (opcional)",
        link="Novo link (opcional)",
        status="Novo status (opcional)"
    )
    @discord.app_commands.choices(frequencia=event_choices.FREQUENCY_CHOICES)
    @discord.app_commands.choices(detalhes=event_choices.DETAILS_CHOICES)
    @discord.app_commands.choices(status=event_choices.STATUS_CHOICES)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def alterarevento(self, interaction: discord.Interaction, id_evento: int, 
                          nome: str = None, data: str = None, hora: str = None, 
                          link: str = None, frequencia: discord.app_commands.Choice[str] = None, 
                          detalhes: discord.app_commands.Choice[str] = None, status: discord.app_commands.Choice[str] = None):
        """Altera detalhes de um evento (apenas administradores)"""
        success, embed = await event_handlers.EventHandlers.handle_alter_event(
            interaction, id_evento, 
            name=nome, date=data, time=hora, link=link, 
            frequency=frequencia, recurrence_details=detalhes, status=status
        )
        await interaction.response.send_message(embed=embed, ephemeral=not success)
    
    @alterarevento.error
    async def alterarevento_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando alterarevento"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="eventos", description="Lista eventos ativos e futuros para usuários")
    async def eventos(self, interaction: discord.Interaction):
        """Lista eventos ativos e futuros para usuários"""
        success, embed = await event_handlers.EventHandlers.handle_list_user_events(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=not success)
    
    @discord.app_commands.command(name="modeventos", description="Lista todos os eventos para moderação (apenas administradores)")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def modeventos(self, interaction: discord.Interaction):
        """Lista todos os eventos para moderação (apenas administradores)"""
        success, embed = await event_handlers.EventHandlers.handle_list_mod_events(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @modeventos.error
    async def modeventos_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando modeventos"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="concluirevento", description="Marca um evento como concluído (apenas administradores)")
    @discord.app_commands.describe(
        id_evento="ID do evento a ser concluído"
    )
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def concluirevento(self, interaction: discord.Interaction, id_evento: int):
        """Marca um evento como concluído (apenas administradores)"""
        success, embed = await event_handlers.EventHandlers.handle_complete_event(interaction, id_evento)
        await interaction.response.send_message(embed=embed, ephemeral=not success)
    
    @concluirevento.error
    async def concluirevento_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando concluirevento"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="limpar_duplicatas", description="Remove eventos duplicados do banco de dados (apenas administradores)")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def limpar_duplicatas(self, interaction: discord.Interaction):
        """Remove eventos duplicados do banco de dados (apenas administradores)"""
        try:
            result = events_service.EventsService.check_and_remove_duplicates()
            
            if result['success']:
                embed = discord.Embed(
                    title="🧹 Limpeza de Duplicatas",
                    description=result['message'],
                    color=discord.Color.green()
                )
                if result['removed'] > 0:
                    embed.add_field(
                        name="📊 Estatísticas",
                        value=f"**Encontrados:** {result['duplicates_found']} grupos de duplicatas\n**Removidos:** {result['removed']} eventos",
                        inline=False
                    )
            else:
                embed = discord.Embed(
                    title="❌ Erro na Limpeza",
                    description=result['message'],
                    color=discord.Color.red()
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Erro ao limpar duplicatas: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @limpar_duplicatas.error
    async def limpar_duplicatas_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando limpar_duplicatas"""
        embed = await event_handlers.EventHandlers.handle_permission_error(interaction, error)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Função necessária para carregar o Cog"""
    await bot.add_cog(Events(bot))
    print("Cog Events carregado e comandos registrados!") 