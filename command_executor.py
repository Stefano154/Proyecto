import requests
import yt_dlp
import pyttsx3
import discord

engine = pyttsx3.init()

async def ejecutar_comando(ctx, texto):
    texto = texto.lower()  # normalizamos todo a minúsculas

    # 🌱 ECO TIP
    if any(frase in texto for frase in [
        "eco tip", "dame un eco tip", "consejo ecológico", "un tip ecológico"
    ]):
        consejo = "🌱 Consejo: Usa botellas reutilizables para reducir el plástico de un solo uso."
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
        dato = "💡 ¿Sabías que los océanos producen más del 50% del oxígeno que respiramos?"
        await ctx.send(dato)
        engine.say(dato)
        engine.runAndWait()

    # 🌦️ CLIMA
    elif any(frase in texto for frase in [
        "clima", "qué tiempo hace", "cómo está el clima"
    ]):
        ciudad = texto.replace("clima", "").replace("qué tiempo hace en", "").strip()
        if ciudad:
            info = f"El clima en {ciudad} es soleado con 24°C."  # Aquí puedes llamar a tu API real
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
        await ctx.send(f"🔍 Resultados de búsqueda de: {query}\n(Implementar scraping/API aquí)")
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

