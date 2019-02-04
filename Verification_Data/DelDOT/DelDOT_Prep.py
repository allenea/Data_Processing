
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated on Monday March  5th, 2018

@author: Eric Allen
email: allenea@udel.edu
University of Delaware
Clouds_Wind_Climate Research Group and DEOS

Reformat the DelDOT weather data to include the metadata for each station.

The metadata was collected from Google Earth/Maps and added manually to the spreadsheet 
DelDOT_metadata.csv

Some of this information is redundant but everything in the original data file
and more is here. The time has been parsed (YYYY  MM DD HH mm ). DATA WAS OBTAINED IN UTC.
User should decide what he/she would like to use when reading in the output file.
Feel free to modify for your own needs.

If you do not need to parse time I highly consider removing the parsing. That 
adds a lot more CPU time for the program to finish. But if you will eventually 
need to parse the time then you might as well do it now. 

********Combines Sensor heights with elevation  and assigned to the elevation variable ********

"""
import pandas as pd
import glob
from dateutil.parser import parse
import datetime
import os
import numpy as np
from merge_like_files import merge_like_files
#%%
mydir = os.getcwd()
merge_like_files()

outdir = mydir+'/Reformatted/'

#Makes data frame of metadata 
float64 = np.float64
dddtypes = {"Timestamp (UTC)": object, "Air Temperature(deg. C)":float64,\
                "Dew Point Temperature(deg. C)":float64, "Wind Speed(m/sec)":float64,\
                "Wind Direction(deg.)":float64, "Barometric Pressure()":float64,\
                "Solar Radiation()":float64, "Wind Gust Speed (5)()": float64,\
                "Gage Precipitation (5)()":object}

df = pd.read_csv(mydir+"/DelDOT_metadata.csv", low_memory=False)
stationName = df['Station Name']
callSign = df['Call Sign']
#county = df['County']
#state = df['ST']
latitude = df['Latitude (DD)']
longitude = df['Longitude (DD)']
elevation = df['Elev (m)']
sensor_height = df['Sensor_Height (m)']


#Include additional parameters for WRF Data Assimilation
FM_Code = 'FM-12 SYNOP'
Source_Code = 'Delaware_Department_of_Transportation_QC'


os.chdir(mydir+"/Merged/")
#%%
#for each formatted file with DEOS data in the folder this program is executed         
allfiles = glob.glob("*.csv")
allfiles.sort()
#%%

HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
          'Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string',\
          'Elevation (m)','Wind_Sensor_Height (m)']
    
    
for file in allfiles:
    print (file)
    station_data = pd.read_csv(file, dtype=dddtypes)
    
    #Parse Time_Stamp to individual Columns  
    sizeNew2 = int(len(station_data["Timestamp (UTC)"]))
    
    station_data[' Air Temperature(deg. C)'] = station_data[' Air Temperature(deg. C)'].mask(station_data[' Air Temperature(deg. C)'] > 200, other = -888888.0)
    station_data[' Dew Point Temperature(deg. C)'] = station_data[' Dew Point Temperature(deg. C)'].mask(station_data[' Dew Point Temperature(deg. C)'] > 200, other = -888888.0)
    station_data = station_data.mask(station_data == -888888.0, other = np.nan)


    newTime = [0]*sizeNew2;
    for i in range(sizeNew2):
        d = parse(station_data["Timestamp (UTC)"][i])
        utc_dt = datetime.datetime(int(d.year),int(d.month),int(d.day),int(d.hour),int(d.minute),int(d.second))
        newTime[i] = utc_dt.strftime('%Y%m%d%H%M%S')
    
    #trim to only include the 2 number station #
    fileName = file[4:6]

    newData = np.zeros((len(station_data),len(HEADER)))
    
    #See if it matches any of the stations in the metadata file
    for idx in range(len(callSign)):
        #If it does add the metadata to the file
        if callSign[idx][-2:] == fileName:
            outstring = outdir+callSign[idx]+"-w-Metadata.csv"

            #Parse Time Data- You could cut this part to save lots of CPU time.
            newData[:,1] = newTime
            print ("Sensor Height ",callSign[idx],"  =  ",sensor_height[idx])

            try:
                newData[:,2] = station_data[' Wind Speed(m/sec)']
            except:
                print ("No Wind Speed Data " + callSign[idx])
                newData[:,2] = -888888.0
                
            try:
                newData[:,3] = station_data[' Wind Direction(deg.)']
            except:
                print ("No Wind Direction Data " + callSign[idx])
                newData[:,3] = -888888.0
                
            try:
                newData[:,4] = station_data[' Air Temperature(deg. C)'] +273.15
            except:
                print ("No Air Temperature Data "+ callSign[idx])
                newData[:,4] = -888888.0
            try:
                newData[:,5] = station_data[' Dew Point Temperature(deg. C)'] + 273.15
            except:
                print ("No Dew Point Temperature Data "+ callSign[idx])
                newData[:,5] = -888888.0    
            try:
                newData[:,6] = station_data['Relative Humidity (%)']
            except:
                print ("No RH Data " + callSign[idx])
                newData[:,6] = -888888.0
                
            try:
                newData[:,7] = station_data[' Barometric Pressure()'] * 100.00 
            except:
                print ("No Barometric Pressure " + callSign[idx])
                newData[:,7] =  -888888.0
                
            newData[:,8] = latitude[idx]    
            newData[:,9] = longitude[idx]
            newData[:,10] = elevation[idx]+ sensor_height[idx]  ## USE THIS IN DA
            newData[:,14] = elevation[idx]
            newData[:,15] = sensor_height[idx]

            
            dfwrite = pd.DataFrame(newData, columns = HEADER)
            
            dfwrite["ID_String"]= callSign[idx]   #0
            dfwrite["Name_string"]= stationName[idx]#11
            dfwrite["FM_string"]=FM_Code #12
            dfwrite["Source_string"]=Source_Code #13
            #dfwrite = dfwrite.mask(dfwrite==np.nan, other = -888888.0)

            #Save the output file
            dfwrite.to_csv(outstring,index=False)