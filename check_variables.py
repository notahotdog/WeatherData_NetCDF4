#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:04:31 2021

@author: umarmoiz
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time 


print("Welcome to NEetCDF4 Data Extractor")
data_file = input("Please input the file_path of the data you wish to extract from: \n")

# print("The file path is : ", data_file)

print("-------")

data = Dataset(data_file)
time_data = data.variables["time"][:]
latitude_data = data.variables["latitude"][:]
longitude_data = data.variables["longitude"][:]
print("time data:" , time_data)



# print("Time data :", time_data )


print(data.variables.keys())


#Extact files from excel

loc_source = pd.read_excel("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/q1b_19_01.xlsx")
# loc_source = pd.read_excel("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_2_ds.xlsx")

# print(loc_source)

loc = pd.DataFrame(loc_source, columns=["Latitude","Longitude"]) #columns need to match act columns
# print(loc)






#for each time, extract weather data

indexCtr = 0
coCtr = 0
time_data_len = data.variables["time"].size #No of time data
cOrdLen = len(loc.index) #Number of coordinates from the excel file



#Creating index 
indexList = []
setIndexCtr = 0
for setIndex in range(time_data_len * cOrdLen):
    indexList.append(setIndexCtr)
    setIndexCtr += 1
    
# print("Index List:" , indexList)


#need to modify the columns array depending on the requirements of the user
#Enter variables you are interested in , parse the , and put it withing the col

#columns shoudl be set according to the list of metrics





# List of functions to extract 
# def eval_param_VMDR(lat,lon,lat_vessel,lon_vessel,time):
#     #Square difference of lat and lon
#     sq_diff_lat = (lat - lat_vessel)**2
#     sq_diff_lon = (lon - lon_vessel)**2

#     #Identifying the index of the minimum value of lat and lon
#     min_index_lat = sq_diff_lat.argmin()
#     min_index_lon = sq_diff_lon.argmin()
    
    
#     # vmdr = data.variables["VMDR_WW"]
    
#     # print("VMDR: ", vmdr[time,min_index_lat,min_index_lon])
    
#     return vmdr[time,min_index_lat,min_index_lon]
    



def eval_param(lat,lon,lat_vessel,lon_vessel,time,metric):
    
      #Square difference of lat and lon
    sq_diff_lat = (lat - lat_vessel)**2
    sq_diff_lon = (lon - lon_vessel)**2

    #Identifying the index of the minimum value of lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    
    #the metric is a string that is used to evaluate the metric
    
    return data.variables[metric][time,min_index_lat,min_index_lon]
    

#Select Parameters to be evaluated

print("Please enter the metrics you wish to extract, once done type in 'done'")

metricCtr = 0
metricList = []
not_done = True
while(not_done):
    metric_selector = input("Metric :")
    if(metric_selector == "done"):
        not_done == False #not necessary i know
        break
    metricList.append(metric_selector)
    metricCtr += 1

print("The metric you have selected are : ", metricList )



columnHeadings = ["time","Latitude","Longitude"] + metricList

# Creating an empty pandas dataframe
df = pd.DataFrame(0,columns=columnHeadings,index = indexList)



# # Creating an empty pandas dataframe
# df = pd.DataFrame(0,columns=["time","Latitude","Longitude","VMDR","VMDR"],index = indexList)



print(df)

ctr = 0
for each_time in range(0, time_data_len):
    for index, row in loc.iterrows():
        #set the latitiude and longtitude 
        
        # Set Current vessel loc
        lat_eval = row["Latitude"]
        lon_eval = row["Longitude"]
        # print("Index:", coCtr, "Time: ",time_data[each_time], "Lat Evaluated:", lat_eval, "Lon Eval:", lon_eval, )
        # print("VMDR Value: ", eval_param_VMDR(latitude_data,longitude_data,lat_eval,lon_eval,each_time))
        
        for each_metric in range(3 + metricCtr):
            if each_metric == 0:
                df.iloc[ctr, each_metric] = time_data[each_time]
            elif each_metric == 1:
                df.iloc[ctr, 1] = lat_eval
            elif each_metric == 2:
                df.iloc[ctr, 2] = lon_eval
            else:
                df.iloc[ctr, each_metric] = eval_param(latitude_data,longitude_data,lat_eval,lon_eval,each_time,metricList[each_metric-3])# retrieve the data equivalent
                

        #Update the Pandas Dataframe with the appropriate values
        ctr += 1

print(df)
   


# print(df)

# ctr = 0
# for each_time in range(0, time_data_len):
#     for index, row in loc.iterrows():
#         #set the latitiude and longtitude 
        
#         # Set Current vessel loc
#         lat_eval = row["Latitude"]
#         lon_eval = row["Longitude"]
#         # print("Index:", coCtr, "Time: ",time_data[each_time], "Lat Evaluated:", lat_eval, "Lon Eval:", lon_eval, )
#         # print("VMDR Value: ", eval_param_VMDR(latitude_data,longitude_data,lat_eval,lon_eval,each_time))
        
        
#         df.iloc[ctr, 0] = time_data[each_time]
#         df.iloc[ctr, 1] = lat_eval
#         df.iloc[ctr, 2] = lon_eval
#         df.iloc[ctr, 3] = eval_param(latitude_data,longitude_data,lat_eval,lon_eval,each_time,"VMDR_WW")
        
#         # df.iloc[ctr, 3] = eval_param_VMDR(latitude_data,longitude_data,lat_eval,lon_eval,each_time)
       
#         #Update the Pandas Dataframe with the appropriate values
#         ctr += 1

# print(df)
   

# file_name = input("Set you file name:") + ".csv"
file_name = "glob_analysis_dataset_" + input("select file number: ") + ".csv"
print("Your file name is: ", file_name )

df.to_csv(file_name)