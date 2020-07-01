import random
import unicodedata
from model.archivo import Archivo
from model.concepto import Concepto
from telebot.credentials import bot_token, bot_user_name,URL

saludos = ["Hola", "Cómo estas", "Qué tal", "Todo en orden", "Holaa", "Holaaa", "Holaaaa", "Buenas", "Buenas!","Cómo va","Qué alegría!","Qué alegría verte por aquí!","Un gusto que me hayas contactado","De vez en cuando está bueno hablarme!", "Hola hola!", "Hola.","Buenos","Buenas buenas","Que tal!","Ciao","Qué le trae por aquí?"]

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
        intro_msj = ["Ah... veo que querés hablar de ", "Okey, veamos que tenemos sobre ",": ","Quiero decirte todo esto acerca de ","Ok! Perfecto. Hablemos de ","Genial!! Tengo esta información de "]
        response.append(random.choice(intro_msj) + msg_lower)
        frases = db.get_rows_by_concept(msg_final)
        #TODO: en los conceptos también hay que recorrer palabra por palabra del mensaje como lo hago cuando no lo detecta... no usar el msg_final
        #archivo = db.get_file_by_concept(msg_final)
        for frase in frases:
            response.append(frase)
    elif msg_final == "/done":
        #keyboard = build_keyboard(items)
        response.append("Genial!!")
    elif msg_final == "/archivos":
        archivos = db.get_nombre_archivos()
        response.append("Lista de archivos subidos a la plataforma Bot Docente: ")
        lista = ""
        for archivo in  archivos:
            lista+= archivo + "\n"
        response.append(lista)
    elif msg_final == "/subirdocumento":
        response.append("Para subir un documento de conocimiento al Bot Docente acceder al siguiente enlace: \n"+URL)
    elif msg_final == "/consejos":
        consejos= ["No dejes para mañana lo que puedes hacer hoy!","Organiza tus tiempos, sé metódico.", "Si estudiás y practicás con anticipación, todo es mucho más fácil.", "Al que madruga, dios lo ayuda.","Los resúmenes SIRVEN, siempre y cuando vos los hayas confeccionado!","Preguntale al BotDocente lo que necesites!","Practica, practica, practica dijo alguna vez Carmine Gallo..."]
        response.append(random.choice(consejos))
    elif msg_final == "/start":
        response.append("Hola! Soy BotDocente, un bot preparado por Ezequiel Binker para aprovechar el tiempo y facilitarte el aprendizaje.")
        response.append("Puedo ayudarte con tus materias, facilitando las respuestas teóricas que necesites conocer de una manera rápida y sencilla. Sólo pregunta.")
    elif msg_final == "/help":
        response.append("Puedes preguntarme lo que quieras acerca del contenido que tengo cargado.")
        response.append("Además, con mis comandos (que aparecen abajo a la derecha en la /, o bien escribiendo '/' en el mensaje) vas a poder subir documentos, conocer los archivos de conocimiento que tengo incorporados, entre otras funcionalidades disponibles.")
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
            error_msj = ["No te entiendo...","¿Podrías expresarte mejor? No puedo entenderte!","No logro seguir tus pensamientos", "Subiste información de este contenido? Te invito a que lo hagas acá!\n"+URL,"BotDocente no puede entenderte.","Entenderte no puedo.","¿Decías?","No entiendo!!!","No puedo procesar esa petición"]
            response.append(random.choice(error_msj))

    return response#, archivo