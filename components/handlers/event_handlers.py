import discord
from services import events_service
from components.formatters import event_formatters
from components.validators import event_validators

class EventHandlers:
    """Classe para gerenciar a lógica de negócio dos comandos de eventos"""
    
    @staticmethod
    async def handle_add_unique_event(interaction, nome: str, data: str, hora: str, link: str = None):
        """
        Gerencia a adição de um evento único
        
        Args:
            interaction: Objeto de interação do Discord
            nome: Nome do evento
            data: Data do evento
            hora: Hora do evento
            link: Link do evento (opcional)
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            # Validações
            is_valid, error_msg = event_validators.EventValidators.validate_date_format(data)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
            
            is_valid, error_msg = event_validators.EventValidators.validate_time_format(hora)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
            
            is_valid, error_msg = event_validators.EventValidators.validate_future_datetime(data, hora)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Data Inválida", error_msg)
            
            # Adicionar evento
            success = events_service.EventsService.add_unique_event(nome, data, hora, link, interaction.user.id)
            
            if success:
                embed = event_formatters.EventFormatters.build_event_added_embed(
                    event_type="único",
                    name=nome,
                    date=data,
                    time=hora,
                    link=link
                )
                return True, embed
            else:
                embed = event_formatters.EventFormatters.build_error_embed(
                    "Erro",
                    "Erro ao adicionar evento. Tente novamente."
                )
                return False, embed
                
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao adicionar evento: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_add_recurring_event(interaction, nome: str, data_inicio: str, hora: str, 
                                       frequencia, detalhes = None, link: str = None, 
                                       auto_concluir = None, tempo_conclusao = None):
        """
        Gerencia a adição de um evento (único ou recorrente)
        
        Args:
            interaction: Objeto de interação do Discord
            nome: Nome do evento
            data_inicio: Data de início
            hora: Hora do evento
            frequencia: Frequência do evento
            detalhes: Detalhes da recorrência (opcional)
            link: Link do evento (opcional)
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            # Validações básicas
            is_valid, error_msg = event_validators.EventValidators.validate_date_format(data_inicio)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
            
            is_valid, error_msg = event_validators.EventValidators.validate_time_format(hora)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
            
            is_valid, error_msg = event_validators.EventValidators.validate_future_datetime(data_inicio, hora)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Data Inválida", error_msg)
            
            # Extrair valores dos objetos Choice
            frequencia_value = frequencia.value if hasattr(frequencia, 'value') else frequencia
            detalhes_value = detalhes.value if detalhes and hasattr(detalhes, 'value') else detalhes
            
            # Verificar se é evento único
            if frequencia_value == "Não se repete":
                # Adicionar como evento único
                success = events_service.EventsService.add_unique_event(nome, data_inicio, hora, link, interaction.user.id)
                
                if success:
                    embed = event_formatters.EventFormatters.build_event_added_embed(
                        event_type="único",
                        name=nome,
                        date=data_inicio,
                        time=hora,
                        link=link
                    )
                    return True, embed
                else:
                    embed = event_formatters.EventFormatters.build_error_embed(
                        "Erro",
                        "Erro ao adicionar evento único. Tente novamente."
                    )
                    return False, embed
            
            # Verificar se é evento mensal que precisa de seleção específica
            if frequencia_value == "Mensalmente (mesmo dia da semana)":
                # Criar seleção interativa para posição no mês
                return await EventHandlers._handle_monthly_selection(
                    interaction, nome, data_inicio, hora, link
                )
            
            # Processar detalhes de recorrência (opcional) para eventos recorrentes
            processed_details = None
            if detalhes_value:
                is_valid, error_msg, processed_details = event_validators.EventValidators.validate_recurrence_details(frequencia_value, detalhes_value)
                if not is_valid:
                    return False, event_formatters.EventFormatters.build_error_embed("Detalhes Inválidos", error_msg)
            
            # Processar configurações de auto-conclusão
            auto_complete_config = None
            if auto_concluir and frequencia_value == "Não se repete":
                auto_complete_value = auto_concluir.value if hasattr(auto_concluir, 'value') else auto_concluir
                tempo_value = tempo_conclusao.value if tempo_conclusao and hasattr(tempo_conclusao, 'value') else "1"
                
                auto_complete_config = {
                    'auto_complete': auto_complete_value == "sim",
                    'complete_after_hours': float(tempo_value)
                }
            
            # Adicionar evento recorrente
            success = events_service.EventsService.add_recurring_event(
                nome, data_inicio, hora, link, frequencia_value, processed_details, 
                interaction.user.id, auto_complete_config
            )
            
            if success:
                embed = event_formatters.EventFormatters.build_event_added_embed(
                    event_type="recorrente",
                    name=nome,
                    date=data_inicio,
                    time=hora,
                    frequency=frequencia_value,
                    details=processed_details,
                    link=link
                )
                return True, embed
            else:
                embed = event_formatters.EventFormatters.build_error_embed(
                    "Erro",
                    "Erro ao adicionar evento recorrente. Tente novamente."
                )
                return False, embed
                
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao adicionar evento: {e}"
            )
            return False, embed
    
    @staticmethod
    async def _handle_monthly_selection(interaction, nome: str, data_inicio: str, hora: str, link: str = None):
        """
        Cria uma seleção interativa para eventos mensais
        
        Args:
            interaction: Objeto de interação do Discord
            nome: Nome do evento
            data_inicio: Data de início
            hora: Hora do evento
            link: Link do evento (opcional)
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            # Analisar a data para determinar o dia da semana e posição no mês
            from datetime import datetime
            date_obj = datetime.strptime(data_inicio, "%d/%m/%Y")
            
            # Obter informações da data
            weekday_name = EventHandlers._get_weekday_name(date_obj.weekday())
            week_position = EventHandlers._get_week_position(date_obj)
            
            # Criar embed de seleção
            embed = discord.Embed(
                title="📅 Configurar Evento Mensal",
                description=f"**{nome}** - {data_inicio} às {hora}",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📊 Informações da Data",
                value=f"**Dia da semana:** {weekday_name}\n**Posição no mês:** {week_position}",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Opções de Recorrência",
                value="Escolha como o evento deve se repetir mensalmente:",
                inline=False
            )
            
            # Criar botões para as opções
            from discord.ui import Button, View
            
            class MonthlySelectionView(View):
                def __init__(self, event_data):
                    super().__init__(timeout=300)  # 5 minutos
                    self.event_data = event_data
                
                @discord.ui.button(label="Primeira ocorrência", style=discord.ButtonStyle.primary, emoji="1️⃣")
                async def first_occurrence(self, button_interaction: discord.Interaction, button: Button):
                    await self._handle_selection(button_interaction, "primeira")
                
                @discord.ui.button(label="Segunda ocorrência", style=discord.ButtonStyle.primary, emoji="2️⃣")
                async def second_occurrence(self, button_interaction: discord.Interaction, button: Button):
                    await self._handle_selection(button_interaction, "segunda")
                
                @discord.ui.button(label="Terceira ocorrência", style=discord.ButtonStyle.primary, emoji="3️⃣")
                async def third_occurrence(self, button_interaction: discord.Interaction, button: Button):
                    await self._handle_selection(button_interaction, "terceira")
                
                @discord.ui.button(label="Quarta ocorrência", style=discord.ButtonStyle.primary, emoji="4️⃣")
                async def fourth_occurrence(self, button_interaction: discord.Interaction, button: Button):
                    await self._handle_selection(button_interaction, "quarta")
                
                @discord.ui.button(label="Última ocorrência", style=discord.ButtonStyle.secondary, emoji="🔚")
                async def last_occurrence(self, button_interaction: discord.Interaction, button: Button):
                    await self._handle_selection(button_interaction, "última")
                
                async def _handle_selection(self, button_interaction: discord.Interaction, position: str):
                    # Verificar se é o usuário correto
                    if button_interaction.user.id != interaction.user.id:
                        await button_interaction.response.send_message(
                            "❌ Apenas quem criou o evento pode fazer esta seleção.", 
                            ephemeral=True
                        )
                        return
                    
                    # Criar frequência específica
                    weekday_name = EventHandlers._get_weekday_name(date_obj.weekday())
                    frequency_value = f"No(a) {position} {weekday_name} de cada mês"
                    
                    # Adicionar evento
                    success = events_service.EventsService.add_recurring_event(
                        self.event_data['nome'], 
                        self.event_data['data_inicio'], 
                        self.event_data['hora'], 
                        self.event_data['link'], 
                        frequency_value, 
                        None, 
                        button_interaction.user.id
                    )
                    
                    if success:
                        embed = event_formatters.EventFormatters.build_event_added_embed(
                            event_type="recorrente",
                            name=self.event_data['nome'],
                            date=self.event_data['data_inicio'],
                            time=self.event_data['hora'],
                            frequency=frequency_value,
                            details=None,
                            link=self.event_data['link']
                        )
                        embed.set_footer(text=f"Selecionado: {position} ocorrência")
                        
                        await button_interaction.response.edit_message(embed=embed, view=None)
                    else:
                        embed = event_formatters.EventFormatters.build_error_embed(
                            "Erro",
                            "Erro ao adicionar evento mensal. Tente novamente."
                        )
                        await button_interaction.response.edit_message(embed=embed, view=None)
            
            # Criar view com botões
            view = MonthlySelectionView({
                'nome': nome,
                'data_inicio': data_inicio,
                'hora': hora,
                'link': link
            })
            
            # Retornar embed com botões (não é sucesso ainda, precisa de seleção)
            return False, (embed, view)
            
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao criar seleção mensal: {e}"
            )
            return False, embed
    
    @staticmethod
    def _get_weekday_name(weekday: int) -> str:
        """Retorna o nome do dia da semana"""
        weekdays = {
            0: "Segunda-feira",
            1: "Terça-feira", 
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
            5: "Sábado",
            6: "Domingo"
        }
        return weekdays.get(weekday, "Desconhecido")
    
    @staticmethod
    def _get_week_position(date_obj) -> str:
        """Determina a posição da semana no mês"""
        day = date_obj.day
        if day <= 7:
            return "Primeira semana"
        elif day <= 14:
            return "Segunda semana"
        elif day <= 21:
            return "Terceira semana"
        elif day <= 28:
            return "Quarta semana"
        else:
            return "Última semana"
    
    @staticmethod
    async def handle_alter_event(interaction, id_evento: int, name=None, date=None, time=None, 
                                link=None, frequency=None, recurrence_details=None, status=None):
        """
        Gerencia a alteração de um evento
        
        Args:
            interaction: Objeto de interação do Discord
            id_evento: ID do evento
            **kwargs: Campos a serem alterados
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            # Extrair valores dos objetos Choice
            frequency_value = frequency.value if frequency and hasattr(frequency, 'value') else frequency
            recurrence_details_value = recurrence_details.value if recurrence_details and hasattr(recurrence_details, 'value') else recurrence_details
            status_value = status.value if status and hasattr(status, 'value') else status
            
            # Criar dicionário de campos para atualização
            update_fields = {}
            if name is not None:
                update_fields['name'] = name
            if date is not None:
                update_fields['date'] = date
            if time is not None:
                update_fields['time'] = time
            if link is not None:
                update_fields['link'] = link
            if frequency_value is not None:
                update_fields['frequency'] = frequency_value
            if recurrence_details_value is not None:
                update_fields['recurrence_details'] = recurrence_details_value
            if status_value is not None:
                update_fields['status'] = status_value
            
            # Verificar se o evento existe
            exists, error_msg, event = event_validators.EventValidators.validate_event_exists(id_evento)
            if not exists:
                return False, event_formatters.EventFormatters.build_error_embed("Evento Não Encontrado", error_msg)
            
            # Validar campos de atualização
            is_valid, error_msg, update_fields = event_validators.EventValidators.validate_update_fields(**update_fields)
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Campos Vazios", error_msg)
            
            # Validar data/hora se fornecida
            if 'date' in update_fields and 'time' in update_fields:
                is_valid, error_msg = event_validators.EventValidators.validate_date_format(update_fields['date'])
                if not is_valid:
                    return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
                
                is_valid, error_msg = event_validators.EventValidators.validate_time_format(update_fields['time'])
                if not is_valid:
                    return False, event_formatters.EventFormatters.build_error_embed("Formato Inválido", error_msg)
            
            # Validar detalhes de recorrência se frequência também fornecida
            if 'recurrence_details' in update_fields and 'frequency' in update_fields:
                is_valid, error_msg, processed_details = event_validators.EventValidators.validate_recurrence_details(
                    update_fields['frequency'], update_fields['recurrence_details']
                )
                if not is_valid:
                    return False, event_formatters.EventFormatters.build_error_embed("Detalhes Inválidos", error_msg)
                update_fields['recurrence_details'] = processed_details
            
            # Alterar evento
            success = events_service.EventsService.alter_event(id_evento, **update_fields)
            
            if success:
                embed = event_formatters.EventFormatters.build_event_updated_embed(
                    event_id=id_evento,
                    updated_fields=update_fields
                )
                return True, embed
            else:
                embed = event_formatters.EventFormatters.build_error_embed(
                    "Erro",
                    "Erro ao alterar evento. Tente novamente."
                )
                return False, embed
                
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao alterar evento: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_list_user_events(interaction):
        """
        Gerencia a listagem de eventos para usuários (apenas da semana atual e ativos)
        
        Args:
            interaction: Objeto de interação do Discord
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            events = events_service.EventsService.get_week_events_for_users()
            embed = event_formatters.EventFormatters.build_user_events_embed(events)
            return True, embed
            
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao listar eventos: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_list_mod_events(interaction, filter_type: str = "todos"):
        """
        Gerencia a listagem de eventos para moderadores com filtros
        
        Args:
            interaction: Objeto de interação do Discord
            filter_type: Tipo de filtro a ser aplicado
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            events = events_service.EventsService.get_filtered_events_for_moderation(filter_type)
            embed = event_formatters.EventFormatters.build_mod_events_embed(events, filter_type)
            return True, embed
            
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao listar eventos: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_complete_event(interaction, id_evento: int):
        """
        Gerencia a conclusão de um evento
        
        Args:
            interaction: Objeto de interação do Discord
            id_evento: ID do evento
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            # Verificar se o evento existe
            exists, error_msg, event = event_validators.EventValidators.validate_event_exists(id_evento)
            if not exists:
                return False, event_formatters.EventFormatters.build_error_embed("Evento Não Encontrado", error_msg)
            
            # Verificar se o evento está ativo
            is_valid, error_msg = event_validators.EventValidators.validate_event_status(event, 'ativo')
            if not is_valid:
                return False, event_formatters.EventFormatters.build_error_embed("Status Inválido", error_msg)
            
            # Marcar como concluído
            success = events_service.EventsService.mark_event_as_completed(id_evento)
            
            if success:
                event_id, name, date, time, link, created_by, event_type, status = event
                embed = event_formatters.EventFormatters.build_event_completed_embed(
                    event_id=id_evento,
                    name=name,
                    date=date,
                    time=time
                )
                return True, embed
            else:
                embed = event_formatters.EventFormatters.build_error_embed(
                    "Erro",
                    "Erro ao concluir evento. Tente novamente."
                )
                return False, embed
                
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao concluir evento: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_permission_error(interaction, error):
        """
        Gerencia erros de permissão
        
        Args:
            interaction: Objeto de interação do Discord
            error: Erro capturado
            
        Returns:
            embed: Embed de erro
        """
        if isinstance(error, discord.app_commands.errors.MissingPermissions):
            return event_formatters.EventFormatters.build_error_embed(
                "Permissão Negada",
                "Você precisa ser administrador para usar este comando."
            )
        else:
            return event_formatters.EventFormatters.build_error_embed(
                "Erro Inesperado",
                f"Erro inesperado: {error}"
            ) 