import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


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


def calculo_Probabilidad(current_node, unvisited_nodes, pheromones, df_distances):
    #Estas dos variables imprescindibles para ACO
    alpha = 1.0
    beta = 2.0
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
    
    # Evitar misma posicion entre clientes 
    if total == 0:
        probabilities = np.ones(len(unvisited_nodes)) / len(unvisited_nodes)
    else:
        probabilities = probabilities / total
    
    return probabilities

def solucion_Vehiculo(df_distances, df_vehicles_shuffled, orders,pheromone_matrix, autonomia_restante=None):
    solution = []
    remaining_customers = set(range(20))
    depot = 20

    if autonomia_restante is None:
        autonomia_restante = {row["vehiculo_id"]: row["autonomia_km"] for _, row in df_vehicles_shuffled.iterrows()}

    for _, vehicle in df_vehicles_shuffled.iterrows():  # Usar el DataFrame reordenado
        vehicle_id = vehicle["vehiculo_id"]
        vehicle_routes = []
        vehicle_capacity = vehicle["capacidad_kg"]
        current_autonomy = autonomia_restante[vehicle_id]

        while remaining_customers and current_autonomy > 0:
            current_route = [depot]  # Inicia en el almacén
            current_capacity = vehicle_capacity
            current_node = depot
            total_distance = 0

            while remaining_customers:
                unvisited_nodes = [
                    node for node in remaining_customers
                    if orders[node] <= current_capacity 
                    and (total_distance + df_distances.iloc[current_node, node] + df_distances.iloc[node, depot]) <= current_autonomy
                ]

                if not unvisited_nodes:
                    break

                probabilities = calculo_Probabilidad(current_node, unvisited_nodes, pheromone_matrix, df_distances)
                next_node = np.random.choice(unvisited_nodes, p=probabilities)

                distance_to_next = df_distances.iloc[current_node, next_node]
                total_distance += distance_to_next
                current_autonomy -= distance_to_next

                current_route.append(next_node)
                current_capacity -= orders[next_node]
                remaining_customers.remove(next_node)
                current_node = next_node

            # Verificar si se agregaron clientes a la ruta
            if len(current_route) == 1:  # Solo el almacén, no hay clientes
                break  # Salir del bucle externo para este vehículo
            else:
                # Regresar al almacén y actualizar autonomía
                distance_to_depot = df_distances.iloc[current_node, depot]
                current_autonomy -= distance_to_depot
                current_route.append(depot)
                if len(current_route) > 2:
                    vehicle_routes.append(current_route)

            # Actualizar autonomía restante después de cada ruta
            autonomia_restante[vehicle_id] = current_autonomy

        if vehicle_routes:
            solution.append((vehicle_id, vehicle_routes))

    return solution, autonomia_restante


def ACO(caso, df_distances, df_vehicles, df_customers):
    # Parámetros de ACO
    num_vehiculos = 6
    num_iterations = 100
    rho = 0.5
    Q = 100

    n_nodes = len(df_customers)+1
    pheromone_matrix = np.ones((n_nodes, n_nodes))

    if caso == 2 :
        num_vehiculos = 3

    solucion_optima = None
    mejor_precio = float('inf')

    for iteration in range(num_iterations):
        # Reordenar aleatoriamente los vehículos en cada iteración
        df_vehicles_shuffled = df_vehicles.sample(frac=1).reset_index(drop=True)

        soluciones = []
        costes = []

        for _ in range(num_vehiculos):
            solution, _ = solucion_Vehiculo(df_distances, df_vehicles_shuffled, df_customers["order_demand"],pheromone_matrix, None)
            total_cost, _ = calculo_Coste(solution, df_distances, df_vehicles_shuffled)
            soluciones.append(solution)
            costes.append(total_cost)

            if total_cost < mejor_precio:
                mejor_precio = total_cost
                solucion_optima = solution

        # Actualizar feromonas
        pheromone_matrix *= (1 - rho)
        for solution, cost in zip(soluciones, costes):
            for vehicle_name, routes in solution:
                for route in routes:
                    for i in range(len(route) - 1):
                        pheromone_matrix[route[i]][route[i + 1]] += Q / cost

    print(solucion_optima, mejor_precio)
    return solucion_optima, mejor_precio

