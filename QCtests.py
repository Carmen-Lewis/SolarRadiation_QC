# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:23:54 2021
@author: Carmen Lewis (carmen@solarXY.org)

Quality control test functions.

C. A. Gueymard, “A reevaluation of the solar constant based on a 42-year total solar irradiance time series and a reconciliation of spaceborne observations,” Solar Energy, vol. 168, pp. 2-9, 2018. DOI: 10.1016/j.solener.2018.04.001
C. Long and E. Dutton, "BSRN Global Network recommended QC tests, V2.0," Tech. Rep. [Online]. Available: https://epic.awi.de/id/eprint/30083/1/BSRN_recommended_QC_tests_V2.pdf (Accessed 25 May 2021)
NREL, “2000 ASTM Standard Extraterrestrial Spectrum Reference E-490-00”, NREL.gov. [Online]. Available: https://www.nrel.gov/grid/solar-resource/spectra-astm-e490.html (Accessed 3 July 2020)
L. Wong and W. Chow, "Solar radiation model," Applied Energy, vol. 69, no. 3, pp. 191-224, 2001.
"""
import plots

import numpy as np
import pandas as pd

from pvlib.solarposition import nrel_earthsun_distance

#solar constant at mean Earth-Sun distance
#S_0 = 1366.1         #(NREL 2000)
S_0 = 1361.1          #(Gueymard 2018)

def LongDutton(df):
    
    df['mu_0'] = df['thetaRad'].apply(np.cos)
    
    df.loc[df['theta'] > 90, 'mu_0'] = 0.0
    
    #[*184]
    #solar constant adjusted for Earth-Sun distance (Long and Dutton)
    df['S_a'] = S_0/df['AU']**2
    #calculate the GHI in terms of the measured DHI and DNI
    df['SumSW'] = df['DHI'] + df['DNI']*df['mu_0']
    
    #Flag 1: Physical GHI
    df.loc[(df['GHI'] > -4) & (df['GHI'] < (df['S_a']*1.5*df['mu_0']**(1.2) + 100)), 'F_G1'] = df['GHI']
    df.loc[(df['GHI'] <= -4) | (df['GHI'] >= (df['S_a']*1.5*df['mu_0']**(1.2) + 100)), 'F_G1_fail'] = df['GHI']
    #Flag 2: Physical DHI
    df.loc[(df['DHI'] > -4) & (df['DHI'] < df['S_a']*0.95*df['mu_0']**(1.2) + 100), 'F_D1'] = df['DHI']
    df.loc[(df['DHI'] <= -4) | (df['DHI'] >= df['S_a']*0.95*df['mu_0']**(1.2) + 100), 'F_D1_fail'] = df['DHI']
    #Flag 3: Physical DNI
    df.loc[(df['DNI'] > -4) & (df['DNI'] < df['S_a']), 'F_I1'] = df['DNI']
    df.loc[(df['DNI'] <= -4) | (df['DNI'] >= df['S_a']), 'F_I1_fail'] = df['DNI']
    
    F_G1 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_G1'].count()
    F_G1_fail = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_G1_fail'].count()
    F_D1 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_D1'].count()
    F_D1_fail = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_D1_fail'].count()
    F_I1 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_I1'].count()
    F_I1_fail = df.groupby(pd.Grouper(key='DateTime', freq='M'))['F_I1_fail'].count()
                           
    print(F_G1.values)
    print(F_G1_fail.values)
    print(F_D1.values)
    print(F_D1_fail.values)
    print(F_I1.values)
    print(F_I1_fail.values)
    
    #plots.DAA_physicalTestPlot(df)
    
    #Flag 4: Ratio GHI
    df.loc[(df['SumSW'] > 50), 'G_ratio'] = df['F_G1']/df['SumSW']
    df.loc[((df['G_ratio'] >= 1.8) | (df['G_ratio'] <= -1.8)) & (df['theta'] <= 75), 'G_flag1'] = 1
    df.loc[((df['G_ratio'] >= 1.15) | (df['G_ratio'] <= -1.15)) & (df['theta'] > 75) & (df['theta'] < 93), 'G_flag2'] = 1
    df.loc[(df['G_flag1'] != 1) & (df['G_flag2'] != 1), 'FG_final'] = df['F_G1']
    #Flag 5: Ratio DHI
    df.loc[(df['F_G1'] > 50), 'D_ratio'] = df['F_D1']/df['F_G1']
    df.loc[(df['D_ratio'] >= 1.05) & (df['theta'] <= 75), 'D_flag1'] = 1
    df.loc[(df['D_ratio'] >= 1.10) & (df['theta'] > 75) & (df['theta'] < 93), 'D_flag2'] = 1
    df.loc[(df['D_flag1'] != 1) & df['D_flag2'] != 1, 'FD_final'] = df['F_D1']
    df['FI_final'] = df['F_I1']
    
    plots.DAA_compareTestPlot(df)
    
    G_flag1 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['G_flag1'].count()
    G_flag2 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['G_flag2'].count()
    D_flag1 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['D_flag1'].count()
    D_flag2 = df.groupby(pd.Grouper(key='DateTime', freq='M'))['D_flag2'].count()
    
    print(G_flag1.values)
    print(G_flag2.values)
    print(D_flag1.values)
    print(D_flag2.values)
    
    #M. J. Reno, C. W. Hansen, and J. S. Stein, "Global horizontal irradiance clear sky models: Implementation and analysis", SANDIA report SAND2012-2389, 2012.
    #df['x'] = (2*np.pi/365)*(df['doy'] - 1) #((360/365)*(df['doy']-81)).astype(float).apply(np.deg2rad)
    #df['F0'] = S_0*(1.00011 + 0.034221*np.cos(df['x']) + 0.00128*np.sin(df['x']) \
    #              - 0.000719*np.cos(2*df['x']) + 0.000077*np.sin(2*df['x']))
