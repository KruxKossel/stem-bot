import discord
from discord.ext import commands
from datetime import datetime, timedelta
from services import events_service

class Events(commands.Cog):
    """Cog para gerenciar eventos do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addevento(self, ctx, nome: str, data: str, hora: str, link: str = None):
        """Adiciona um novo evento ao calendário"""
        try:
            # Validar formato da data (DD/MM/YYYY)
            datetime.strptime(data, '%d/%m/%Y')
            
            # Validar formato da hora (HH:MM)
            datetime.strptime(hora, '%H:%M')
            
            # Usar o serviço para adicionar o evento
            success = events_service.EventsService.add_event(nome, data, hora, link, ctx.author.id)
            
            if success:
                embed = discord.Embed(
                    title="✅ Evento Adicionado",
                    description=f"**{nome}** foi adicionado ao calendário!",
                    color=discord.Color.green()
                )
                embed.add_field(name="Data", value=data, inline=True)
                embed.add_field(name="Hora", value=hora, inline=True)
                if link:
                    embed.add_field(name="Link", value=link, inline=False)
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Erro ao adicionar evento. Tente novamente.")
            
        except ValueError:
            await ctx.send("❌ Formato inválido! Use: `!addevento <nome> <DD/MM/YYYY> <HH:MM> [link]`")
        except Exception as e:
            await ctx.send(f"❌ Erro ao adicionar evento: {e}")
    
    @commands.command()
    async def eventos(self, ctx):
        """Lista todos os eventos da semana"""
        try:
            # Usar o serviço para buscar eventos da semana
            events = events_service.EventsService.get_events_of_the_week()
            
            if not events:
                embed = discord.Embed(
                    title="📅 Eventos da Semana",
                    description="Nenhum evento programado para esta semana.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            
            # Calcular período da semana para exibição
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            embed = discord.Embed(
                title="📅 Eventos da Semana",
                description=f"Eventos de {week_start.strftime('%d/%m/%Y')} a {week_end.strftime('%d/%m/%Y')}",
                color=discord.Color.blue()
            )
            
            for event in events:
                name, date, time, link, created_by = event
                event_info = f"📅 {date} às {time}"
                if link:
                    event_info += f"\n🔗 {link}"
                
                embed.add_field(
                    name=f"🎯 {name}",
                    value=event_info,
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao listar eventos: {e}")
    
    @discord.app_commands.command(name="addevento", description="Adiciona um novo evento ao calendário")
    @discord.app_commands.describe(
        nome="Nome do evento",
        data="Data do evento (DD/MM/YYYY)",
        hora="Hora do evento (HH:MM)",
        link="Link do evento (opcional)"
    )
    async def addevento_slash(self, interaction: discord.Interaction, nome: str, data: str, hora: str, link: str = None):
        """Comando slash para adicionar evento"""
        try:
            # Validar formato da data (DD/MM/YYYY)
            datetime.strptime(data, '%d/%m/%Y')
            
            # Validar formato da hora (HH:MM)
            datetime.strptime(hora, '%H:%M')
            
            # Usar o serviço para adicionar o evento
            success = events_service.EventsService.add_event(nome, data, hora, link, interaction.user.id)
            
            if success:
                embed = discord.Embed(
                    title="✅ Evento Adicionado",
                    description=f"**{nome}** foi adicionado ao calendário!",
                    color=discord.Color.green()
                )
                embed.add_field(name="Data", value=data, inline=True)
                embed.add_field(name="Hora", value=hora, inline=True)
                if link:
                    embed.add_field(name="Link", value=link, inline=False)
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("❌ Erro ao adicionar evento. Tente novamente.", ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message("❌ Formato inválido! Use: `/addevento nome data hora [link]`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao adicionar evento: {e}", ephemeral=True)
    
    @discord.app_commands.command(name="eventos", description="Lista todos os eventos da semana")
    async def eventos_slash(self, interaction: discord.Interaction):
        """Comando slash para listar eventos"""
        try:
            # Usar o serviço para buscar eventos da semana
            events = events_service.EventsService.get_events_of_the_week()
            
            if not events:
                embed = discord.Embed(
                    title="📅 Eventos da Semana",
                    description="Nenhum evento programado para esta semana.",
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
                return
            
            # Calcular período da semana para exibição
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            embed = discord.Embed(
                title="📅 Eventos da Semana",
                description=f"Eventos de {week_start.strftime('%d/%m/%Y')} a {week_end.strftime('%d/%m/%Y')}",
                color=discord.Color.blue()
            )
            
            for event in events:
                name, date, time, link, created_by = event
                event_info = f"📅 {date} às {time}"
                if link:
                    event_info += f"\n🔗 {link}"
                
                embed.add_field(
                    name=f"🎯 {name}",
                    value=event_info,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao listar eventos: {e}", ephemeral=True)

async def setup(bot):
    """Função necessária para carregar o Cog"""
    await bot.add_cog(Events(bot))
    print("Cog Events carregado e comandos registrados!") 