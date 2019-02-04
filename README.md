# Data_Processing

Eric Allen, University of Delaware, Last Updated: 2/4/2019
Contact allenea@udel.edu with any questions.

Program to process data and it's metadata for verification of wrf, analysis, plotting, etc. 
	- Creates uniform format with quality control for each type of data.
	- Add a new directory and follow protocols for new sources of data
	- I'll take a closer look and make this better at some point when I have time......
	

Everything is ordered in the order it should be processed. Each data source Prep (Convert) then CombineAll. Then for all data Combine,Prep, QC.
** I rearranged some things and changed a few directory names to be more generic. If there is an issue check that first. **


#### Verification_Data ####

	#### NDBC BUOY DATA ####
	 - ndbc_data_retrieval.py : add the station names and start year and it'll retrieve any available NDBC data for those stations
	 - Buoy_Prep.py
	 - CombineAll_NDBC.py
	 - Metadata for the stations I used in the DelMarVa region
 
	#### DelDOT DATA ####
	 - DelDOT_Prep.py
	 - CombineAll_DELDOT.py
 
 
	 #### DEOS DATA ####
	 - DEOS_Prep.py
	 - CombineAll_DEOS.py
 
	 #### Mesowest DATA ####
	 - Mesowest_Prep.py  (Missing anemometer heights if that's important to you. Also metadata provided can be a bit sketchy)
 
	 #### NCEI_LCD DATA ####
	  - ReadData_Convert.py
	  - NCEI_Prep.py
	  - WBAN CODES. INCOMPLETE. MISSING STATION ABBRIVATIONS (CALLSIGNS) 
  
	#### NJMET DATA ####
	 - NJMET_Prep.py
	 - CombineAll_NJMET.py
 
	 --------------------------
 
 
	 #### Verify_Converted DATA ####
	 - All_Sources: Contains all the data sources processed above
	 - CombineAll_data.py
	 - Prep_4_r.py
	 - Quality_Control.py

 
 
 ----------------------------
 
 #### Python_Casestudy_Analysis ####
 
	#### FILES: ####
	 - PullingStationData_4_CaseStudy.py: IMPORTANT. Set your list of case studies and run to extract.
	 - map_OBS_Assimilation.py
	 - map_OBS_Verification.py
	 - hr_avg_for_verification.py: Forward 30-min avg (not well tested wrote to do what I needed).
	 - trim_hr_avg.py: Trims to case study time
	 
  	#### Plotting_Programs: ####
	 - Create a simple time series for the different variables.
	 
	 
 ----------------------------
 
 #### Assimilation_Data ####
	#### EMPTY: Where the OBS_CSV_TO_LITTLE_R repository would go.....
		- Directory "Ferry_Data" will be created to put data extracted from this directory for analysis.
		
		