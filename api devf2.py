from flask import Flask, jsonify, render_template, request
import pandas as pd
import datetime as dt
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def root():
    title = "Bienvenido a la API de Bolsa de valores Dev.f"
    return render_template("api.html", title=title)


@app.route('/acción', methods=['POST', 'GET'])
def acción():
    response = {}
    empresas = pd.read_csv("C:/Users/eldia/OneDrive/Documentos/Modelo Acciones a corto plazo/listabmvtotal.csv")
    clave = request.args.get('clave')
    días = request.args.get('días')

    if clave not in empresas["Símbolo"].values:
        response = {'status': 400, 'message': 'clave no existe'}
        
    else:
        clave = clave + ".MX"
        end = dt.datetime.now()
        start = end - dt.timedelta(days=int(días))
        tabla = yf.download(clave, start, end)
        tabla = tabla["Close"]
        desviación = tabla.std()
        promedio = tabla.mean()
                        
        response = {'status': 200, 'message': 'Todo bien', 'promedio': promedio, 'std': desviación}

    return jsonify(response)

app.run(debug=True, host="localhost", port=5000)



