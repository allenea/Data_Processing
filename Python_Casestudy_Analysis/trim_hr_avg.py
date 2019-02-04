#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 17:10:07 2018

@author: allenea

to case study
"""

#IMPORTS
import numpy as np
import pandas as pd
import os
import glob
import datetime

#case_time = ['2014-06-04','2014-06-08', "2015-08-14"]
casestudy_time = ['2014-06-04_06:00','2014-06-08_06:00','2015-08-14_06:00']
dtype_subusage = ['10m','original']
dtype_usage = ["Verification", "Assimilation"]
for case_time in casestudy_time:
    for usage in dtype_usage:
        for dtype in dtype_subusage:
            data_dir = os.path.abspath('../')
            print (case_time[:10],"   ", case_time)
            if usage == "Verification":
                data_file = data_dir+"/Verification_Data/hr_avg_verify/"+dtype+"/"+case_time[:10]+"/"
                outdir =  data_dir+"/Verification_Data/hr_avg_trim/"+dtype+"/"+case_time[:10]+"/"
    
            elif usage == "Assimilation":
                data_file =  data_dir+"/Ferry_Data/hr_avg_verify/"+dtype+"/"+case_time[:10]+"/"
                outdir =  data_dir+"/Ferry_Data/hr_avg_trim/"+dtype+"/"+case_time[:10]+"/"
            
            print("OUT DIRECTORY ", outdir)

            if not os.path.exists(outdir):
                print ("OUT DIRECTORY ", outdir)
                os.makedirs(outdir)
 
    
            print (case_time[0:4],case_time[5:7],case_time[8:10],case_time[11:13], case_time[14:16])
            start_dte = datetime.datetime(int(case_time[0:4]),int(case_time[5:7]),int(case_time[8:10]),int(case_time[11:13]), int(case_time[14:16]))
            end_dte = datetime.datetime(int(case_time[0:4]),int(case_time[5:7]),int(case_time[8:10])+1,int(case_time[11:13]), int(case_time[14:16]))

            #%% Blank Arrays to Append Data
            # Outer loop to do for each file
            for file in glob.glob(data_file+"/"+'*.csv'):
                fname = file[:-19].split("/")[-1]
                fname = fname.strip()
                print (fname)
                
                #DEL07_2014060406.csv
                #%% Read In Data   
                data = pd.read_csv(file, low_memory=False)
                data.columns.tolist()
                
                
                #%% Load In Data
                ID_String = np.array(data['ID_String'])
                #Date = np.array(data['DATE'])
                WSpd= np.array(data['Wind_Speed (m/s)'])
                WDir = np.array(data['Wind_Direction (deg)'])
                temp = np.array(data['Air_Temperature (K)']) 
                dewpt = np.array(data['Dewpoint_Temperature (K)']) 
            
                rh = np.array(data['Relative Humidity (%)']) 
                press = np.array(data['Pressure (Pa)']) 
                lat = np.array(data['Latitude']) 
                long = np.array(data['Longitude']) 
                elev = np.array(data['Elevation (m)']) 
                name = np.array(data['Name_string']) 
                fm = np.array(data['FM_string']) 
                source = np.array(data['Source_string']) 
                
                year =np.array(data['YEAR']) 
                month =np.array(data['MONTH']) 
                day = np.array(data['DAY']) 
                hour =np.array(data['HOUR']) 
                minute = np.array(data['MINUTE']) 
                
                
                
                avg_year   = []        
                avg_month  = []
                avg_day    = []     
                avg_hour   = []
                avg_min    = []
                avg_ID     = []
                avg_name   = []
                avg_fm     = []
                avg_source = []
                avg_lat    = []
                avg_long   = []
                avg_elev   = []
                avg_wspd   = []
                avg_wdir   = []
                avg_temp   = []
                avg_dewpt  = []
                avg_rh     = []
                avg_press  = []
            
            
            
                for i in range(len(year)):
                    #print (int(year[i]),int(month[i]),int(day[i]),int(hour[i]),int(minute[i]))
                    dte = datetime.datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i]),int(minute[i]))
                    #dt= dte.strftime('%Y-%m-%d %H:%M')
                    if dte >= start_dte and dte <= end_dte:
                        #20140608171600
                        dt= dte.strftime('%Y-%m-%d %H:%M')
                        avg_year.append(year[i])        
                        avg_month.append(month[i])  
                        avg_day.append(day[i])    
                        avg_hour.append(hour[i])  
                        avg_min.append(minute[i])  
                        avg_ID.append(ID_String[i])  
                        avg_name.append(name[i])  
                        avg_fm.append(fm[i])  
                        avg_source.append(source[i])  
                        avg_lat.append(lat[i])  
                        avg_long.append(long[i])  
                        avg_elev.append(elev[i])  
                        avg_wspd.append(WSpd[i])  
                        avg_wdir.append(WDir[i])  
                        avg_temp.append(temp[i])
                        avg_dewpt.append(dewpt[i])
                        avg_rh.append(rh[i])  
                        avg_press.append(press[i])  
                        
                
                #%% HEADERS
                HEADING  =  ["YEAR","MONTH","DAY","HOUR","MINUTE",'ID_String','Latitude',\
                             'Longitude','Elevation (m)',"Wind_Speed (m/s)",'Wind_Direction (deg)',\
                             'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative Humidity (%)','Pressure (Pa)',\
                             'Name_string','FM_string','Source_string']    
                
                
                 
                
                #%% SAVE DATA BEFORE OUTPUT
                
                blankMatrix = np.zeros((len(avg_year),len(HEADING)))
                
                blankMatrix[:,0] =  [int(yr) for yr in avg_year]
                blankMatrix[:,1] = [int(yr) for yr in avg_month]
                blankMatrix[:,2] = [int(dy) for dy in avg_day]
                blankMatrix[:,3] = [int(hr) for hr in avg_hour]
                blankMatrix[:,4] = [int(mi) for mi in avg_min]
                #blankMatrix[:,5] = avg_ID ##
                
                
                blankMatrix[:,6] = [float(lt) for lt in avg_lat]
                blankMatrix[:,7] = [float(lg) for lg in avg_long]
                blankMatrix[:,8] = [float(el) for el in avg_elev]
                blankMatrix[:,9] = [float(ws) for ws in avg_wspd] 
                blankMatrix[:,10] =[float(wd) for wd in avg_wdir]
                blankMatrix[:,11] = [float(t) for t in avg_temp]
                blankMatrix[:,12] = [float(td) for td in avg_dewpt]

                blankMatrix[:,13] = [float(rh2) for rh2 in avg_rh]
                blankMatrix[:,14] = [float(p) for p in avg_press]
                
                
                #%% Make and save data in output file
                outstring = outdir + fname +"_hr_avg_trim.csv"
                print(outstring)
                df = pd.DataFrame(blankMatrix, columns = HEADING, index=None)
                df['ID_String'] = avg_ID # BLANK 0
                df['Name_string'] = avg_name # BLANK 0
                df['FM_string'] = avg_fm # BLANK 0
                df['Source_string'] = avg_source # BLANK 0
                
                df = pd.DataFrame.replace(df,to_replace=' ', value=np.nan)
                  
                df.to_csv(outstring, index=False)
                
                del blankMatrix,data,df  ## Comment out for debugging
                #break
            
                