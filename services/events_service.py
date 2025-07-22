import sqlite3
from datetime import datetime, timedelta
from dados.database import get_connection, update_event_date, alter_event

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
            print(f"Erro ao validar data/hora: {e}")
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
            print(f"Erro ao adicionar evento único: {e}")
            return False
    
    @staticmethod
    def add_recurring_event(name: str, start_date: str, time: str, link: str, 
                          frequency_option: str, recurrence_detail_input: str = None, created_by: int = None) -> bool:
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
                print(f"Formato de data inválido: {start_date}. Use DD/MM/YYYY")
                return False
            
            # Validar formato da hora
            try:
                datetime.strptime(time, '%H:%M')
            except ValueError:
                print(f"Formato de hora inválido: {time}. Use HH:MM")
                return False
            
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (name, date, time, link, created_by, type, status, frequency, recurrence_details)
                VALUES (?, ?, ?, ?, ?, 'recorrente', 'ativo', ?, ?)
            ''', (name, start_date, time, link, created_by, frequency_option, recurrence_detail_input))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar evento recorrente: {e}")
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
            if "Diariamente" in frequency_option:
                next_date = current_date + timedelta(days=1)
                
            elif "Semanalmente a cada" in frequency_option:
                # Extrair dia da semana da opção
                weekday_map = {
                    "Segunda-feira": 0, "Terça-feira": 1, "Quarta-feira": 2,
                    "Quinta-feira": 3, "Sexta-feira": 4, "Sábado": 5, "Domingo": 6
                }
                
                for day_name, day_num in weekday_map.items():
                    if day_name in frequency_option:
                        # Calcular próxima ocorrência do dia da semana
                        days_ahead = (day_num - current_date.weekday()) % 7
                        if days_ahead == 0:  # Se é hoje, vai para próxima semana
                            days_ahead = 7
                        next_date = current_date + timedelta(days=days_ahead)
                        break
                else:
                    next_date = current_date + timedelta(weeks=1)
                    
            elif "Quinzenalmente a cada" in frequency_option:
                # Similar ao semanal, mas 14 dias
                weekday_map = {
                    "Segunda-feira": 0, "Terça-feira": 1, "Quarta-feira": 2,
                    "Quinta-feira": 3, "Sexta-feira": 4, "Sábado": 5, "Domingo": 6
                }
                
                for day_name, day_num in weekday_map.items():
                    if day_name in frequency_option:
                        days_ahead = (day_num - current_date.weekday()) % 7
                        if days_ahead == 0:
                            days_ahead = 14
                        else:
                            days_ahead += 7
                        next_date = current_date + timedelta(days=days_ahead)
                        break
                else:
                    next_date = current_date + timedelta(weeks=2)
                    
            elif "Mensalmente no dia" in frequency_option:
                # Próximo mês, mesmo dia
                if current_date.month == 12:
                    next_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    next_date = current_date.replace(month=current_date.month + 1)
                    
            elif "Anualmente no dia" in frequency_option:
                # Próximo ano, mesmo dia e mês
                next_date = current_date.replace(year=current_date.year + 1)
                
            elif "Todos os dias úteis" in frequency_option:
                # Próximo dia útil (segunda a sexta)
                next_date = current_date + timedelta(days=1)
                while next_date.weekday() >= 5:  # Sábado ou domingo
                    next_date += timedelta(days=1)
                    
            else:
                # Fallback: avançar 1 dia
                next_date = current_date + timedelta(days=1)
            
            next_date_str = next_date.strftime("%d/%m/%Y")
            next_time_str = current_time_str
            
            return next_date_str, next_time_str
            
        except Exception as e:
            print(f"Erro ao calcular próxima ocorrência: {e}")
            return None, None
    
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
            
            # Usar função do banco de dados
            return alter_event(event_id, **kwargs)
            
        except Exception as e:
            print(f"Erro ao alterar evento: {e}")
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
            print(f"Erro ao buscar eventos recorrentes vencidos: {e}")
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
                print(f"Evento {event_id} atualizado para {next_date_str} {next_time_str}")
            return success
            
        except Exception as e:
            print(f"Erro ao atualizar evento para próxima ocorrência: {e}")
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
            print(f"Erro ao marcar evento como concluído: {e}")
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
            print(f"Erro ao buscar eventos ativos para usuários: {e}")
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
            print(f"Erro ao buscar eventos para moderação: {e}")
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
            print(f"Erro ao buscar eventos da semana: {e}")
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
            print(f"Erro ao buscar todos os eventos: {e}")
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
            print(f"Erro ao buscar evento por ID: {e}")
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
            print(f"Erro ao remover evento: {e}")
            return False 

    @staticmethod
    def check_and_remove_duplicates() -> dict:
        """
        Verifica e remove eventos duplicados no banco de dados
        
        Returns:
            dict: Estatísticas da limpeza
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar eventos duplicados (mesmo nome, data, hora e tipo)
            cursor.execute('''
                SELECT name, date, time, type, COUNT(*) as count
                FROM events
                WHERE status = 'ativo'
                GROUP BY name, date, time, type
                HAVING COUNT(*) > 1
            ''')
            
            duplicates = cursor.fetchall()
            
            if not duplicates:
                return {
                    'success': True,
                    'duplicates_found': 0,
                    'removed': 0,
                    'message': 'Nenhum evento duplicado encontrado'
                }
            
            total_removed = 0
            
            for duplicate in duplicates:
                name, date, time, event_type, count = duplicate
                
                # Manter apenas o primeiro evento (menor ID) e remover os outros
                cursor.execute('''
                    DELETE FROM events 
                    WHERE name = ? AND date = ? AND time = ? AND type = ? AND status = 'ativo'
                    AND id NOT IN (
                        SELECT MIN(id) 
                        FROM events 
                        WHERE name = ? AND date = ? AND time = ? AND type = ? AND status = 'ativo'
                    )
                ''', (name, date, time, event_type, name, date, time, event_type))
                
                removed_count = cursor.rowcount
                total_removed += removed_count
                print(f"Removidos {removed_count} eventos duplicados: {name} ({date} {time})")
            
            conn.commit()
            
            return {
                'success': True,
                'duplicates_found': len(duplicates),
                'removed': total_removed,
                'message': f'Removidos {total_removed} eventos duplicados de {len(duplicates)} grupos'
            }
            
        except Exception as e:
            print(f"Erro ao verificar duplicatas: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Erro ao verificar duplicatas: {e}'
            } 