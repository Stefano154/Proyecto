import discord
import asyncio
from speech_engine import escuchar_continuamente
from command_executor import ejecutar_comando

async def join_voice(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("✅ Me he unido al canal de voz.")
    else:
        await ctx.send("❌ Debes estar en un canal de voz.")

async def leave_voice(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Me desconecté del canal de voz.")
    else:
        await ctx.send("❌ No estoy en ningún canal de voz.")

async def start_voice_listener(ctx):
    await ctx.send("🎤 Escuchando continuamente. Di **'activar bot'** para empezar.")
    await escuchar_continuamente(ctx, on_command_detected=ejecutar_comando)
