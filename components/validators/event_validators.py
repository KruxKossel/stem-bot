from datetime import datetime
from services import events_service

class EventValidators:
    """Classe para validar entradas de eventos"""
    
    @staticmethod
    def validate_date_format(date_str: str) -> tuple[bool, str]:
        """
        Valida se a data está no formato correto (DD/MM/YYYY)
        
        Args:
            date_str: String da data para validar
            
        Returns:
            tuple: (é_válida, mensagem_erro)
        """
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True, ""
        except ValueError:
            return False, "Formato de data inválido. Use DD/MM/YYYY"
    
    @staticmethod
    def validate_time_format(time_str: str) -> tuple[bool, str]:
        """
        Valida se a hora está no formato correto (HH:MM)
        
        Args:
            time_str: String da hora para validar
            
        Returns:
            tuple: (é_válida, mensagem_erro)
        """
        try:
            datetime.strptime(time_str, '%H:%M')
            return True, ""
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM"
    
    @staticmethod
    def validate_future_datetime(date_str: str, time_str: str) -> tuple[bool, str]:
        """
        Valida se a data/hora combinada é no futuro
        
        Args:
            date_str: Data no formato DD/MM/YYYY
            time_str: Hora no formato HH:MM
            
        Returns:
            tuple: (é_válida, mensagem_erro)
        """
        if not events_service.EventsService._validate_future_datetime(date_str, time_str):
            return False, "A data e hora do evento devem ser no futuro!"
        return True, ""
    
    @staticmethod
    def validate_event_exists(event_id: int) -> tuple[bool, str, object]:
        """
        Valida se um evento existe no banco de dados
        
        Args:
            event_id: ID do evento para validar
            
        Returns:
            tuple: (existe, mensagem_erro, evento_ou_none)
        """
        event = events_service.EventsService.get_event_by_id(event_id)
        if not event:
            return False, "Evento não encontrado.", None
        return True, "", event
    
    @staticmethod
    def validate_event_status(event, expected_status: str = 'ativo') -> tuple[bool, str]:
        """
        Valida se um evento tem o status esperado
        
        Args:
            event: Objeto do evento
            expected_status: Status esperado (padrão: 'ativo')
            
        Returns:
            tuple: (é_válido, mensagem_erro)
        """
        if not event:
            return False, "Evento não encontrado."
        
        event_id, name, date, time, link, created_by, event_type, status = event
        
        if status != expected_status:
            return False, f"Evento já está {status}."
        
        return True, ""
    
    @staticmethod
    def validate_recurrence_details(frequency: str, details: str) -> tuple[bool, str, str]:
        """
        Valida se os detalhes de recorrência são apropriados para a frequência
        
        Args:
            frequency: Frequência selecionada
            details: Detalhes fornecidos
            
        Returns:
            tuple: (é_válido, mensagem_erro, detalhes_processados)
        """
        if not details:
            return True, "", None
        
        # Validações específicas por frequência
        if "Mensalmente" in frequency:
            if not details.startswith("dia "):
                return False, "Para eventos mensais, os detalhes devem ser 'dia X' (ex: 'dia 15')", None
        
        elif "Anualmente" in frequency:
            valid_months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            if not any(month in details for month in valid_months):
                return False, "Para eventos anuais, os detalhes devem incluir o mês (ex: '22 de Julho')", None
        
        elif any(freq in frequency for freq in ["Semanalmente", "Quinzenalmente", "Diariamente", "Todos os dias úteis"]):
            # Para essas frequências, detalhes são opcionais e podem ser ignorados
            return True, "", None
        
        return True, "", details
    
    @staticmethod
    def validate_update_fields(**kwargs) -> tuple[bool, str, dict]:
        """
        Valida se pelo menos um campo foi fornecido para atualização
        
        Args:
            **kwargs: Campos fornecidos para atualização
            
        Returns:
            tuple: (é_válido, mensagem_erro, campos_filtrados)
        """
        # Filtrar campos que não são None
        update_fields = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_fields:
            return False, "Nenhum campo fornecido para atualização.", {}
        
        return True, "", update_fields
    
    @staticmethod
    def validate_permissions(interaction) -> tuple[bool, str]:
        """
        Valida se o usuário tem permissões de administrador
        
        Args:
            interaction: Objeto de interação do Discord
            
        Returns:
            tuple: (tem_permissão, mensagem_erro)
        """
        if not interaction.user.guild_permissions.administrator:
            return False, "Você precisa ser administrador para usar este comando."
        
        return True, "" 