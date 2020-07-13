from flask import Flask, request, render_template, redirect, url_for
import telegram
from werkzeug.utils import secure_filename
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response
from processing.fileupload import process_file
import os
import unicodedata
from dbhelper import DBHelper
from pptx import Presentation

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'pptx'}

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'subidas'), exist_ok=True)

db = DBHelper()
db.setup()

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_input(text):
    input_cleaned = text
    input_cleaned = input_cleaned.replace("?", "")
    input_cleaned= input_cleaned.replace("¿", "")
    input_cleaned= input_cleaned.replace("¡", "")
    input_cleaned= input_cleaned.replace("!", "")
    input_cleaned= strip_accents(input_cleaned)
    return input_cleaned

def clean_response(respuesta):
    respuesta_final = respuesta.replace("('", "")
    respuesta_final= respuesta_final.replace("',)", "")
    return respuesta_final

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    #msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()
    text = clean_input(text)

    if len(text)>0:
        responses, archivo = get_response(text, db)
        print (str(responses))
        for response in responses:
            respuesta = str(response)
            respuesta = clean_response(respuesta)
            bot.sendMessage(chat_id=chat_id, text=respuesta)

        if archivo:
            try:           
                bot.send_document(chat_id=chat_id, caption="Te adjunto acá también, el material biblográfico de referencia para leer más sobre el tema", document=open(archivo, 'rb'))
            except Exception:
                print("TELEGRAM ERROR: Connection problems")
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    file = request.files['file']
    if request.method == 'POST' and allowed_file(file.filename):
        f = request.files['file']
        path = os.path.join(app.instance_path, 'subidas', secure_filename(f.filename))
        f.save(path)
        process_file(path, db)
        return render_template("exitoso.html")
    else:
        return render_template("error.html")

if __name__ == '__main__':
    app.run(threaded=True)