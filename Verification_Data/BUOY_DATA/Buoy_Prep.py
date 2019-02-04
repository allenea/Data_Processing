#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 17:16:57 2018

@author: allenea

# This file will take a little while to run since it is processing so much data


RAW -->(Buoy_Prep)--> MERGED ----> REFORMATED -->(CombineALL_NDBC)--> Verification_Data

"""

import glob
import pandas as pd
import datetime
import numpy as np
import os


#YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS  TIDE
#yr  mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC   mi    ft
#2014 09 11 16 50 120  5.0  6.0   0.6     6   4.2 134 1016.5  29.3  30.5  24.4   MM +0.3    MM

stheader = ["Year", "Month", "Day", "Hour","Minute","WDIR (deg)","WSPD (m/s)","GUST (m/s)",\
            "Sigf_Wave_Height (m)","Dominant_Wave_Period (sec)","Avg_Wave_Period (sec)",\
            "Mean_Wave_Direction (deg)","PRES (hPa)","ATMP (degC)","WTMP (degC)","DEWP (degC)",\
            "VIS (mi)","TIDE (ft)"]
float64 = np.float64
sttypesDict={"Year": int, "Month":int,"Day":int,"Hour":int,"Minute":int, "WDIR (deg)":int,\
            "WSPD (m/s)":float64, "GUST (m/s)"  : float64,"Sigf_Wave_Height (m)":float64,\
            "Dominant_Wave_Period (sec)":float64,"Avg_Wave_Period (sec)":float64,\
            "Mean_Wave_Direction (deg)":float64,"PRES (hPa)":float64,"ATMP (degC)":float64,"WTMP (degC)":float64,"DEWP (degC)":float64,\
            "VIS (mi)":object,"TIDE (ft)":object}
            

#YY  MM DD hh mm WDIR WSPD GDR GST GTIME
#yr  mo dy hr mn degT m/s degT m/s hhmm
#2014 09 11 16 50 117  5.2 120  6.0 1644

cwheader = ["Year", "Month", "Day", "Hour","Minute","WDIR (deg)","WSPD (m/s)","GUSTDIR (deg)",\
            "GUST (m/s)","GTIME (UTC HHMM)"]

cwtypesDict={"Year": int, "Month":int,"Day":int,"Hour":int,"Minute":int, "WDIR (deg)":int,\
            "WSPD (m/s)":float64, "GUSTDIR (deg)":int,"GUST (m/s)"  : float64,"GTIME (UTC HHMM)":int}


wkdir = os.path.abspath('../BUOY_DATA')
os.chdir(wkdir)

#Makes dataframe of metadata 
metadata = wkdir+"/NDBC_Metadata.csv"
df = pd.read_csv(metadata)
stationName = df['Station_Name']
callSign = df['Call_Sign']
state = df['ST']
latitude = df['Latitude (DD)']
longitude = df['Longitude (DD)']
elevation = df['Elev (m)']
temp_sensor = df['Air_Temperature(m)']
wind_sensor = df['Anemometor(m)']
pres_sensor = df['Barometer(m)']
sea_sensor = df['Sea_Temp(m)']


# Sets paths and changes to correct directory
wkdir =   os.getcwd()+"/Raw/"
mergedir = os.getcwd()+"/Merged/"
outdir = os.getcwd()+"/Reformatted/"
os.chdir(wkdir)

types = ['stdmet', 'cwind']
listFiles = glob.glob('*.txt')
listFiles.sort()      
      
for buoy in callSign:
    for typeD in types:
        dfs = []
        print ("Buoy Name: " +buoy + "  Data Type:  " + typeD)
        for f in listFiles:
            if f.startswith(buoy) and typeD in f:
                print ("File Name: ", f)
                f1 = pd.read_table(f,delim_whitespace=True,header=None,skiprows=2)
                dfs.append(f1)
                finaldf = pd.concat(dfs, axis=0, join='inner')
                if typeD == 'stdmet':
                    finaldf.to_csv(mergedir+buoy+"_"+typeD+"_merged.csv",index=False,header=stheader)
                elif typeD == 'cwind':
                    finaldf.to_csv(mergedir+buoy+"_"+typeD+"_merged.csv",index=False,header=cwheader)
                    
                    
print ("BEGINNING REFORMATTING")

#%%
##########                  HEADERS         ###################################

HEADER1 = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
  'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
  'Latitude','Longitude','Elevation_SensorHeight (m)',\
  'Name_string','FM_string','Source_string',\
  'Elevation (m)','Wind_Sensor_Height (m)',"Gust_Direction (deg)",\
  "Gust (m/s)","Gust_Time (UTC HHMM)"]


HEADER2 = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
      'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
      'Latitude','Longitude','Elevation_SensorHeight (m)',\
      'Name_string','FM_string','Source_string',\
      'Elevation (m)','Wind_Sensor_Height (m)',"Sigf_Wave_Height (m)",\
      "Dominant_Wave_Period (sec)","Avg_Wave_Period (sec)","Mean_Wave_Direction (deg)","Water_Temperature (K)","Gust (m/s)"]

####################################################


#Include additional parameters for WRF Data Assimilation
FM_Code = "FM-18 BUOY"
Source_Code = 'NDBC'


os.chdir(mergedir)

for file in glob.glob('*merged.csv'):
    if "cwind" in file:
        data2 = pd.read_csv(file, usecols=cwheader,dtype=cwtypesDict)
        data2.columns.tolist()
        outstring = outdir+ file[:-10]+"metadata.csv"

        
        # FORMAT TIME       
        newTime = np.empty(len(data2))
        for i in range(len(data2)):
            utc_dt = datetime.datetime(data2['Year'][i],data2['Month'][i],data2['Day'][i],data2['Hour'][i],data2['Minute'][i],int(0))
            fmtTime= utc_dt.strftime('%Y%m%d%H%M%S')
            newTime[i] = fmtTime
            
        # SET MISSING VALUES
        data2 = data2.mask(data2 == 999.0, other= np.nan)
        data2 = data2.mask(data2 == 99.0, other= np.nan)
        data2 = data2.mask(data2 == 9999.0, other= np.nan)  
        data2 = data2.mask(data2 == '', other= np.nan)  
        data2 = data2.mask(data2 == ' ', other= np.nan)  

        newData = np.zeros((len(data2),len(HEADER1)))
        fileName = file.split('_')[0]
        
        #See if it matches any of the stations in the metadata file
        for idx in range(len(callSign)):
            #If it does add the metadata to the file
            if callSign[idx] == fileName:
                print ("Sensor Height ",callSign[idx],"  =  ",wind_sensor[idx])

                #Parse Time Data- You could cut this part to save lots of CPU time.
                newData[:,1] = newTime
                try:
                    newData[:,2] = data2["WSPD (m/s)"]
                except:
                    print ("No Wind Speed Data " + callSign[idx])
                    newData[:,2] = -888888.0
                    
                try:
                    newData[:,3] = data2["WDIR (deg)"]
                except:
                    print ("No Wind Direction Data " + callSign[idx])
                    newData[:,3] = -888888.0
                    
                try:
                    newData[:,4] = data2["ATMP (degC)"] +273.15  ## ALREADY IN KELVIN
                except:
                    print ("No Air Temperature Data "+ callSign[idx])
                    newData[:,4] = -888888.0
                    
                    
                try:
                    newData[:,5] = data2["DEWP (degC)"]+273.15 ## ALREADY IN KELVIN
                except:
                    print ("No Dewpoint Temperature " + callSign[idx])
                    newData[:,5] = -888888.0   
                    
                    
                # MEANT TO BE MISSING NOT REAL NAME B/C THERE ISNT ONE   
                try:
                    newData[:,6] = data2['Relative_Humidity (%)']  ## FAILS 
                except:
                    print ("No RH Data " + callSign[idx])
                    newData[:,6] = -888888.0
                    
                try:
                    newData[:,7] = data2["PRES (hPa)"] *100.0
                except:
                    print ("No Barometric Pressure " + callSign[idx])
                    newData[:,7] =  -888888.0

                        
                newData[:,8] = latitude[idx]
                newData[:,9] = longitude[idx]
                newData[:,10] = elevation[idx]+ wind_sensor[idx]  ## USE THIS IN DA
                newData[:,14] = elevation[idx]
                newData[:,15] = wind_sensor[idx]
                newData[:,16] = data2["GUSTDIR (deg)"]
                newData[:,17] = data2["GUST (m/s)"]
                newData[:,18] = data2["GTIME (UTC HHMM)"]


                dfwrite = pd.DataFrame(newData, columns = HEADER1)
                
                dfwrite["ID_String"]= callSign[idx]   #0
                dfwrite["Name_string"]= stationName[idx]#11
                dfwrite["FM_string"]=FM_Code #12
                dfwrite["Source_string"]=Source_Code #13
                
                dfwrite = dfwrite.mask(dfwrite == np.nan, -888888.0)            
                
                #Save the output file
                dfwrite.to_csv(outstring,index=False)
                del data2
                
                
    elif "stdmet" in file:
        data2 = pd.read_csv(file, usecols=stheader,dtype=sttypesDict)
        data2.columns.tolist()
        outstring = outdir+ file[:-10]+"metadata.csv"

        #Format Time
        newTime = np.empty(len(data2))
        for i in range(len(data2)):
            utc_dt = datetime.datetime(data2['Year'][i],data2['Month'][i],data2['Day'][i],data2['Hour'][i],data2['Minute'][i],int(0))
            fmtTime= utc_dt.strftime('%Y%m%d%H%M%S')
            newTime[i] = fmtTime
        

        # SET MISSING VALUES
        data2 = data2.mask(data2 == 999.0, other= np.nan)
        data2 = data2.mask(data2 == 99.0, other= np.nan)
        data2 = data2.mask(data2 == 9999.0, other= np.nan)  
        data2 = data2.mask(data2 == '', other= np.nan)  
        data2 = data2.mask(data2 == ' ', other= np.nan)  

        # DO AFTER MASKING
        data2["PRES (hPa)"] = data2["PRES (hPa)"] * 100.00
        data2["ATMP (degC)"] = data2["ATMP (degC)"] + 273.15
        data2["WTMP (degC)"] = data2["WTMP (degC)"] + 273.15
        data2["DEWP (degC)"] = data2["DEWP (degC)"] + 273.15
        

        newData = np.zeros((len(data2),len(HEADER2)))
        fileName = file.split('_')[0]
        
        #See if it matches any of the stations in the metadata file
        for idx in range(len(callSign)):
            #If it does add the metadata to the file
            if callSign[idx] == fileName:
                print ("Sensor Height ",callSign[idx],"  =  ",wind_sensor[idx])

                #Parse Time Data- You could cut this part to save lots of CPU time.
                newData[:,1] = newTime
                try:
                    newData[:,2] = data2["WSPD (m/s)"]
                except:
                    print ("No Wind Speed Data " + callSign[idx])
                    newData[:,2] = -888888.0
                    
                try:
                    newData[:,3] = data2["WDIR (deg)"]
                except:
                    print ("No Wind Direction Data " + callSign[idx])
                    newData[:,3] = -888888.0
                    
                try:
                    newData[:,4] = data2["ATMP (degC)"]  ## ALREADY IN KELVIN
                except:
                    print ("No Air Temperature Data "+ callSign[idx])
                    newData[:,4] = -888888.0 
                    
                try:
                    newData[:,5] = data2["DEWP (degC)"]  ## ALREADY IN KELVIN
                except:
                    print ("No Dewpoint Temperature " + callSign[idx])
                    newData[:,5] = -888888.0   
                    
                try:
                    newData[:,6] = data2['Relative_Humidity (%)']  ## FAILS 
                except:
                    print ("No RH Data " + callSign[idx])
                    newData[:,6] = -888888.0
                    
                try:
                    newData[:,7] = data2["PRES (hPa)"]  ## ALREADY IN PA
                except:
                    print ("No Barometric Pressure " + callSign[idx])
                    newData[:,7] =  -888888.0
                    
                try:
                    newData[:,20] = data2["WTMP (degC)"]
                except:
                    newData[:,20] = -888888.0
                    
                    
                newData[:,8] = latitude[idx]
                newData[:,9] = longitude[idx]
                newData[:,10] = elevation[idx]+ wind_sensor[idx]  ## USE THIS IN DA
                newData[:,14] = elevation[idx]
                newData[:,15] = wind_sensor[idx]
                newData[:,16] = data2["Sigf_Wave_Height (m)"]
                newData[:,17] = data2["Dominant_Wave_Period (sec)"]
                newData[:,18] = data2["Avg_Wave_Period (sec)"]
                newData[:,19] = data2["Mean_Wave_Direction (deg)"]
                newData[:,21] = data2["GUST (m/s)"]
                
                
                dfwrite = pd.DataFrame(newData, columns = HEADER2)
                
                dfwrite["ID_String"]= callSign[idx]   #0
                dfwrite["Name_string"]= stationName[idx]#11
                dfwrite["FM_string"]=FM_Code #12
                dfwrite["Source_string"]=Source_Code #13
                
                dfwrite = dfwrite.mask(dfwrite ==np.nan, -888888.0)            

                #Save the output file
                dfwrite.to_csv(outstring,index=False)
                del data2
    del dfwrite, newData