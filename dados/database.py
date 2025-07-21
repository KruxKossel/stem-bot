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
        
        # Criar tabela de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                link TEXT,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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