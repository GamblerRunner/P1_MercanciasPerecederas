import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# Cargar datos
def df_orders_caso3(df_order_historic_demand):
    data = df_order_historic_demand
    data = data.dropna(subset=['order_demand'])  # Eliminar filas con valores nulos en 'order_demand'
    data['mes_anio'] = pd.to_datetime(data['mes_anio'], format='%m-%Y')

    # Crear variables para el modelo de predicción
    data['month'] = data['mes_anio'].dt.month
    data['year'] = data['mes_anio'].dt.year

    # Resultados consolidados
    final_results = []

    # Iterar por cliente
    clientes = data['cliente'].unique()
    for cliente in clientes:
        cliente_data = data[data['cliente'] == cliente]  # Filtrar datos por cliente
        
        # Crear el conjunto de entrenamiento y prueba
        X = cliente_data[['month', 'year']]
        y = cliente_data['order_demand']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entrenar el modelo de regresión
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Crear datos para predecir el próximo mes
        next_month = pd.DataFrame({'month': [1], 'year': [2025]})
        predicted_demand = model.predict(next_month)[0]
        
        # Calcular las rutas necesarias
        routes_needed = np.ceil(predicted_demand / 1000)
        
        # Almacenar resultados
        final_results.append({
            'cliente': cliente,
            'mes_anio': '2025-01',
            'predicted_demand': predicted_demand,
            'routes_needed': int(routes_needed)
        })

    # Crear un DataFrame con todos los resultados
    results_df = pd.DataFrame(final_results)

    # Mostrar los resultados finales
    print(results_df)

    # Visualización de datos históricos y predicción (opcional)
    plt.figure(figsize=(12, 6))
    for cliente in clientes:
        cliente_data = data[data['cliente'] == cliente]
        plt.plot(cliente_data['mes_anio'], cliente_data['order_demand'], label=f'Demanda {cliente}')
    plt.axhline(y=results_df['predicted_demand'].mean(), color='r', linestyle='--', label='Predicción promedio')
    plt.title('Demanda de Pedidos - Histórico y Predicción')
    plt.xlabel('Mes/Año')
    plt.ylabel('Demanda de pedidos')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

    return data