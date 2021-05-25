# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:09:38 2021
@author: Carmen Lewis (carmen@solarXY.org)

Main function for solar radiation quality control tests.

Reda, I. and Andreas, A. "Solar position algorithm for solar radiation applications," Solar Energy, vol. 76, pp. 577–589, 2004. DOI: 10.1016/j.solener.2003.12.003
"""

import plots

import pandas as pd
import numpy as np

from pvlib.location import Location
from pvlib.solarposition import spa_python

import datetime as dt
import sys
import glob
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#set location parameters
#LOCATION = Location(-33.92810059, 18.86540031,'Etc/GMT+2', 119, 'SUN')
LOCATION = Location(-30.6667, 23.9930,'Etc/GMT+2', 1287, 'DAA')

#set filepath
#FILEPATH = 'SUN Minute.csv'
FILEPATH = 'Data_%s/' %LOCATION.name

#set datasource, either BSRN or SAURAN
DATASOURCE = 'BSRN'

def read():

    if(DATASOURCE == 'SAURAN'):
        #date format
        dateparse = lambda x: dt.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
        #read csv
        try:
            df = pd.read_csv(FILEPATH, skiprows=[0,2,3], parse_dates=['TmStamp'], 
                             index_col='TmStamp', date_parser=dateparse)
            
            #set columns names
            df.rename(columns = {'SunWM_Avg':'GHI', 'AirTC_Avg':'T',
                                 'TrackerWM_Avg':'DNI_1', 'Tracker2WM_Avg':'DNI_2',
                                 'ShadowWM_Avg': 'DHI_1', 'ShadowbandWM_Avg ':'DHI_2'}, inplace = True) 
            df['P'] = df['BP_mB_Avg']*100   #barometric pressure in Pa

        except IOError:
            print('Unable to load', FILEPATH)
            sys.exit()
    elif(DATASOURCE == 'BSRN'):
        #date format
        dateparse = lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M')
        #read each file within FILEPATH
        try:
            all_files = glob.glob(os.path.join(FILEPATH, '*.tab'))
            all_df = []
            for f in all_files:
                if('2019' in f):
                    rws = 33
                else:
                    rws = 31
                df = pd.read_csv(f, sep="\t", skiprows=rws, index_col=0, 
                                 parse_dates=True, date_parser=dateparse,
                                 header=None)
                all_df.append(df)
                
            df = pd.concat(all_df)
            
            #set column names

            df.columns = ['Height', 'GHI', 'GHI_std_dev',
                          'GHI_min', 'GHI_max', 'DNI', 'DIR_std_dev',
                          'DNI_min', 'DNI_max', 'DHI', 'DHI_std_dev',
                          'DHI_min', 'DHI_max', 'LWD', 'LWD_std_dev',
                          'LWD_min', 'LWD_max', 'T', 'RH', 'P']

        except IOError:
            print('Directory not accessible', FILEPATH)
            sys.exit()
    else:
        print('Data source %s does not exist' %DATASOURCE)
        sys.exit()
        
    #clean dataset of possible duplicates
    df = df.dropna(subset=['GHI'])

    #add missing timestamps within range to dataframe
    r = pd.date_range(start='%s' %df.index[0], end='%s' %df.index[-1], freq='min')
    df = df.reindex(r).reset_index().set_index('index')
    df['DateTime'] = df.index
    
    #replace NaN temperature & pressure values within standard values
    df.loc[df['P'].isnull(), 'P'] = 873.2465*100
    df.loc[df['T'].isnull(), 'T'] = 18
    
    #Calculate the solar zenith angle, theta and convert series to df (Reda and Andreas 2008)
    df1 = spa_python(df.index, LOCATION.latitude, LOCATION.longitude, \
                    altitude=LOCATION.altitude, pressure=df['P'], \
                    temperature=df['T'], atmos_refract=None).zenith.to_frame()
    #localize new df to LOCATION timezone, convert to UTC and localize to naive
    df1 = df1.tz_localize(LOCATION.tz).tz_convert('UTC').tz_localize(None)
    #cast new df column to original df
    df['theta'] = df1['zenith']
    #solar zenith angle in radians
    df['thetaRad'] = df['theta'].astype(float).apply(np.deg2rad)
    
    return df

if __name__ == "__main__":
    df = read()
    plots.press_temp(df)                    #test plot pressure and temperature
