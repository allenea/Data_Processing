#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 18:07:12 2018

@author: allenea
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Last Updated on March 8th 2018

@author: Eric Allen, University of Delaware
Questions?: allenea@udel.edu

Cloud Wind and Climate Research Group & Delaware Environmental Observing System 




RAW -->(DELDOT_Prep)--> MERGED ----> REFORMATED -->(CombineALL_NDBC)--> Verification_Data

"""

import numpy as np
import pandas as pd
import glob
import os

HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
          'Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string',\
          'Elevation (m)','Wind_Sensor_Height (m)']

float64 = np.float64

dtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64,\
            "Wind_Direction (deg)":float64, "Air_Temperature (K)": float64,\
            "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64,\
            "Pressure (Pa)":float64, "Latitude":float64, "Longitude":float64,\
            "Elevation_SensorHeight (m)":float64, "Name_string" : object, "FM_string":object,\
            "Source_string":object, "Elevation (m)":float64,"Wind_Sensor_Height (m)":float64}

os.chdir(os.getcwd()+"/Reformatted/")
outstring = os.path.abspath('../..')+"/Verify_Converted/All_Sources/DELDOT-verify-converted.csv"

allfiles =  glob.glob("*.csv")   
print ("DelDOT File Count:", len(allfiles))

dfs = [pd.read_csv(f, usecols=HEADER,dtype=dtypesDict) for f in allfiles]
finaldf = pd.concat(dfs, axis=0, join='inner')
sortdf=finaldf.sort_values(['ID_String','DATE'])

#%%
wspd = np.array(sortdf["Wind_Speed (m/s)"])
wdir = np.array(sortdf["Wind_Direction (deg)"])
#print (type(wspd),type(wdir))
WS30 = np.where(wspd > 30)[0]
WDIR180 = np.where(wdir == 180)[0]
WDIR361 = np.where(wdir == 361)[0]

badLoc = list(set(WS30) & ( set(WDIR361) | set(WDIR180)))
badLoc.sort()

for idx in badLoc:
    wspd[idx] = np.nan
    wdir[idx] = np.nan
    
sortdf['Wind_Speed (m/s)']=wspd
sortdf['Wind_Direction (deg)'] = wdir   

print(np.nanmax(sortdf['Wind_Speed (m/s)']))
print(np.nanmin(sortdf['Wind_Speed (m/s)']))
print(np.nanmean(sortdf['Wind_Speed (m/s)']))
sortdf = sortdf.mask(sortdf=='',  -888888.0)
sortdf = sortdf.mask(sortdf==' ',  -888888.0)
sortdf = sortdf.mask(sortdf==np.nan, -888888.0)


sortdf.to_csv(outstring,index=False) 