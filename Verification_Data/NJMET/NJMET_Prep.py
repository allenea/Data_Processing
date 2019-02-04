#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated on Monday February  4th, 2019

@author: Eric Allen
email: allenea@udel.edu
University of Delaware
Clouds_Wind_Climate Research Group and DEOS

Reformat the DEOS data to include the metadata for each station.
Some of this information is redundant but everything in the original data file
and more is here. The time has been parsed (YYYY  MM DD HH mm ).
User should decide what he/she would like to use when reading in the output file.
Feel free to modify for your own needs.

If you do not need to parse time I highly consider removing the parsing. That 
adds a lot more CPU time for the program to finish. But if you will eventually 
need to parse the time then you might as well do it now. 

********Combines Sensor heights with elevation  and assigned to the elevation variable ********
"""

import numpy as np
import pandas as pd
import glob
from dateutil.parser import parse
import datetime
import os

def temperature_F_to_K(temp_F):
    return 5./9 * (temp_F - 32) + 273.15

def merge_csv(file1,file2):
    a = pd.read_csv(file1, low_memory=False)
    b = pd.read_csv(file2, low_memory=False)
    merged = pd.concat([a,b])
    merged.to_csv(mydir + '/Merged/'+file1[:-19]+"-njmet-verify-data.csv", index=False)

    
mydir =   os.getcwd()
#Makes data frame of metadata 
df = pd.read_csv(mydir+"/NJMesonet_Metadata_csv.csv", low_memory=False)

stationName = df['Station_Name']
callSign = df['CallSign']
#state = df['ST']
latitude = df['Latitude']
longitude = df['Longitude']
elevation = df['Elevation']
sensor_height = df['Sensor_Height']

#Include additional parameters for WRF Data Assimilation
FM_Code = 'FM-12 SYNOP'
Source_Code = 'New Jersey Mesonet'
  
### SET PATHS
wkdir =   os.getcwd()+"/Raw/"  
outdir = os.getcwd()+'/Reformatted/'
os.chdir(wkdir)

#for each formatted file with DEOS data in the folder this program is executed         
fileList=glob.glob('*.csv')
fileList.sort()
mergedList = []
for file1 in fileList:
    for file2 in fileList:
        if file1[:-19] == file2[:-19] and file1 !=file2 and file1[:-19] not in mergedList:
            #print file1, file2
            merge_csv(file1,file2)
            mergedList.append(file1[:-19])
            print ("MERGED", file1[:-19])
        elif file1[:-19] != file2[:-19] and file1!=file2 and file1[:-19] not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mydir + '/Merged/'+file1[:-19]+"-njmet-verify-data.csv", index=False)
            print ("SINGLE" , file1[:-19])
        elif file1[:-19] == file2[:-19] and file1==file2 and file1[:-19] not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mydir + '/Merged/'+file1[:-19]+"-njmet-verify-data.csv", index=False)
            print ("SINGLE" , file1[:-19])
print (fileList)


os.chdir(mydir+"/Merged/")
#%%
HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)',\
          'Pressure (Pa)','Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string','Elevation (m)','Wind_Sensor_Height (m)']
float64 = np.float64
InHeader = ["Station","Date/Time","Tempavg_5min","DPavg_5min","windspavg_5min","winddiravg_5min","RHavg_5min","BPavg_5min"]

dtypesDict={"Station": object, "Date/Time":object, "Tempavg_5min":float64,\
            "DPavg_5min":float64, "windspavg_5min"  : float64,\
            "winddiravg_5min" :float64, "RHavg_5min" :float64,\
            "BPavg_5min":float64}


#for each formatted file with DEOS data in the folder this program is executed         
for file in glob.glob('*.csv'):
    print (file)
    #trim to only include the 4 letter station name
    fileName = file[:-22]
    print (fileName)
    
    #Read it in
    station_data = pd.read_csv(file, dtype=dtypesDict)
    station_data = station_data.drop(station_data.columns[len(InHeader):], axis=1)    
    
    station_data.columns = InHeader
    station_data = station_data.mask(station_data == -999.0, other= np.nan)
    station_data = station_data.mask(station_data == "", other= np.nan)
    station_data = station_data.mask(station_data == " ", other= np.nan)
    station_data = station_data.mask(station_data == 0, other= np.nan)
    station_data = station_data.mask(station_data == "NaN", other= np.nan)

    #Parse Time_Stamp to individual Columns  
    sizeNew2 = int(len(station_data["Date/Time"]))

    newTime = [0]*sizeNew2;
    for i in range(sizeNew2):
        d = parse(station_data["Date/Time"][i])
        utc_dt = datetime.datetime(int(d.year),int(d.month),int(d.day),int(d.hour),int(d.minute),int(d.second))
        newTime[i] = utc_dt.strftime('%Y%m%d%H%M%S')

    
    #Add a directory path if you want
    outstring = outdir+fileName+"-w-Metadata.csv"
    
    newData = np.zeros((len(station_data),len(HEADER)))

    #See if it matches any of the stations in the metadata file
    for idx in range(len(stationName)):
        #If it does add the metadata to the file
        if stationName[idx] == fileName:
            #Parse Time Data- You could cut this part to save lots of CPU time.
            newData[:,1] = newTime
            try:
                newData[:,2] = station_data['windspavg_5min'] * 0.44704
            except:
                print ("No Wind Speed Data " + callSign[idx])
                newData[:,2] = -888888.0
                
            try:
                newData[:,3] = station_data['winddiravg_5min']
            except:
                print ("No Wind Direction Data " + callSign[idx])
                newData[:,3] = -888888.0
                
            try:
                newData[:,4] = [temperature_F_to_K(temp) for temp in station_data["Tempavg_5min"]]
            except:
                print ("No Air Temperature Data "+ callSign[idx])
                newData[:,4] = -888888.0
            try:
                newData[:,5] = [temperature_F_to_K(td) for td in station_data['DPavg_5min']]
            except:
                print ("No Dew Point Temperature Data "+ callSign[idx])
                newData[:,5] = -888888.0    
            try:
                newData[:,6] = station_data['RHavg_5min']
            except:
                print ("No RH Data " + callSign[idx])
                newData[:,6] = -888888.0
            try:
                newData[:,7] = station_data['BPavg_5min'] * 3386.389
            except:
                print ("No Barometric Pressure " + callSign[idx])
                newData[:,7] =  -888888.0
                
            newData[:,8] = latitude[idx]    
            newData[:,9] = longitude[idx]
            newData[:,10] = elevation[idx]+ sensor_height[idx]  ## USE THIS IN DA
            newData[:,14] = elevation[idx]
            newData[:,15] = sensor_height[idx]

            print ("Sensor Height ",callSign[idx],"  =  ",sensor_height[idx])
            
            dfwrite = pd.DataFrame(newData, columns = HEADER)
            
            dfwrite["ID_String"]= callSign[idx]   #0
            dfwrite["Name_string"]= stationName[idx]#11
            dfwrite["FM_string"]=FM_Code #12
            dfwrite["Source_string"]=Source_Code #13
                    
            #dfwrite = dfwrite.mask(dfwrite == np.nan, -888888.0)
            #dfwrite = dfwrite.mask(dfwrite == '',  -888888.0)

            #Concatenate the DataFrames 
            output_data= dfwrite

            #Save the output file
            output_data.to_csv(outstring,index=False)