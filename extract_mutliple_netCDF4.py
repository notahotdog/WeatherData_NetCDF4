#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:52:07 2021

@author: umarmoiz
"""


from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time 
from datetime import datetime,timedelta
from cftime import num2date



#Asks for the long lat of the file intended,
#returns the timing for each long lat issued.






print("Welcome to NEetCDF4 Data Extractor")
data_file = input("Please input the file_path of the netCDF4 data you wish to extract from: \n")

#Extracts the data from the netCDF4 file 
print("-------")
data = Dataset(data_file)
time_data = data.variables["time"][:]
latitude_data = data.variables["latitude"][:]
longitude_data = data.variables["longitude"][:]
print("time data:" , time_data)
print(data.variables.keys())


# #Extact files from excel

# loc_source = pd.read_excel("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_2_ds.xlsx")
# # loc_source = pd.read_excel("/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_2_ds.xlsx")

# # print(loc_source)

# loc = pd.DataFrame(loc_source, columns=["Latitude","Longitude"]) #columns need to match act columns
# # print(loc)

# #Obtain a list of sources to extract from






def eval_param(lat,lon,lat_vessel,lon_vessel,time,metric):
    
      #Square difference of lat and lon
    sq_diff_lat = (lat - lat_vessel)**2
    sq_diff_lon = (lon - lon_vessel)**2

    #Identifying the index of the minimum value of lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    
    #the metric is a string that is used to evaluate the metric
    
    return data.variables[metric][time,min_index_lat,min_index_lon]
 



#Function will extract netCDF4 and save file with time and location
def retrieveData(loc):

#for each time, extract weather data
    loc = loc
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



    print(df)



    print(time_data)
    # formatted_time_data = num2date(time_data[:], units = time_data.units, calendar = time_data.calendar)

    # print(formatted_time_data)

    ctr = 0
    for each_time in range(0, time_data_len):
        for index, row in loc.iterrows():
        #set the latitiude and longtitude 
        
        # Set Current vessel loc
            lat_eval = row["Latitude"]
            lon_eval = row["Longitude"]
            # print("Index:", coCtr, "Time: ",time_data[each_time], "Lat Evaluated:", lat_eval, "Lon Eval:", lon_eval, )
            # print("VMDR Value: ", eval_param_VMDR(latitude_data,longitude_data,lat_eval,lon_eval,each_time))
            print("." + str(ctr))
            for each_metric in range(3 + metricCtr):
                if each_metric == 0:
                    df.iloc[ctr, each_metric] = time_data[each_time]
                    # num2date(time_data[each_time],units=time_data.units, calendar=times.calendar)
                elif each_metric == 1:
                    df.iloc[ctr, 1] = lat_eval
                elif each_metric == 2:
                    df.iloc[ctr, 2] = lon_eval
                else:
                    df.iloc[ctr, each_metric] = eval_param(latitude_data,longitude_data,lat_eval,lon_eval,each_time,metricList[each_metric-3])# retrieve the data equivalent
                

        #Update the Pandas Dataframe with the appropriate values
            ctr += 1

    print(df)
   
   

# file_name = input("Set you file name:") + ".csv"
    file_name = "glob_analysis_dataset_" + input("select file number: ") + ".csv"
    print("Your file name is: ", file_name )

    df.to_csv(file_name)








#This is the location to be extracted for each vessel
location_source_extract = [
    # "/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_1_ds.xlsx",
    # "/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/loc_2_ds.xlsx"
    # "/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/SOG_loc_data/SantaGracielaLoc.xlsx"
    "/Users/umarmoiz/Desktop/AIS_ML_Project/Weather_Data/weather_data_code/SOG_loc_data/capicornloc.xlsx"
 ]



 





locArr = []
for each_loc_source in location_source_extract:
    loc = pd.DataFrame(pd.read_excel(each_loc_source),columns=["Latitude","Longitude"])
    
    #Extracts data and save details
    print("Evaluating File")
    retrieveData(loc)
    
    

print("Donezo")

