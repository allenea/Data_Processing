#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 13:53:27 2018

@author: allenea

AUTHOR:  Eric Allen, UNIVERSITY OF DELAWARE, ** allenea@udel.edu 
** Contact with any questions or suggestions

Last Modified: Tuesday October 31st 6:16 PM EDT

GET --> RAW ---> MERGED ----> REFORMATED ---->Verification_Data

"""
import time
import os
import gzip
import wget


## STATIONS YOU WANT DATA FROM MAKE SURE YOU ALSO ADD THOSE STATIONS TO THE METADATA CSV FILE
station_list = ["DELD1","CHCM2","SJSN4","BRND1","CMAN4","LWSD1",\
                "JCRN4","ACMN4","44009","OCIM2","BISM2","CAMM2",\
                "TPLM2","TCBM2","44062","44058","RPLV2","WAHV2",\
                "AVAN4","SCLD1","DRSD1"]

#station_list = ["DELD1", "RDYD1", "SJSN4", "BTHD1", "44009", "OCSM2","TCBM2", "ACYN4", "JCRN4", "MRCP1", "44089", "OCIM2", "LWSD1", "CMAN4", "CHCM2", "BRND1", "BISM2"] 
#### OCSM2, BTHD1, SCLD1 and JCTN4 have no data.... must get from NERRS... don't want to so remove.

## SET START YEAR
start = 2010





#%% NDBC DOES NOT HAVE HISTORICAL DATA FOR THE CURRENT YEAR
end = int(time.ctime()[-4:])
print ("Start Year: " + str(start) +". End Year: ",str(end))
data_dir = os.getcwd()+"/Raw/"
print ("LENGTH OF LIST: ", len(station_list))



for station in station_list:
    for year in range(start,end):
        #https://www.ndbc.noaa.gov/view_text_file.php?filename=44009h2005.txt.gz&dir=data/historical/stdmet/
        getFile1 = "https://www.ndbc.noaa.gov/data/historical/stdmet/"+station.lower()+"h"+str(year)+".txt.gz"
        
        getFile2 ="https://www.ndbc.noaa.gov/data/historical/cwind/"+station.lower()+"c"+str(year)+".txt.gz"
        tmpoutfile1 = data_dir+station+"h"+str(year)+".txt.gz"
        tmpoutfile2 = data_dir+station+"c"+str(year)+".txt.gz"

        outfile1 = data_dir + station +"_stdmet_"+str(year)+".txt" 
        outfile2 = data_dir + station +"_cwind_"+str(year)+".txt" 
        #%% Continuous Wind Data (every 10 minutes)     
         
        try:
            os.remove(outfile1)
        except OSError:
            pass
         
            
        try:
            wget.download(getFile1, tmpoutfile1)
            try:
                inF = gzip.GzipFile(tmpoutfile1, 'rb')
                s = inF.read()
                inF.close()
            
                outF = open(outfile1, 'wb')
                outF.write(s)
                outF.close()
                os.remove(tmpoutfile1)

            except:
                print ("STD MET FILE DOWNLOADED, UNABLE TO GZIP")
        except:
            print ("MISSING stdmet:", station, year)
            
        #%% Continuous Wind Data (every 10 minutes)     
        try:
            os.remove(outfile2)
        except OSError:
            pass
         
            
        try:
            wget.download(getFile2, tmpoutfile2)
            
            try:
                inF = gzip.GzipFile(tmpoutfile2, 'rb')
                s = inF.read()
                inF.close()
            
                outF = open(outfile2, 'wb')
                outF.write(s)
                outF.close()
                os.remove(tmpoutfile2)
        
            except:
                print ("WIND FILE DOWNLOADED, UNABLE TO GZIP")
        except:
            print ("MISSING cwind:", station, year)
       