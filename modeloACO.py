import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

def ACO():

    df_order_historic_demand = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_historic_order_demand.xlsx')
    df_distances = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_distance_km.xlsx')
    df_distance_min = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_distance_min.xlsx')
    df_location = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_location.xlsx')
    df_customers = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_orders.xlsx')
    df_vehicles = pd.read_excel('C:/Users/JWinn01/Desktop/IABD/material/datos/Datos_P1/df_vehicle.xlsx')


    #cambiar posicion de almacen por mas comodidad

    # Mostrar las primeras filas para verificar el contenido original
    print("Datos originales:")
    print(df_distances.head())


    # Parámetros de ACO
    num_vehiculos = 10
    num_iterations = 100
    alpha = 1.0
    beta = 2.0
    rho = 0.5
    Q = 100

    n_nodes = len(df_customers)+1
    pheromone_matrix = np.ones((n_nodes, n_nodes))

    def calculo_Probabilidad(current_node, unvisited_nodes, pheromones, df_distances):
        probabilities = []
        for node in unvisited_nodes:
            distance = df_distances.iloc[current_node, node]
            if distance > 0:  
                tau = pheromones[current_node][node] ** alpha
                eta = (1 / distance) ** beta
                probabilities.append(tau * eta)
            else:
                probabilities.append(0)  
        
        probabilities = np.array(probabilities)
        total = probabilities.sum()
        
        # Evitar misma posicion entre clientes (DUDA)
        if total == 0:
            probabilities = np.ones(len(unvisited_nodes)) / len(unvisited_nodes)
        else:
            probabilities = probabilities / total
        
        return probabilities

    # Función para construir solución por una hormiga
    def solucion_Vehiculo(df_distances, df_vehicles, orders):
        solution = []  
        remaining_customers = set(range(n_nodes - 1))  #contamos cuantos clientes van quedando
        depot = n_nodes - 1  # indice del almacen

        for _, vehicle in df_vehicles.iterrows():  
            vehicle_routes = []  
            vehicle_capacity = vehicle["capacidad_kg"]

            while remaining_customers:
                current_route = [depot]  # Inicia en el depósito
                current_capacity = vehicle_capacity
                current_node = depot
                while remaining_customers:
                    unvisited_nodes = [node for node in remaining_customers if orders[node] <= current_capacity]
                    if not unvisited_nodes:  # No hay clientes factibles
                        break

                    probabilities = calculo_Probabilidad(current_node, unvisited_nodes, pheromone_matrix, df_distances)
                    next_node = np.random.choice(unvisited_nodes, p=probabilities)

                    current_route.append(next_node)
                    current_capacity -= orders[next_node]
                    remaining_customers.remove(next_node)
                    current_node = next_node

                current_route.append(depot) 
                if len(current_route) > 2: 
                    vehicle_routes.append(current_route)

            if vehicle_routes:  
                solution.append((vehicle["vehiculo_id"], vehicle_routes))
        return solution



    # costo por vehiculo
    def calculo_Coste(solution, df_distances, df_vehicles):
        total_cost = 0
        vehicle_costes = []
        for vehicle_name, routes in solution:
            vehicle = df_vehicles.loc[df_vehicles["vehiculo_id"] == vehicle_name]
            price_per_km = vehicle["costo_km"].values[0]
            vehicle_total = 0
            
            for route in routes:
                route_cost = sum(df_distances.iloc[route[i], route[i + 1]] for i in range(len(route) - 1))
                vehicle_total += route_cost * price_per_km
            total_cost += vehicle_total
            vehicle_costes.append((vehicle_name, vehicle_total))
        return total_cost, vehicle_costes


    def crear_Solucion(pheromones, df_distances, vehicle_capacity, orders):
        solution = []
        remaining_customers = set(range(1, n_nodes))  
        while remaining_customers:
            current_route = [0]  # "Decimos aqui desde donde empezamos" por ende decimos el almacen
            current_capacity = vehicle_capacity
            current_node = 0

            while remaining_customers:
                unvisited_nodes = [node for node in remaining_customers if orders[node] <= current_capacity]
                if not unvisited_nodes:  # Evitar excepciones
                    break

                # Llamada a funcion T2
                probabilities = calculo_Probabilidad(current_node, unvisited_nodes, pheromones, df_distances)
                next_node = np.random.choice(unvisited_nodes, p=probabilities)
                
                current_route.append(next_node)
                current_capacity -= orders[next_node]
                remaining_customers.remove(next_node)
                current_node = next_node

            current_route.append(0)  # regresamos hacia el almacen
            solution.append(current_route)
        return solution


    # costo de una solución
    def coste(solution, df_distances, price_per_km):
        total_cost = 0
        for route in solution:
            route_cost = sum(df_distances.iloc[route[i], route[i + 1]] for i in range(len(route) - 1))
            total_cost += route_cost * price_per_km
        return total_cost



    # Output
    solucion_optima = None
    mejor_precio = float('inf')

    for iteration in range(num_iterations):
        soluciones = []
        costes = []

        #Soluciones distintas, revisar para posibles mejores 
        for _ in range(num_vehiculos):
            solution = solucion_Vehiculo( df_distances, df_vehicles, df_customers["order_demand"])
            total_cost, vehicle_costes = calculo_Coste(solution, df_distances, df_vehicles)
            soluciones.append(solution)
            costes.append(total_cost)
            # Actualizar mejor solución
            if total_cost < mejor_precio:
                mejor_precio = total_cost
                solucion_optima = solution

        pheromone_matrix *= (1 - rho)
        for solution, cost in zip(soluciones, costes):
            for vehicle_name, routes in solution:
                for route in routes:
                    for i in range(len(route) - 1):
                        pheromone_matrix[route[i]][route[i + 1]] += Q / cost

    df_customers = pd.concat( #Añadimos esto(error de indice si quitamos esto)
        [pd.DataFrame({"Cliente": ["Almacén"], "order_demand": [0]}), df_customers],
        ignore_index=True
    )
    print("\nMejor solución encontrada:")
    
    print((solucion_optima))
    #print(mejor_precio)
    """
    for vehicle_name, routes in solucion_optima:
        print(f"Vehículo: {vehicle_name}")
        for i, route in enumerate(routes):
            print(df_customers.iloc)
            clientes = [df_customers.iloc[node]['cliente'] for node in route]
            print(f"  Ruta {i + 1}: {clientes}")
    print(f"Costo total: {mejor_precio}") """

    return solucion_optima , mejor_precio

ACO()