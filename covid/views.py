#vam estar todas las rutas que tengan que ver con la app (en este caso app covid)

from flask import render_template, request
from covid import app
import csv
import json
from datetime import date


@app.route("/provincias")
def provincias():
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    csvreader = csv.reader(fichero, delimiter=",")

    lista = []
    for registro in csvreader:
        d= {'codigo': registro[0], 'valor': registro[1]}
        lista.append(d)

    fichero.close()
    #print(lista)
    return json.dumps(lista)


@app.route("/provincia/<codigoProvincia>") #para poner un parametro que no se aun literal
def laprovincia(codigoProvincia):
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia'])
    for registro in dictreader:
        if registro['codigo'] == codigoProvincia:
            fichero.close()
            return registro['provincia']
    
    fichero.close()
    return "El valor no existe. Largo de aquí!!!"

#@app.route("/casos/<int:year>/<int:mes>/<int:dia>") #ponemos "int" para restringir la entrada de datos, y obligar q sean numericos enteros.
#def casos(year, mes, dia):
    fecha = "{:04d}-{:02d}-{:02d}".format(year,mes,dia) #02d pone dos dijitos minimo de la entrada obligando a poner un 0 delante. Convirtiendo fehca en string

    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero)
    
    sumNumCasos = 0
    sumCasosPcr = 0
    sumCasosAc = 0
    sumCasosAg = 0
    sumCasosElisa = 0
    sumCasosDes = 0
    lista=[]
    for registro in dictreader:
        #if (year and mes) and (year and dia) and (mes and dia) in registro['fecha']: no funciona porque estoy comparando valores numericos 
        # con la fecha que es un string.
        
        if fecha == registro['fecha']:
        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia):
            i = registro['num_casos']
            sumNumCasos += int(i)
        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia): 
            dPcr = registro['num_casos_prueba_pcr']
            sumCasosPcr += int(dPcr)
        
        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia): 
            dAc = registro['num_casos_prueba_test_ac']
            sumCasosAc += int(dAc)
            
        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia): 
            dAg = registro['num_casos_prueba_ag']
            sumCasosAg += int(dAg)

        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia): 
            dEl = registro['num_casos_prueba_elisa']
            sumCasosElisa += int(dEl)

        #if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia): 
            dDs = registro['num_casos_prueba_desconocida']
            sumCasosDes += int(dDs)

    d = {
        "num_casos": sumNumCasos,
        "num_casos_prueba_pcr": sumCasosPcr,
        "num_casos_prueba_test_ac":sumCasosAc,
        "num_casos_prueba_ag": sumCasosAg,
        "num_casos_prueba_elisa": sumCasosElisa,
        "num_casos_prueba_desconocida": sumCasosDes
    }
    lista.append(d)
    fichero.close()
    return json.dumps(lista)


@app.route("/casos/<int:year>", defaults={"mes": None, "dia":None})
@app.route("/casos/<int:year>/<int:mes>", defaults={"dia":None})
@app.route("/casos/<int:year>/<int:mes>/<int:dia>") #ponemos "int" para restringir la entrada de datos, y obligar q sean numericos enteros.
def casos(year, mes, dia):
    #validar fecha. Es importante orden del if, primero el mes, y despues el dia.
    if not mes:
        fecha = "{:04d}".format(year)
    elif not dia:
        fecha = "{:04d}-{:02d}".format(year,mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year,mes,dia) #02d pone dos dijitos minimo de la entrada obligando a poner un 0 delante. Convirtiendo fehca en string

    #fecha = "{:04d}-{:02d}-{:02d}".format(year,mes,dia) #02d pone dos dijitos minimo de la entrada obligando a poner un 0 delante. Convirtiendo fehca en string
    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero)
    
    res ={
        'num_casos' : 0,
        'num_casos_prueba_pcr': 0, 
        'num_casos_prueba_test_ac': 0,
        'num_casos_prueba_ag': 0, 
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }
    
    for registro in dictreader:
        if fecha in registro['fecha']:
            for clave in res:
                res[clave]+= int(registro[clave])
        
        elif registro['fecha'] > fecha:
            break

    fichero.close
    return json.dumps(res) #te garantiza que salga de tal manera que json lo pueda leer en el servidor.


@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    fichero = open("data/provincias.csv", "r", encoding="utf8")
    csvreader = csv.reader(fichero, delimiter=",")
    next(csvreader) #--> nos salta la primera linia de la lectura del fichero (donde pone el texto "codigo y provincias")

    lista = []
    for registro in csvreader:
        d= {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)

    #ponemos las provincias como un desplegable de selección. Ademas nosotros vemos el nombre entero, pero el servidor solo recibe 
    #el codigo de la provincia, puesto que hacemos una lista de diccionarios.
    fichero.close()


    if request.method == 'GET':
        return render_template("alta.html", datos = formulario, provincias = lista)
    
    #Validaciones
    #vamos a utilizar request.form
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser no negativo')
    except ValueError:
        return render_template("alta.html", datos=formulario, provincias = lista, error = "PCR no puede ser negativa")
    
    return 'Ha hecho un post'
