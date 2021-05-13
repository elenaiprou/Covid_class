#vam estar todas las rutas que tengan que ver con la app (en este caso app covid)
from covid import app

@app.route("/")
def index(): #no hace falta escribir index, puedes poner el nombre que se quiera
    return "Flask está funcionando desde views!"