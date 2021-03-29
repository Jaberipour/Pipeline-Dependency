'''Date: 2/28/2021
   Email: majid.jaberipour@gmail.com'''
import numpy as np
import pandas as pd
from scipy.linalg import norm
import matplotlib.pyplot as plt
import math
import os
import plotly.graph_objects as go
from Auxiliary import *
import warnings
warnings.filterwarnings("ignore")

cwd = os.getcwd()
'Read DataSample and POIList'
DataSample= pd.read_csv('DataSample.csv')
POIList= pd.read_csv('POIList.csv')
'''Cleanup DataSample CSV and POIList CSV files '''

'''****************************1. Cleanup  ********************'''

DS_cleaned = DataSample.drop_duplicates(subset=[' TimeSt','Latitude','Longitude'], keep='first',ignore_index=True)
POIList_cleaned = POIList.drop_duplicates(subset=[' Latitude','Longitude'], keep='first',ignore_index=True)
print('***1. Cleanup was done***')

'''****************************2. Label  **********************'''

'''Convert POIList_cleaned to numpy array'''
POI_info=POIList_cleaned.to_numpy()
''' ADD Label and distance columns to cleaned datasample '''
DS=Label_function(DS_cleaned, POI_info )
print('***2. Label was done ***')

for p in range(len(POI_info)):
    POI=POI_info[p]
    label=POI[0]
    print('--------------------')
    print('Selected POI : ', label)
    '''Find all requests related to POI id'''
    Assigned_requests=DS[DS['Label']==label]
    '''****************************3. Analysis  **********************'''
    '''Calculate Mean, sd, density and redius'''
    r, density, sd, average = Extract_statistical_info(Assigned_requests)
    print('[Radius, Density, Standard deviation, Average] :', [r, density, sd, average])
    '''Draw circle with r radius, POI as a center and its assigned requests'''
    Draw_circle(Assigned_requests, POI, r)
    print('***3. Analysis was done ***')
    '''****************************4a. Model  **********************'''
    Center = np.array([POI[1], POI[2]])
    '''Map all assigned requests to range [-10,10]'''
    requests_transformed, Origin = Map_to(Assigned_requests, Center, 10)
    '''Draw circle with radius 10, POI center and its translated requests'''
    Draw_Maped_points(requests_transformed, Origin,label, 10)
    print('***Task 4a was done***')
    '''****************************4b. Pipeline Dependency  **********************'''

graph = {'97': ['102', ],
             '75': ['31', '37'],
             '100': ['20'],
             '102': ['31', '37', '36'],
             '16': ['37'],
             '39': ['73', '100'],
             '41': ['73', '112'],
             '62': ['55'],
             '112': ['97'],
             '20': ['94', '97'],
             '21': ['20'],
             '73': ['20'],
             '56': ['102', '75', '55'],
             '55': ['31', '37'],
             '94': ['56', '102'],
             '36': [],
             '37': [],
             '31': []
             }

'''Find all paths starts from task 73 and ends at task 36
    output is : [['73', '20', '94', '56', '102', '36'],
                 ['73', '20', '94', '102', '36'],
                 ['73', '20', '97', '102', '36']]'''

paths=Find_all_possible_paths(graph, '73', '36', path=[])
print('All Paths:', paths)
print('***Task 4b was done***')


