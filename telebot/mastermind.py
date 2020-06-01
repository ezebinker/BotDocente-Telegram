import random
import unicodedata
from model.archivo import Archivo
from model.concepto import Concepto

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
    response=[]
    #archivo=""
    busco_concepto= False

    saludos_para_comparar=[]
    for i in range(len(saludos)):
        texto= strip_accents(saludos[i])
        texto= texto.lower()
        saludos_para_comparar.append(texto)

    msg_lower = msg.lower()
    msg_final = strip_accents(msg_lower)
    palabras = msg_lower.split()

    conceptos = db.get_conceptos()

    conceptos_nombre = []
    for concepto in conceptos:
        conceptos_nombre.append(concepto.texto)

    if len([i for i in palabras if i in saludos_para_comparar])>0:
        response.append(random.choice(saludos))
    elif msg_final in saludos_para_comparar:
        response.append(random.choice(saludos))
    elif len([i for i in palabras if i in conceptos_nombre])>0:
        response.append( "Ah... veo que querés hablar de "+msg_lower)
        frases = db.get_rows_by_concept(msg_final)
        #TODO: en los conceptos también hay que recorrer palabra por palabra del mensaje como lo hago cuando no lo detecta... no usar el msg_final
        #archivo = db.get_file_by_concept(msg_final)
        for frase in frases:
            response.append(frase)
    elif msg_final == "/done":
        #keyboard = build_keyboard(items)
        response.append("Genial!!")
    elif msg_final == "/start":
        response.append("Hola! Soy tu BotDocente. Puedo ayudarte con tus materias. Preguntame lo que necesites.")
    elif msg_final.startswith("/"):
        response.append("Parece que quieres activar algún comando...")
    else:
        for palabra in palabras:
            frases = db.get_rows_by_word(palabra)
            if len(frases)>0:
                busco_concepto=True

        if busco_concepto:
            if frases is not None:
                for frase in frases:
                    response.append(frase)
        else:
            response.append("No te entiendo...")

    return response#, archivo