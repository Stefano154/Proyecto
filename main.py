import discord, os, audioop, logic as l, random as r, commandapi as ca, ambiente as amb
from dotenv import load_dotenv
from logic import *
from discord.ext import commands
from voice_manager import join_voice, leave_voice, start_voice_listener
import commandapi as api, pyttsx3
import datetime
import requests
import yt_dlp
import pyttsx3

load_dotenv ()
token = os.getenv("dt")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
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
    dato_fact = api.obtener_dato_curioso()
    await ctx.send(f"💡 Dato curioso: {dato_fact}")
    api.speak(dato_fact)

engine = pyttsx3.init()

def configurar_voz(genero: str):
    voces = engine.getProperty("voices")
    if genero.lower() == "masculino":
        engine.setProperty("voice", voces[0].id)
    elif genero.lower() == "femenino":
        engine.setProperty("voice", voces[1].id)
    else:
        raise ValueError("Género no válido. Usa 'masculino' o 'femenino'.")

def speak(texto: str):
    engine.say(texto)
    engine.runAndWait()

# 🔊 Unirse al canal de voz
@bot.command()
async def join(ctx):
    await join_voice(ctx)
    await start_voice_listener(ctx)

# 👋 Salir del canal de voz
@bot.command()
async def leave(ctx):
    await leave_voice(ctx)

# 📡 Estado de conexión
@bot.command()
async def status(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        await ctx.send(f"✅ Estoy conectado al canal de voz: **{ctx.voice_client.channel}**")
    else:
        await ctx.send("❌ No estoy conectado a ningún canal de voz.")

@bot.command(name="huella")
async def huella(ctx, km: float):
    """
    Calcula la huella de carbono de un recorrido en auto.
    Uso: !huella <kilómetros>
    """
    # Factor promedio: 0.233 kg CO2/km (auto promedio)
    co2 = km * 0.233
    await ctx.send(f"🚗 Tu recorrido generó aprox. **{co2:.2f} kg de CO₂**.\n🌱 ¡Considera usar bicicleta o transporte público!")

eco_quiz_questions = [
    {
        "pregunta": "¿Cuál es el gas principal responsable del efecto invernadero?",
        "opciones": ["A) CO₂", "B) N₂", "C) O₂"],
        "respuesta": "A"
    },
    {
        "pregunta": "¿Cuánto tarda en degradarse una botella de plástico?",
        "opciones": ["A) 50 años", "B) 450 años", "C) 10 años"],
        "respuesta": "B"
    }
]

# Ejemplo de preguntas
eco_quiz_questions = [
    {
        "pregunta": "¿Cuál de estos materiales es 100% reciclable?",
        "opciones": ["A) Vidrio", "B) Plástico", "C) Papel"],
        "respuesta": "A"
    },
    {
        "pregunta": "¿Cuál es la capa de la atmósfera que protege de la radiación UV?",
        "opciones": ["A) Troposfera", "B) Estratosfera", "C) Ionosfera"],
        "respuesta": "B"
    }
]

@bot.command(name="eco_quiz")
async def eco_quiz(ctx):
    """
    Envía una pregunta de trivia ambiental.
    Uso: $eco_quiz
    """
    q = r.choice(eco_quiz_questions)
    opciones = "\n".join(q["opciones"])
    await ctx.send(f"🌍 **{q['pregunta']}**\n{opciones}\n✍️ Responde con A, B o C.")

    def check(m):
        # Asegura que solo se tome la respuesta del mismo usuario y en el mismo canal
        return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in ["A", "B", "C"]

    try:
        respuesta = await bot.wait_for("message", check=check, timeout=20.0)
    except Exception:
        await ctx.send("⏰ Se acabó el tiempo para responder.")
        return

    if respuesta.content.upper() == q["respuesta"]:
        await ctx.send("✅ ¡Correcto!")
    else:
        await ctx.send(f"❌ Incorrecto. La respuesta correcta era **{q['respuesta']}**.")

@bot.command(name="comandos")
async def comandos(ctx):
    """
    Muestra la lista de comandos disponibles del bot en un embed.
    Uso: $comandos
    """
    embed = discord.Embed(title="📜 Comandos disponibles", description="Prefijo: `$`", color=0x5865F2)


    comandos = sorted(bot.commands, key=lambda c: c.name)


    for cmd in comandos:
        if getattr(cmd, 'hidden', False):
            continue
        nombre = f"${cmd.name}"
        descripcion = cmd.help or "Sin descripción disponible."
        embed.add_field(name=nombre, value=descripcion, inline=False)


    embed.set_footer(text=f"{len([c for c in comandos if not getattr(c,'hidden',False)])} comandos listados")
    await ctx.send(embed=embed)


@bot.command(name="ayuda")
async def ayuda(ctx):
    """Alias en español para $comandos."""
    await comandos(ctx)

bot.run(token)