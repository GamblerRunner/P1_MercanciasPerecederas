from flask import Flask, render_template, redirect, url_for, request
import os
import pandas as pd
import osmnx as ox
import folium
import modeloACO as maco

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/opcion/<tipo>')
def opcion(tipo):
    if tipo == "datos":
        return redirect(url_for('datos'))
    elif tipo == "apartados":
        return render_template('apartados.html')
    else:
        return "Opción no válida."

@app.route('/datos')
def datos():
    # Obtener una lista de archivos CSV en la carpeta "static/csvs"
    csv_folder = os.path.join(app.static_folder, 'excels')
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.xlsx')]
    return render_template('datos.html', csv_files=csv_files)

import chardet

@app.route('/ver_datos/<filename>', methods=['GET', 'POST'])
def ver_datos(filename):
    csv_folder = os.path.join(app.static_folder, 'excels')
    file_path = os.path.join(csv_folder, filename)
    print(file_path)
    if not os.path.exists(file_path):
        return render_template('error.html', message=f"El archivo '{filename}' no existe en la carpeta csvs.")

    try:
        # Detectar la codificación del archivo
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']

        if filename.endswith('.csv'):
            df = pd.read_csv(file_path, encoding=encoding)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return render_template('error.html', message=f"El archivo '{filename}' no es un formato válido.")

        data = df.to_dict(orient='records')
        columns = df.columns.tolist()

        return render_template('ver_datos.html', filename=filename, data=data, columns=columns)
    except Exception as e:
        return render_template('error.html', message=f"Ocurrió un error al procesar el archivo: {str(e)}")

@app.route('/modificar_datos/<filename>', methods=['GET', 'POST'])
def modificar_datos(filename):
    csv_folder = os.path.join(app.static_folder, 'excels')
    file_path = os.path.join(csv_folder, filename)

    if not os.path.exists(file_path):
        return render_template('error.html', message=f"El archivo '{filename}' no existe en la carpeta csvs.")

    try:
        if request.method == 'POST':
            # Procesar los datos enviados por el formulario
            updated_data = request.form.to_dict(flat=False)
            rows = []
            for i in range(len(updated_data[list(updated_data.keys())[0]])):
                row = {col: updated_data[f"data[{i}][{col}]"][0] for col in updated_data if f"data[{i}]" in col}
                rows.append(row)
            
            # Convertir a DataFrame y guardar
            df = pd.DataFrame(rows)
            if filename.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            return redirect(url_for('ver_datos', filename=filename))

        # Leer los datos actuales del archivo
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return render_template('error.html', message=f"El archivo '{filename}' no es un formato válido.")

        # Agregar índices a los datos para Jinja2
        data = [{'index': idx, **row} for idx, row in enumerate(df.to_dict(orient='records'))]
        columns = df.columns.tolist()

        return render_template('modificar_datos.html', filename=filename, data=data, columns=columns)
    except Exception as e:
        print(e)
        return render_template('error.html', message=f"Ocurrió un error al procesar el archivo: {str(e)}")


import numpy as np
import random

@app.route('/apartado1')
def apartado1():
    # Cargar datos de localización de clientes desde el Excel
    file_path = "static/excels/df_location.xlsx"  # Asegúrate de colocar tu archivo Excel aquí
    df = pd.read_excel(file_path)

    # Asegurar que las columnas sean correctas
    df.columns = df.columns.str.strip()

    # Corregir claves: Cliente_X → X-1 (Ej. Cliente_13 → 12)
    coordenadas_clientes = {
        int(row["Cliente"].replace("Cliente_", "")) - 1: (row["Latitud"], row["Longitud"])
        for _, row in df.iterrows() if isinstance(row["Cliente"], str) and "Cliente_" in row["Cliente"]
    }

    # Agregar el almacén con clave 20
    almacen = df[df["Cliente"] == "Almacén"][["Latitud", "Longitud"]].values
    if len(almacen) > 0:
        coordenadas_clientes[20] = tuple(almacen[0])  

    # Usar la ubicación del almacén como centro del mapa
    start_location = coordenadas_clientes.get(20, list(coordenadas_clientes.values())[0])
    m = folium.Map(location=start_location, zoom_start=13)

    # Lista de rutas
    rutas = [
        (
            np.float64(1.0),
            [
                [20, np.int64(8), np.int64(5), 20],
                [20, np.int64(15), np.int64(0), 20],
                [20, np.int64(10), np.int64(13), 20],
                [20, np.int64(3), np.int64(9), 20],
                [20, np.int64(4), np.int64(16), 20],
                [20, np.int64(2), np.int64(18), 20],
                [20, np.int64(7), np.int64(14), 20],
                [20, np.int64(17), np.int64(11), 20],
                [20, np.int64(6), np.int64(1), 20],
                [20, np.int64(12), np.int64(19), 20],
            ],
        )
    ]

    rutas, coste_total = maco.ACO()


    # Dibujar rutas en el mapa
    for vehiculo, rutas_por_vehiculo in rutas:
        for ruta in rutas_por_vehiculo:
            ruta = [cliente for cliente in ruta if cliente != 0]  # Filtrar ceros
            coordenadas = [coordenadas_clientes.get(cliente, start_location) for cliente in ruta]

            # Color aleatorio por ruta
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            folium.PolyLine(coordenadas, color=color, weight=2.5, opacity=0.8).add_to(m)

    # Agregar marcadores de clientes y almacén
    for cliente, coords in coordenadas_clientes.items():
        if cliente == 20:
            nombre = "Almacén"
            color = "red"  # Rojo para el almacén
        else:
            nombre = f"Cliente {cliente + 1}"  # Sumamos 1 solo para la visualización
            color = "blue"  # Azul para clientes
        
        folium.Marker(
            location=coords,
            popup=nombre,
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(m)

    # Guardar el mapa
    map_path = "static/map.html"
    m.save(map_path)

    # Datos ficticios de resultados
    resultados = {
        "costes": str(coste_total)+"€",
        "iteraciones": 50,
        "texto1": "Resultado adicional 1",
        "texto2": "Resultado adicional 2",
    }

    return render_template('caso1.html', titulo="Caso 1", map_file=map_path, resultados=resultados)


@app.route('/apartado2')
def apartado2():
    return "Contenido del Apartado 2"

@app.route('/apartado3')
def apartado3():
    return "Contenido del Apartado 3"

@app.route('/apartado4')
def apartado4():
    return "Contenido del Apartado 4"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
