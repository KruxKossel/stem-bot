import discord

# Opções de frequência para eventos recorrentes (simplificadas)
FREQUENCY_CHOICES = [
    # Opção para eventos únicos
    discord.app_commands.Choice(name="Não se repete", value="Não se repete"),
    
    # Frequências semanais (7 opções)
    discord.app_commands.Choice(name="Semanalmente a cada Segunda-feira", value="Semanalmente a cada Segunda-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Terça-feira", value="Semanalmente a cada Terça-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Quarta-feira", value="Semanalmente a cada Quarta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Quinta-feira", value="Semanalmente a cada Quinta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Sexta-feira", value="Semanalmente a cada Sexta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Sábado", value="Semanalmente a cada Sábado"),
    discord.app_commands.Choice(name="Semanalmente a cada Domingo", value="Semanalmente a cada Domingo"),
    
    # Frequências quinzenais (7 opções)
    discord.app_commands.Choice(name="Quinzenalmente a cada Segunda-feira", value="Quinzenalmente a cada Segunda-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Terça-feira", value="Quinzenalmente a cada Terça-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Quarta-feira", value="Quinzenalmente a cada Quarta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Quinta-feira", value="Quinzenalmente a cada Quinta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Sexta-feira", value="Quinzenalmente a cada Sexta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Sábado", value="Quinzenalmente a cada Sábado"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Domingo", value="Quinzenalmente a cada Domingo"),
    
    # Frequências mensais (simplificadas)
    discord.app_commands.Choice(name="Mensalmente (mesmo dia)", value="Mensalmente (mesmo dia)"),
    discord.app_commands.Choice(name="Mensalmente (mesmo dia da semana)", value="Mensalmente (mesmo dia da semana)"),
    
    # Frequências anuais
    discord.app_commands.Choice(name="Anualmente (mesmo dia)", value="Anualmente (mesmo dia)"),
    
    # Frequências diárias
    discord.app_commands.Choice(name="Todos os dias úteis (segunda a sexta-feira)", value="Todos os dias úteis (segunda a sexta-feira)")
]

# Opções de detalhes para eventos recorrentes (limitado a 25 para respeitar o limite do Discord)
DETAILS_CHOICES = [
    # Opção padrão
    discord.app_commands.Choice(name="Sem detalhes específicos", value=""),
    
    # Detalhes para eventos mensais
    discord.app_commands.Choice(name="Primeira semana", value="primeira semana"),
    discord.app_commands.Choice(name="Segunda semana", value="segunda semana"),
    discord.app_commands.Choice(name="Terceira semana", value="terceira semana"),
    discord.app_commands.Choice(name="Quarta semana", value="quarta semana"),
    discord.app_commands.Choice(name="Última semana", value="última semana"),
    
    # Detalhes para eventos anuais
    discord.app_commands.Choice(name="Janeiro", value="Janeiro"),
    discord.app_commands.Choice(name="Fevereiro", value="Fevereiro"),
    discord.app_commands.Choice(name="Março", value="Março"),
    discord.app_commands.Choice(name="Abril", value="Abril"),
    discord.app_commands.Choice(name="Maio", value="Maio"),
    discord.app_commands.Choice(name="Junho", value="Junho"),
    discord.app_commands.Choice(name="Julho", value="Julho"),
    discord.app_commands.Choice(name="Agosto", value="Agosto"),
    discord.app_commands.Choice(name="Setembro", value="Setembro"),
    discord.app_commands.Choice(name="Outubro", value="Outubro"),
    discord.app_commands.Choice(name="Novembro", value="Novembro"),
    discord.app_commands.Choice(name="Dezembro", value="Dezembro"),
    
    # Combinações comuns para anual
    discord.app_commands.Choice(name="1 de Janeiro", value="1 de Janeiro"),
    discord.app_commands.Choice(name="15 de Janeiro", value="15 de Janeiro"),
    discord.app_commands.Choice(name="22 de Julho", value="22 de Julho"),
    discord.app_commands.Choice(name="25 de Dezembro", value="25 de Dezembro"),
    
    # Detalhes para eventos semanais/quinzenais
    discord.app_commands.Choice(name="Manhã (09:00)", value="manhã"),
    discord.app_commands.Choice(name="Tarde (14:00)", value="tarde"),
    discord.app_commands.Choice(name="Noite (19:00)", value="noite")
]

# Opções de status para eventos
STATUS_CHOICES = [
    discord.app_commands.Choice(name="Ativo", value="ativo"),
    discord.app_commands.Choice(name="Concluído", value="concluido"),
    discord.app_commands.Choice(name="Cancelado", value="cancelado"),
    discord.app_commands.Choice(name="Adiado", value="adiado")
]

# Opções de filtro para listagem de eventos
FILTER_CHOICES = [
    discord.app_commands.Choice(name="Todos os eventos", value="todos"),
    discord.app_commands.Choice(name="Apenas ativos", value="ativos"),
    discord.app_commands.Choice(name="Apenas concluídos", value="concluidos"),
    discord.app_commands.Choice(name="Apenas cancelados", value="cancelados"),
    discord.app_commands.Choice(name="Apenas adiados", value="adiados"),
    discord.app_commands.Choice(name="Últimos adicionados", value="ultimos"),
    discord.app_commands.Choice(name="Da semana atual", value="semana")
]

# Opções de auto-conclusão (apenas para eventos únicos)
AUTO_COMPLETE_CHOICES = [
    discord.app_commands.Choice(name="✅ Sim - Concluir automaticamente após o evento", value="sim"),
    discord.app_commands.Choice(name="❌ Não - Manter evento ativo", value="nao")
]

# Opções de tempo para auto-conclusão (apenas para eventos únicos)
AUTO_COMPLETE_TIME_CHOICES = [
    discord.app_commands.Choice(name="⏰ 30 minutos após o evento", value="0.5"),
    discord.app_commands.Choice(name="⏰ 1 hora após o evento", value="1"),
    discord.app_commands.Choice(name="⏰ 2 horas após o evento", value="2"),
    discord.app_commands.Choice(name="⏰ 3 horas após o evento", value="3"),
    discord.app_commands.Choice(name="⏰ 6 horas após o evento", value="6"),
    discord.app_commands.Choice(name="⏰ 12 horas após o evento", value="12"),
    discord.app_commands.Choice(name="⏰ 24 horas após o evento", value="24")
] 