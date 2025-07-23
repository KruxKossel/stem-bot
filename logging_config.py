import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configura o sistema de logging estruturado para o bot
    
    Configura:
    - Logging para console (INFO)
    - Logging para arquivo (DEBUG)
    - Formato estruturado com timestamp
    - Rotação de logs por data
    """
    
    # Criar pasta de logs se não existir
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Nome do arquivo de log com data
    log_filename = f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar formato do log
    log_format = '%(asctime)s %(levelname)-8s %(name)-20s %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar handlers
    handlers = []
    
    # Handler para console (INFO e acima)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # Handler para arquivo (DEBUG e acima)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(file_formatter)
    handlers.append(file_handler)
    
    # Configurar logging root
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True  # Força reconfiguração se já configurado
    )
    
    # Configurar níveis específicos para alguns módulos
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('discord.http').setLevel(logging.WARNING)
    logging.getLogger('discord.gateway').setLevel(logging.WARNING)
    
    # Log de inicialização
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado")
    logger.info(f"Logs sendo salvos em: {log_filename}")
    
    return logger

def get_logger(name):
    """
    Retorna um logger configurado para o módulo especificado
    
    Args:
        name: Nome do módulo (geralmente __name__)
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name) 