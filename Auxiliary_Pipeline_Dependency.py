import numpy as np
import pandas as pd
from scipy.linalg import norm
import matplotlib.pyplot as plt
import math
import os
import plotly.graph_objects as go
'''  This function detects which POI_id is the closest to the specific request .
     Finding_min_distance has two inputs:
     1. Geo information of the request in  Datasample cleaned
     2. All information of POIList_cleaned. 
    Output:  shortest distance between the sample instance and POI_id locations'''
def Finding_min_distance(request, POI_info):
    POI_ini = np.array([POI_info[0, 1], POI_info[0, 2]])
    min_distance = norm(request - POI_ini, None)
    for p in range(1, len(POI_info)):
        POI = np.array([POI_info[p, 1], POI_info[p, 2]])
        min_distance = np.hstack((min_distance, norm(request - POI, None)))
    return min_distance


'''   Label function adds two columns to the cleaned Datasample. 
      Output:  cleaned Datasample  with two more columns: Label and min_distance
      Label column determines the closest POI_id to each request. 
      min_distance indicts the distance between the request and label
      '''
def Label_function(Data, POI_info):
    IDs_length = len(Data)
    for i in range(IDs_length):
        request = Data.iloc[i]
        request_geoinfo = np.array([request['Latitude'], request['Longitude']])
        shortest_path = Finding_min_distance(request_geoinfo, POI_info)
        index = np.argmin(shortest_path)
        Data.loc[i, 'Label'] = POI_info[index, 0]
        Data.loc[i, 'min_distance'] = shortest_path[index]
    return Data


'''' Radius, density, average and standard deviation of the distance between 
     the POI and each of its assigned requests are determined using this function.'''

def Extract_statistical_info(Sub_group_sample):
    All_values = Sub_group_sample['min_distance']
    average=round(np.mean(All_values))
    sd=round(np.std(All_values))
    r = round(np.max(All_values))
    density = round(len(All_values) / (r ** 2 * math.pi))
    return r,density, sd, average
'''  Draw_circle draws a circle with the center at the POI within
     all its assigned requests.'''
def Draw_circle(Sub_group_sample, POI, r):
    fig, ax = plt.subplots()
    fig.dpi=100
    fig.figsize=(25,25)
    ax.scatter(POI[1], POI[2],s=2,color="r") ## center of circle
    ax.scatter(Sub_group_sample['Latitude'], Sub_group_sample['Longitude'],s=0.5,color="b")
    theta = np.linspace(0, 2*np.pi, 100)
    x1 = POI[1]+(r+1)*np.cos(theta)
    x2 = POI[2]+(r+1)*np.sin(theta)
    ax.plot(x1, x2,color='r')
    ax.set_aspect(1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.title(POI[0])
    plt.show()

'''Task4a: Assume we have  a set X={x_0,x_1,x_2,...,x_n} with n+1 points in R^N   .
How do we translate X to the range [-k, k ], with x 0 as the centre?
The following are the actions we must take:
1. Shift x_0 to the origin. We would change  You can do this by subtracting x_0 from each point 
X_shifted={0,x_1-x_0,x_2-x_0,...,x_n-x_0}
2- Measure the largest possible distance between all moved points and the origin. So, r_max <- max_{j} ||x_j-x_0|| 
3. Scale all points by 1/r_max. No we have a unit circle with origin center and all points located within it. 
Unit_circle={0,(x_1-x_0)/r_max,(x_2-x_0)/r_max,...,(x_n-x_0)/r_max}
3. Scale unit_circle by factor k; k-circle={0,k(x_1-x_0)/r_max,k(x_2-x_0)/r_max,...,k(x_n-x_0)/r_max}
Function Map_to gets all requests relevent to each POI as  Data_points,POI id as Center and scale factor as k.
The output is a translation of all assigned requests into a k-radius circle with origin center'''

def Map_to(Data_points, Center, k):
    points = Data_points[['Latitude', 'Longitude']].to_numpy()
    Shifted_points = points - Center
    r_max = np.max(norm(Shifted_points, axis=1))
    points_scaled = k * Shifted_points / r_max
    Data_points[['Latitude', 'Longitude']] = points_scaled
    Center = np.array([0, 0])
    return Data_points, Center

''' Draw_Maped_points function illustrates the popularity of all allocated requests in the circle with radius k  .'''
def Draw_Maped_points(requests_mapped,center,label,k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=requests_mapped['Latitude'], y=requests_mapped['Longitude'], mode="markers"))
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=center[0]-k, y0=center[1]-k,
        x1=center[0]+k, y1=center[1]+k,
        opacity=0.2,
        fillcolor="orange",
        line_color="orange",
    )
    fig.update_layout(title=label,title_x=0.5)
    fig.update_xaxes()
    fig.show()


'''Task4b: Pipeline Dependency'''
def Find_all_possible_paths(graph, start, end, path=[]):
    try:
        paths = []
        path = path + [start]
        if start == end:
            return [path]
        for node in graph[start]:
            if node not in path:
                newpaths = Find_all_possible_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    except:
        print('This start point does not exist. Please change start point')


