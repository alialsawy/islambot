
from flask import Flask
from threading import Thread
import socket

app = Flask('')

@app.route('/')
def home():
    return "أنا شغال تمام 😎"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # عرض رابط الريبل
    hostname = socket.gethostname()
    print("الرابط: https://" + hostname + ".repl.co")
    
    t = Thread(target=run)
    t.start()
