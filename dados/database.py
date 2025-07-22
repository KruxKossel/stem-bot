import sqlite3
import os
from pathlib import Path

class DatabaseContext:
    """Classe para gerenciar o contexto do banco de dados"""
    
    def __init__(self):
        self.db_path = Path('dados') / 'stem_bot.db'
        self.connection = None
    
    def setup_database(self):
        """Configura o banco de dados e cria as tabelas necessárias"""
        # Criar pasta dados se não existir
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Conectar ao banco de dados
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        # Verificar se a tabela events existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            # Criar tabela de eventos com todas as colunas
            cursor.execute('''
                CREATE TABLE events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    link TEXT,
                    created_by INTEGER NOT NULL,
                    type TEXT NOT NULL DEFAULT 'unico',
                    status TEXT NOT NULL DEFAULT 'ativo',
                    frequency TEXT,
                    recurrence_details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("Tabela events criada com sucesso!")
        else:
            # Verificar se as novas colunas existem
            cursor.execute("PRAGMA table_info(events)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Adicionar colunas que não existem
            if 'type' not in columns:
                cursor.execute('ALTER TABLE events ADD COLUMN type TEXT NOT NULL DEFAULT "unico"')
                print("Coluna 'type' adicionada à tabela events")
            
            if 'status' not in columns:
                cursor.execute('ALTER TABLE events ADD COLUMN status TEXT NOT NULL DEFAULT "ativo"')
                print("Coluna 'status' adicionada à tabela events")
            
            if 'frequency' not in columns:
                cursor.execute('ALTER TABLE events ADD COLUMN frequency TEXT')
                print("Coluna 'frequency' adicionada à tabela events")
            
            if 'recurrence_details' not in columns:
                cursor.execute('ALTER TABLE events ADD COLUMN recurrence_details TEXT')
                print("Coluna 'recurrence_details' adicionada à tabela events")
            
            # Atualizar eventos existentes para ter status 'ativo' e type 'unico'
            cursor.execute('UPDATE events SET status = "ativo" WHERE status IS NULL')
            cursor.execute('UPDATE events SET type = "unico" WHERE type IS NULL')
            print("Eventos existentes atualizados com valores padrão")
        
        self.connection.commit()
        print(f"Banco de dados configurado: {self.db_path}")
    
    def get_connection(self):
        """Retorna a conexão com o banco de dados"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def close_connection(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def update_event_date(self, event_id: int, new_date: str, new_time: str) -> bool:
        """
        Atualiza a data e hora de um evento específico
        
        Args:
            event_id: ID do evento a ser atualizado
            new_date: Nova data no formato DD/MM/YYYY
            new_time: Nova hora no formato HH:MM
            
        Returns:
            bool: True se o evento foi atualizado com sucesso, False caso contrário
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE events 
                SET date = ?, time = ? 
                WHERE id = ?
            ''', (new_date, new_time, event_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao atualizar data do evento: {e}")
            return False
    
    def alter_event(self, event_id: int, **kwargs) -> bool:
        """
        Altera campos específicos de um evento
        
        Args:
            event_id: ID do evento a ser alterado
            **kwargs: Campos a serem atualizados (name, date, time, link, type, status, frequency, recurrence_details)
            
        Returns:
            bool: True se o evento foi alterado com sucesso, False caso contrário
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Campos permitidos para atualização
            allowed_fields = ['name', 'date', 'time', 'link', 'type', 'status', 'frequency', 'recurrence_details']
            
            # Filtrar apenas campos permitidos
            update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
            
            if not update_fields:
                print("Nenhum campo válido fornecido para atualização")
                return False
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{field} = ?" for field in update_fields.keys()])
            values = list(update_fields.values()) + [event_id]
            
            query = f'''
                UPDATE events 
                SET {set_clause}
                WHERE id = ?
            '''
            
            cursor.execute(query, values)
            conn.commit()
            
            updated = cursor.rowcount > 0
            if updated:
                print(f"Evento {event_id} atualizado: {list(update_fields.keys())}")
            
            return updated
            
        except Exception as e:
            print(f"Erro ao alterar evento: {e}")
            return False

# Instância global do contexto do banco de dados
db_context = DatabaseContext()

def setup_database():
    """Função para configurar o banco de dados"""
    db_context.setup_database()

def get_connection():
    """Função para obter a conexão com o banco de dados"""
    return db_context.get_connection()

def close_connection():
    """Função para fechar a conexão com o banco de dados"""
    db_context.close_connection()

def update_event_date(event_id: int, new_date: str, new_time: str) -> bool:
    """Função para atualizar a data e hora de um evento"""
    return db_context.update_event_date(event_id, new_date, new_time)

def alter_event(event_id: int, **kwargs) -> bool:
    """Função para alterar campos específicos de um evento"""
    return db_context.alter_event(event_id, **kwargs) 