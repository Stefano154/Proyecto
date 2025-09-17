import os
import aiohttp
import asyncio
import requests
import yt_dlp
import pyttsx3
import discord
from utils import consejo_del_dia
from api import obtener_dato_curioso 
from api import consultar_clima

engine = pyttsx3.init()

async def buscar_google_cse(query: str) -> str:
    """
    Usa Google Custom Search (CSE) para obtener hasta 3 resultados.
    Requiere configurar GOOGLE_API_KEY y GOOGLE_CX en el .env.
    Devuelve un texto formateado listo para enviar en Discord.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    if not api_key or not cx:
        return "❌ Faltan GOOGLE_API_KEY o GOOGLE_CX en .env"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx, "q": query, "num": 3}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    return f"❌ Error al consultar Google CSE: {resp.status}\n{text[:300]}"
                data = await resp.json()
    except asyncio.TimeoutError:
        return "❌ Tiempo de espera agotado al consultar Google."
    except Exception as e:
        return f"❌ Error al consultar Google: {e}"

    items = data.get("items", [])
    if not items:
        return "🔍 No se encontraron resultados."

    lines = [f"🔍 Resultados para: **{query}**\n"]
    for it in items:
        title = it.get("title", "Sin título")
        snippet = it.get("snippet", "").replace("\n", " ")
        link = it.get("link", "")
        lines.append(f"- {title}\n  {snippet}\n  {link}\n")
    return "\n".join(lines)


async def ejecutar_comando(ctx, texto):
    texto = texto.lower()  # normalizamos todo a minúsculas

  # 🌱 ECO TIP
    if any(frase in texto for frase in [
        "eco tip", "dame un eco tip", "consejo ecológico", "un tip ecológico"
    ]):
        consejoeco = consejo_del_dia()  # aquí llamas la función
        consejo = f"🌱 Consejo ecológico del día:\n{consejoeco}"
        await ctx.send(consejo)
        engine.say(consejo)
        engine.runAndWait()

    # 🌍 ECO RETO
    elif any(frase in texto for frase in [
        "eco reto", "dame un reto ecológico", "reto semanal"
    ]):
        reto = "♻️ Reto: Esta semana evita las bolsas plásticas. Usa bolsas de tela."
        await ctx.send(reto)
        engine.say(reto)
        engine.runAndWait()

    # 💡 DATO CURIOSO
    elif any(frase in texto for frase in [
        "dato curioso", "cuéntame un dato", "sorpréndeme"
    ]):
        dato_fact = obtener_dato_curioso()
        dato = f"💡 Dato curioso: {dato_fact}"
        await ctx.send(dato)
        engine.say(dato)
        engine.runAndWait()

    # 🌦️ CLIMA
    elif any(frase in texto for frase in [
        "clima", "qué tiempo hace", "cómo está el clima"
    ]):
        info_clima = consultar_clima
        ciudad = texto.replace("clima", "").replace("qué tiempo hace en", "").strip()
        if ciudad:
            info = f"El clima en {ciudad} es: {info_clima}"  # Aquí puedes llamar a tu API real
            await ctx.send(info)
            engine.say(info)
            engine.runAndWait()
        else:
            await ctx.send("❌ Por favor, dime una ciudad. Ejemplo: 'clima Lima'")

    # 🎲 MONEDA
    elif any(frase in texto for frase in [
        "lanza una moneda", "cara o cruz", "tira una moneda"
    ]):
        import random
        resultado = random.choice(["Cara", "Cruz"])
        await ctx.send(f"🪙 {resultado}")
        engine.say(resultado)
        engine.runAndWait()

    # 😂 CHISTE
    elif any(frase in texto for frase in [
        "cuéntame un chiste", "dime un chiste", "hazme reír"
    ]):
        chiste = "😂 ¿Qué le dijo una impresora a otra? — ¿Esa hoja es tuya o es una impresión mía?"
        await ctx.send(chiste)
        engine.say(chiste)
        engine.runAndWait()

    # 🔎 YOUTUBE
    elif "youtube" in texto:
        query = texto.replace("buscar en youtube", "").strip()
        if not query:
            await ctx.send("❌ Debes decir qué buscar en YouTube.")
            return
        url = f"ytsearch1:{query}"
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video = info['entries'][0]
            await ctx.send(f"🔗 {video['title']} – {video['webpage_url']}")
            engine.say(f"Encontré {video['title']} en YouTube.")
            engine.runAndWait()

    # 🌍 GOOGLE
    elif "google" in texto:
        query = texto.replace("buscar en google", "").strip()
        if not query:
            await ctx.send("❌ Debes decir qué buscar en Google.")
            return
        resultado = await buscar_google_cse(query)
        await ctx.send(resultado)
        engine.say(f"Mostrando resultados para {query}")
        engine.runAndWait()


    # 🗑️ RECICLAJE
    elif "reciclar" in texto:
        if "botella" in texto:
            msg = "Depósitala en el contenedor amarillo (plásticos)."
        elif "papel" in texto:
            msg = "Depósitalo en el contenedor azul (papel y cartón)."
        elif "vidrio" in texto:
            msg = "Depósitalo en el contenedor verde (vidrios)."
        else:
            msg = "No reconozco ese material, pero recuerda separar residuos reciclables."
        await ctx.send(msg)
        engine.say(msg)
        engine.runAndWait()

    # 🔊 CAMBIAR VOZ
    elif "voz masculina" in texto:
        engine.setProperty("voice", "male")
        msg = "✅ Voz cambiada a masculina."
        await ctx.send(msg)
        engine.say(msg)
        engine.runAndWait()

    elif "voz femenina" in texto:
        engine.setProperty("voice", "female")
        msg = "✅ Voz cambiada a femenina."
        await ctx.send(msg)
        engine.say(msg)
        engine.runAndWait()

    # ❌ NO RECONOCIDO
    else:
        await ctx.send(f"❌ Comando no reconocido: {texto}")
        engine.say("Comando no reconocido.")
        engine.runAndWait()



