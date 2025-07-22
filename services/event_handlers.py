import discord
from services import events_service
from services import event_formatters
from services import event_validators

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
                                       frequencia, detalhes = None, link: str = None):
        """
        Gerencia a adição de um evento recorrente
        
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
            
            # Processar detalhes de recorrência (opcional)
            processed_details = None
            if detalhes_value:
                is_valid, error_msg, processed_details = event_validators.EventValidators.validate_recurrence_details(frequencia_value, detalhes_value)
                if not is_valid:
                    return False, event_formatters.EventFormatters.build_error_embed("Detalhes Inválidos", error_msg)
            
            # Adicionar evento
            success = events_service.EventsService.add_recurring_event(
                nome, data_inicio, hora, link, frequencia_value, processed_details, interaction.user.id
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
        Gerencia a listagem de eventos para usuários
        
        Args:
            interaction: Objeto de interação do Discord
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            events = events_service.EventsService.get_active_events_for_users()
            embed = event_formatters.EventFormatters.build_user_events_embed(events)
            return True, embed
            
        except Exception as e:
            embed = event_formatters.EventFormatters.build_error_embed(
                "Erro",
                f"Erro ao listar eventos: {e}"
            )
            return False, embed
    
    @staticmethod
    async def handle_list_mod_events(interaction):
        """
        Gerencia a listagem de eventos para moderadores
        
        Args:
            interaction: Objeto de interação do Discord
            
        Returns:
            tuple: (sucesso, embed_resposta)
        """
        try:
            events = events_service.EventsService.get_all_events_for_moderation()
            embed = event_formatters.EventFormatters.build_mod_events_embed(events)
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