import discord, os, audioop, logic as l, random as r, commandapi as ca, ambiente as amb
from dotenv import load_dotenv
from logic import *
from discord.ext import commands
import commandapi as api

load_dotenv ()
token = os.getenv("dt")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot el cual tiene diferentes funciones y mi nombre es: {bot.user}, para saber como usarme escribe en el chat $commands')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command(name = "psw")
async def password(ctx, lenght=25):
    a = l.contra(lenght)
    await ctx.send(f"🔒Su contraseña sera generada {a}")

@bot.command(name = "coin")
async def luck(ctx):
    await ctx.send(l.coin())

@bot.command(name = "meme")
async def chiste(ctx):
    a = l.meme()
    await ctx.send(file = a)
    
@bot.command(name = "momo")
async def chistes(ctx):
    a = l.momo()
    await ctx.send(file = a)

@bot.command(name = "pato")
async def patos(ctx):
    a = ca.duck_image()
    await ctx.send(a)

@bot.command(name="eco")
async def ecologia(ctx, opc:int):
    if opc == 1:
        await ctx.send(embed=amb.solucion_suelo1())
    elif opc == 2:
        await ctx.send(embed=amb.solucion_suelo2())
    elif opc == 3:
        await ctx.send(embed=amb.solucion_suelo3())
    else:
        await ctx.send("esta opcion no existe")

@bot.command(name='clima')
async def clima(ctx, ciudad: str):
    info_clima = api.consultar_clima(ciudad)
    if info_clima:
        await ctx.send(f"El clima en {ciudad} es: {info_clima}")
        api.speak(info_clima)
    else:
        await ctx.send("No se pudo obtener el clima. Por favor, inténtalo de nuevo más tarde.")
        api.speak("No se pudo obtener el clima.")

@bot.command(name='fact')
async def fact(ctx):
    dato = api.obtener_dato_curioso()
    await ctx.send(f"💡 Dato curioso: {dato}")
    api.speak(dato)

@bot.command(name='voz')
async def voz(ctx, genero: str):
    """Cambia la voz del bot (masculino o femenino)."""
    global voz_actual
    voz_actual = genero
    configurar_voz(genero)
    await ctx.send(f"✅ Voz cambiada a: {genero}")
    api.speak(f"Ahora estoy usando una voz {genero}")

bot.run(token)