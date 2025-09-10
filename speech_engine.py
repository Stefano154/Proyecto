import sounddevice as sd
import vosk
import queue
import json

model = vosk.Model("vosk_model")  # carpeta del modelo descargado
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

async def escuchar_continuamente(ctx, on_command_detected):
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        activar = False
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                texto = result.get("text", "").lower()
                if not activar and "activar bot" in texto:
                    activar = True
                    await ctx.send("✅ Bot activado por voz. Ahora puedes dar órdenes.")
                elif activar and texto:
                    await on_command_detected(ctx, texto)
