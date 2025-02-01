import numpy as np
import pandas as pd
import random
from decimal import Decimal, getcontext

# Configurar precisión decimal
getcontext().prec = 8

def calculo_Coste(solution, df_distances, df_vehicles):
    total_cost = Decimal('0')
    vehicle_costes = []
    
    for vehicle_name, routes in solution:
        vehicle = df_vehicles.loc[df_vehicles["vehiculo_id"] == vehicle_name]
        price_per_km = Decimal(str(vehicle["costo_km"].values[0]))
        vehicle_total = Decimal('0')
        
        for route in routes:
            # Calcular distancia exacta de la ruta
            route_distance = sum(Decimal(str(df_distances.iloc[route[i], route[i + 1]])) 
                               for i in range(len(route) - 1))
            
            # Calcular costo con precisión decimal
            route_cost = route_distance * price_per_km
            vehicle_total += route_cost
        
        # Redondear solo al final para el vehículo
        vehicle_total = vehicle_total.quantize(Decimal('0.00'))
        total_cost += vehicle_total
        vehicle_costes.append((vehicle_name, float(vehicle_total)))
    
    # Redondear total final
    total_cost = total_cost.quantize(Decimal('0.00'))
    return float(total_cost), vehicle_costes

def calculo_Probabilidad(current_node, unvisited_nodes, pheromones, df_distances):
    alpha = 1.0
    beta = 2.0
    probabilities = []
    
    for node in unvisited_nodes:
        distance = df_distances.iloc[current_node, node]
        if distance > 0:  
            tau = pheromones[current_node][node] ** alpha
            eta = (1 / float(distance)) ** beta  # Usar float para operaciones numéricas
            probabilities.append(tau * eta)
        else:
            probabilities.append(0)  
    
    total = sum(probabilities)
    
    if total == 0:
        return [1/len(unvisited_nodes)] * len(unvisited_nodes)
    return [p/total for p in probabilities]

def solucion_Vehiculo(df_distances, df_vehicles_shuffled, orders, pheromone_matrix, autonomia_restante=None):
    solution = []
    remaining_customers = set(range(20))
    depot = 20

    if autonomia_restante is None:
        autonomia_restante = {row["vehiculo_id"]: Decimal(str(row["autonomia_km"])) 
                            for _, row in df_vehicles_shuffled.iterrows()}

    for _, vehicle in df_vehicles_shuffled.iterrows():
        vehicle_id = vehicle["vehiculo_id"]
        vehicle_routes = []
        vehicle_capacity = Decimal(str(vehicle["capacidad_kg"]))
        current_autonomy = autonomia_restante[vehicle_id]

        while remaining_customers and current_autonomy > Decimal('0'):
            current_route = [depot]
            current_capacity = vehicle_capacity
            current_node = depot
            total_distance = Decimal('0')

            while remaining_customers:
                # Convertir a float para comparación
                available_customers = [
                    node for node in remaining_customers
                    if Decimal(str(orders[node])) <= current_capacity 
                    and (total_distance + 
                         Decimal(str(df_distances.iloc[current_node, node])) + 
                         Decimal(str(df_distances.iloc[node, depot])) <= current_autonomy)
                ]

                if not available_customers:
                    break

                probabilities = calculo_Probabilidad(current_node, available_customers, 
                                                    pheromone_matrix, df_distances)
                next_node = np.random.choice(available_customers, p=probabilities)

                distance_to_next = Decimal(str(df_distances.iloc[current_node, next_node]))
                total_distance += distance_to_next
                current_autonomy -= distance_to_next

                current_route.append(next_node)
                current_capacity -= Decimal(str(orders[next_node]))
                remaining_customers.remove(next_node)
                current_node = next_node

            if len(current_route) > 1:
                distance_to_depot = Decimal(str(df_distances.iloc[current_node, depot]))
                total_distance += distance_to_depot
                current_autonomy -= distance_to_depot
                current_route.append(depot)
                vehicle_routes.append(current_route)

            autonomia_restante[vehicle_id] = current_autonomy

        if vehicle_routes:
            solution.append((vehicle_id, vehicle_routes))

    return solution, autonomia_restante

def ACO(caso, df_distances, df_vehicles, df_customers):
    num_vehiculos = 6
    num_iterations = 100
    rho = 0.5
    Q = Decimal('100')

    n_nodes = len(df_customers) + 1
    pheromone_matrix = np.ones((n_nodes, n_nodes))

    if caso == 2:
        num_vehiculos = 3

    mejor_solucion = None
    mejor_costo = Decimal('Infinity')

    for _ in range(num_iterations):
        df_vehicles_shuffled = df_vehicles.sample(frac=1).reset_index(drop=True)
        soluciones = []
        costes = []

        for _ in range(num_vehiculos):
            solution, _ = solucion_Vehiculo(df_distances, df_vehicles_shuffled, 
                                          df_customers["order_demand"], pheromone_matrix)
            costo_total, _ = calculo_Coste(solution, df_distances, df_vehicles_shuffled)
            costo_decimal = Decimal(str(costo_total))
            
            soluciones.append(solution)
            costes.append(costo_decimal)

            if costo_decimal < mejor_costo:
                mejor_costo = costo_decimal
                mejor_solucion = solution

        # Actualización de feromonas con precisión decimal
        pheromone_matrix *= (1 - rho)
        for solucion, costo in zip(soluciones, costes):
            if costo == 0:
                continue
            deposito_feromona = Q / costo
            for _, rutas in solucion:
                for ruta in rutas:
                    for i in range(len(ruta) - 1):
                        pheromone_matrix[ruta[i]][ruta[i+1]] += float(deposito_feromona)

    print(f"Mejor costo encontrado: {mejor_costo:.2f}")
    return mejor_solucion, mejor_costo