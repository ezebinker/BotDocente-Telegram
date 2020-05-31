import os.path
from pptx import Presentation
import PyPDF2
import slate3k as slate
import pandas as pd
from cgitb import text
import nltk
import spacy
from model.archivo import Archivo

def process_file(source, db):
    
    #Obtengo referencias al nombre y extensión del archivo
    base=os.path.basename(source)
    nombre=os.path.splitext(base)[0]
    extension=os.path.splitext(base)[1]

    contenido = []

    #Curso en base a la extensión del archivo. 
    if extension=='.pptx':
        prs = Presentation(source)
            
        #Lectura de la PPT
        for slide in prs.slides:
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        contenido.append(run.text) 
            contenido.append('.')

        #Elimino residuos del contenido
        indices_a_borrar = []
        for index, item in enumerate(contenido):
            if len(item)<3 and item!='.':
                indices_a_borrar.append(index)

        for index in sorted(indices_a_borrar, reverse=True):
            del contenido[index]

    elif extension=='.pdf':
          
        with open(source,'rb') as f:
            contenido = slate.PDF(f)
        f.close() 

    elif extension=='.txt':
        print("hola")

        file = open(source,mode='r')
        contenido = file.read()
        file.close()
    else:
        print("No se como abrir eso! ")

    #### GENERAL A CUALQUIER ARCHIVO DE CONTENIDO ####

    #Obtenemos los conceptos o palabras que más aparecen en el contenido
    freq = nltk.FreqDist(contenido)
    
    topPalabras = '['

    for key,val in sorted(freq.items()):
        if val>1:
            itemActual='{'+str(key) + ',' + str(val) + '}'
            topPalabras+=str(itemActual)
    
    topPalabras+=']'

    archivo = Archivo(nombre,topPalabras)

    db.add_archivo(archivo)
    #id_archivo = db.get_last_id
    
    #Elimino residuos del contenido gral
    contenido= [frase.replace('\n', '') for frase in contenido]
    contenido= [frase.replace('\t', '') for frase in contenido]

    #Genero un solo texto con todo el contenido
    strcont = ' '.join(contenido)

    oraciones = strcont.split('.')
    print(oraciones)

    # USO DE LIBRERÍA SPACY

    #Obtengo referencias de nlp de la librería SpaCy
    #nlp=spacy.load('es_core_news_md')

    #doc = nlp(strcont)

    #for token in doc:
       # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

    #print("Verbos:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    #sentencias = [s for s in doc.sents]
    #print(sentencias[1])

    #FIN DE BLOQUE LIBRERÍA SPACY

    return archivo.nombre + "      " + archivo.topPalabras
