import random
import unicodedata

saludos = ["Hola", "Cómo estas", "Qué tal", "Todo en orden", "Holaa", "Holaaa", "Holaaaa", "Buenas", "Buenas!","Cómo va"]

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def get_response(msg, db):

    saludos_para_comparar=[]
    for i in range(len(saludos)):
        texto= strip_accents(saludos[i])
        texto= texto.lower()
        saludos_para_comparar.append(texto)

    msg_lower = msg.lower()
    msg_final = strip_accents(msg_lower)
    palabras = msg_lower.split()

    temas = db.get_temas()

    if len([i for i in palabras if i in saludos_para_comparar])>0:
        response=random.choice(saludos)
    elif msg_final in saludos_para_comparar:
        response=random.choice(saludos)
    elif len([i for i in palabras if i in temas])>0:
        response= "Ah... veo que querés hablar de "+msg_lower 
    elif msg_final == "/done":
        #keyboard = build_keyboard(items)
        response="Genial!!"
    elif msg_final == "/start":
        response="Hola! Soy tu BotDocente. Puedo ayudarte con tus materias. Preguntame lo que necesites."
    elif msg_final.startswith("/"):
        response="Parece que quieres activar algún comando..."
    else:
        response="No te entiendo..."
    return response