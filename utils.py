# eco_utils.py
import datetime

consejos = [
    "Apaga las luces que no uses para ahorrar energía.",
    "Cierra la llave mientras te cepillas los dientes para ahorrar agua.",
    "Separa la basura en orgánica, reciclable y no reciclable.",
    "Lleva tu propia bolsa reutilizable cuando vayas de compras.",
    "Reduce el uso de plástico desechable.",
    "Usa transporte público, bicicleta o camina siempre que puedas.",
    "Planta un árbol y cuida las áreas verdes de tu comunidad.",
    "Compra productos locales para reducir la huella de carbono.",
    "Reutiliza envases y frascos de vidrio o plástico.",
    "Apaga y desconecta los aparatos eléctricos que no estés usando."
]

def consejo_del_dia():
    dia = datetime.datetime.now().timetuple().tm_yday
    indice = dia % len(consejos)
    return consejos[indice]
