import discord

# Opções de frequência para eventos recorrentes
FREQUENCY_CHOICES = [
    discord.app_commands.Choice(name="Semanalmente a cada Segunda-feira", value="Semanalmente a cada Segunda-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Terça-feira", value="Semanalmente a cada Terça-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Quarta-feira", value="Semanalmente a cada Quarta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Quinta-feira", value="Semanalmente a cada Quinta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Sexta-feira", value="Semanalmente a cada Sexta-feira"),
    discord.app_commands.Choice(name="Semanalmente a cada Sábado", value="Semanalmente a cada Sábado"),
    discord.app_commands.Choice(name="Semanalmente a cada Domingo", value="Semanalmente a cada Domingo"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Segunda-feira", value="Quinzenalmente a cada Segunda-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Terça-feira", value="Quinzenalmente a cada Terça-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Quarta-feira", value="Quinzenalmente a cada Quarta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Quinta-feira", value="Quinzenalmente a cada Quinta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Sexta-feira", value="Quinzenalmente a cada Sexta-feira"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Sábado", value="Quinzenalmente a cada Sábado"),
    discord.app_commands.Choice(name="Quinzenalmente a cada Domingo", value="Quinzenalmente a cada Domingo"),
    discord.app_commands.Choice(name="Mensalmente no dia X do mês", value="Mensalmente no dia X do mês"),
    discord.app_commands.Choice(name="Anualmente no dia X de Y", value="Anualmente no dia X de Y"),
    discord.app_commands.Choice(name="Todos os dias úteis (segunda a sexta-feira)", value="Todos os dias úteis (segunda a sexta-feira)"),
    discord.app_commands.Choice(name="Diariamente", value="Diariamente")
]

# Opções de detalhes para eventos recorrentes (limitado a 25 para respeitar o limite do Discord)
DETAILS_CHOICES = [
    # Dias do mês (1-25)
    discord.app_commands.Choice(name="Dia 1", value="dia 1"),
    discord.app_commands.Choice(name="Dia 5", value="dia 5"),
    discord.app_commands.Choice(name="Dia 10", value="dia 10"),
    discord.app_commands.Choice(name="Dia 15", value="dia 15"),
    discord.app_commands.Choice(name="Dia 20", value="dia 20"),
    discord.app_commands.Choice(name="Dia 25", value="dia 25"),
    # Meses do ano
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
    discord.app_commands.Choice(name="1 de Março", value="1 de Março"),
    discord.app_commands.Choice(name="15 de Março", value="15 de Março"),
    discord.app_commands.Choice(name="1 de Julho", value="1 de Julho"),
    discord.app_commands.Choice(name="22 de Julho", value="22 de Julho"),
    discord.app_commands.Choice(name="25 de Dezembro", value="25 de Dezembro")
]

# Opções de status para eventos
STATUS_CHOICES = [
    discord.app_commands.Choice(name="Ativo", value="ativo"),
    discord.app_commands.Choice(name="Concluído", value="concluido"),
    discord.app_commands.Choice(name="Cancelado", value="cancelado")
] 