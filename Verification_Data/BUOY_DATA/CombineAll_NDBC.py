#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Last Updated on March 8th 2018

@author: Eric Allen, University of Delaware
Questions?: allenea@udel.edu

Cloud Wind and Climate Research Group & Delaware Environmental Observing System 




RAW -->(Buoy_Prep)--> MERGED ----> REFORMATED -->(CombineALL_NDBC)--> Verification_Data

"""

import numpy as np
import pandas as pd
import glob
import os

#%%

float64 = np.float64
cwHEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
              'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
              'Latitude','Longitude','Elevation_SensorHeight (m)',\
              'Name_string','FM_string','Source_string',\
              'Elevation (m)','Wind_Sensor_Height (m)',"Gust_Direction (deg)",\
              "Gust (m/s)","Gust_Time (UTC HHMM)"]
        
cwtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64, "Wind_Direction (deg)":float64, "Air_Temperature (K)"  : float64,\
            "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64, "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64,\
            "Elevation_SensorHeight (m)":float64, "Name_string" : object, "FM_string" : object, "Source_string" : object, "Elevation (m)"  : float64,\
            "Wind_Sensor_Height (m)":float64,"Gust_Direction (deg)":float64,"Gust (m/s)":float64,"Gust_Time (UTC HHMM)":float64}


stHEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
          'Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string',\
          'Elevation (m)','Wind_Sensor_Height (m)',"Sigf_Wave_Height (m)",\
          "Dominant_Wave_Period (sec)","Avg_Wave_Period (sec)","Mean_Wave_Direction (deg)","Water_Temperature (K)","Gust (m/s)"]
        
        
sttypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64, "Wind_Direction (deg)":float64, "Air_Temperature (K)"  : float64,\
            "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64, "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64,\
            "Elevation_SensorHeight (m)":float64, "Name_string" : object, "FM_string" : object, "Source_string" : object, "Elevation (m)"  : float64,\
            "Wind_Sensor_Height (m)":float64,"Sigf_Wave_Height (m)":float64,"Dominant_Wave_Period (sec)":float64,"Avg_Wave_Period (sec)":float64,\
            "Mean_Wave_Direction (deg)":float64,"Water_Temperature (K)":float64,"Gust (m/s)":float64}


os.chdir( os.getcwd()+"/Reformatted/")
types = ['stdmet', 'cwind']
for type1 in types:
    allfiles = glob.glob("*"+type1+"*.csv")
    allfiles.sort()
    if type1 == 'stdmet':
        dfs = [pd.read_csv(f, usecols=stHEADER,dtype=sttypesDict) for f in allfiles]
        finaldf = pd.concat(dfs, axis=0, join='inner')
        sortdf=finaldf.sort_values(['ID_String','DATE'])
        outstring = os.path.abspath('../..')+"/Verify_Converted/All_Sources/NDBC_stdmet-verify-converted.csv"
        sortdf = sortdf.mask(sortdf=='', -888888.0)
        sortdf = sortdf.mask(sortdf==' ',  -888888.0)
        sortdf = sortdf.mask(sortdf==np.nan, -888888.0)
        sortdf.to_csv(outstring,index=False) 
        print("Finished STDMET")
        
    elif type1 == 'cwind':
        dfs = [pd.read_csv(f, usecols=cwHEADER, dtype=cwtypesDict) for f in allfiles]
        finaldf = pd.concat(dfs, axis=0, join='inner')
        sortdf=finaldf.sort_values(['ID_String','DATE'])
        outstring = os.path.abspath('../..')+"/Verify_Converted/All_Sources/NDBC_cwind-verify-converted.csv"
        sortdf = sortdf.mask(sortdf=='',  -888888.0)
        sortdf = sortdf.mask(sortdf==' ',  -888888.0)
        sortdf = sortdf.mask(sortdf==np.nan, -888888.0)
        sortdf.to_csv(outstring,index=False) 
        print("Finished CWIND")