from discord.ext import commands
from discord import Embed, Member, VoiceChannel
from datetime import datetime, timedelta

class Comandi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):        
        print("Comandi caricati!")


    @commands.command(name="temperatura", aliases=['temp'], help="Se il bot gira su un raspberry ritorna la temperatura della CPU")
    @commands.is_owner()
    async def temperatura(self, ctx):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as file:
                temperatura = float(file.readline(3))/10
                emoji = ':fire:' if temperatura > 56 else ':ice_cube:'
                await ctx.send(f"*Temperatura:*  **{temperatura}** *°C*  {emoji}")
        except:
            await ctx.send(f"C'è stato un errore nel leggere la temperatura, il bot sta eseguendo su un raspberry? :thinking:")


    @commands.command(name="chisono", aliases=['whoami'], help="Ti ricorda chi sei veramente")
    async def chisono(self, ctx):
        await ctx.send(f"Sei un trimone {ctx.message.author.mention}")


    @commands.command(name="scorreggia", aliases=["scoreggia", "cagati"], help="Comando inutile, provare per credere")
    async def scorreggia(self, ctx):
        await ctx.send(f"Oh no mi sono cagato addosso")


    @commands.command(name="pinga", aliases=["pinga_utente", "ping"], help="Pinga un utente")
    async def pinga(self, ctx, user : Member, amount=1): 
        if (amount > 5):
                await ctx.send("Oh ma sei impazzito? Non posso pingare tutte quelle volte")
        else:                
            for x in range(0, amount):
                await ctx.send(f"{user.mention}")


    @commands.command(name="raduna", aliases=["radunata", "meeting"], help="Raduna tutti gli utenti in chat vocale nello stesso canale")
    @commands.has_permissions(administrator=True)
    async def raduna(self, ctx, canale : VoiceChannel=None):
        if canale is None:
            if ctx.author.voice is None:
                return await ctx.send(f"{ctx.author.mention} Devi essere in un canale vocale o specificare quale canale in cui radunare la gente")
            else:
                canale = ctx.author.voice.channel

        for channel in ctx.guild.voice_channels:
            for member in channel.members:
                await member.move_to(canale)


    @commands.command(name="cancella", aliases=["delete","canc"],help="Cancella # messaggi")
    @commands.has_permissions(manage_messages=True)
    async def cancella(self, ctx, amount : int, mode="messaggi"):
        if amount < 1:
            return await ctx.send("Inserisci un valore valido per la quantità di messaggi da eliminare")

        if (mode == "messaggi" or mode == "mess"):
            if (amount > 100):
                return await ctx.send("Oh ma sei impazzito? Non posso cancellare tutti quei messaggi")
            else:    
                await ctx.channel.purge(limit=int(amount)+1)

        elif (mode in ['minuto','minuti','min','m','ora','ore','h','o','giorno','giorni','g','d']):
            if mode in ['ora','ore','h','o']: amount = amount * 60
            if mode in ['giorno','giorni','g','d']: amount = amount * 1440

            if amount > 4320: 
                return await ctx.send(f"Oh ma sei impazzito? Non posso cancellare tutti quei messaggi")

            data_comando = ctx.channel.last_message.created_at
            differenza = timedelta(minutes=amount)
            messaggi = await ctx.channel.history(after=(data_comando-differenza)).flatten()
            await ctx.channel.delete_messages(messaggi)

        else:
            await ctx.send("Puoi cancellare gli ultimi # messaggi con:\n\t``` cancella # messaggi```\nOppure cancellare i messaggi inviati negli ultimi minuti/ore/giorni con:\n\t``` cancella 5 minuti  /  cancella 1 ora  /  cancella 2 giorni```")


def setup(bot):
    bot.add_cog(Comandi(bot))