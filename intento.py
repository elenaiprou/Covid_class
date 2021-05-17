@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero)
    
    sumNumCasos = 0
    for registro in dictreader:
            while registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia):
                d = registro['num_casos']
                sumNumCasos += int(d)
                fichero.close()
            return str(sumNumCasos)
    
    fichero.close()


@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero)

    lista = []
    for registro in dictreader:
            while registro['fecha'] == year and mes and dia: #str(year)+'-'+ str(mes)+'-'+str(dia):
                d = (registro['provincia_iso'])
                lista.append(d)
            
            fichero.close()
            print(lista)
            return json.dumps(lista)
    
    fichero.close()
    return "No lo sabes leer bien!!!"

@app.route("/casos/<year>/<mes>/<dia>")
def casos(year, mes, dia):
    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero)
    
    sumNumCasos = 0
    for registro in dictreader:

        # print(registro['fecha'])
        # print( str(year)+'-'+ str(mes)+'-'+str(dia))

        if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia):
            #print(sumNumCasos)  
            d = registro['num_casos']
            sumNumCasos += int(d)
    fichero.close()
    return str(sumNumCasos)

#aqui me funcionaba--------------------------------------:

#vam estar todas las rutas que tengan que ver con la app (en este caso app covid)
from covid import app
import csv
import json

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

@app.route("/casos/<year>/<mes>/<dia>")
def casos(year, mes, dia):
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
        if registro['fecha'] == str(year)+'-'+ str(mes)+'-'+str(dia):
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
