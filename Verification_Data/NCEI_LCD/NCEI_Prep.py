#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 17:49:30 2018

@author: allenea

I know these files are separated by year because that's how I requested them.
Also only a subset of year. This might need to be improved to station or monthly.

Need to add Callsigns to any new station or find a file that has the WBAN Code and Station Abbriviation
"""
import glob
import pandas as pd
import numpy as np
import datetime
import os
import pytz

def wban_match():
    WBAN = []
    wban_id=[]
    readData = open(os.path.abspath('..')+"/WBN_CODES.txt",'r').readlines()

    for row in readData:
        if "UNITED STATES" in row:

            row_data = row.strip().split("\t")
            row_data = list(filter(None, row_data))

            for i in range(len(row_data)):
                if len(row_data[i]) == 4:
                    WBAN.append(row_data[i])
                    wban_id.append(row_data[0])

    return  WBAN, wban_id



HEADING  = ["STATION","STATION_NAME","ELEVATION","LATITUDE","LONGITUDE","YEAR","MONTH","DAY","HOUR","MINUTE","FZRN_FOUND","REPORTTYPE",
    
                    "HOURLYSKYCONDITIONS", "HOURLYVISIBILITY", "PRECIP", 
    
                    "HOURLYDRYBULBTEMPF", "HOURLYDRYBULBTEMPC","HOURLYWETBULBTEMPF","HOURLYWETBULBTEMPC",
    
                    "HOURLYDewPointTempF", "HOURLYDewPointTempC", "HOURLYRelativeHumidity","HOURLYWindSpeed",
    
                    "HOURLYWindDirection", "HOURLYWindGustSpeed", "HOURLYStationPressure","HOURLYPressureTendency",
    
                    "HOURLYPressureChange","HOURLYSeaLevelPressure", "HOURLYPrecip", "HOURLYAltimeterSetting", "DAILYMaximumDryBulbTemp",
    
                    "DAILYMinimumDryBulbTemp", "DAILYAverageDryBulbTemp", "DAILYDeptFromNormalAverageTemp", "DAILYAverageRelativeHumidity",
    
                    "DAILYAverageDewPointTemp", "DAILYAverageWetBulbTemp", "DAILYHeatingDegreeDays", "DAILYCoolingDegreeDays", "DAILYSunrise",
    
                    "DAILYSunset", "DAILYWeather","CLOUD_FOUND"]



ogdir = os.getcwd()
wkdir =   os.getcwd()+"/Reformatted/"  
### SET PATHS
outdir = os.getcwd()+'/Merged/'
os.chdir(wkdir)

asos_sensor_heights = 10 #meters

for file in glob.glob("*-metadata.csv"):

    data = pd.read_csv(file,low_memory=False)
    df = data.mask(data =='',other = np.nan)
    df = data.mask(data==' ',other = np.nan)


    WBAN, wban_id = wban_match()
    WBAN_data2 = list(set(df['STATION']))
    WBAN_data=[]
    for shorter in WBAN_data2:
        tmp = shorter.strip().split(":")
        WBAN_data.append(tmp[1])
    
    ### IMPROVE THIS IN THE FUTURE SO EACH # has a callsign in the file
    WBAN_dict = {}
    for eachWBAN in WBAN_data:
        for idx in range(len(WBAN)):
            if eachWBAN == wban_id[idx]:
                WBAN_dict[eachWBAN] = WBAN[idx]
                #ID_Station = stName[idx]
            elif eachWBAN == "93720":
                    WBAN_dict[eachWBAN] = "KSBY"
            elif eachWBAN == "93739":
                    WBAN_dict[eachWBAN] = "KWAL"
            elif eachWBAN == "03726":
                    WBAN_dict[eachWBAN] = "KWWD"
            elif eachWBAN == "00356":
                    WBAN_dict[eachWBAN] = "KCGE"
            elif eachWBAN == "03756":
                    WBAN_dict[eachWBAN] = "KESN"
            elif eachWBAN == "03724":
                    WBAN_dict[eachWBAN] = "KDMW"
            #else:  ### DO NOT USE THIS MESSEDS IT UP! WORRIED ABOUT THIS.... UNTESTED... Compile a legit list and redo this.
            #        WBAN_dict[eachWBAN] = "UNKN"; # NEED TO KNOW YOUR STATIONS DATA HEAD OF TIME AND JUST HAVE IT MATCH IT HERE.
    print (WBAN_dict, WBAN_data)
    #%% HONESTLY FORGET WHAT THIS IS DOING EXACTLY
    ID_Station = []
    station = np.array(df['STATION'])
    for idname in station:
        ID_Station.append(WBAN_dict.get(idname[5:]))    

    newTime = []
    for idx in range(len(df)):
        local = pytz.timezone ("America/New_York")  ### SINCE WE ARE ONLY USING EAST COAST STATIONS 
        naive = datetime.datetime(int(df["YEAR"][idx]),int(df["MONTH"][idx]),int(df["DAY"][idx]),int(df["HOUR"][idx]),int( df["MINUTE"][idx]),int(0))
        local_dt = local.localize(naive, is_dst=True)
        utc_dt = local_dt.astimezone (pytz.utc)
        fmtTime= utc_dt.strftime('%Y%m%d%H%M%S')
        newTime.append(fmtTime)

    HEADER_OUT = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)','Air_Temperature (K)',\
               'Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)','Latitude','Longitude',\
               'Elevation_SensorHeight (m)','Name_string','FM_string','Source_string','Elevation (m)','Wind_Sensor_Height (m)']
    
    #HEADER_OUT = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)','Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)','Latitude','Longitude','Elevation (m)','Name_string','FM_string','Source_string']
    DATAF = np.zeros((len(ID_Station),len(HEADER_OUT)))
    newdf1 = pd.DataFrame(DATAF,columns=HEADER_OUT)


    newdf1["ID_String"] = ID_Station
    newdf1['DATE'] = newTime
    newdf1['Wind_Speed (m/s)'] = df["HOURLYWindSpeed"] *  0.44704 # mph to m/s
    newdf1['Wind_Direction (deg)'] = df["HOURLYWindDirection"]
    newdf1['Air_Temperature (K)']= df["HOURLYDRYBULBTEMPC"] + 273.15
    newdf1['Dewpoint_Temperature (K)'] = df["HOURLYDewPointTempC"]+ 273.15
    newdf1['Relative_Humidity (%)'] = df["HOURLYRelativeHumidity"]
    newdf1['Pressure (Pa)'] = df["HOURLYStationPressure"]  * 3386.389 # 1hg to Pa
    newdf1['Latitude'] = df["LATITUDE"]
    newdf1['Longitude'] = df["LONGITUDE"]
    newdf1['Elevation_SensorHeight (m)'] =df["ELEVATION"] + asos_sensor_heights
    newdf1['Name_string'] = df["STATION_NAME"]
    newdf1['Source_string'] = "NCEI Local Climate Data"
    newdf1['Elevation (m)'] = df["ELEVATION"]
    newdf1['Wind_Sensor_Height (m)'] = asos_sensor_heights
    #newdf1['FM_string'] = df["REPORTTYPE"]
    [FM12] = np.where(df["REPORTTYPE"]  == "FM-12")
    [FM15] = np.where(df["REPORTTYPE"]  == "FM-15")
    [FM16] = np.where(df["REPORTTYPE"]  == "FM-16")
    fmtypes = [""]* len(df["REPORTTYPE"])
    for idx in FM15:
        fmtypes[idx] = "FM-15 METAR"
    for idx in FM12:
        fmtypes[idx] = "FM-12 SYNOP"
    for idx in FM16:
        fmtypes[idx] = "FM-16 SPECI"
    
    #print (fmtypes)
    newdf1['FM_string'] = fmtypes
        
        
    #newdf1 = newdf1.mask(newdf1==np.nan ,other = -888888.0)
    #newdf1 = newdf1.mask(newdf1=='', other = -888888.0)
    newdf1.to_csv(outdir+str(int(df["YEAR"][0]))+"_lcd-merged.csv", index=False)

#%%
os.chdir(ogdir+"/Merged/")
dfs = [pd.read_csv(f) for f in os.listdir(os.getcwd()) if f.endswith('csv')]
finaldf = pd.concat(dfs, axis=0, join='inner')
sortdf=finaldf.sort_values(['ID_String','DATE'])
sortdf = sortdf.mask(sortdf=='', -888888.0)
sortdf = sortdf.mask(sortdf==' ',  -888888.0)
sortdf = sortdf.mask(sortdf==np.nan,  -888888.0)
sortdf.to_csv(os.path.abspath('../../')+"/Verify_Converted/All_Sources/LocalClimateData-converted.csv",index=False)
