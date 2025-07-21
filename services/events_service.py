import sqlite3
from datetime import datetime, timedelta
from dados.database import get_connection

class EventsService:
    """Serviço para gerenciar operações de eventos no banco de dados"""
    
    @staticmethod
    def add_event(name: str, date: str, time: str, link: str, created_by: int) -> bool:
        """
        Adiciona um novo evento ao banco de dados
        
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
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (name, date, time, link, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, date, time, link, created_by))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar evento: {e}")
            return False
    
    @staticmethod
    def get_events_of_the_week() -> list:
        """
        Busca todos os eventos da semana atual
        
        Returns:
            list: Lista de tuplas com os dados dos eventos (name, date, time, link, created_by)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Calcular início e fim da semana
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            cursor.execute('''
                SELECT name, date, time, link, created_by
                FROM events
                WHERE date BETWEEN ? AND ?
                ORDER BY date, time
            ''', (week_start.strftime('%d/%m/%Y'), week_end.strftime('%d/%m/%Y')))
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            print(f"Erro ao buscar eventos da semana: {e}")
            return []
    
    @staticmethod
    def get_all_events() -> list:
        """
        Busca todos os eventos do banco de dados
        
        Returns:
            list: Lista de tuplas com os dados dos eventos
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT name, date, time, link, created_by
                FROM events
                ORDER BY date, time
            ''')
            
            events = cursor.fetchall()
            return events
            
        except Exception as e:
            print(f"Erro ao buscar todos os eventos: {e}")
            return []
    
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