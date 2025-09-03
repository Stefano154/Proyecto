import requests
import pyttsx3

engine = pyttsx3.init()
voz_actual = "femenino"  # Voz por defecto

def configurar_voz(genero: str):
    """Cambia la voz entre masculina y femenina."""
    voices = engine.getProperty('voices')
    if genero.lower() == "masculino":
        for voice in voices:
            if "male" in voice.name.lower() or "hombre" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    elif genero.lower() == "femenino":
        for voice in voices:
            if "female" in voice.name.lower() or "mujer" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

def speak(text:str):
    engine.say(text)
    engine.runAndWait()

def traducir_texto(texto: str, idioma_destino: str = "es") -> str:
    url = f"https://api.mymemory.translated.net/get?q={texto}&langpair=en|{idioma_destino}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("responseData", {}).get("translatedText", texto)
    else:
        return texto

def consultar_clima(ciudad:str) -> str:
    url = f"https://wttr.in/{ciudad}?format=%C+%t"
    response = requests.get(url)

    if response.status_code==200:
        return response.text.strip()
    else:
        return "No se pudo encontrar información sobre la ciudad nombrada"
    
def obtener_dato_curioso(idioma_destino: str = "es") -> str:
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        hecho = data.get("text", "No se encontró ningún hecho en la respuesta.")
        return traducir_texto(hecho, idioma_destino)
    else:
        return "No se pudo obtener un dato curioso en este momento."