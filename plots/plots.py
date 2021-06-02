# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:16:00 2021
@author: Carmen Lewis (carmen@solarXY.org)

Test and result plots for QC tests.
"""

import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
plt.rcParams.update({'font.size': 12, 'font.family': 'cmr10', 'mathtext.fontset': 'cm'})
import datetime as dt
from calendar import monthrange
import pandas as pd
import seaborn as sns
import numpy as np

#colour range
cl = ['#9e0142','#d53e4f','#f46d43','#fdae61', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2']

def GHI(df):
    
    rcParams['figure.figsize'] = 20, 2
    fig, ax = plt.subplots(1, 1)
    
    #slice dataset to specific year & month
    df1 = df[(df['DateTime'].dt.year == 2019) & (df['DateTime'].dt.month == 1)]
    
    ax.plot(df1['SumSW'], lw=0.8, color=cl[1], label='Calculated')
    ax.plot(df1['GHI'], lw=0.8, color='black', label='Measured')
    
    ax.legend()
    
def DAA_compareTestPlot(df):
    
    rcParams['figure.figsize'] = 20, 10
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)

    #slice dataset to specific year & month
    df1 = df[(df['DateTime'].dt.year == 2019) & (df['DateTime'].dt.month == 1)]
    
    ax[0].title.set_text('DAA: QC Physical Tests')
    ax[0].plot(df1['DateTime'], df1['GHI'], lw=0.8, color='black')
    ax[0].plot(df1['G_flag1'], lw=5, color=cl[1])
    ax[0].plot(df1['G_flag2'], lw=5, color=cl[6])
    ax[0].set_ylabel('GHI')
    ax[0].set_ylim(0, 1490)
    ax[0].set_xlim(dt.datetime(2019, 1, 1, 0, 0, 0), dt.datetime(2019, 1, 30, 23, 59, 0))
    ax[0].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T1')
    ax[0].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_G1_fail'].count())
    
    ax[1].plot(df1['DateTime'], df1['DNI'], lw=0.8, color='black')
    #ax[1].plot(df1['F_I1_fail'], lw=5, color=cl[1])
    ax[1].set_ylabel('DNI')
    ax[1].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T2')
    ax[1].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_I1_fail'].count())
    
    ax[2].plot(df1['DateTime'], df1['DHI'], lw=0.8, color='black')
    ax[2].plot(df1['D_flag1'], lw=5, color=cl[1])
    ax[2].plot(df1['D_flag2'], lw=5, color=cl[6])
    ax[2].set_ylabel('DHI')
    ax[2].set_xlabel('Date')
    ax[2].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T3')
    ax[2].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_D1_fail'].count())
    
    fig.subplots_adjust(wspace=0, hspace=0)
    plt.savefig('ComparativeTests_DAA.png',  bbox_inches='tight', format='png', dpi=600)

def DAA_physicalTestPlot(df):
    
    rcParams['figure.figsize'] = 20, 10
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)

    #slice dataset to specific year & month
    df1 = df[(df['DateTime'].dt.year == 2019) & (df['DateTime'].dt.month == 1)]
    
    ax[0].title.set_text('DAA: QC Physical Tests')
    ax[0].plot(df1['DateTime'], df1['GHI'], lw=0.8, color='black')
    ax[0].plot(df1['F_G1_fail'], lw=5, color=cl[1])
    ax[0].set_ylabel('GHI')
    ax[0].set_ylim(0, 1490)
    ax[0].set_xlim(dt.datetime(2019, 1, 1, 0, 0, 0), dt.datetime(2019, 1, 30, 23, 59, 0))
    ax[0].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T1')
    ax[0].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_G1_fail'].count())
    
    ax[1].plot(df1['DateTime'], df1['DNI'], lw=0.8, color='black')
    ax[1].plot(df1['F_I1_fail'], lw=5, color=cl[1])
    ax[1].set_ylabel('DNI')
    ax[1].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T2')
    ax[1].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_I1_fail'].count())
    
    ax[2].plot(df1['DateTime'], df1['DHI'], lw=0.8, color='black')
    ax[2].plot(df1['F_D1_fail'], lw=5, color=cl[1])
    ax[2].set_ylabel('DHI')
    ax[2].set_xlabel('Date')
    ax[2].text(dt.datetime(2019, 1, 1, 5, 30, 0), 1350, 'T3')
    ax[2].text(dt.datetime(2019, 1, 29, 12, 0, 0), 1350, "Failed: %s" %df1['F_D1_fail'].count())
    
    fig.subplots_adjust(wspace=0, hspace=0)
    plt.savefig('PhysicalTests_DAA.png',  bbox_inches='tight', format='png', dpi=600)
    
def press_temp(df):
    
    #rcParams['figure.figsize'] = 20, 2
    #fig, ax = plt.subplots(2, 1)
    
    df['year'] = df.index.year
    
    piv = pd.pivot_table(df, index=['doy'], columns=['year'], values=['T'])    
    piv.plot()
    
    piv = pd.pivot_table(df, index=['doy'], columns=['year'], values=['P'])    
    piv.plot()
    
    #ax.plot(piv)
    #ax.legend()
