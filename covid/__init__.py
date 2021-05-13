from flask import Flask

app = Flask(__name__)

@app.route("/")
def index(): #no hace falta escribir index, puedes poner el nombre que se quiera
    return "Flask está funcionando!"