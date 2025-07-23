FROM python:3.10-slim

# Definir usuário não-root para segurança
RUN groupadd -r bot && useradd -r -g bot bot

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

# Criar pasta para dados e logs
RUN mkdir -p dados logs \
    && chown -R bot:bot /app

# Mudar para usuário não-root
USER bot

# Bot Discord não expõe portas HTTP

# Health check não aplicável para bot Discord (não expõe HTTP)
# O bot pode ser monitorado através dos logs

# Comando para executar o bot
CMD ["python", "bot.py"] 