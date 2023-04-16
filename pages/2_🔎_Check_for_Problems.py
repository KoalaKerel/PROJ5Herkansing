# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:18:00 2022

@author: damon
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import numpy as np
from matplotlib.patches import Patch
import streamlit as sl
from PIL import Image

sl.set_page_config(page_title="Check for Problems", page_icon="🔎")

if sl.session_state['noinput'] == True:
    sl.markdown("No schedule has been uploaded. Please return to the frontpage and upload a schedule.")
    noinputimg = Image.open('Geeninput.png')
    sl.image(noinputimg)
    
if sl.session_state['mismatch'] == True and sl.session_state['noinput']==False:
    sl.markdown("The uploaded schedule is not formatted correctly or does not match the uploaded data. Please check if both are correct.")
    badinputimg = Image.open('Fouteinput.png')
    sl.image(badinputimg)
    
if sl.session_state['mismatch'] == False and sl.session_state['noinput']==False and sl.session_state['wrongdata']==True:
    sl.markdown("The uploaded shedule does not match the current data. Please check if both are correct.")
    sl.image(Image.open('Fouteinput.png'))
    
    
if sl.session_state['mismatch'] == False and sl.session_state['noinput'] == False and sl.session_state['wrongdata']==False:
    
    dataA = sl.session_state['datainput']
    soh = sl.session_state['soc']
    usage = sl.session_state['stroomverbruik']
    idata = sl.session_state['dienstdata']
    errors = pd.DataFrame(columns=['Error Type', 'Bus', 'Timestamp'])
    
    #Schedule A controleren
    power = []
    for bus in dataA['omloop nummer'].unique():
        current = dataA[dataA['omloop nummer']==bus]
        current.reset_index(drop=True, inplace=True)
        current = current.sort_values(by=['start_time'])
        soc = 350000 * soh/100 * 0.9
        socs = []
        for i in current.index.values.tolist():
            #Out of power
            socs.append(soc)
            if current.activiteit[i] == 'opladen':
                soc = soc + current.tte[i] * 4.1667
                if soc > 350000 * soh/100 * 0.9:
                    soc = 350000 * soh/100 * 0.9
            elif current.activiteit[i] == 'idle':
                soc = soc - (current.tte[i]*0.01)
            else:
                soc = soc - (idata.loc[idata['activiteit']==current.type[i], 'afstand in meters'].iloc[0] * usage)
            if soc <= (350000 * soh/100 * 0.1):
                newerror = ["Out of Power", current['omloop nummer'][i], current.starttijd[i]]
                errors.loc[len(errors)] = newerror
            
            #Not at location
            if (i > min(current.index.values.tolist())) and (current.startlocatie[i] != current.eindlocatie[i-1]):
                newerror = ['Not at Location', current['omloop nummer'][i], current.starttijd[i]]
                errors.loc[len(errors)] = newerror
            
            #Double Location
            if (i > min(current.index.values.tolist())) and (current.start_time[i] < current.end_time[i-1]):
                newerror = ['Double Location', current['omloop nummer'][i], current.starttijd[i]]
                errors.loc[len(errors)] = newerror
                
            #Unaccounted Idle
            if (i > min(current.index.values.tolist())) and (current.start_time[i] - current.end_time[i-1] > 1):
                newerror = ['Unaccounted Idle', current['omloop nummer'][i], current.starttijd[i]]
                errors.loc[len(errors)] = newerror
                
        power.append(socs)
        
    derrors = pd.DataFrame(columns=['Error Type', 'Location', 'Timestamp', 'Route'])
    dienst = sl.session_state['dienstregeling']
    for i in range(len(dienst)):
        dienst['vertrektijd'][i] = str(dienst['vertrektijd'][i])
    dienst['start_time'] = pd.to_datetime(dienst.vertrektijd)
    for i in range(len(dienst)):
        dienst['start_time'][i] = dienst['start_time'][i].minute + 60 * dienst['start_time'][i].hour
    for i in range(len(dienst)):
        if dienst['start_time'][i]<300:
            dienst['start_time'][i] = dienst['start_time'][i] + 1440
        
    
    for i in range(len(dienst)):
        possibles = dataA[dataA.start_time == dienst.start_time[i]]
        possibles = possibles[possibles.activiteit == 'dienst rit']
        #Demand not satisfied
        if len(possibles[possibles.startlocatie == dienst.startlocatie[i]]) < 1:
            newerror = ['Demand not satisfied', dienst.startlocatie[i], dienst.vertrektijd[i], dienst.buslijn[i]]
            derrors.loc[len(derrors)] = newerror
        #Double busses
        if len(possibles[possibles.startlocatie == dienst.startlocatie[i]]) > 1:
            newerror = ['Double Bus Planned', dienst.startlocatie[i], dienst.vertrektijd[i], dienst.buslijn[i]]
            derrors.loc[len(derrors)] = newerror

    
    #Schedule B controleren
    if sl.session_state['Bactief'] == True:
        dataB = sl.session_state['datainputB']
        errorsB = pd.DataFrame(columns=['Error Type', 'Bus', 'Timestamp'])
        powerB = []
        for bus in dataB['omloop nummer'].unique():
            current = dataB[dataB['omloop nummer']==bus]
            current.reset_index(drop=True, inplace=True)
            current = current.sort_values(by=['start_time'])
            soc = 350000 * soh/100 * 0.9
            socs = []
            for i in len(current):
                #Out of power
                socs.append(soc)
                if current.activiteit[i] == 'opladen':
                    soc = soc + current.tte[i] * 4.1667
                    if soc > 350000 * soh/100 * 0.9:
                        soc = 350000 * soh/100 * 0.9
                elif current.activiteit[i] == 'idle':
                    soc = soc - (current.tte[i]*0.01)
                else:
                    soc = soc - (idata.loc[idata['activiteit']==current.type[i], 'afstand in meters'].iloc[0] * usage)
                if soc <= (350000 * soh/100 * 0.1):
                    newerror = ["Out of Power", current['omloop nummer'][i], current.starttijd[i]]
                    errorsB.loc[len(errorsB)] = newerror
            
                #Not at location
                if (i > min(current.index.values.tolist())) and (current.startlocatie[i] != current.eindlocatie[i-1]):
                    newerror = ['Not at Location', current['omloop nummer'][i], current.starttijd[i]]
                    errorsB.loc[len(errorsB)] = newerror
                
                #Double Location
                if (i > min(current.index.values.tolist())) and (current.start_time[i] < current.end_time[i-1]):
                    newerror = ['Double Location', current['omloop nummer'][i], current.starttijd[i]]
                    errorsB.loc[len(errorsB)] = newerror
                    
                #Unaccounted Idle
                if (i > min(current.index.values.tolist())) and (current.start_time[i] - current.end_time[i-1] > 1):
                    newerror = ['Unaccounted Idle', current['omloop nummer'][i], current.starttijd[i]]
                    errorsB.loc[len(errorsB)] = newerror
                    
            power.append(socs)
            
        derrorsB = pd.DataFrame(columns=['Error Type', 'Location', 'Timestamp', 'Route'])
        
        for i in range(len(dienst)):
            possibles = dataB[dataB.start_time == dienst.start_time[i]]
            possibles = possibles[possibles.activiteit == 'dienst rit']
            #Demand not satisfied
            if len(possibles[possibles.startlocatie == dienst.startlocatie[i]]) < 1:
                newerror = ['Demand not satisfied', dienst.startlocatie[i], dienst.vertrektijd[i], dienst.buslijn[i]]
                derrorsB.loc[len(derrorsB)] = newerror
            #Double busses
            if len(possibles[possibles.startlocatie == dienst.startlocatie[i]]) > 1:
                newerror = ['Double Bus Planned', dienst.startlocatie[i], dienst.vertrektijd[i], dienst.buslijn[i]]
                derrorsB.loc[len(derrorsB)] = newerror

    sl.header("Check for errors")
    sl.write("On this page you can view errors that may occur within the planning. There are various types of errors that may be found. For each error the busnumber and timestamp of the start of the activity causing the problem will be given. Generally speaking in order for a schedule to be feasible, there must be no errors.")
    with sl.expander("Which types of errors exist?"):
        sl.write('**Out of power** occurs when the bus falls below a threshold of 10% of its maximum charge. Generally this happens because the bus is not charged enough. However it might also be cause by a high usage value or a low state of health value.')
        sl.write('**Not at Location** occurs when the bus is planned to execute an activity but is not at the right place at the right time. This error most often occurs because of the preceding activity. Please check if the ending location of the preceding activity matches the starting location of the next activity.')
        sl.write('**Double Location** occurs when the timeframe for two activities for a bus overlap. In order to do both activities the bus would have to be at two locations, which is not possible.')
        sl.write('**Double Bus** is the error that happens when two busses have the exact same activity at the same time. Only one bus is allowed to satisfy each demanded service.')
        sl.write('**Unaccounted Idle** occurs when there is an unexplained gap in the schedule. We advise that gaps in the schedule be filled up with the idle activity in order to create a better overview of the schedule.' )
        sl.write('**Demand not satisfied** occurs when the one or more of the required services is not accounted for in the provided schedule.')

    sl.header("Out of power")
    sl.write('If the bus is not charged often enough it will eventually out of power. To make sure that the no busses come to a sudden halt during its operations, charging activities can be added.')
    if len(errors[errors['Error Type'] == 'Out of power']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(errors[errors['Error Type'] == 'Out of power'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(errorsB[errorsB['Error Type'] == 'Out of power']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(errorsB[errorsB['Error Type'] == 'Out of power'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')
        
        
    sl.header('Not at Location')
    sl.write('If the bus is not at the location it is supposed to start an activity from, this type of error occurs. In order to fix this, check if the end destination of the previous activity matches the start activity of the following activity.')
    if len(errors[errors['Error Type'] == 'Not at Location']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(errors[errors['Error Type'] == 'Not at Location'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(errorsB[errorsB['Error Type'] == 'Not at Location']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(errorsB[errorsB['Error Type'] == 'Not at Location'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')
        
    sl.header('Double Location')
    sl.write('If the bus is planned to be at multiple locations at the same time, this error occurs. Check if the timespans of two activities overlap if this error occurs.')
    if len(errors[errors['Error Type'] == 'Double Location']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(errors[errors['Error Type'] == 'Double Location'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(errorsB[errorsB['Error Type'] == 'Double Location']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(errorsB[errorsB['Error Type'] == 'Double Location'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')  
    
    sl.header('Unaccounted Idle')
    sl.write('If the bus is not undertaking any activity during the schedule and the time that it is not doing anything it is not allocated to the idle activity, this error occurs. Please make sure that if a bus is waiting at a station is it noted as the idle activity.')
    if len(errors[errors['Error Type'] == 'Unaccounted Idle']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(errors[errors['Error Type'] == 'Unaccounted Idle'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(errorsB[errorsB['Error Type'] == 'Unaccounted Idle']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(errorsB[errorsB['Error Type'] == 'Unaccounted Idle'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')
            
    sl.header('Demand not Satisfied')
    sl.write('If there are no busses providing a service that is demanded for the schedule, this error will occur. Ensure that all required service rides are accounted for in the schedules. Instead of showing a bus committing this error, it will instead show the time and startinglocation of the service that is lacking in the schedule.')
    if len(derrors[derrors['Error Type'] == 'Demand not satisfied']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(derrors[derrors['Error Type'] == 'Demand not satisfied'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(derrorsB[derrorsB['Error Type'] == 'Demand not satisfied']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(derrorsB[derrorsB['Error Type'] == 'Demand not satisfied'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')
            
    sl.header('Double Bus Planned')
    sl.write("This error occurs when two busses are planned to provide the same service at the same time. Every demanded service is supposed to be satisfied by a single bus. Provided is the startinglocation and timestamp of the double planned activity")
    if len(derrors[derrors['Error Type'] == 'Double Bus Planned']) > 0:
        sl.write("Errors of this kind have been found in schedule A. Please see the table below:")
        sl.dataframe(errors[errors['Error Type'] == 'Double Bus Planned'])
    else:
        sl.write('There are no errors of this kind in schedule A. Well done!')
    if sl.session_state['Bactief'] == True:
        if len(derrorsB[derrorsB['Error Type'] == 'Double Bus Planned']) > 0:
            sl.write("Errors of this kind have been found in schedule B. Please see the table below:")
            sl.dataframe(derrorsB[derrorsB['Error Type'] == 'Double Bus Planned'])
        else:
            sl.write('There are no errors of this kind in schedule B. Well done!')
