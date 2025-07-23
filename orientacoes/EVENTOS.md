# 📅 Sistema de Eventos - Guia Completo

## 📋 Visão Geral

O Bot STEM-GIRL possui um sistema completo de gerenciamento de eventos que permite criar, listar, alterar e concluir eventos únicos e recorrentes.

## 🎯 Tipos de Eventos

### **1. Eventos Únicos**
- **Definição**: Eventos que acontecem apenas uma vez
- **Exemplo**: Workshop, reunião específica, deadline
- **Características**: 
  - ✅ Podem ter auto-conclusão configurada
  - ✅ Permanecem ativos até serem concluídos manualmente
  - ✅ Aparecem apenas uma vez nas listagens

### **2. Eventos Recorrentes**
- **Definição**: Eventos que se repetem automaticamente
- **Exemplo**: Reunião semanal, evento mensal, encontro anual
- **Características**:
  - 🔄 Atualizam automaticamente para próxima ocorrência
  - ⏰ Ignoram configurações de auto-conclusão
  - 📅 Podem ser diários, semanais, quinzenais, mensais ou anuais

## 🛠️ Comandos Disponíveis

### **Para Usuários:**

#### **`/eventos`**
**Descrição**: Lista eventos ativos da semana atual para usuários

**O que mostra:**
- ✅ Eventos ativos da semana atual
- ✅ Apenas eventos futuros (não passados)
- ✅ Informações essenciais: nome, data, hora, link

**Exemplo de uso:**
```bash
/eventos
```

### **Para Administradores:**

#### **`/addevento`**
**Descrição**: Adiciona um novo evento (único ou recorrente)

**Parâmetros:**
- `nome` - Nome do evento
- `data_inicio` - Data de início (DD/MM/YYYY)
- `hora` - Hora do evento (HH:MM)
- `frequencia` - Frequência do evento (escolha 'Não se repete' para evento único)
- `detalhes` - Detalhes da recorrência (opcional)
- `link` - Link do evento (opcional)
- `auto_concluir` - Auto-conclusão (apenas eventos únicos)
- `tempo_conclusao` - Tempo para auto-conclusão (apenas eventos únicos)

**Exemplos:**

**Evento Único:**
```bash
/addevento nome:"Workshop Python" data_inicio:"15/12/2024" hora:"14:00" frequencia:"Não se repete" link:"https://meet.google.com/abc123"
```

**Evento Recorrente:**
```bash
/addevento nome:"Reunião Semanal" data_inicio:"15/12/2024" hora:"10:00" frequencia:"Semanalmente a cada Segunda-feira"
```

#### **`/alterarevento`**
**Descrição**: Altera detalhes de um evento existente

**Parâmetros:**
- `id_evento` - ID do evento a ser alterado
- `nome` - Novo nome (opcional)
- `data` - Nova data (opcional)
- `hora` - Nova hora (opcional)
- `frequencia` - Nova frequência (opcional)
- `detalhes` - Novos detalhes (opcional)
- `link` - Novo link (opcional)
- `status` - Novo status (opcional)

**Exemplo:**
```bash
/alterarevento id_evento:5 nome:"Workshop Python Avançado" hora:"15:00"
```

#### **`/modeventos`**
**Descrição**: Lista eventos para moderação com filtros

**Filtros disponíveis:**
- **Todos os eventos** - Mostra todos os eventos
- **Apenas ativos** - Apenas eventos ativos
- **Apenas concluídos** - Apenas eventos concluídos
- **Apenas cancelados** - Apenas eventos cancelados
- **Apenas adiados** - Apenas eventos adiados
- **Últimos adicionados** - Eventos mais recentes
- **Da semana atual** - Eventos da semana atual

**Exemplo:**
```bash
/modeventos filtro:"Apenas ativos"
```

#### **`/concluirevento`**
**Descrição**: Marca um evento como concluído

**Parâmetros:**
- `id_evento` - ID do evento a ser concluído

**Exemplo:**
```bash
/concluirevento id_evento:5
```

## ⏰ Auto-Conclusão de Eventos

### **Como Funciona:**
A auto-conclusão é uma funcionalidade que permite que eventos únicos sejam marcados como "concluídos" automaticamente após um tempo configurado.

### **Parâmetros de Auto-Conclusão:**

#### **`auto_concluir`**
**Opções:**
- ✅ **"Sim - Concluir automaticamente após o evento"**
  - O evento será marcado como "concluído" automaticamente
  - Útil para eventos que têm duração definida
  - Evita que eventos passados fiquem "ativos" indefinidamente

- ❌ **"Não - Manter evento ativo"**
  - O evento permanecerá ativo mesmo após sua ocorrência
  - Útil para eventos que podem ser referenciados posteriormente
  - Permite controle manual da conclusão

#### **`tempo_conclusao`**
**Opções:**
- ⏰ **30 minutos após o evento**
- ⏰ **1 hora após o evento**
- ⏰ **2 horas após o evento**
- ⏰ **3 horas após o evento**
- ⏰ **6 horas após o evento**
- ⏰ **12 horas após o evento**
- ⏰ **24 horas após o evento**

### **Exemplo com Auto-Conclusão:**
```bash
/addevento nome:"Reunião de Equipe" data_inicio:"15/12/2024" hora:"14:00" frequencia:"Não se repete" auto_concluir:"✅ Sim - Concluir automaticamente após o evento" tempo_conclusao:"⏰ 2 horas após o evento"
```

