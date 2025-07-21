import discord
from discord.ext import commands
from datetime import datetime

class Welcome(commands.Cog):
    """Cog para gerenciar mensagens de boas-vindas e saída"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Evento executado quando um membro entra no servidor"""
        # Usar ID específico do canal de boas-vindas
        welcome_channel = member.guild.get_channel(1396900097610088538)
        
        if welcome_channel:
            # Mensagem simples de boas-vindas
            await welcome_channel.send(f"Bem-vinda, {member.mention}! 🌷")
            
            # Embed detalhado
            embed = discord.Embed(
                title="🎉 Bem-vinda ao STEM-GIRL!",
                description=f"Olá **{member.name}**! Seja muito bem-vinda à nossa comunidade!",
                color=discord.Color.green()
            )
            
            
            embed.add_field(
                name="📋 Próximos passos",
                value="• Apresente-se no canal #apresentações\n• Leia as regras em #regras\n• Participe das conversas!",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Eventos",
                value="\n\nUse `/eventos` para ver os próximos eventos da semana!",
                inline=False
            )

            embed.add_field(
                    name="\n\n🔗 Links úteis",
                    value="• [STEM GIRL - Linktree](https://linktr.ee/stemgirlsoficial)\n• Conecte-se conosco nas redes sociais!",
                    inline=False
                )
            
            
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text=f"Você é o membro #{len(member.guild.members)} do servidor!")
            
            await welcome_channel.send(embed=embed)
            
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Evento executado quando um membro sai do servidor"""
        # Usar ID específico do canal de saídas
        leave_channel = member.guild.get_channel(1396901336619941909)
        
        if leave_channel:
            # Obter informações detalhadas para a equipe de moderação
            current_time = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            member_count = member.guild.member_count
            
            # Embed detalhado para a staff
            embed = discord.Embed(
                title="👋 Membro Saiu do Servidor",
                description=f"**{member.name}** deixou o servidor",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="📋 Informações do Usuário",
                value=f"**Nome:** {member.name}\n**ID:** {member.id}\n**Entrou no servidor:** {member.joined_at.strftime('%d/%m/%Y')}",
                inline=True
            )
            
            embed.add_field(
                name="⏰ Informações da Saída",
                value=f"**Hora da saída:** {current_time}\n**Membros restantes:** {member_count}",
                inline=True
            )
            
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="Informações para a equipe de moderação")
            
            await leave_channel.send(embed=embed)
    
    @discord.app_commands.command(name="welcome", description="Testa a mensagem de boas-vindas")
    async def test_welcome(self, interaction: discord.Interaction):
        """Comando para testar a mensagem de boas-vindas"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Você precisa ser administrador para usar este comando.", ephemeral=True)
            return
        
        # Simular evento de boas-vindas
        await self.on_member_join(interaction.user)
        await interaction.response.send_message("✅ Mensagem de boas-vindas enviada!", ephemeral=True)

async def setup(bot):
    """Função necessária para carregar o Cog"""
    await bot.add_cog(Welcome(bot))
    print("Cog Welcome carregado e comandos registrados!") 