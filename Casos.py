import pandas as pd
import modeloACO as maco
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


def start_df(caso = 1):
    df_distances = pd.read_excel('static/excels/df_distance_km.xlsx')
    df_customers = pd.read_excel('static/excels/df_orders.xlsx')
    df_vehicles = pd.read_excel('static/excels/df_vehicle.xlsx')

    df_vehicles = df_vehicles.sort_values(by="costo_km", ascending=True).reset_index(drop=True)

    if caso == 2:
        df_vehicles = caso_2(df_vehicles)

    elif caso == 3:
        df_historic_orders = pd.read_excel('static/excels/df_historic_order_demand.xlsx')
        df_customers = caso_3(df_historic_orders) 

    elif caso == 4:
        df_vehicles = caso_4(df_vehicles)

    resultado = maco.ACO(caso, df_distances, df_vehicles, df_customers)
    if resultado is None:
        raise ValueError("La función ACO devolvió None")
    rutas, coste_total = resultado
    
    return rutas, coste_total


def caso_2(df_vehicles):
    #Solo recogemos la mitad de los vehiculos pero de manera random
    return df_vehicles.sample(n=len(df_vehicles)//2, random_state=42) 
    

def caso_3(df_order_historic_demand):
    # Cargar datos
    order = df_order_historic_demand.dropna(subset=['order_demand'])
    #IQR
    Q1 = order['order_demand'].quantile(0.25)
    Q3 = order['order_demand'].quantile(0.75)
    IQR = Q3 - Q1

    # Esto lo usamos para poner un limite a nuestros datos(vamos a darle chamba de outliers)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    order = order[(order['order_demand'] >= lower_bound) & (order['order_demand'] <= upper_bound)]
    order['mes_anio'] = pd.to_datetime(order['mes_anio'], format='%m-%Y')
    order['month'] = order['mes_anio'].dt.month
    order['year'] = order['mes_anio'].dt.year

    resultados = []

    for cliente in order['cliente'].unique():
        cliente_data = order[order['cliente'] == cliente]
        
        if len(cliente_data) < 2:
            continue  
        
        X = cliente_data[['month', 'year']]
        y = cliente_data['order_demand']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        #enero de 2025
        next_month = pd.DataFrame({'month': [1], 'year': [2025]})
        predicted_demand = model.predict(next_month)[0]
        
        
        resultados.append({
            'cliente': cliente,
            'mes_anio': '2025-01',
            'order_demand': predicted_demand
        })

    df_customers = pd.DataFrame(resultados)

    return df_customers


def caso_4(df_vehicles):
    return df_vehicles.sample(n=1)


