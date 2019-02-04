#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 12:29:45 2018

@author: allenea
"Forward" 30-min average
"""

import pandas as pd
import numpy as np
import glob
import itertools
import os 

HEADING  =  ["YEAR","MONTH","DAY","HOUR","MINUTE",'ID_String','Latitude',\
             'Longitude','Elevation (m)',"Wind_Speed (m/s)",'Wind_Direction (deg)',\
             'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative Humidity (%)','Pressure (Pa)',\
             'Name_string','FM_string','Source_string']    
                
casestudy_time = ['2014-06-04_06:00','2014-06-08_06:00','2015-08-14_06:00']
dtype_subusage = ['10m','original']
dtype_usage = ["Verification", "Assimilation"]

# SUB_HOUR_FREQUENCY OF AVERAGING PROGRAM
avg_interval = 30

for case_time in casestudy_time:
    for usage in dtype_usage:
        for dtype in dtype_subusage:
            data_dir = os.path.abspath('../')

            print (case_time[:10],"   ", case_time)
            if usage == "Verification":
                data_file = data_dir+'/Verification_Data/verify_case_study_data/'+dtype+'/'
                outdir = data_dir+"/Verification_Data/hr_avg_verify/"+dtype+"/"+case_time[:10]+"/"
    
            elif usage == "Assimilation":
                data_file = data_dir+'/Ferry_Data/case_study_data/'+dtype+'/'
                outdir = data_dir+"/Ferry_Data/hr_avg_verify/"+dtype+"/"+case_time[:10]+"/"
    
            if not os.path.exists(outdir):
                os.makedirs(outdir)
                
            # Outer loop to do for each file'
            for file in glob.glob(data_file+case_time[:10]+"/"+'*.csv'):
                
                #print(min(year_raw),max(year_raw)+1)
                #print(min(month_raw),max(month_raw)+1)
                #print(min(day_raw),max(day_raw)+1):
                
                fname = file[:-15].split("/")[-1]
                fname = fname.strip()
                print (fname)
                
                #DEL07_2014060406.csv
                #%% Read In Data   
                data = pd.read_csv(file, low_memory=False)
                data.columns.tolist()
                data = data.mask(data == -888888.0, other= np.nan)
                
                
                #%% Load In Data
                ID_String = np.array(data['ID_String'])
                Date = np.array(data['DATE'])
                WSpd= np.array(data['Wind_Speed (m/s)'])
                WDir = np.array(data['Wind_Direction (deg)'])
                temp = np.array(data['Air_Temperature (K)']) 
                dewpt = np.array(data['Dewpoint_Temperature (K)']) 
                rh = np.array(data['Relative Humidity (%)']) 
                press = np.array(data['Pressure (Pa)']) 
                lat = np.array(data['Latitude']) 
                long = np.array(data['Longitude']) 
                elev = np.array(data['Elevation (m)'])  ## SENSOR + ELEVATION
                name = np.array(data['Name_string']) 
                fm = np.array(data['FM_string']) 
                source = np.array(data['Source_string']) 
                
            
                            
            
                year_raw   = np.empty(len(Date))
                month_raw  = np.empty(len(Date))
                day_raw    = np.empty(len(Date))
                hour_raw   = np.empty(len(Date))
                minute_raw = np.empty(len(Date))
                for idx in range(len(Date)):
                    dte = str(int(Date[idx]))
                    #20140608171600
                    year_raw[idx] = int(dte[0:4])
                    month_raw[idx] = int(dte[4:6])
                    day_raw[idx] = int(dte[6:8])
                    hour_raw[idx] = int(dte[8:10])
                    minute_raw[idx] = int(dte[10:12])
                    
                # In order to not throw off averages w/ missing data replace 
                # missing values(-) or zero values with np.nan.
                # This is unfortunate necessity.    
                for i in range(len(temp)):
                    if temp[i] <= 0.0:
                        temp[i] = np.nan
            
                    elif temp[i] <= 0:
                        temp[i] = np.nan
                        
                        
                for i in range(len(dewpt)):
                    if dewpt[i] <= 0.0:
                        dewpt[i] = np.nan
            
                    elif dewpt[i] <= 0:
                        dewpt[i] = np.nan    
                        
                        
                for j in range(len(rh)):
                    if rh[j] <= 0.0:
                        rh[j] = np.nan
            
                    elif rh[j] <= 0:
                        rh[j] = np.nan    
                        
                        
                for k in range(len(press)):
                    if press[k] <= 0.0:
                        press[k] = np.nan
            
                    elif press[k] <= 0:
                        press[k] = np.nan      
            
                #!!! IMPORTANT FOR SEA BREEZE RESEARCH
                # In order to not throw off averages w/ missing data replace 
                # missing values(-) or zero values with np.nan.
                # This is unfortunate necessity.  
                for i in range(len(WDir)):
                    if WDir[i] == 0.0:
                        WDir[i] = np.nan
            
                    if WSpd[i] == 0.0:
                        WSpd[i] = np.nan
                        
                    if WSpd[i] <0.0:
                        WSpd[i] = np.nan
            
                    if WDir[i] <0.0:
                        WDir[i] = np.nan
                        
            
                #%% Blank Arrays to Append Data
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
                  
                
                ## SET AS NUMPY ARRAY FOR THE WHERE AND NANMEAN TO WORK
                year_raw=np.array(year_raw)  
                month_raw=np.array(month_raw)        
                day_raw=np.array(day_raw)        
                hour_raw=np.array(hour_raw)        
                minute_raw=np.array(minute_raw)   
                WSpd= np.array(WSpd)
                WDir = np.array(WDir)
                temp = np.array(temp) 
                dewpt = np.array(dewpt) 
            
                rh = np.array(rh) 
                press = np.array(press)   
            
            ## ASSUMES NOT A FULL YEAR/month/ WITH MISSING MONTHS or days in between. otherwise put in the first and last month/day/year value for it to iterate through. Otherwise it'll find the right ones.          
            ## YEAR MONTH HOUR DAY MIN SEC MUST BE IN NP ARRAY TO BE USING IN NP.WHERE
                
                print(min(year_raw),max(year_raw)+1)
                print(min(month_raw),max(month_raw)+1)
                print("Average Interval: ", avg_interval)
            
                #%% LOOPING
                for year in range(int(min(year_raw)),int(max(year_raw)+1)):
                    #print (year)
                    if year%400 == 0:
                        leap = 0
                    elif year%100 == 0:
                        leap = 1
                    elif year%4 == 0:
                        leap = 0
                    else:
                        leap = 1
                    
                    for month in range(int(min(month_raw)),int(max(month_raw)+1)):
                        #print (month)
                        # IF NOT LEAP YEAR
                        if month == 2 and leap != 0:
                            for day in range(1,28+1):
                                for hour in range(0,24):
                                    ## LOOKING AT THE CURRENT HOUR AND THE 0th MINUTE OF THE NEXT
                                    fHour1 = np.where((hour_raw==hour)&(day_raw ==day)&(month_raw==month)\
                                    	&(year_raw == year))
                                    #print (fHour1)
                                    if hour+1 == 24:
                                        if day + 1 == 29:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==1)&(month_raw==month+1)\
                                	              &(year_raw == year)&(minute_raw==0))
                                        else:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==day+1)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    else:
                                        fHour2 = np.where((hour_raw==hour+1)&(day_raw ==day)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    #COMBINE
                                    fHour3 = np.array(fHour1).tolist()
                                    fHour4 = np.array(fHour2).tolist()
                                    #for item in 
                                    fHour5 = fHour3+fHour4
                                    hHour = list(itertools.chain.from_iterable(fHour5))
                                    
                                    ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan...
                                    ## NEEDS TO DO IT FOR EACH 15-min step
                                    if len(hHour) == 0:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            avg_year.append(year)        
                                            avg_month.append(month)
                                            if ijk == (60-avg_interval):
                                                if hour == 23:
                                                    avg_min.append(0)
                                                    avg_hour.append(0)
                                                    avg_day.append(day+1)
                                                else:
                                                    avg_min.append(0)
                                                    avg_hour.append(hour+1)
                                                    avg_day.append(day)     
            
                                            else:
                                                avg_min.append(ijk+avg_interval)
                                                avg_hour.append(hour)
                                                avg_day.append(day)    
                                            avg_ID.append(ID_String[0])
                                            avg_name.append(name[0])
                                            avg_fm.append(fm[0])
                                            avg_source.append(source[0])
                                            avg_lat.append(lat[0])
                                            avg_long.append(long[0])
                                            avg_elev.append(elev[0])
                                            avg_wspd.append(np.nan)
                                            avg_wdir.append(np.nan)
                                            avg_temp.append(np.nan)
                                            avg_dewpt.append(np.nan)
            
                                            avg_rh.append(np.nan)
                                            avg_press.append(np.nan)   
            
            
                                    # IS DATA - np.nanmean() and append
                                    elif hour_raw[hHour][0] == hour or hour_raw[hHour][0] == hour+1:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            tmp = ijk + 1
                                            #for tmpMin in minute_raw[hHour]:
                                            if ijk == (60-avg_interval):
                                                fMin1 = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                if hour+1 == 24: #need to go to a new day
                                                    if day+1 == 29: # go to the next month
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==1)&\
                                                            (month_raw==month+1)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                        
                                                    else: # add a day set min to 0
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==day+1)&\
                                                            (month_raw==month)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                    
                                                else: # no new day just add the hour
                                                    fMin2 = np.where((hour_raw==hour+1)&(day_raw ==day)&\
                                                        (month_raw==month)&(year_raw == year)&\
                                                        (minute_raw == 0))
                                                    
                                                fMin3 = np.array(fMin1).tolist()
                                                fMin4 = np.array(fMin2).tolist()
                                                fMin5 = fMin3+fMin4
                                                hMin = list(itertools.chain.from_iterable(fMin5))
            
                                            else: # not minute 45 idx
                                                fMin = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                hMin = np.array(fMin).tolist()[0]
                   
                                            #print (hMin)
                                            #hMin = np.array(fMin).tolist()[0]
                                            #print(hMin, minute_raw[hMin],ijk)
                                            ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan... 
                                        	## NEEDS TO DO IT FOR EACH 15-min step
                                            if len(hMin) == 0:
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
            
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(np.nan)
                                                avg_wdir.append(np.nan)
                                                avg_temp.append(np.nan)
                                                avg_dewpt.append(np.nan)
                                                avg_rh.append(np.nan)
                                                avg_press.append(np.nan)  
                                            # WHAT IF THE 0 ELEMENT IS 60
                                            elif (minute_raw[hMin][0] >= tmp and\
                                            	minute_raw[hMin][0] < ijk+avg_interval)\
                                                  or (minute_raw[hMin][0] == 0 and ijk == (60-avg_interval)):  
                                                ## SHOULD IT BE GREATER OR LESS THAN????
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
                                                tmp_wspd=  np.nanmean([WSpd[index] for index in hMin])
                                                tmp_wdir = np.nanmean([WDir[index] for index in hMin])
                                                tmp_temp = np.nanmean([temp[index] for index in hMin])
                                                tmp_dewpt = np.nanmean([dewpt[index] for index in hMin])
                                                tmp_rh = np.nanmean([rh[index] for index in hMin])
                                                tmp_press = np.nanmean([press[index] for index in hMin])
                                                
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(tmp_wspd)
                                                avg_wdir.append(tmp_wdir)
                                                avg_temp.append(tmp_temp)
                                                avg_dewpt.append(tmp_dewpt)
                                                avg_rh.append(tmp_rh)
                                                avg_press.append(tmp_press)
                                                            
            
                        # IF LEAP YEAR
                        elif month == 2 and leap == 0:
                            for day in range(1,29+1):
                                for hour in range(0,24):
                                    ## LOOKING AT THE CURRENT HOUR AND THE 0th MINUTE OF THE NEXT
                                    fHour1 = np.where((hour_raw==hour)&(day_raw ==day)&(month_raw==month)\
                                    	&(year_raw == year))
                                    #print (fHour1)
                                    if hour+1 == 24:
                                        if day + 1 == 30:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==1)&(month_raw==month+1)\
                                	              &(year_raw == year)&(minute_raw==0))
                                        else:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==day+1)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    else:
                                        fHour2 = np.where((hour_raw==hour+1)&(day_raw ==day)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    #COMBINE
                                    fHour3 = np.array(fHour1).tolist()
                                    fHour4 = np.array(fHour2).tolist()
                                    #for item in 
                                    fHour5 = fHour3+fHour4
                                    hHour = list(itertools.chain.from_iterable(fHour5))
                                    
                                    ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan...
                                    ## NEEDS TO DO IT FOR EACH 15-min step
                                    if len(hHour) == 0:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            avg_year.append(year)        
                                            avg_month.append(month)
                                            if ijk == (60-avg_interval):
                                                if hour == 23:
                                                    avg_min.append(0)
                                                    avg_hour.append(0)
                                                    avg_day.append(day+1)
                                                else:
                                                    avg_min.append(0)
                                                    avg_hour.append(hour+1)
                                                    avg_day.append(day)     
            
                                            else:
                                                avg_min.append(ijk+avg_interval)
                                                avg_hour.append(hour)
                                                avg_day.append(day)    
                                                
                                            avg_ID.append(ID_String[0])
                                            avg_name.append(name[0])
                                            avg_fm.append(fm[0])
                                            avg_source.append(source[0])
                                            avg_lat.append(lat[0])
                                            avg_long.append(long[0])
                                            avg_elev.append(elev[0])
                                            avg_wspd.append(np.nan)
                                            avg_wdir.append(np.nan)
                                            avg_temp.append(np.nan)
                                            avg_dewpt.append(np.nan)
                                            avg_rh.append(np.nan)
                                            avg_press.append(np.nan)   
            
            
                                    # IS DATA - np.nanmean() and append
                                    elif hour_raw[hHour][0] == hour or hour_raw[hHour][0] == hour+1:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            tmp = ijk + 1
                                            #for tmpMin in minute_raw[hHour]:
                                            if ijk == (60-avg_interval):
                                                fMin1 = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                if hour+1 == 24: #need to go to a new day
                                                    if day+1 == 30: # go to the next month
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==1)&\
                                                            (month_raw==month+1)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                        
                                                    else: # add a day set min to 0
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==day+1)&\
                                                            (month_raw==month)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                    
                                                else: # no new day just add the hour
                                                    fMin2 = np.where((hour_raw==hour+1)&(day_raw ==day)&\
                                                        (month_raw==month)&(year_raw == year)&\
                                                        (minute_raw == 0))
                                                    
                                                fMin3 = np.array(fMin1).tolist()
                                                fMin4 = np.array(fMin2).tolist()
                                                fMin5 = fMin3+fMin4
                                                hMin = list(itertools.chain.from_iterable(fMin5))
            
                                            else: # not minute 45 idx
                                                fMin = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                hMin = np.array(fMin).tolist()[0]
                   
                                            #print (hMin)
                                            #hMin = np.array(fMin).tolist()[0]
                                            #print(hMin, minute_raw[hMin],ijk)
                                            ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan... 
                                        	## NEEDS TO DO IT FOR EACH 15-min step
                                            if len(hMin) == 0:
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(np.nan)
                                                avg_wdir.append(np.nan)
                                                avg_temp.append(np.nan)
                                                avg_dewpt.append(np.nan)
                                                avg_rh.append(np.nan)
                                                avg_press.append(np.nan)  
                                            # WHAT IF THE 0 ELEMENT IS 60
                                            elif (minute_raw[hMin][0] >= tmp and\
                                            	minute_raw[hMin][0] < ijk+avg_interval)\
                                                  or (minute_raw[hMin][0] == 0 and ijk == (60-avg_interval)):  
                                                ## SHOULD IT BE GREATER OR LESS THAN????
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
                                                tmp_wspd=  np.nanmean([WSpd[index] for index in hMin])
                                                tmp_wdir = np.nanmean([WDir[index] for index in hMin])
                                                tmp_temp = np.nanmean([temp[index] for index in hMin])
                                                tmp_dewpt = np.nanmean([dewpt[index] for index in hMin])
            
                                                tmp_rh = np.nanmean([rh[index] for index in hMin])
                                                tmp_press = np.nanmean([press[index] for index in hMin])
                                                
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(tmp_wspd)
                                                avg_wdir.append(tmp_wdir)
                                                avg_temp.append(tmp_temp)
                                                avg_dewpt.append(tmp_dewpt)
                                                avg_rh.append(tmp_rh)
                                                avg_press.append(tmp_press)
                        ###############
                        elif month == 4 or month == 6 or month == 9 or month ==11:
                            for day in range(int(min(day_raw)),int(max(day_raw)+1)):
                                #print( list(range(min(day_raw),max(day_raw)+1)))
                                for hour in range(0,24):
                                    
                                    ## LOOKING AT THE CURRENT HOUR AND THE 0th MINUTE OF THE NEXT
                                    fHour1 = np.where((hour_raw==hour)&(day_raw ==day)&(month_raw==month)\
                                    	&(year_raw == year))
                                    #print (fHour1)
                                    if hour+1 == 24:
                                        if day + 1 == 31:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==1)&(month_raw==month+1)\
                                	              &(year_raw == year)&(minute_raw==0))
                                        else:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==day+1)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    else:
                                        fHour2 = np.where((hour_raw==hour+1)&(day_raw ==day)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    #COMBINE
                                    fHour3 = np.array(fHour1).tolist()
                                    fHour4 = np.array(fHour2).tolist()
                                    #for item in 
                                    fHour5 = fHour3+fHour4
                                    hHour = list(itertools.chain.from_iterable(fHour5))
                                    
                                    ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan...
                                    ## NEEDS TO DO IT FOR EACH 15-min step
                                    if len(hHour) == 0:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            avg_year.append(year)        
                                            avg_month.append(month)
                                            if ijk == (60-avg_interval):
                                                if hour == 23:
                                                    avg_min.append(0)
                                                    avg_hour.append(0)
                                                    avg_day.append(day+1)
                                                else:
                                                    avg_min.append(0)
                                                    avg_hour.append(hour+1)
                                                    avg_day.append(day)     
            
                                            else:
                                                avg_min.append(ijk+avg_interval)
                                                avg_hour.append(hour)
                                                avg_day.append(day)    
                                                
                                            avg_ID.append(ID_String[0])
                                            avg_name.append(name[0])
                                            avg_fm.append(fm[0])
                                            avg_source.append(source[0])
                                            avg_lat.append(lat[0])
                                            avg_long.append(long[0])
                                            avg_elev.append(elev[0])
                                            avg_wspd.append(np.nan)
                                            avg_wdir.append(np.nan)
                                            avg_temp.append(np.nan)
                                            avg_dewpt.append(np.nan)
                                            avg_rh.append(np.nan)
                                            avg_press.append(np.nan)   
            
            
                                    # IS DATA - np.nanmean() and append
                                    elif hour_raw[hHour][0] == hour or hour_raw[hHour][0] == hour+1:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            tmp = ijk + 1
                                            #for tmpMin in minute_raw[hHour]:
                                            if ijk == (60-avg_interval):
                                                fMin1 = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                if hour+1 == 24: #need to go to a new day
                                                    if day+1 == 31: # go to the next month
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==1)&\
                                                            (month_raw==month+1)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                        
                                                    else: # add a day set min to 0
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==day+1)&\
                                                            (month_raw==month)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                    
                                                else: # no new day just add the hour
                                                    fMin2 = np.where((hour_raw==hour+1)&(day_raw ==day)&\
                                                        (month_raw==month)&(year_raw == year)&\
                                                        (minute_raw == 0))
                                                    
                                                fMin3 = np.array(fMin1).tolist()
                                                fMin4 = np.array(fMin2).tolist()
                                                fMin5 = fMin3+fMin4
                                                hMin = list(itertools.chain.from_iterable(fMin5))
            
                                            else: # not minute 45 idx
                                                fMin = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                hMin = np.array(fMin).tolist()[0]
                   
                                            #print (hMin)
                                            #hMin = np.array(fMin).tolist()[0]
                                            #print(hMin, minute_raw[hMin],ijk)
                                            ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan... 
                                        	## NEEDS TO DO IT FOR EACH 15-min step
                                            if len(hMin) == 0:
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)     
            
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(np.nan)
                                                avg_wdir.append(np.nan)
                                                avg_temp.append(np.nan)
                                                avg_dewpt.append(np.nan)
                                                avg_rh.append(np.nan)
                                                avg_press.append(np.nan)  
                                            # WHAT IF THE 0 ELEMENT IS 60
                                            elif (minute_raw[hMin][0] >= tmp and\
                                                  minute_raw[hMin][0] < ijk+avg_interval)\
                                                  or (minute_raw[hMin][0] == 0 and ijk == (60-avg_interval)):  
                                                ## SHOULD IT BE GREATER OR LESS THAN????
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
                                                tmp_wspd=  np.nanmean([WSpd[index] for index in hMin])
                                                tmp_wdir = np.nanmean([WDir[index] for index in hMin])
                                                tmp_temp = np.nanmean([temp[index] for index in hMin])
                                                tmp_dewpt = np.nanmean([dewpt[index] for index in hMin])
                                                tmp_rh = np.nanmean([rh[index] for index in hMin])
                                                tmp_press = np.nanmean([press[index] for index in hMin])
                                                
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(tmp_wspd)
                                                avg_wdir.append(tmp_wdir)
                                                avg_temp.append(tmp_temp)
                                                avg_dewpt.append(tmp_dewpt)
            
                                                avg_rh.append(tmp_rh)
                                                avg_press.append(tmp_press)
                                                
            
                        else:
                            for day in range(int(min(day_raw)),int(max(day_raw)+1)):
                                #print( list(range(min(day_raw),max(day_raw)+1)))
                                for hour in range(0,24):
                                    ## LOOKING AT THE CURRENT HOUR AND THE 0th MINUTE OF THE NEXT
                                    fHour1 = np.where((hour_raw==hour)&(day_raw ==day)&(month_raw==month)\
                                    	&(year_raw == year))
                                    if hour+1 == 24:
                                        if day + 1 == 32:
                                            if month == 12:
                                                fHour2 = np.where((hour_raw==0)&(day_raw ==1)&(month_raw==1)\
                                    	              &(year_raw == year+1)&(minute_raw==0))  
                                                
                                            else:
                                                fHour2 = np.where((hour_raw==0)&(day_raw ==1)&(month_raw==month+1)\
                                    	              &(year_raw == year)&(minute_raw==0))
                                        else:
                                            fHour2 = np.where((hour_raw==0)&(day_raw ==day+1)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    else:
                                        fHour2 = np.where((hour_raw==hour+1)&(day_raw ==day)&(month_raw==month)\
                                    	         &(year_raw == year)&(minute_raw==0))
                                    #COMBINE
                                    fHour3 = np.array(fHour1).tolist()
                                    fHour4 = np.array(fHour2).tolist()
                                    #for item in 
                                    fHour5 = fHour3+fHour4
                                    hHour = list(itertools.chain.from_iterable(fHour5))
                                    
                                    ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan...
                                    ## NEEDS TO DO IT FOR EACH 15-min step
                                    if len(hHour) == 0:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            avg_year.append(year)        
                                            avg_month.append(month)
                                            if ijk == (60-avg_interval):
                                                if hour == 23:
                                                    avg_min.append(0)
                                                    avg_hour.append(0)
                                                    avg_day.append(day+1)
                                                else:
                                                    avg_min.append(0)
                                                    avg_hour.append(hour+1)
                                                    avg_day.append(day)     
            
                                            else:
                                                avg_min.append(ijk+avg_interval)
                                                avg_hour.append(hour)
                                                avg_day.append(day)    
                                                
                                            avg_ID.append(ID_String[0])
                                            avg_name.append(name[0])
                                            avg_fm.append(fm[0])
                                            avg_source.append(source[0])
                                            avg_lat.append(lat[0])
                                            avg_long.append(long[0])
                                            avg_elev.append(elev[0])
                                            avg_wspd.append(np.nan)
                                            avg_wdir.append(np.nan)
                                            avg_temp.append(np.nan)
                                            avg_dewpt.append(np.nan)
                                            avg_rh.append(np.nan)
                                            avg_press.append(np.nan)   
            
            
                                    # IS DATA - np.nanmean() and append
                                    elif hour_raw[hHour][0] == hour or hour_raw[hHour][0] == hour+1:
                                         for kji in range(0,60,avg_interval):
                                            ijk= kji
                                            tmp = ijk + 1
                                            #for tmpMin in minute_raw[hHour]:
                                            if ijk == (60-avg_interval):
                                                fMin1 = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                if hour+1 == 24: #need to go to a new day
                                                    if day+1 == 32: # go to the next month
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==1)&\
                                                            (month_raw==month+1)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                        
                                                    else: # add a day set min to 0
                                                        fMin2 = np.where((hour_raw==0)&(day_raw ==day+1)&\
                                                            (month_raw==month)&(year_raw == year)&\
                                                            (minute_raw == 0))
                                                    
                                                else: # no new day just add the hour
                                                    fMin2 = np.where((hour_raw==hour+1)&(day_raw ==day)&\
                                                        (month_raw==month)&(year_raw == year)&\
                                                        (minute_raw == 0))
                                                    
                                                fMin3 = np.array(fMin1).tolist()
                                                fMin4 = np.array(fMin2).tolist()
                                                fMin5 = fMin3+fMin4
                                                hMin = list(itertools.chain.from_iterable(fMin5))
            
                                            else: # not minute 45 idx
                                                fMin = np.where((hour_raw==hour)&(day_raw ==day)&\
                                                    (month_raw==month)&(year_raw == year)&\
                                                    (minute_raw >= tmp)\
                                                    &(minute_raw < ijk+avg_interval))
                                                hMin = np.array(fMin).tolist()[0]
                   
                                            #print (hMin)
                                            #hMin = np.array(fMin).tolist()[0]
                                            #print(hMin, minute_raw[hMin],ijk)
                                            ## NEED CONDITION FOR HOUR WITH NO DATA - np.nan... 
                                        	## NEEDS TO DO IT FOR EACH 15-min step
                                            if len(hMin) == 0:
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
            
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(np.nan)
                                                avg_wdir.append(np.nan)
                                                avg_temp.append(np.nan)
                                                avg_dewpt.append(np.nan)
                                                avg_rh.append(np.nan)
                                                avg_press.append(np.nan)  
                                            # WHAT IF THE 0 ELEMENT IS 60
                                            elif (minute_raw[hMin][0] >= tmp and\
                                            	minute_raw[hMin][0] < ijk+avg_interval)\
                                                  or (minute_raw[hMin][0] == 0 and ijk == (60-avg_interval)):  
                                                ## SHOULD IT BE GREATER OR LESS THAN????
                                                avg_year.append(year)        
                                                avg_month.append(month)
                                                if ijk == (60-avg_interval):
                                                    if hour == 23:
                                                        avg_min.append(0)
                                                        avg_hour.append(0)
                                                        avg_day.append(day+1)
                                                    else:
                                                        avg_min.append(0)
                                                        avg_hour.append(hour+1)
                                                        avg_day.append(day)     
            
                                                else:
                                                    avg_min.append(ijk+avg_interval)
                                                    avg_hour.append(hour)
                                                    avg_day.append(day)    
                                                tmp_wspd=  np.nanmean([WSpd[index] for index in hMin])
                                                tmp_wdir = np.nanmean([WDir[index] for index in hMin])
                                                tmp_temp = np.nanmean([temp[index] for index in hMin])
                                                tmp_dewpt = np.nanmean([dewpt[index] for index in hMin])
                                                tmp_rh = np.nanmean([rh[index] for index in hMin])
                                                tmp_press = np.nanmean([press[index] for index in hMin])
                                                
                                                avg_ID.append(ID_String[0])
                                                avg_name.append(name[0])
                                                avg_fm.append(fm[0])
                                                avg_source.append(source[0])
                                                avg_lat.append(lat[0])
                                                avg_long.append(long[0])
                                                avg_elev.append(elev[0])
                                                avg_wspd.append(tmp_wspd)
                                                avg_wdir.append(tmp_wdir)
                                                avg_temp.append(tmp_temp)
                                                avg_dewpt.append(tmp_dewpt)
                                                avg_rh.append(tmp_rh)
                                                avg_press.append(tmp_press)
                                                

                #print ("DONE")

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
                outstring = outdir + fname +"_hr_avg_control.csv"
                    
                df = pd.DataFrame(blankMatrix, columns = HEADING, index=None)
                df['ID_String'] = avg_ID # BLANK 0
                df['Name_string'] = avg_name # BLANK 0
                df['FM_string'] = avg_fm # BLANK 0
                df['Source_string'] = avg_source # BLANK 0
            
                df = pd.DataFrame.replace(df,to_replace=' ', value=np.nan)
            
                df.to_csv(outstring)
                
                del blankMatrix,data,df  ## Comment out for debugging
                #break
                
                
                ### NEED TO GET RID OF TIME BEFORE AND AFTER THE CASE STUDY with trim_hr_avg