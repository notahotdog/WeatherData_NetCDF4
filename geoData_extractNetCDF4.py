#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:21:35 2021

@author: umarmoiz
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time 



# Steps 
# 1. Load data to be assesed
# 2. Find interested data to be extracted 








#Reading in the netCDF4 File
data = Dataset("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/global-analysis-forecast-wav-001-027_1613370842929.nc","r")

#Displaying the name of the variables 
print(data.variables.keys())

#Accessing the variables
lat = data.variables["latitude"][:]
lon = data.variables["longitude"][:]
vmdr = data.variables["VMDR_WW"]





print(lat)
print(lon)
#print(time)

#print(vmdr)

#Accessing data of variables

time_data = data.variables["time"][:]
latitude_data = data.variables["latitude"][:]
longitude_data = data.variables["longitude"][:]
print("time data:" , time_data)





#Extact files from excel

loc_source = pd.read_excel("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_2_ds.xlsx")
# print(loc_source)

loc = pd.DataFrame(loc_source, columns=["Latitude","Longitude"]) #columns need to match act columns
print(loc)




#Array of weather data
latArr = [14.8,25.51307667,0.655536667,-20.26840167,-23.8468]
lonArr = [114.525,121.0867167,150.37217,153.43839,151.6321783]


#for each time, extract weather data

indexCtr = 0
coCtr = 0

timeDataLen = data.variables["time"].size #No of time data
cOrdLen = len(loc.index) #Number of coordinates from the excel file


#used to evaluate the specific parameter
def eval_param_VDMR(lat,lon,lat_vessel,lon_vessel,time):
    #Square difference of lat and lon
    sq_diff_lat = (lat - lat_vessel)**2
    sq_diff_lon = (lon - lon_vessel)**2

    #Identifying the index of the minimum value of lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    
    
    vmdr = data.variables["VMDR_WW"]
    
    # print("VDMR: ", vmdr[time,min_index_lat,min_index_lon])
    
    return vmdr[time,min_index_lat,min_index_lon]
    


#Creating index 
indexList = []
setIndexCtr = 0
for setIndex in range(timeDataLen * cOrdLen):
    indexList.append(setIndexCtr)
    setIndexCtr += 1
    
print("Index List:" , indexList)


# Creating an empty pandas dataframe
df = pd.DataFrame(0,columns=["time","Latitude","Longitude","VDMR"],index = indexList)


print(df)

ctr = 0
for each_time in range(0, timeDataLen):
    for index, row in loc.iterrows():
        #set the latitiude and longtitude 
        
        # Set Current vessel loc
        lat_eval = row["Latitude"]
        lon_eval = row["Longitude"]
        print("Index:", coCtr, "Time: ",time_data[each_time], "Lat Evaluated:", lat_eval, "Lon Eval:", lon_eval, )
        print("VDMR Value: ", eval_param_VDMR(latitude_data,longitude_data,lat_eval,lon_eval,each_time))
        
        df.iloc[ctr, 0] = time_data[each_time]
        df.iloc[ctr, 1] = lat_eval
        df.iloc[ctr, 2] = lon_eval
        df.iloc[ctr, 3] = eval_param_VDMR(latitude_data,longitude_data,lat_eval,lon_eval,each_time)
       
        #Update the Pandas Dataframe with the appropriate values
        ctr += 1

print(df)
   

file_name = input("Set you file name:") + ".csv"
print("Your file name is: ", file_name )

df,to_csv(file_name)

# df.to_csv("vdmr_loc2.csv")

   
   