#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

Author Eric Allen, allenea@udel.edu
Date  8-13-2018
This is a temporary script file.
COMMENTED OUT SAVE TO CSV FILE
 

#%%  CHANGE THIS BLOCK DEPENDING ON WHAT YOU ARE TRYING TO DO
# THIS DOES NOT HANDLE GOING FROM A DAY IN ONE MONTH TO A DAY IN ANOTHER MONTH. 
#   You control the code. It's there to do most the heavy lifting

"""
#%%
#IMPORTS
import numpy as np
import pandas as pd
import os


float64 = np.float64

dtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64, "Wind_Direction (deg)":float64,\
            "Air_Temperature (K)"  : float64, "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64,\
            "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64, "Elevation_SensorHeight (m)":float64,\
            "Name_string":object, "FM_string":object, "FM_Code":object, "Source_string":object}

HEADER_IN = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)','Air_Temperature (K)',"Dewpoint_Temperature (K)",\
              'Relative Humidity (%)','Pressure (Pa)','Latitude','Longitude','Elevation (m)','Name_string','FM_string','FM_Code','Source_string']

HEADER_OUT  = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)','Air_Temperature (K)',"Dewpoint_Temperature (K)",\
              'Relative Humidity (%)','Pressure (Pa)','Latitude','Longitude','Elevation (m)','Name_string','FM_string','Source_string']
            

runTime_D = 1

casestudy_time = ['2014-06-04_06:00','2014-06-08_06:00','2015-08-14_06:00']
dtype_subusage = ['10m','original']
dtype_usage = ["Verification", "Assimilation"]



for case_time in casestudy_time:
    for usage in dtype_usage:
        for dtype in dtype_subusage:
            #OPEN/READ DATA FILE - GET FARBER LOCATION
            data_dir = os.path.abspath('../')
            print (case_time)
            
            ### Verification Data Archive, for NJ and DE, INTERPOLATED TO 10m WINDS (DEOS, NDBC, NCEI, DELDOT, NJMesonet,Meoswest**)
            if usage == "Verification" and dtype == "10m":
                data_file = data_dir+'/Verification_Data/all_verification_10mdata_BADARC.txt'
                directory = data_dir + '/Verification_Data/verify_case_study_data/10m/'+ case_time[:10]+'/' ## FARBER
                print (data_file,"\n",directory)
                
            ### Verification Data Archive, for NJ and DE, (DEOS, NDBC, NCEI, DELDOT, NJMesonet,Meoswest**) - can be used for assimilation
            elif usage == "Verification" and dtype == "original":
                data_file = data_dir+'/Verification_Data/all_verification_OBSdata_BADARC.txt'
                directory = data_dir + '/Verification_Data/verify_case_study_data/original/'+ case_time[:10]+'/' ## FARBER
                print (data_file,"\n",directory)
                
            ### STANDARD ASSIMILATION DATA INTERPOLATED TO 10m WINDS (CMLF, DEOS)
            elif usage == "Assimilation" and dtype=="10m":
                data_file = data_dir+'/Assimilation_Data/Assimilation_Data_10m_DEOS_CMLF.txt'
                directory = data_dir +'/Ferry_Data/case_study_data/10m/'+ case_time[:10]+'/' ## FARBER
                print (data_file,"\n",directory)
                
            ### STANDARD ASSIMILATION DATA (CMLF, DEOS)
            elif usage == "Assimilation" and dtype=="original":
                data_file = data_dir+'/Assimilation_Data/data_CMLF2011_2016_D2010_2017.txt'
                directory = data_dir +'/Ferry_Data/case_study_data/original/'+ case_time[:10]+'/' ## FARBER
                print (data_file,"\n",directory)
            
            
            if not os.path.exists(directory):
                os.makedirs(directory)
            

            infile = pd.read_table(data_file, delim_whitespace=True,dtype = dtypesDict,header=None, names = HEADER_IN)
            infile["FM_string"] = infile["FM_string"] +" "+ infile["FM_Code"]
            readData = infile.drop(['FM_Code'],axis=1)
            print(list(set(infile["ID_String"])))
            #print readData
            data = np.array(readData)
            
            year = case_time[0:4]
                
            month = case_time[5:7]
            intMonth = int(month)
                
            day = case_time[8:10] 
            intDay = int(day)
            
            endDay = intDay + runTime_D
            
            
            
            if (endDay < 10):
                endDay = '0'+ str(endDay)    
            else:
                endDay = str(endDay)
                
            
            hour = case_time[11:13]
            intHour = int(hour)
            
            minute = case_time[14:16]
            intMinute = int(minute)
            
            
            ## for each file iterate hour, hour +1 , hour +2 and create output filess   
            print ("Year:",year, ". Month:",month,". Day:",day,". Hour:",hour,".Minute:", minute)
            
            # TIME STEP-WHAT DO I WANT TO USE?
            Start_Time = year+month+day+hour + minute +'00'
            End_Time = year+month+endDay+hour + minute +'00'
            print (Start_Time, "   ", End_Time, int(End_Time)-int(Start_Time))
            
            #%% Iterate backwards through the data.
            masterKey = []
            stationID = []

            for row in data:
                #Cut computing time to next to nothing my cutting out almost all irrelevant data for the time period
                time = str(row[1])
                if (time[0:4] != year): continue
                elif (intMonth ==12 or intMonth == 1): print ("*************YEAR TROUBLE*********************")
                if int(time[4:6]) < intMonth: continue
                elif (((intMonth==2 and intDay == 28) or (intMonth==2 and intDay == 29)) or intDay==30 or intDay ==31): print ("*************END MONTH TROUBLE*********************")
                if (int(time[6:8]) < intDay): continue
                if (int(time[6:8])) > int(endDay):continue
                #print(time, row)

                if(time <= End_Time and time >= Start_Time):
                    #print ("   ",time)
                    
                    masterKey.append(row)
                    stationID.append(row[0])
                    
            #%%
            listStationID = list(set(stationID))  
            print (listStationID)
            allDEOS_GOOD = 0
            allDEOS_BAD = 0
            
            CMLF_GOOD = 0
            CMLF_BAD = 0
            
              
            for ID in listStationID:
                
                badOBS = 0
                goodOBS = 0
            
                outputfile = directory + ID +'_'+Start_Time[:-4]+".csv"
                stationData = []
                print (outputfile)
                for row2 in masterKey:
                    if ID == row2[0]:
                        stationData.append(row2)
                df= pd.DataFrame(stationData,columns=HEADER_OUT)
                df.to_csv(outputfile, index=False)
            
                for value in list(df['Latitude']):
                    if value =='-888888.00000':
                        badOBS +=1
                    elif value != '-888888.00000':
                        goodOBS +=1
                    else:
                        print (value)
                if ID == "CMLF":
                    CMLF_GOOD = goodOBS
                    CMLF_BAD = badOBS
            
                else:
                    print (ID)
                    allDEOS_GOOD += goodOBS
                    allDEOS_BAD += badOBS
            #%%
            
            print ("This depends on if it's set up for DEOS/CMLF or Mesowest")
            print ("")
            print ("CMLF has " + str(CMLF_GOOD) + "  Good Observations")
            print ("CMLF has " + str(CMLF_BAD) + "  Bad Observations")
            print ("")
            print ("")
            print ("DEOS/Mesowest has " + str(allDEOS_GOOD) + "  Good Observations")
            print ("DEOS/Mesowest has " + str(allDEOS_BAD) + "  Bad Observations")
            print ("")
            print ("")
            print ("Combined has " + str(CMLF_GOOD+allDEOS_GOOD) + "  Good Observations")
            print ("Combined has " + str(CMLF_BAD+allDEOS_BAD) + "  Bad Observations")

            
            
