import sqlite3
import logging
from datetime import datetime, timedelta
from dados.database import get_connection, update_event_date, alter_event

# Configurar logging
logger = logging.getLogger(__name__)

class EventsService:
    """Serviço para gerenciar operações de eventos no banco de dados"""
    
    @staticmethod
    def _validate_future_datetime(date_str: str, time_str: str) -> bool:
        """
        Valida se a data e hora combinadas são no futuro
        
        Args:
            date_str: Data no formato DD/MM/YYYY
            time_str: Hora no formato HH:MM
            
        Returns:
            bool: True se a data/hora é no futuro, False caso contrário
        """
        try:
            # Converter strings para datetime
            event_datetime = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            current_datetime = datetime.now()
            
            return event_datetime > current_datetime
            
        except ValueError as e:
            logger.error(f"Erro ao validar data/hora: {e}")
            return False
    
    @staticmethod
    def _get_weekday_name(date_str: str) -> str:
        """
        Retorna o nome do dia da semana para uma data
        
        Args:
            date_str: Data no formato DD/MM/YYYY
            
        Returns:
            str: Nome do dia da semana em português
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
            return weekdays[date_obj.weekday()]
        except ValueError:
            return "Data inválida"
    
    @staticmethod
    def add_unique_event(name: str, date: str, time: str, link: str, created_by: int) -> bool:
        """
        Adiciona um novo evento único ao banco de dados
        
        Args:
            name: Nome do evento
            date: Data do evento (DD/MM/YYYY)
            time: Hora do evento (HH:MM)
            link: Link do evento (opcional)
            created_by: ID do usuário que criou o evento
            
        Returns:
            bool: True se o evento foi adicionado com sucesso, False caso contrário
        """
        try:
            # Validar se a data/hora é no futuro
            if not EventsService._validate_future_datetime(date, time):
                raise ValueError("A data e hora do evento devem ser no futuro")
            
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (name, date, time, link, created_by, type, status)
                VALUES (?, ?, ?, ?, ?, 'unico', 'ativo')
            ''', (name, date, time, link, created_by))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar evento único: {e}")
            return False
    
    @staticmethod
    def add_recurring_event(name: str, start_date: str, time: str, link: str, 
                          frequency_option: str, recurrence_detail_input: str = None, created_by: int = None,
                          auto_complete_config: dict = None) -> bool:
        """
        Adiciona um novo evento recorrente ao banco de dados
        
        Args:
            name: Nome do evento
            start_date: Data de início (DD/MM/YYYY)
            time: Hora do evento (HH:MM)
            link: Link do evento (opcional)
            frequency_option: Opção de frequência do Discord UI
            recurrence_detail_input: Detalhes adicionais da recorrência
            created_by: ID do usuário que criou o evento
            
        Returns:
            bool: True se o evento foi adicionado com sucesso, False caso contrário
        """
        try:
            # Validar se a data/hora é no futuro
            if not EventsService._validate_future_datetime(start_date, time):
                raise ValueError("A data e hora do evento devem ser no futuro")
            
            # Validar formato da data
            try:
                datetime.strptime(start_date, '%d/%m/%Y')
            except ValueError:
                logger.error(f"Formato de data inválido: {start_date}. Use DD/MM/YYYY")
                return False
            
            # Validar formato da hora
            try:
                datetime.strptime(time, '%H:%M')
            except ValueError:
                logger.error(f"Formato de hora inválido: {time}. Use HH:MM")
                return False
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Processar configurações de auto-conclusão
            auto_complete = 1  # Padrão: True
            complete_after_hours = 1  # Padrão: 1 hora
            
            if auto_complete_config and frequency_option == "Não se repete":
                auto_complete = 1 if auto_complete_config.get('auto_complete', True) else 0
                complete_after_hours = auto_complete_config.get('complete_after_hours', 1)
            
            # Determinar tipo baseado na frequência
            event_type = EventsService._determine_event_type(frequency_option)
            
            cursor.execute('''
                INSERT INTO events (name, date, time, link, created_by, type, status, frequency, recurrence_details, auto_complete, complete_after_hours)
                VALUES (?, ?, ?, ?, ?, ?, 'ativo', ?, ?, ?, ?)
            ''', (name, start_date, time, link, created_by, event_type, frequency_option, recurrence_detail_input, auto_complete, complete_after_hours))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar evento recorrente: {e}")
            return False
    
    @staticmethod
    def calculate_next_occurrence(current_date_str: str, current_time_str: str, 
                                frequency_option: str, recurrence_details_internal: str) -> tuple:
        """
        Calcula a próxima ocorrência de um evento recorrente baseado nas opções do Discord
        
        Args:
            current_date_str: Data atual do evento (DD/MM/YYYY)
            current_time_str: Hora atual do evento (HH:MM)
            frequency_option: Opção de frequência do Discord UI
            recurrence_details_internal: Detalhes internos da recorrência
            
        Returns:
            tuple: (nova_data_str, nova_hora_str) ou (None, None) se erro
        """
        try:
            current_date = datetime.strptime(current_date_str, "%d/%m/%Y")
            current_time = datetime.strptime(current_time_str, "%H:%M").time()
            
            # Mapear opções do Discord para cálculos
            if frequency_option == "Não se repete":
                # Evento único, não calcular próxima ocorrência
                logger.info("Evento único, não há próxima ocorrência")
                return None, None
                
            elif "Semanalmente a cada" in frequency_option:
                # Sempre avançar 7 dias para eventos semanais
                next_date = current_date + timedelta(weeks=1)
                logger.info(f"Evento semanal: próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                    
            elif "Quinzenalmente a cada" in frequency_option:
                # Sempre avançar 14 dias para eventos quinzenais
                next_date = current_date + timedelta(weeks=2)
                logger.info(f"Evento quinzenal: próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                    
            elif frequency_option == "Mensalmente (mesmo dia)":
                # Próximo mês, mesmo dia
                if current_date.month == 12:
                    next_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    next_date = current_date.replace(month=current_date.month + 1)
                logger.info(f"Evento mensal (mesmo dia): próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                    
            elif "No(a)" in frequency_option and "de cada mês" in frequency_option:
                # Evento mensal com posição específica (primeira, segunda, etc.)
                if current_date.month == 12:
                    next_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                else:
                    next_date = current_date.replace(month=current_date.month + 1, day=1)
                
                # Extrair informações da frequência
                parts = frequency_option.split()
                position = parts[1]  # primeira, segunda, terceira, quarta, última
                weekday_name = parts[2]  # Segunda-feira, Terça-feira, etc.
                
                # Mapear nome do dia para número
                weekday_map = {
                    "Segunda-feira": 0, "Terça-feira": 1, "Quarta-feira": 2,
                    "Quinta-feira": 3, "Sexta-feira": 4, "Sábado": 5, "Domingo": 6
                }
                weekday_num = weekday_map.get(weekday_name, 0)
                
                # Encontrar a ocorrência correta
                if position == "última":
                    # Última ocorrência do mês
                    last_occurrence = None
                    temp_date = next_date
                    while temp_date.month == next_date.month:
                        if temp_date.weekday() == weekday_num:
                            last_occurrence = temp_date
                        temp_date += timedelta(days=1)
                    next_date = last_occurrence
                else:
                    # Primeira, segunda, terceira ou quarta ocorrência
                    position_map = {"primeira": 1, "segunda": 2, "terceira": 3, "quarta": 4}
                    target_occurrence = position_map.get(position, 1)
                    
                    occurrences = 0
                    while occurrences < target_occurrence:
                        if next_date.weekday() == weekday_num:
                            occurrences += 1
                        if occurrences < target_occurrence:
                            next_date += timedelta(days=1)
                            
                logger.info(f"Evento mensal ({position} {weekday_name}): próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                    
            elif frequency_option == "Anualmente (mesmo dia)":
                # Próximo ano, mesmo dia e mês
                next_date = current_date.replace(year=current_date.year + 1)
                logger.info(f"Evento anual: próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                
            elif "Todos os dias úteis" in frequency_option:
                # Próximo dia útil (segunda a sexta)
                next_date = current_date + timedelta(days=1)
                while next_date.weekday() >= 5:  # Sábado ou domingo
                    next_date += timedelta(days=1)
                logger.info(f"Evento dias úteis: próxima ocorrência em {next_date.strftime('%d/%m/%Y')}")
                    
            else:
                # Fallback: avançar 1 dia para qualquer frequência não reconhecida
                logger.warning(f"Frequência não reconhecida: {frequency_option}, usando fallback de 1 dia")
                next_date = current_date + timedelta(days=1)
            
            next_date_str = next_date.strftime("%d/%m/%Y")
            next_time_str = current_time_str
            
            logger.info(f"Próxima ocorrência calculada: {next_date_str} {next_time_str} para frequência '{frequency_option}'")
            return next_date_str, next_time_str
            
        except Exception as e:
            logger.error(f"Erro ao calcular próxima ocorrência: {e}")
            return None, None
    
    @staticmethod
    def _determine_event_type(frequency: str) -> str:
        """
        Determina o tipo do evento baseado na frequência
        
        Args:
            frequency: Frequência do evento
            
        Returns:
            str: 'unico' ou 'recorrente'
        """
        if frequency == "Não se repete":
            return "unico"
        else:
            return "recorrente"
    
    @staticmethod
    def alter_event(event_id: int, **kwargs) -> bool:
        """
        Altera campos específicos de um evento
        
        Args:
            event_id: ID do evento
            **kwargs: Campos a serem alterados
            
        Returns:
            bool: True se alterado com sucesso, False caso contrário
        """
        try:
            # Validar data/hora se fornecida
            if 'date' in kwargs and 'time' in kwargs:
                if not EventsService._validate_future_datetime(kwargs['date'], kwargs['time']):
                    raise ValueError("A nova data e hora devem ser no futuro")
            
            # Se a frequência foi alterada, atualizar automaticamente o tipo
            if 'frequency' in kwargs:
                new_type = EventsService._determine_event_type(kwargs['frequency'])
                kwargs['type'] = new_type
                logger.info(f"Tipo do evento {event_id} atualizado para '{new_type}' baseado na frequência '{kwargs['frequency']}'")
            
            # Usar função do banco de dados
            return alter_event(event_id, **kwargs)
            
        except Exception as e:
            logger.error(f"Erro ao alterar evento: {e}")
            return False
    
    @staticmethod
    def get_all_active_recurring_events_past_due() -> list:
        """
        Busca todos os eventos recorrentes ativos cuja data e hora já passaram
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (id, name, date, time, frequency, recurrence_details)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Data e hora atual
            now = datetime.now()
            current_date = now.strftime('%d/%m/%Y')
            current_time = now.strftime('%H:%M')
            
            cursor.execute('''
                SELECT id, name, date, time, frequency, recurrence_details
                FROM events
                WHERE type = 'recorrente' 
                AND status = 'ativo'
                AND (date < ? OR (date = ? AND time <= ?))
                ORDER BY date, time
            ''', (current_date, current_date, current_time))
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos recorrentes vencidos: {e}")
            return []
    
    @staticmethod
    def update_event_to_next_occurrence(event_id: int, next_date_str: str, next_time_str: str) -> bool:
        """
        Atualiza um evento para sua próxima ocorrência
        
        Args:
            event_id: ID do evento
            next_date_str: Nova data (DD/MM/YYYY)
            next_time_str: Nova hora (HH:MM)
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            success = update_event_date(event_id, next_date_str, next_time_str)
            if success:
                logger.info(f"Evento {event_id} atualizado para {next_date_str} {next_time_str}")
            return success
            
        except Exception as e:
            logger.error(f"Erro ao atualizar evento para próxima ocorrência: {e}")
            return False
    
    @staticmethod
    def mark_event_as_completed(event_id: int) -> bool:
        """
        Marca um evento como concluído
        
        Args:
            event_id: ID do evento a ser marcado como concluído
            
        Returns:
            bool: True se o evento foi marcado com sucesso, False caso contrário
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE events 
                SET status = 'concluido' 
                WHERE id = ? AND status = 'ativo'
            ''', (event_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Erro ao marcar evento como concluído: {e}")
            return False
    
    @staticmethod
    def get_active_events_for_users() -> list:
        """
        Busca eventos ativos e futuros para usuários
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (id, name, date, time, link)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Data e hora atual
            now = datetime.now()
            current_date = now.strftime('%d/%m/%Y')
            current_time = now.strftime('%H:%M')
            
            cursor.execute('''
                SELECT id, name, date, time, link
                FROM events
                WHERE status = 'ativo' 
                AND (date > ? OR (date = ? AND time > ?))
                ORDER BY date, time
            ''', (current_date, current_date, current_time))
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos ativos para usuários: {e}")
            return []
    
    @staticmethod
    def get_all_events_for_moderation() -> list:
        """
        Busca todos os eventos para moderação
        
        Returns:
            list: Lista de tuplas com todos os dados dos eventos
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                FROM events
                ORDER BY date DESC, time DESC
            ''')
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos para moderação: {e}")
            return []
    
    @staticmethod
    def get_events_of_the_week() -> list:
        """
        Busca eventos ativos da semana atual e futuros (mantido para compatibilidade)
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (id, name, date, time, link, created_by, type, status)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Calcular início da semana atual
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            
            cursor.execute('''
                SELECT id, name, date, time, link, created_by, type, status
                FROM events
                WHERE status = 'ativo' 
                AND date >= ?
                ORDER BY date, time
            ''', (week_start.strftime('%d/%m/%Y'),))
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos da semana: {e}")
            return []
    
    @staticmethod
    def get_all_events() -> list:
        """
        Busca todos os eventos do banco de dados (mantido para compatibilidade)
        
        Returns:
            list: Lista de tuplas com os dados dos eventos
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, date, time, link, created_by, type, status
                FROM events
                ORDER BY date, time
            ''')
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os eventos: {e}")
            return []
    
    @staticmethod
    def get_event_by_id(event_id: int) -> tuple:
        """
        Busca um evento específico pelo ID
        
        Args:
            event_id: ID do evento
            
        Returns:
            tuple: Dados do evento ou None se não encontrado
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, date, time, link, created_by, type, status
                FROM events
                WHERE id = ?
            ''', (event_id,))
            
            event = cursor.fetchone()
            return event
            
        except Exception as e:
            logger.error(f"Erro ao buscar evento por ID: {e}")
            return None
    
    @staticmethod
    def delete_event(event_id: int) -> bool:
        """
        Remove um evento do banco de dados
        
        Args:
            event_id: ID do evento a ser removido
            
        Returns:
            bool: True se o evento foi removido com sucesso, False caso contrário
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Erro ao remover evento: {e}")
            return False 

 

    @staticmethod
    def get_week_events_for_users() -> list:
        """
        Busca eventos ativos da semana atual para usuários
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (id, name, date, time, link)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Calcular início e fim da semana atual
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            # Data e hora atual
            now = datetime.now()
            current_date = now.strftime('%d/%m/%Y')
            current_time = now.strftime('%H:%M')
            
            cursor.execute('''
                SELECT id, name, date, time, link
                FROM events
                WHERE status = 'ativo' 
                AND date >= ? AND date <= ?
                AND (date > ? OR (date = ? AND time > ?))
                ORDER BY date, time
            ''', (week_start.strftime('%d/%m/%Y'), week_end.strftime('%d/%m/%Y'), 
                  current_date, current_date, current_time))
            
            events = cursor.fetchall()
            logger.info(f"Encontrados {len(events)} eventos da semana para usuários")
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos da semana para usuários: {e}")
            return []
    
    @staticmethod
    def get_filtered_events_for_moderation(filter_type: str = "todos") -> list:
        """
        Busca eventos filtrados para moderação
        
        Args:
            filter_type: Tipo de filtro ("todos", "ativos", "concluidos", "cancelados", "adiados", "ultimos", "semana")
            
        Returns:
            list: Lista de tuplas com os dados dos eventos
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if filter_type == "todos":
                # Todos os eventos
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    ORDER BY date DESC, time DESC
                ''')
                
            elif filter_type == "ativos":
                # Apenas eventos ativos
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    WHERE status = 'ativo'
                    ORDER BY date DESC, time DESC
                ''')
                
            elif filter_type == "concluidos":
                # Apenas eventos concluídos
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    WHERE status = 'concluido'
                    ORDER BY date DESC, time DESC
                ''')
                
            elif filter_type == "cancelados":
                # Apenas eventos cancelados
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    WHERE status = 'cancelado'
                    ORDER BY date DESC, time DESC
                ''')
                
            elif filter_type == "adiados":
                # Apenas eventos adiados
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    WHERE status = 'adiado'
                    ORDER BY date DESC, time DESC
                ''')
                
            elif filter_type == "ultimos":
                # Últimos 10 eventos adicionados
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    ORDER BY id DESC
                    LIMIT 10
                ''')
                
            elif filter_type == "semana":
                # Eventos da semana atual
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)
                
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    WHERE date >= ? AND date <= ?
                    ORDER BY date, time
                ''', (week_start.strftime('%d/%m/%Y'), week_end.strftime('%d/%m/%Y')))
                
            else:
                # Filtro inválido, retornar todos
                logger.warning(f"Filtro inválido '{filter_type}', retornando todos os eventos")
                cursor.execute('''
                    SELECT id, name, date, time, link, created_by, type, status, frequency, recurrence_details
                    FROM events
                    ORDER BY date DESC, time DESC
                ''')
            
            events = cursor.fetchall()
            logger.info(f"Encontrados {len(events)} eventos com filtro '{filter_type}' para moderação")
            return events
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos filtrados para moderação: {e}")
            return [] 

    @staticmethod
    def get_unique_events_past_due_for_auto_complete() -> list:
        """
        Busca eventos únicos vencidos que devem ser auto-concluídos
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (id, name, date, time, auto_complete, complete_after_hours)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Data e hora atual
            now = datetime.now()
            current_date = now.strftime('%d/%m/%Y')
            current_time = now.strftime('%H:%M')
            
            cursor.execute('''
                SELECT id, name, date, time, auto_complete, complete_after_hours
                FROM events
                WHERE type = 'unico' 
                AND status = 'ativo'
                AND auto_complete = 1
                AND (date < ? OR (date = ? AND time < ?))
            ''', (current_date, current_date, current_time))
            
            events = cursor.fetchall()
            
            # Filtrar eventos que já passaram do tempo de auto-conclusão
            events_to_complete = []
            for event in events:
                event_id, name, date, time, auto_complete, complete_after_hours = event
                
                # Calcular quando o evento deve ser concluído
                event_datetime = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
                complete_datetime = event_datetime + timedelta(hours=complete_after_hours)
                
                # Se já passou do tempo de conclusão, adicionar à lista
                if now >= complete_datetime:
                    events_to_complete.append(event)
            
            logger.info(f"Encontrados {len(events_to_complete)} eventos únicos vencidos para auto-conclusão")
            return events_to_complete
            
        except Exception as e:
            logger.error(f"Erro ao buscar eventos únicos vencidos para auto-conclusão: {e}")
            return [] 