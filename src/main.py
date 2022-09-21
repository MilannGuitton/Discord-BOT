from dis import disco
from email import message
from email.mime import audio
from http import client
from discord.ext import commands
from discord.utils import get
import discord
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = "Milann#3147"  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.event
async def on_message(message):
    if message.author == bot.user: # Checks that the bot is not the one sending the message
     return
    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul") # Responds 'Salut tout seul'
    await bot.process_commands(message) # Processes the message


@bot.command()
async def pong(ctx):
    await ctx.send('pong') # Prints 'pong'

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name) # Prints user name

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6)) # Prints a random nomber between 1 and 6


@bot.command(pass_context = True)
async def admin(ctx, *arg):
    if (arg == ()):
        await ctx.send("Veuillez préciser qui vous voulez mettre Admin.") # If no parameters were given
        return
    role = get(ctx.guild.roles, name = "Admin") # Get the Admin role
    if (role is None): 
        await ctx.guild.create_role(name = "Admin", permissions = discord.Permissions(permissions = 22)) # Create role if ir doesn't exist
        await ctx.send("Le rôle Admin a été créé")
        role = get(ctx.guild.roles, name = "Admin")
    for usr in arg:
        member = get(ctx.guild.members, name = usr) # Get the requested member
        if (member is None):
            await ctx.send(f'L\'utilisateur {usr} n\'existe pas')
        else:
            await member.add_roles(role) # Add role to user
            await ctx.send(usr + " a été ajouté comme Admin")

@bot.command()
async def ban(ctx, *arg):
    if (arg == ()):
        await ctx.send("Veuillez préciser qui vous voulez bannir.") # If no parameters were given
        return
    for usr in arg:
        member = get(ctx.guild.members, name = usr) # Get the requested member
        if (member is None):
            await ctx.send(f'L\'utilisateur {usr} n\'existe pas')
        elif member == ctx.message.author:
            await ctx.send("Tu ne peux pas te bannir toi-même")
        else:
            await ctx.guild.ban(member, reason = "Juste parce que j'avais envie") # Ban user
            await ctx.send(usr + " a été banni comme un malpropre")

@bot.command()
async def count(ctx):

    offline = 0
    online = 0
    dnd = 0
    idle = 0
    for m in ctx.guild.members: # Count statuses (ugly but working I guess)
        if m.status == discord.Status.online:
            online += 1
        elif m.status == discord.Status.do_not_disturb:
            dnd += 1
        elif m.status == discord.Status.idle:
            idle += 1
        else:
            offline += 1
    await ctx.send(f'{online} members are online, {offline} are offline, {dnd} are in do not distrub and {idle} are idle')

@bot.command()
async def xkcd(ctx):
    await ctx.send('Here\'s your random comic: https://c.xkcd.com/random/comic') # Could probably give some more througts about this...

@bot.command()
async def poll(ctx):
    questions = ["On est d'accord qu'on dit Chocolatine?", "Les promos impaires sont BIEN meilleures que les promos impaires non?", "L'été c'est bien mieux que l'hiver"] # The ultimate questions
    q = questions[random.randint(0, len(questions)) - 1]
    await ctx.send(f"Réglons ça une bonne fois pour toutes: {q}")
    message = await ctx.send(q)
    await message.add_reaction('\N{THUMBS UP SIGN}')
    await message.add_reaction('\N{THUMBS DOWN SIGN}')


token = ""
bot.run(token)  # Starts the bot