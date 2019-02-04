#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:51:23 2018

@author: allenea
"""
import pandas  as pd
import os
import glob 

mydir =  os.getcwd() #os.path.abspath('..')

def merge_csv(file1,file2):
    a = pd.read_csv(file1,low_memory=False)
    b = pd.read_csv(file2,low_memory=False)
    a = a.mask(a==' ',other = -888888.0)
    b = b.mask(b==' ',other = -888888.0)

    merged = pd.concat([a,b])
    merged.to_csv(mydir + '/Merged/'+file1[:6]+"-deldot-verify-data.csv", index=False)
        
        
def merge_like_files():

    os.chdir(os.getcwd()+'/Raw/')
    
    fileList = glob.glob('*.csv')
    fileList.sort()
    
    mergedList = []
    for file1 in fileList:
        for file2 in fileList:
            if file1[:6] == file2[:6] and file1 !=file2 and file1[:6] not in mergedList:
                #print file1, file2
                merge_csv(file1,file2)
                mergedList.append(file1[:6])
                print ("MERGED", file1[:6])
            elif file1[:6] != file2[:6] and file1!=file2 and file1[:6] not in mergedList and file2 == fileList[-1]  :
                #print file1, file2
                a = pd.read_csv(file1,low_memory=False)
                a = a.mask(a==' ',other = -888888.0)

                a.to_csv(mydir + '/Merged/'+file1[:6]+"-deldot-verify-data.csv", index=False)
                print ("SINGLE" , file1[:6])
            elif file1[:6] == file2[:6] and file1==file2 and file1[:6] not in mergedList and file2 == fileList[-1]  :
                #print file1, file2
                a = pd.read_csv(file1,low_memory=False)
                a = a.mask(a==' ',other = -888888.0)
                a.to_csv(mydir + '/Merged/'+file1[:6]+"-deldot-verify-data.csv", index=False)
                print ("SINGLE" , file1[:6])