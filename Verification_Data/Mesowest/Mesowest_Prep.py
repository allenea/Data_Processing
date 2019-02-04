#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 15:05:39 2018

@author: allenea


RAW ---> REFORMATTED ----> MERGED ---->Verification_Data
"""
import glob
import csv
import pandas as pd
import datetime
import numpy as np
import os


### DEOS ## ['ID_String', 'DATE', 'Wind_Speed (m/s)', 'Wind_Direction (deg)', 'Air_Temperature (K)', 'Relative Humidity (%)', 'Pressure (Pa)', 'Latitude', 'Longitude', 'Elevation (m)', 'Elevation+SensorHeight', 'Sensor_height', 'Name_string', 'FM_string', 'Source_string']
HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
              'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
              'Latitude','Longitude','Elevation_SensorHeight (m)',\
              'Name_string','FM_string','Source_string',\
              'Elevation (m)','Wind_Sensor_Height (m)']


wkdir =   os.getcwd()+"/Raw/"  
outdir = os.getcwd() +'/Reformatted/'
mergedir = os.getcwd() +'/Merged/'
os.chdir(wkdir)


for file in glob.glob('*.csv'):
    #print (file)
    outstring = outdir+ file[:-4]+"-w-Metadata.csv"
    data = []
    with open(file,'rt') as infile:
        print ("Editing  " + file)
        raw = csv.reader(infile,dialect='excel',delimiter=',')
        for row in raw:
            data.append(row)
    dataset = []; metadata=[];
    oldheader =[]; oldunits = []
    rowcount = 1 
    for row in data:
        if rowcount <= 6:
            rowcount +=1
            tmpData = row[0].split(":")[1]
            metadata.append(tmpData)
        elif rowcount <=7:
            oldheader= row
            rowcount +=1
        elif rowcount <=8:
            oldunits = row
            rowcount +=1
        else:
            dataset.append(row[0:len(oldheader)])
            
 #%%           
            
    station_id = metadata[0]
    station_name = metadata[1]
    latitude = metadata[2]
    longitude = metadata[3]
    elevation = metadata[4]
    state = metadata[5]
    
    df = pd.DataFrame(dataset, columns=oldheader)
    df = df.loc[:,~df.columns.duplicated()]
    df = df.mask(df=='', other = -888888.0)

    time = []
    for date in df['Date_Time']:
        dt_object = datetime.datetime.strptime(date,'%m/%d/%Y %H:%M %Z')
        strTime =dt_object.strftime('%Y%m%d%H%M%S')
        time.append(strTime)
        ## Is there a way to check for LST vs GMT???
        
        
    if 'wind_speed_set_1' in df:
        wind_speed = [float(ws)* 0.44704 for ws in df['wind_speed_set_1']]     #MPH to m/s
    else:
        print (station_id + "  is missing wind speed" )
        wind_speed = [-888888.0 for ws in range(len(time))]     #MPH to m/s

    if 'wind_direction_set_1' in df:
        wind_direction = [float(WD) for WD in df['wind_direction_set_1']]
    else:
        print (station_id + "  is missing wind direction")
        wind_direction = [-888888.0 for WD in range(len(time))]     #MPH to m/s

    if 'air_temp_set_1' in df:
        temperature = [(5./9.) * (float(T) - 32.) + 273.15 for T in df['air_temp_set_1']] #F to C to K
    else:
        print (station_id + "  is missing temperature")
        temperature = [-888888.0 for T in range(len(time))]    
        
    if 'dew_point_temperature_set_1d' in df:
        dewpoint = [(5./9.) * (float(Td) - 32.) + 273.15 for Td in df['dew_point_temperature_set_1d']]    #F to C to K
    else:
        print (station_id + "  is missing dewpoint temperature")
        dewpoint = [-888888.0 for Td in range(len(time))]      
        
    if 'relative_humidity_set_1' in df:
        relative_humidity = [float(RH) for RH in df['relative_humidity_set_1']]
    else:
        print (station_id + "  is missing relative humidity")
        relative_humidity = [-888888.0 for RH in range(len(time))]

    
    if 'pressure_set_1d' in df:
        pressure = [float(P) * 3386.3886666667 for P in df['pressure_set_1d']]
    else:
        print (station_id + "  is missing pressure")
        pressure = [-888888.0 for P in range(len(time))]    

    blank = range(len(time))
    lat = []; lon = []; elev=[];stName=[];stID=[]
    lat = [float(latitude) for val in blank]
    lon = [float(longitude) for val in blank]
    elev = [int(elevation) for val in blank]
    name = [station_name for val in blank]
    FM_String = ['FM-12 SYNOP' for val in blank] #!!!!???????????
    source = [state for val in blank]
    ID= [station_id for val in blank]
    
    DATAF = np.zeros((len(time),len(HEADER)))
    DATAF[:,2] = wind_speed
    DATAF[:,3] = wind_direction
    DATAF[:,4] = temperature
    DATAF[:,5] = dewpoint
    DATAF[:,6] = relative_humidity
    DATAF[:,7] = pressure
    DATAF[:,8] = lat
    DATAF[:,9] = lon
    DATAF[:,10] = elev
    DATAF[:,14] = elev
    DATAF[:,15] = -888888.0

    print ("WARNING: UNKNOWN SENSOR HEIGHTS USING MESOWEST (USING -888888.0).... BEST TO GET DIRECTLY FROM SOURCE TO MINIMIZE ERROR.")
    final_df = pd.DataFrame(DATAF,columns=HEADER)
    final_df["ID_String"] = ID #0
    final_df["DATE"] = time #1
    final_df['Name_string'] = name#11
    final_df['FM_string'] = FM_String#12
    final_df['Source_string'] = source#13
    final_df.to_csv(outstring,index=False)
    del wind_speed, wind_direction, pressure, temperature, relative_humidity, lat, lon, elev
    del FM_String, time, ID, name, source, df, DATAF, final_df, oldheader,dataset


def merge_csv(file1,file2):
    file1short = file1[-20:-15]
    a = pd.read_csv(file1, low_memory=False)
    b = pd.read_csv(file2, low_memory=False)
    merged = pd.concat([a,b])
    merged.to_csv(mergedir+file1short+"-mesowest-data.csv", index=False)

os.chdir(os.path.abspath('../Reformatted'))
fileList = []
#for each formatted file with DEOS data in the folder this program is executed         
for file in glob.glob('*.csv'):
    fileList.append(file)
mergedList = []

for file1 in fileList:
    for file2 in fileList:
        file1short = file1[-20:-15]
        file2short = file2[-20:-15]
        if file1short == file2short and file1 !=file2 and file1short not in mergedList:
            #print file1, file2
            merge_csv(file1,file2)
            mergedList.append(file1short)
            print ("MERGED", file1short)
        elif file1short != file2short and file1!=file2 and file1short not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mergedir+file1short+"-mesowest-data.csv", index=False)
            print ("SINGLE" , file1short)
        elif file1short == file2short and file1==file2 and file1short not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mergedir+file1short+"-mesowest-data.csv", index=False)
            print ("SINGLE" , file1short)


print (mergedList)


#%%
os.chdir(mergedir)
dfs = [pd.read_csv(f) for f in os.listdir(os.getcwd()) if f.endswith('csv')]
finaldf = pd.concat(dfs, axis=0, join='inner')
sortdf=finaldf.sort_values(['ID_String','DATE'])
sortdf.to_csv(os.path.abspath('../../')+"/Verify_Converted/All_Sources/Mesowest-converted.csv",index=False)