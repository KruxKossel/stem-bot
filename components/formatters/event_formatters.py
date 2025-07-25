import discord
from datetime import datetime

class EventFormatters:
    """Classe para formatar e construir Embeds de eventos"""
    
    @staticmethod
    def _format_date_with_day(date_str: str) -> str:
        """
        Formata uma data no formato DD/MM/YYYY para incluir o dia da semana
        
        Args:
            date_str: Data no formato DD/MM/YYYY
            
        Returns:
            str: Data formatada com dia da semana (ex: "22/07/2025 (Terça-feira)")
        """
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            weekdays = {
                0: "Segunda-feira",
                1: "Terça-feira", 
                2: "Quarta-feira",
                3: "Quinta-feira",
                4: "Sexta-feira",
                5: "Sábado",
                6: "Domingo"
            }
            weekday_name = weekdays[date_obj.weekday()]
            return f"{date_str} ({weekday_name})"
        except ValueError:
            return date_str
    
    @staticmethod
    def build_user_events_embed(events_list: list) -> discord.Embed:
        """
        Constrói um Embed formatado para usuários finais (eventos da semana atual)
        
        Args:
            events_list: Lista de tuplas de eventos (id, name, date, time, link)
            
        Returns:
            discord.Embed: Embed formatado para usuários
        """
        if not events_list:
            embed = discord.Embed(
                title="📅 Eventos da Semana",
                description="Nenhum evento ativo programado para esta semana.",
                color=discord.Color.blue()
            )
            return embed
        
        embed = discord.Embed(
            title="📅 Eventos da Semana",
            description="Eventos ativos programados para esta semana:",
            color=discord.Color.blue()
        )
        
        for event in events_list:
            event_id, name, date, time, link = event
            
            # Formatar data com dia da semana
            formatted_date = EventFormatters._format_date_with_day(date)
            
            # Construir informações do evento
            event_info = f" {formatted_date} às {time}"
            if link:
                event_info += f"\n🔗 [Clique aqui para ver o evento]({link})"
            
            embed.add_field(
                name=f"🎯 {name}",
                value=event_info,
                inline=False
            )
        
        return embed
    
    @staticmethod
    def build_mod_events_embed(events_list: list, filter_type: str = "todos") -> discord.Embed:
        """
        Constrói um Embed formatado para moderadores com filtros
        
        Args:
            events_list: Lista de tuplas de eventos completos (id, name, date, time, link, created_by, type, status, frequency, recurrence_details)
            filter_type: Tipo de filtro aplicado
            
        Returns:
            discord.Embed: Embed formatado para moderadores
        """
        if not events_list:
            filter_names = {
                "todos": "Todos os eventos",
                "ativos": "Eventos ativos",
                "concluidos": "Eventos concluídos",
                "cancelados": "Eventos cancelados",
                "adiados": "Eventos adiados",
                "ultimos": "Últimos eventos adicionados",
                "semana": "Eventos da semana atual"
            }
            filter_name = filter_names.get(filter_type, "Eventos")
            
            embed = discord.Embed(
                title=f"Moderação - {filter_name}",
                description="Nenhum evento encontrado com este filtro.",
                color=discord.Color.blue()
            )
            return embed
        
        filter_names = {
            "todos": "Todos os Eventos",
            "ativos": "Eventos Ativos",
            "concluidos": "Eventos Concluídos",
            "cancelados": "Eventos Cancelados",
            "adiados": "Eventos Adiados",
            "ultimos": "Últimos Eventos Adicionados",
            "semana": "Eventos da Semana Atual"
        }
        filter_name = filter_names.get(filter_type, "Eventos")
        
        embed = discord.Embed(
            title=f"Moderação - {filter_name}",
            description=f"Total de eventos: {len(events_list)}",
            color=discord.Color.purple()
        )
        
        for event in events_list:
            event_id, name, date, time, link, created_by, event_type, status, frequency, recurrence_details = event
            
            # Formatar data com dia da semana
            formatted_date = EventFormatters._format_date_with_day(date)
            
            # Construir informações detalhadas para moderação
            event_info = f"**ID:** {event_id}\n"
            event_info += f"**Data:** {formatted_date} às {time}\n"
            event_info += f"**Tipo:** {event_type.title()}\n"
            event_info += f"**Status:** {status.title()}\n"
            event_info += f"**Criado por:** <@{created_by}>\n"
            
            if frequency:
                event_info += f"**Frequência:** {frequency}\n"
            if recurrence_details:
                event_info += f"**Detalhes:** {recurrence_details}\n"
            if link:
                event_info += f"**Link:** [Clique aqui]({link})\n"
            
            embed.add_field(
                name=f"{name}",
                value=event_info,
                inline=False
            )
        
        return embed
    
    @staticmethod
    def build_success_embed(title: str, description: str, fields: dict = None) -> discord.Embed:
        """
        Constrói um Embed de sucesso padronizado
        
        Args:
            title: Título do Embed
            description: Descrição do Embed
            fields: Dicionário opcional com campos {nome: valor}
            
        Returns:
            discord.Embed: Embed de sucesso
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green()
        )
        
        if fields:
            for field_name, field_value in fields.items():
                embed.add_field(name=field_name, value=field_value, inline=True)
        
        return embed
    
    @staticmethod
    def build_error_embed(title: str, description: str) -> discord.Embed:
        """
        Constrói um Embed de erro padronizado
        
        Args:
            title: Título do erro
            description: Descrição do erro
            
        Returns:
            discord.Embed: Embed de erro
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red()
        )
        
        return embed
    
    @staticmethod
    def build_event_added_embed(event_type: str, name: str, date: str, time: str, 
                              frequency: str = None, details: str = None, link: str = None) -> discord.Embed:
        """
        Constrói um Embed para confirmar adição de evento
        
        Args:
            event_type: Tipo do evento ("único" ou "recorrente")
            name: Nome do evento
            date: Data do evento
            time: Hora do evento
            frequency: Frequência (apenas para eventos recorrentes)
            details: Detalhes (apenas para eventos recorrentes)
            link: Link do evento
            
        Returns:
            discord.Embed: Embed de confirmação
        """
        # Formatar data com dia da semana
        formatted_date = EventFormatters._format_date_with_day(date)
        
        if event_type == "único":
            title = "Evento Único Adicionado"
            description = f"**{name}** foi adicionado ao calendário!"
        else:
            title = "Evento Recorrente Adicionado"
            description = f"**{name}** foi adicionado ao calendário!"
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green()
        )
        
        # Campos comuns
        embed.add_field(name="Data", value=formatted_date, inline=True)
        embed.add_field(name="Hora", value=time, inline=True)
        
        if event_type == "único":
            embed.add_field(name="Tipo", value="Evento único", inline=True)
        else:
            embed.add_field(name="Frequência", value=frequency, inline=True)
            if details:
                embed.add_field(name="Detalhes", value=details, inline=True)
        
        if link:
            embed.add_field(name="Link", value=f"[Clique aqui para ver o evento]({link})", inline=False)
        
        return embed
    
    @staticmethod
    def build_event_updated_embed(event_id: int, updated_fields: dict) -> discord.Embed:
        """
        Constrói um Embed para confirmar alteração de evento
        
        Args:
            event_id: ID do evento alterado
            updated_fields: Dicionário com campos alterados {campo: novo_valor}
            
        Returns:
            discord.Embed: Embed de confirmação
        """
        embed = discord.Embed(
            title="Evento Alterado",
            description=f"Evento **{event_id}** foi alterado com sucesso!",
            color=discord.Color.green()
        )
        
        for field, value in updated_fields.items():
            embed.add_field(name=f"Novo {field.title()}", value=str(value), inline=True)
        
        return embed
    
    @staticmethod
    def build_event_completed_embed(event_id: int, name: str, date: str, time: str) -> discord.Embed:
        """
        Constrói um Embed para confirmar conclusão de evento
        
        Args:
            event_id: ID do evento
            name: Nome do evento
            date: Data do evento
            time: Hora do evento
            
        Returns:
            discord.Embed: Embed de confirmação
        """
        # Formatar data com dia da semana
        formatted_date = EventFormatters._format_date_with_day(date)
        
        embed = discord.Embed(
            title="Evento Concluído",
            description=f"**{name}** foi marcado como concluído!",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Data", value=formatted_date, inline=True)
        embed.add_field(name="Hora", value=time, inline=True)
        embed.add_field(name="ID", value=event_id, inline=True)
        
        return embed 