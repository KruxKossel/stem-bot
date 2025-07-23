import discord
from discord.ext import commands, tasks
import logging
from services import event_handlers
from services import event_scheduler
from services import event_choices
from services import events_service

# Configurar logging
logger = logging.getLogger(__name__)

class Events(commands.Cog):
    """Cog para gerenciar eventos do servidor"""
    
    # Variável de classe para controlar se a tarefa já está rodando
    _task_running = False
    
    def __init__(self, bot):
        self.bot = bot
        # Verificar se a tarefa já está rodando antes de iniciar
        if not Events._task_running and not self.recurring_event_updater.is_running():
            logger.info("Iniciando background task para eventos recorrentes")
            self.recurring_event_updater.start()
            Events._task_running = True
        else:
            logger.info("Background task já está em execução, pulando inicialização")
    
    def cog_unload(self):
        """Para a tarefa quando o cog é descarregado"""
        if self.recurring_event_updater.is_running():
            logger.info("Parando background task de eventos recorrentes")
            self.recurring_event_updater.cancel()
            Events._task_running = False
    
    @tasks.loop(hours=1)  # Executar a cada hora
    async def recurring_event_updater(self):
        """Atualiza eventos recorrentes que já passaram e auto-conclui eventos únicos"""
        logger.info("Executando verificação de eventos recorrentes vencidos...")
        result = event_scheduler.EventScheduler.update_recurring_events()
        if result['success']:
            logger.info(f"Verificação concluída: {result['message']}")
        else:
            logger.error(f"Erro na verificação: {result['error']}")
        
        # Auto-concluir eventos únicos vencidos
        logger.info("Executando verificação de eventos únicos para auto-conclusão...")
        auto_complete_result = event_scheduler.EventScheduler.auto_complete_unique_events()
        if auto_complete_result['success']:
            logger.info(f"Auto-conclusão concluída: {auto_complete_result['message']}")
        else:
            logger.error(f"Erro na auto-conclusão: {auto_complete_result['error']}")
    
    @recurring_event_updater.before_loop
    async def before_recurring_event_updater(self):
        """Aguarda o bot estar pronto antes de iniciar a tarefa"""
        await self.bot.wait_until_ready()
        logger.info("Bot pronto, background task iniciada")
    

    
    @discord.app_commands.command(name="addevento", description="Adiciona um novo evento (único ou recorrente) (apenas administradores)")
    @discord.app_commands.describe(
        nome="Nome do evento",
        data_inicio="Data de início (DD/MM/YYYY)",
        hora="Hora do evento (HH:MM)",
        frequencia="Frequência do evento (escolha 'Não se repete' para evento único)",
        detalhes="Detalhes da recorrência (opcional)",
        link="Link do evento (opcional)",
        auto_concluir="Auto-conclusão: 'Sim' para concluir automaticamente após o evento, 'Não' para manter ativo (apenas eventos únicos)",
        tempo_conclusao="Tempo de espera: 30min, 1h, 2h, 3h, 6h, 12h ou 24h após o evento para auto-conclusão (apenas eventos únicos)"
    )
    @discord.app_commands.choices(frequencia=event_choices.FREQUENCY_CHOICES)
    @discord.app_commands.choices(detalhes=event_choices.DETAILS_CHOICES)
    @discord.app_commands.choices(auto_concluir=event_choices.AUTO_COMPLETE_CHOICES)
    @discord.app_commands.choices(tempo_conclusao=event_choices.AUTO_COMPLETE_TIME_CHOICES)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def addevento(self, interaction: discord.Interaction, nome: str, data_inicio: str, hora: str, 
                          frequencia: discord.app_commands.Choice[str], detalhes: discord.app_commands.Choice[str] = None, 
                          link: str = None, auto_concluir: discord.app_commands.Choice[str] = None, 
                          tempo_conclusao: discord.app_commands.Choice[str] = None):
        """Adiciona um novo evento (único ou recorrente) ao calendário (apenas administradores)"""
        success, response = await event_handlers.EventHandlers.handle_add_recurring_event(
            interaction, nome, data_inicio, hora, frequencia, detalhes, link, auto_concluir, tempo_conclusao
        )
        
        # Verificar se é uma resposta especial (embed + view para seleção mensal)
        if not success and isinstance(response, tuple) and len(response) == 2:
            embed, view = response
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            # Resposta normal (embed apenas)
            await interaction.response.send_message(embed=response, ephemeral=not success)
    
    @addevento.error
    async def addevento_error(self, interaction: discord.Interaction, error):
        """Trata erros do comando addevento"""
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
    
    @discord.app_commands.command(name="modeventos", description="Lista eventos para moderação com filtros (apenas administradores)")
    @discord.app_commands.describe(
        filtro="Filtro para listar eventos específicos"
    )
    @discord.app_commands.choices(filtro=event_choices.FILTER_CHOICES)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def modeventos(self, interaction: discord.Interaction, filtro: discord.app_commands.Choice[str] = None):
        """Lista eventos para moderação com filtros (apenas administradores)"""
        # Usar "todos" como padrão se nenhum filtro for especificado
        filter_value = filtro.value if filtro else "todos"
        success, embed = await event_handlers.EventHandlers.handle_list_mod_events(interaction, filter_value)
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
    




async def setup(bot):
    """Função necessária para carregar o Cog"""
    await bot.add_cog(Events(bot))
    print("Cog Events carregado e comandos registrados!") 