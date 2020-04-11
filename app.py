from __future__ import print_function
import os
import os.path
import subprocess
from flask import Flask, request, render_template, url_for, redirect, send_file,send_from_directory, jsonify
import pandas as pd
import numpy as np
import requests
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
app = Flask(__name__)

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(data['vehicle_id'][vehicle_id])
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(data['depot_id'][node_index], route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(data['depot_id'][manager.IndexToNode(index)],
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n\n'.format(route_load)
        total_distance += route_distance
        total_load += route_load
    plan_output+='Total distance of all routes: {}m\n'.format(total_distance)+'Total load of all routes: {}'.format(total_load)
    return (plan_output)
def create_data_model(name):
    data_file=pd.read_csv(name,dtype=str)
    data={}
    key=open('key','r')
    key=key.read()
    key=key[:-1]
    url='https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='
    origin=str(data_file.iloc[0,0])+','+str(data_file.iloc[0,1]) #warehouse coordinates are always index 0
    destinations=str(data_file.iloc[0,0])+','+str(data_file.iloc[0,1])
    data['depot_id']=['Warehouse']
    for i in range(0,len(data_file)):
        if (data_file.iloc[i,2]=='x'):
            break
        origin+=';'+str(data_file.iloc[i,2])+','+str(data_file.iloc[i,3])
        destinations+=';'+str(data_file.iloc[i,2])+','+str(data_file.iloc[i,3])
        if (str(data_file.iloc[i,5])=='nan'):
            data['depot_id'].append(data_file.iloc[i,5])
        else :
            data['depot_id'].append('Depot '+str(i))
    num_depots=i
    data['vehicle_id']=[]
    for i in range(0,len(data_file)):
        if (data_file.iloc[i,6]=='x'):
            break
        if (str(data_file.iloc[i,7])!='nan'):
            data['vehicle_id'].append(data_file.iloc[i,7])
        else :
            data['vehicle_id'].append(str(i))   
    travelMode='driving'
    num_vehicles=i
    url+=origin+'&'+'destinations='+destinations+'&travelMode='+travelMode+'&key='+key
    #print (url)
    distance_matrix = [[0 for i in range(num_depots+1)] for j in range(num_depots+1)]
    return_json=requests.get(url).json()['resourceSets'][0]['resources'][0]['results']
    for i in return_json:
        distance_matrix[i['originIndex']][i['destinationIndex']]=int(float(i['travelDistance'])*1000) #in metres
    data['distance_matrix']=distance_matrix
    data['depot']=0
    data['num_vehicles']=num_vehicles
    data['demands']=[0]
    for i in range(num_depots):
        data['demands'].append(float(data_file.iloc[i,4]))
    data['vehicle_capacities']=[]
    for i in range(num_vehicles):
         data['vehicle_capacities'].append(float(data_file.iloc[i,6]))
    return data
def compute_vrp(name):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(name)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console.
    print (data)
    if solution:
        return print_solution(data, manager, routing, solution)
    else :
        return 'No Possible Solution'

def is_csv(name):
    if (name[-4:]=='.csv' or name[-4:]=='.tmp'):
        return True
    else :
        return False
@app.route("/")
def fileFrontPage():
    return render_template('fileform.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload(): 
    print (request.files)
    if 'datax' in request.files: #all files should come in datax format
        data = request.files['datax']
        if data.filename != '' and is_csv(data.filename):
            os.system('rm -f *.csv')
            curr_path=os.getcwd()
            name = str(len([name for name in os.listdir('.') if os.path.isfile(name)]))+'.csv'
            data.save(name)
            sol = compute_vrp(name)
            fileName = name[:-4]+'_sol.csv'
            return (sol)#send_from_directory(os.getcwd(),fileName,as_attachment=True,attachment_filename=fileName)

       # else :
       #     return redirect(url_for('fileErrPage'))
    #else :
     #   return redirect(url_for('fileErrPage'))

    return redirect(url_for('fileFrontPage'))
if __name__=='__main__':
        app.run()