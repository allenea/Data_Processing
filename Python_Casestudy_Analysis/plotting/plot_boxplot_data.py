#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:41:51 2018

@author: allenea

Combine Verification data with assimilation data and plot it by case study and variable.

Box and Whisker Plot with CMLF and Average (all other) data plotted.
"""

import glob
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import sys
import os


casestudy_time = ['2014-06-04_06:00','2014-06-08_06:00','2015-08-14_06:00']
dtype_subusage = ['10m','original']
dtype_usage = ["Verification", "Assimilation"]
variables = ['Wind_Speed (m/s)','Wind_Direction (deg)','Air_Temperature (K)','Dewpoint_Temperature (K)','Relative Humidity (%)','Pressure (Pa)']
#variables = ['Wind_Direction (deg)']

isRaw = False
mydir = os.path.abspath('../')
data_dir = os.path.abspath('../../')

for variable in variables:
    print (variable)
    for case_time in casestudy_time:
        #for usage in dtype_usage:
        for dtype1 in dtype_subusage:
            filelst= []
            for datype in dtype_usage:
                if dtype1 == "original" and datype =="Verification":
                    if isRaw == True:
                        data_file = data_dir+"/Verification_Data/verify_case_study_data/"+dtype1+"/"+case_time[0:10]+'/' ### RAW
                    else:
                        data_file = data_dir+"/Verification_Data/hr_avg_trim/"+dtype1+"/"+case_time[0:10]+'/' ### TRIM

        
                elif dtype1 == "10m" and datype =="Verification":
                    if variable !='Wind_Speed (m/s)':
                        break
                    else:
                        if isRaw == True:
                            data_file = data_dir+"/Verification_Data/verify_case_study_data/"+dtype1+"/"+case_time[0:10]+'/' #### RAW
                        else:
                            data_file = data_dir+"/Verification_Data/hr_avg_trim/"+dtype1+"/"+case_time[0:10]+'/' #### TRIM
                        
                elif dtype1 == "original" and datype =="Assimilation":
                    if isRaw == True:
                        data_file = data_dir+"/Ferry_Data/case_study_data/"+dtype1+"/"+case_time[0:10]+'/' ### RAW
                    else:
                        data_file = data_dir+"/Ferry_Data/hr_avg_trim/"+dtype1+"/"+case_time[0:10]+'/' ### TRIM

        
                elif dtype1 == "10m" and datype =="Assimilation":
                    if variable !='Wind_Speed (m/s)':
                        break
                    else:
                        if isRaw == True:
                            data_file = data_dir+"/Ferry_Data/case_study_data/"+dtype1+"/"+case_time[0:10]+'/' #### RAW
                        else:
                            data_file = data_dir+"/Ferry_Data/hr_avg_trim/"+dtype1+"/"+case_time[0:10]+'/' #### TRIM
                            
                     
                if isRaw == True:
                    outdir =  mydir+"/plots/All_Data/OBS/"
                elif isRaw == False:
                    outdir =  mydir+"/plots/All_Data/AVG/BOX/"
        
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                    
                filelst.append(data_file)
                
            if len(filelst) == 0:
                continue
            print(filelst)
            
            fig, ax = plt.subplots(sharex=True, figsize=(15,7)) 

            curMax = 0
    
            legendNames=[]
            allWinds = []
            landWinds = []
            waterWinds = []
            
            isDEOS1DA = False; isDEOS2V = False; isDelDOT = False; isASOS = False; isNDBC = False
            isCMLF = False; isNJMET= False
            lenFile = len(glob.glob(data_file+'*.csv'))
            allWinds = []
            count = 0
            for fileDIR in filelst:
                for file in glob.glob(fileDIR+'*.csv'):    
                    data = pd.read_csv(file, low_memory=False)
                    data.columns.tolist()
                    data = data.mask(data == " ",other = np.nan)
                    data = data.mask(data == "",other = np.nan)
                    data = data.mask(data == -888888.0, other = np.nan)
                    data['Wind_Speed (m/s)'] = data['Wind_Speed (m/s)'].mask(data['Wind_Speed (m/s)'] < 0, other = np.nan)
        
        
                    ID_String = np.array(data['ID_String'],dtype=str)
                    if variable == 'Wind_Speed (m/s)':
                        variable_data= np.array(data['Wind_Speed (m/s)'])
                    elif variable == 'Wind_Direction (deg)':
                        variable_data = np.array(data['Wind_Direction (deg)'])
                        #countWDIR = 0
                        #new_wdir = [pd1 * (m.pi / 180)  for pd1 in tmp_wdir]

                        #variable_data = np.array(new_wdir)
                    elif variable == 'Air_Temperature (K)':
                        variable_data = np.array(data['Air_Temperature (K)'])
                    elif variable == 'Dewpoint_Temperature (K)':
                        variable_data = np.array(data['Dewpoint_Temperature (K)']) 
                    elif variable == "Relative Humidity (%)":
                        variable_data = np.array(data['Relative Humidity (%)'])
                    elif variable == "Pressure (Pa)":
                        variable_data = np.array(data['Pressure (Pa)']) 
                    else:
                        sys.exit(0)
                    
                    time = []
        
                    if isRaw == False:
                        year =np.array(data['YEAR'],dtype=int) 
                        month =np.array(data['MONTH'],dtype=int) 
                        day = np.array(data['DAY'],dtype=int) 
                        hour =np.array(data['HOUR'],dtype=int) 
                        minute = np.array(data['MINUTE'],dtype=int) 
                        for idx in range(len(year)):
                            utc_dt= datetime.datetime(year[idx],month[idx],day[idx],hour[idx],minute[idx])
                            time.append(utc_dt.strftime('%d/%H:%M'))
                    elif isRaw == True:
                            Date = np.array(data['DATE'],dtype=str)
                            for dte in Date:
                                utc_dt= datetime.datetime(int(dte[0:4]),int(dte[4:6]),int(dte[6:8]),int(dte[8:10]),int(dte[10:12]),int(dte[12:14]))
                                #dt= utc_dt.strftime('%Y-%m-%d %H:%M:%S')
                                dt= utc_dt.strftime('%d/%H:%M')
                                time.append(dt)
                     
                    ## THIS SHOULD BE NUMBER OF HOURS * 2 + 1
                    if (len(variable_data) != 49) or ID_String[0] == "CMLF":
                        pass
                    else:
                        allWinds.append(variable_data.tolist())
                    curMax +=1
                    
                    if ID_String[0] == "CMLF":
                        if isCMLF == False:
                            isCMLF = True
                            ax.plot(time,variable_data,marker= '*',linestyle=None,color='green',linewidth=4,label="CMLF")
                        else:
                            ax.plot(time,variable_data,marker= '*',linestyle=None,color='green',label="CMLF")
                        
            tmpWindsAll = np.array(allWinds)
            tmpWindsWater = np.array(waterWinds)
            tmpWindsLand = np.array(landWinds)
    
            avgWinds = np.nanmean(tmpWindsAll,axis=0)       
            avgWindsLand = np.nanmean(tmpWindsLand,axis=0)
            avgWindsWater = np.nanmean(tmpWindsWater,axis=0)
            
            ax.plot(time,avgWinds,'gold',linewidth=4,label="Average")
            #ax.plot(time,avgWindsLand,'k',linewidth=4,label="Average Land Obs")
            #ax.plot(time,avgWindsWater,'c',linewidth=4,label="Average Marine Obs")
            
            
            df = pd.DataFrame(allWinds,columns=time)
            """
            
            Make a box-and-whisker plot from DataFrame columns, optionally grouped by some other columns.
            A box plot is a method for graphically depicting groups of numerical data through their quartiles.
            The box extends from the Q1 to Q3 quartile values of the data, with a line at the median (Q2).
            The whiskers extend from the edges of box to show the range of the data.
            The position of the whiskers is set by default to 1.5 * IQR (IQR = Q3 - Q1) from the edges of the box.
            Outlier points are those past the end of the whiskers.
            
            boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)

            """
    
            if "Wind_Speed (m/s)" == variable:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                ax.set_yticks(np.arange(0, 13, step=0.5))
                ax.set_yticklabels(np.arange(0, 13, step=0.5), fontsize=14)
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')
                
            elif 'Air_Temperature (K)' == variable:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                ax.set_yticks(np.arange(280, 315, step=5))
                ax.set_yticklabels(np.arange(280, 315, step=5), fontsize=14)
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')
                
            elif 'Dewpoint_Temperature (K)' == variable:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                ax.set_yticks(np.arange(280, 315, step=5))
                ax.set_yticklabels(np.arange(280, 315, step=5), fontsize=14)
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')  
          
            elif 'Relative Humidity (%)' == variable:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                ax.set_yticks(np.arange(0, 101, step=10))
                ax.set_yticklabels(np.arange(0, 101, step=10), fontsize=14)
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')  
                
            elif 'Wind_Direction (deg)' == variable:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                #http://snowfence.cfans.umn.edu/Components/winddirectionanddegreeswithouttable3.htm
                awdir = np.arange(-11.25,371.26,22.5)
                text_wdir = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_yticks(awdir[::2])
                ax.set_yticklabels(text_wdir[::2], fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')
                
            else:
                boxplot = df.boxplot(column=time,ax=ax,grid=False,return_type='axes',rot=45, fontsize=14)
                atime = np.arange(len(time))
                ax.set_xticks(atime[::2])
                ax.set_xticklabels(time[::2], fontsize=14)
                ax.set_yticklabels(ax.get_yticks(), fontsize=14)
                ax.set_ylabel(variable, fontsize=16,fontweight='bold')
                ax.set_xlabel('Time (UTC)', fontsize=16,fontweight='bold')
                
                
            plt.legend(loc="best", ncol=4, fontsize=14, labelspacing = -0.1, columnspacing =  0.5)
            plt.gcf().autofmt_xdate()



            if isRaw == True:
                if "Wind_Speed (m/s)" in variable and dtype1 == "10m":
                    plt.title("Observed "+dtype1+" Wind Speeds (m/s) - "+case_time, fontsize=20)
                    
                elif "Wind_Speed (m/s)" in variable and dtype1 == "original":
                    plt.title("Observed Wind Speeds (m/s) - "+case_time, fontsize=20)
                    
                else:
                    plt.title("Observed "+variable+"  -  "+case_time, fontsize=20)
            else:
            
                if "Wind_Speed (m/s)" in variable and dtype1 == "10m":
                    plt.title("30 Minute Averaged "+dtype1+" Wind Speeds Observed On "+case_time, fontsize=20)
                    
                elif "Wind_Speed (m/s)" in variable and dtype1 == "original":
                    plt.title("30 Minute Averaged "+dtype1+" Wind Speeds Observed On "+case_time, fontsize=20)
    
                else:
                    plt.title("30 Minute Averaged "+variable+" Observed On "+case_time, fontsize=20)
                 
    
    
            if isRaw == True:
                plt.savefig(outdir+"Time-Series_obs_"+dtype1+"_"+variable[:-6]+"_"+case_time[0:10]+"BOX.png")
            else:
                plt.savefig(outdir+"Time-Series_avg_"+dtype1+"_"+variable[:-6]+"_"+case_time[0:10]+"BOX.png")
            
            plt.close()