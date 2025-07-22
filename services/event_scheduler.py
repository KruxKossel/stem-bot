from services import events_service

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
            print("Verificando eventos recorrentes vencidos...")
            
            # Buscar eventos recorrentes que já passaram
            past_due_events = events_service.EventsService.get_all_active_recurring_events_past_due()
            
            if not past_due_events:
                print("Nenhum evento recorrente vencido encontrado")
                return {
                    'success': True,
                    'total_events': 0,
                    'updated_events': 0,
                    'failed_events': 0,
                    'message': 'Nenhum evento recorrente vencido encontrado'
                }
            
            print(f"Encontrados {len(past_due_events)} eventos recorrentes vencidos")
            
            updated_count = 0
            failed_count = 0
            failed_events = []
            
            for event in past_due_events:
                event_id, name, date, time, frequency, recurrence_details = event
                
                try:
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
                            print(f"Evento '{name}' (ID: {event_id}) atualizado para {next_date} {next_time}")
                        else:
                            failed_count += 1
                            failed_events.append(f"Falha ao atualizar evento '{name}' (ID: {event_id})")
                            print(f"Falha ao atualizar evento '{name}' (ID: {event_id})")
                    else:
                        failed_count += 1
                        failed_events.append(f"Não foi possível calcular próxima ocorrência para evento '{name}' (ID: {event_id})")
                        print(f"Não foi possível calcular próxima ocorrência para evento '{name}' (ID: {event_id})")
                        
                except Exception as e:
                    failed_count += 1
                    error_msg = f"Erro ao processar evento '{name}' (ID: {event_id}): {e}"
                    failed_events.append(error_msg)
                    print(error_msg)
            
            print(f"Atualização concluída: {updated_count}/{len(past_due_events)} eventos atualizados")
            
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
            print(error_msg)
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
            
            return {
                'active_recurring_count': len(active_recurring),
                'future_events_count': len(future_events),
                'scheduler_healthy': True,
                'last_check': 'Agora'
            }
            
        except Exception as e:
            return {
                'scheduler_healthy': False,
                'error': str(e),
                'last_check': 'Erro'
            } 