**Resultado:**
- Evento criado para 15/12/2024 às 14:00
- Será concluído automaticamente às 16:00 (2 horas depois)
- Aparecerá como "concluído" após esse tempo

## 🔄 Frequências Disponíveis

### **Eventos Únicos:**
- **"Não se repete"** - Evento único

### **Eventos Diários:**
- **"Todos os dias úteis (segunda a sexta-feira)"** - Dias úteis

### **Eventos Semanais:**
- **"Semanalmente a cada Segunda-feira"**
- **"Semanalmente a cada Terça-feira"**
- **"Semanalmente a cada Quarta-feira"**
- **"Semanalmente a cada Quinta-feira"**
- **"Semanalmente a cada Sexta-feira"**
- **"Semanalmente a cada Sábado"**
- **"Semanalmente a cada Domingo"**

### **Eventos Quinzenais:**
- **"Quinzenalmente a cada Segunda-feira"**
- **"Quinzenalmente a cada Terça-feira"**
- **"Quinzenalmente a cada Quarta-feira"**
- **"Quinzenalmente a cada Quinta-feira"**
- **"Quinzenalmente a cada Sexta-feira"**
- **"Quinzenalmente a cada Sábado"**
- **"Quinzenalmente a cada Domingo"**

### **Eventos Mensais:**
- **"Mensalmente (mesmo dia)"** - Mesmo dia do mês
- **"Mensalmente (mesmo dia da semana)"** - Mesmo dia da semana

### **Eventos Anuais:**
- **"Anualmente (mesmo dia)"** - Mesmo dia do ano

## 📊 Status dos Eventos

### **Status Disponíveis:**
- **`ativo`** - Evento ativo e visível
- **`concluido`** - Evento já aconteceu
- **`cancelado`** - Evento foi cancelado
- **`adiado`** - Evento foi adiado

## 🔧 Funcionalidades Automáticas

### **1. Atualização de Eventos Recorrentes:**
- ✅ **Background task** roda a cada hora
- ✅ **Verifica** eventos recorrentes passados
- ✅ **Calcula** próxima ocorrência automaticamente
- ✅ **Atualiza** data e hora do evento

### **2. Auto-Conclusão de Eventos Únicos:**
- ✅ **Background task** roda a cada hora
- ✅ **Verifica** eventos únicos com auto-conclusão
- ✅ **Calcula** se já passou o tempo configurado
- ✅ **Marca** como "concluído" automaticamente

### **3. Seleção Interativa para Eventos Mensais:**
- ✅ **Embed interativo** após confirmação da data
- ✅ **Botões** para selecionar semana do mês
- ✅ **Opções**: Primeira, segunda, terceira, quarta, última semana

## 📋 Exemplos Práticos

### **Criando um Workshop:**
```bash
/addevento nome:"Workshop de Python" data_inicio:"20/12/2024" hora:"14:00" frequencia:"Não se repete" link:"https://meet.google.com/abc123" auto_concluir:"✅ Sim - Concluir automaticamente após o evento" tempo_conclusao:"⏰ 3 horas após o evento"
```

### **Criando uma Reunião Semanal:**
```bash
/addevento nome:"Reunião de Equipe" data_inicio:"15/12/2024" hora:"10:00" frequencia:"Semanalmente a cada Segunda-feira" link:"https://discord.gg/team"
```

### **Criando um Evento Mensal:**
```bash
/addevento nome:"Encontro Mensal" data_inicio:"15/12/2024" hora:"19:00" frequencia:"Mensalmente (mesmo dia da semana)" detalhes:"Primeira semana"
```

## 🎯 Casos de Uso Recomendados

### **✅ Use Auto-Conclusão Para:**
- 📅 **Reuniões** com duração definida
- 🎯 **Deadlines** de projetos
- 📚 **Aulas** ou workshops
- 🏥 **Consultas médicas**
- 🍽️ **Reservas** de restaurante

### **❌ Não Use Auto-Conclusão Para:**
- 📋 **Eventos de referência** (datas importantes)
- 🎉 **Aniversários** ou datas comemorativas
- 📝 **Lembretes** que devem permanecer visíveis
- 🔄 **Eventos recorrentes** (já são gerenciados automaticamente)

## 🔍 Verificação e Monitoramento

### **Comandos de Verificação:**
```bash
# Verificar eventos ativos da semana
/eventos

# Verificar todos os eventos (admin)
/modeventos filtro:"Todos os eventos"

# Verificar apenas eventos concluídos (admin)
/modeventos filtro:"Apenas concluídos"
```

### **Logs do Sistema:**
O bot registra automaticamente:
- 📝 Criação de eventos
- 🔄 Atualização de eventos recorrentes
- ✅ Auto-conclusão de eventos únicos
- 🛠️ Alterações manuais

## ✅ Status do Sistema

**Sistema de eventos implementado com sucesso!**

- 🎯 **Comandos completos** para usuários e administradores
- ⏰ **Auto-conclusão** configurável para eventos únicos
- 🔄 **Atualização automática** de eventos recorrentes
- 📊 **Filtros avançados** para moderação
- 🎨 **Interface intuitiva** com embeds e botões

**O sistema está pronto para uso!** 🎉 