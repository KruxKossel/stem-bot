import logging
from services import events_service

# Configurar logging
logger = logging.getLogger(__name__)

class EventScheduler:
    """Classe para gerenciar tarefas agendadas de eventos"""
    
    @staticmethod
    def update_recurring_events():
        """
        Atualiza eventos recorrentes que já passaram
        
        Returns:
            dict: Estatísticas da atualização
        """
        try:
            logger.info("Iniciando verificação de eventos recorrentes vencidos...")
            
            # Buscar eventos recorrentes que já passaram
            past_due_events = events_service.EventsService.get_all_active_recurring_events_past_due()
            
            if not past_due_events:
                logger.info("Nenhum evento recorrente vencido encontrado")
                return {
                    'success': True,
                    'total_events': 0,
                    'updated_events': 0,
                    'failed_events': 0,
                    'message': 'Nenhum evento recorrente vencido encontrado'
                }
            
            logger.info(f"Encontrados {len(past_due_events)} eventos recorrentes vencidos")
            
            updated_count = 0
            failed_count = 0
            failed_events = []
            
            for event in past_due_events:
                event_id, name, date, time, frequency, recurrence_details = event
                
                try:
                    logger.debug(f"Processando evento '{name}' (ID: {event_id}) - {date} {time}")
                    
                    # Calcular próxima ocorrência
                    next_date, next_time = events_service.EventsService.calculate_next_occurrence(
                        date, time, frequency, recurrence_details
                    )
                    
                    if next_date and next_time:
                        # Atualizar evento para próxima ocorrência
                        success = events_service.EventsService.update_event_to_next_occurrence(
                            event_id, next_date, next_time
                        )
                        
                        if success:
                            updated_count += 1
                            logger.info(f"Evento '{name}' (ID: {event_id}) atualizado para {next_date} {next_time}")
                        else:
                            failed_count += 1
                            error_msg = f"Falha ao atualizar evento '{name}' (ID: {event_id})"
                            failed_events.append(error_msg)
                            logger.error(error_msg)
                    else:
                        failed_count += 1
                        error_msg = f"Não foi possível calcular próxima ocorrência para evento '{name}' (ID: {event_id})"
                        failed_events.append(error_msg)
                        logger.error(error_msg)
                        
                except Exception as e:
                    failed_count += 1
                    error_msg = f"Erro ao processar evento '{name}' (ID: {event_id}): {e}"
                    failed_events.append(error_msg)
                    logger.error(error_msg)
            
            logger.info(f"Atualização concluída: {updated_count}/{len(past_due_events)} eventos atualizados")
            
            return {
                'success': True,
                'total_events': len(past_due_events),
                'updated_events': updated_count,
                'failed_events': failed_count,
                'failed_details': failed_events,
                'message': f"Atualização concluída: {updated_count}/{len(past_due_events)} eventos atualizados"
            }
            
        except Exception as e:
            error_msg = f"Erro na atualização de eventos recorrentes: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'message': error_msg
            }
    
    @staticmethod
    def get_scheduler_status():
        """
        Retorna o status atual do agendador
        
        Returns:
            dict: Status do agendador
        """
        try:
            # Verificar se há eventos recorrentes ativos
            active_recurring = events_service.EventsService.get_all_active_recurring_events_past_due()
            
            # Verificar eventos futuros
            future_events = events_service.EventsService.get_active_events_for_users()
            
            status = {
                'active_recurring_count': len(active_recurring),
                'future_events_count': len(future_events),
                'scheduler_healthy': True,
                'last_check': 'Agora'
            }
            
            logger.debug(f"Status do scheduler: {status}")
            return status
            
        except Exception as e:
            logger.error(f"Erro ao obter status do scheduler: {e}")
            return {
                'scheduler_healthy': False,
                'error': str(e),
                'last_check': 'Erro'
            } 

    @staticmethod
    def auto_complete_unique_events():
        """
        Auto-conclui eventos únicos vencidos
        
        Returns:
            dict: Estatísticas da auto-conclusão
        """
        try:
            logger.info("Iniciando verificação de eventos únicos para auto-conclusão...")
            
            # Buscar eventos únicos vencidos que devem ser auto-concluídos
            events_to_complete = events_service.EventsService.get_unique_events_past_due_for_auto_complete()
            
            if not events_to_complete:
                logger.info("Nenhum evento único vencido para auto-conclusão")
                return {
                    'success': True,
                    'total_events': 0,
                    'completed_events': 0,
                    'failed_events': 0,
                    'message': 'Nenhum evento único vencido para auto-conclusão'
                }
            
            logger.info(f"Encontrados {len(events_to_complete)} eventos únicos para auto-conclusão")
            
            completed_count = 0
            failed_count = 0
            failed_events = []
            
            for event in events_to_complete:
                event_id, name, date, time, auto_complete, complete_after_hours = event
                
                try:
                    logger.debug(f"Auto-concluindo evento '{name}' (ID: {event_id}) - {date} {time}")
                    
                    # Marcar como concluído
                    success = events_service.EventsService.mark_event_as_completed(event_id)
                    
                    if success:
                        completed_count += 1
                        logger.info(f"Evento único '{name}' (ID: {event_id}) auto-concluído após {complete_after_hours} hora(s)")
                    else:
                        failed_count += 1
                        error_msg = f"Falha ao auto-concluir evento '{name}' (ID: {event_id})"
                        failed_events.append(error_msg)
                        logger.error(error_msg)
                        
                except Exception as e:
                    failed_count += 1
                    error_msg = f"Erro ao auto-concluir evento '{name}' (ID: {event_id}): {e}"
                    failed_events.append(error_msg)
                    logger.error(error_msg)
            
            logger.info(f"Auto-conclusão concluída: {completed_count}/{len(events_to_complete)} eventos concluídos")
            
            return {
                'success': True,
                'total_events': len(events_to_complete),
                'completed_events': completed_count,
                'failed_events': failed_count,
                'failed_details': failed_events,
                'message': f"Auto-conclusão concluída: {completed_count}/{len(events_to_complete)} eventos concluídos"
            }
            
        except Exception as e:
            error_msg = f"Erro na auto-conclusão de eventos únicos: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'message': error_msg
            } 