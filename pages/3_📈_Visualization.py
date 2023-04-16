# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 19:31:15 2022

@author: damon
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import numpy as np
from matplotlib.patches import Patch
import streamlit as sl
from PIL import Image

sl.set_page_config(page_title="Visualization", page_icon="📅")

#Aangeven dat er data onbreekt
if sl.session_state['noinput'] == True:
    sl.markdown("No schedule has been uploaded. Please return to the frontpage and upload a schedule.")
    noinputimg = Image.open('Geeninput.png')
    sl.image(noinputimg)
    
if sl.session_state['mismatch'] == True and sl.session_state['noinput']==False:
    sl.markdown("The uploaded schedule is not formatted correctly or does not match the uploaded data. Please check if both are correct.")
    badinputimg = Image.open('Fouteinput.png')
    sl.image(badinputimg)
    
if sl.session_state['mismatch'] == False and sl.session_state['noinput'] == False:
    data = sl.session_state['datainput']
    if sl.session_state['Bactief'] == True:
        dataB = sl.session_state['datainputB']
    #Kleurtjes
    types = ['materiaal rit', 'dienst rit', 'opladen', 'idle']
    #Hier geeft hij een kleur aan elk type rit, tot 30 verschillende ritten.
    kleur = ['#C0392B', '#2E86C1', '#E4D00A', '#7CFC00']
    c_dict = {}
    for i in range(len(types)):
        c_dict[types[i]] = kleur[i]
    
    def color(row):
        return c_dict[row['activiteit']]
    data['color'] = data.apply(color, axis=1)
    
    #plot
    fig, ax = plt.subplots(1, figsize=(16, 6))
    ax.barh(data['omloop nummer'], data.tte, left=data.start_time, color=data.color) 
    
    
    #legenda
    #c_dict = {'materiaalrit garage bus':'#C0392B','m_ag':'#D98880', 'm_gb':'#FFC300', 'm_bg':'#F7DC6F', 'm_ab':'#D35400', 'm_ba':'#E59866', '401ba':'#2ECC71', '401ab':'#239B56', '400ab':'#85C1E9', '400ba':'#2E86C1', 'opl':'#7D3C98', 'idle':'#D2B4DE'}
    legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
    plt.legend(handles=legend_elements)
    
    #Assen:
    aantalbus = max(data['omloop nummer'])
    yticks = np.arange(1, aantalbus+1, 1)
    yticklabels = np.arange(1, aantalbus+1, 1)
    ax.set_yticks(yticks)
    ax.set_ylabel("Busses")
    
    #De x-as wordt naar uren afgerond
    xticks = np.arange(np.floor(data.start_time.min()/60)*60, np.floor(data.end_time.max()/60)*60 + 60, 60)
    val = np.floor(data.start_time.min()/60)*60
    xticklabels = []
    while val < (np.floor(data.end_time.max()/60)*60 + 60):
        xticklabels.append(str(datetime.timedelta(minutes=val)))
        val = val + 60
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=45)
    
    #plot laten zien
    sl.header("Visualisations")
    sl.write("On this page you can find various visualisations of the uploaded schedules. These are meant to gain further insight into the way the schedule is structured. These visualisations might prove useful in spotting anomalies and errors within the created schedule.")
    sl.header("Gannt Diagram")
    sl.write("Below you can find gannt diagrams of the uploaded schedules. The schedules are expressed in the 4 different types of activities a bus can undertake.")
    sl.markdown("**Gannt Diagram Schedule A**")
    sl.pyplot(fig)
    
    if sl.session_state['Bactief'] == True:
        #Kleurtjes
        typesB =['materiaal rit', 'dienst rit', 'opladen', 'idle']
        c_dict = {}
        for i in range(len(typesB)):
            c_dict[typesB[i]] = kleur[i]
        
        def color(row):
            return c_dict[row['activiteit']]
        dataB['color'] = dataB.apply(color, axis=1)
        
        #plot
        figB, axB = plt.subplots(1, figsize=(16, 6))
        axB.barh(dataB['omloop nummer'], dataB.tte, left=dataB.start_time, color=dataB.color) 
        
        
        #legenda
        #c_dict = {'materiaalrit garage bus':'#C0392B','m_ag':'#D98880', 'm_gb':'#FFC300', 'm_bg':'#F7DC6F', 'm_ab':'#D35400', 'm_ba':'#E59866', '401ba':'#2ECC71', '401ab':'#239B56', '400ab':'#85C1E9', '400ba':'#2E86C1', 'opl':'#7D3C98', 'idle':'#D2B4DE'}
        legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
        plt.legend(handles=legend_elements)
        
        #Assen:
        aantalbus = max(dataB['omloop nummer'])
        yticks = np.arange(1, aantalbus+1, 1)
        yticklabels = np.arange(1, aantalbus+1, 1)
        axB.set_yticks(yticks)
        axB.set_ylabel("Busses")
        
        #De x-as wordt naar uren afgerond
        xticks = np.arange(np.floor(dataB.start_time.min()/60)*60, np.floor(dataB.end_time.max()/60)*60 + 60, 60)
        val = np.floor(dataB.start_time.min()/60)*60
        xticklabels = []
        while val < (np.floor(dataB.end_time.max()/60)*60 + 60):
            xticklabels.append(str(datetime.timedelta(minutes=val)))
            val = val + 60
        
        axB.set_xticks(xticks)
        axB.set_xticklabels(xticklabels, rotation=45)
        
        sl.markdown("**Gannt Diagram Schedule B**")
        sl.pyplot(figB)
    
    soh = sl.session_state['soc']
    usage = sl.session_state['stroomverbruik']
    idata = sl.session_state['dienstdata']
        
    power = []
    alltimes =[]
    for bus in data['omloop nummer'].unique():
        current = data[data['omloop nummer']==bus].sort_values(by=['start_time'])
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
                    sl.write(current.tte[i])
            else:
                soc = soc - (idata.loc[idata['activiteit']==current.type[i], 'afstand in meters'].iloc[0] * usage)
        times = current.start_time
        alltimes.append(times)
        power.append(socs)
    
    sl.header("Power visualisation")
    sl.write("Here you can find visualisations of the amount of power the bus has over time. You can select which bus' graph you want to view in the select box below. If two schedules are uploaded each schedule will have a seperate selectionbox.")
    bussen = range(len(data['omloop nummer'].unique())+1)[1:]
    sl.markdown('**Schedule A**')
    selected = sl.multiselect('select for schedule A:',bussen)
    for i in selected:
        powerfig, powerax = plt.subplots(1, figsize=(16, 6))
        powerax.plot(alltimes[i-1], power[i-1])
        #legenda
        plt.legend(['Power in bus battery'])
        
        #Assen:
        powerax.set_ylabel("Power (kWh)")
        
        #De x-as wordt naar uren afgerond
        xticks = np.arange(np.floor(data.start_time.min()/60)*60, np.floor(data.end_time.max()/60)*60 + 60, 60)
        val = np.floor(data.start_time.min()/60)*60
        xticklabels = []
        while val < (np.floor(data.end_time.max()/60)*60 + 60):
            xticklabels.append(str(datetime.timedelta(minutes=val)))
            val = val + 60
            
        powerax.set_title("Power Visualisation of bus "+str(i)+" A")
        powerax.set_xticks(xticks)
        powerax.set_xticklabels(xticklabels, rotation=45)
        sl.pyplot(powerfig) 
        
    if sl.session_state['Bactief'] == True:
        powerB = []
        alltimesB =[]
        for bus in dataB['omloop nummer'].unique():
            current = dataB[dataB['omloop nummer']==bus].sort_values(by=['start_time'])
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
            times = current.start_time
            alltimesB.append(times)
            powerB.append(socs)
        
        bussenB = range(len(dataB['omloop nummer'].unique())+1)[1:]
        sl.markdown('**Schedule B**')
        selectedB = sl.multiselect('select for schedule B:',bussenB-1)
        for i in selectedB:
            powerfigB, poweraxB = plt.subplots(1, figsize=(16, 6))
            poweraxB.plot(alltimesB[i-1], powerB[i-1])
            
            #legenda
            plt.legend(['Power in bus battery'])
            
            #Assen:
            poweraxB.set_ylabel("Power (kWh)")
            
            #De x-as wordt naar uren afgerond
            xticks = np.arange(np.floor(dataB.start_time.min()/60)*60, np.floor(dataB.end_time.max()/60)*60 + 60, 60)
            val = np.floor(dataB.start_time.min()/60)*60
            xticklabels = []
            while val < (np.floor(dataB.end_time.max()/60)*60 + 60):
                xticklabels.append(str(datetime.timedelta(minutes=val)))
                val = val + 60
                
            poweraxB.set_title("Power Visualisation of bus "+str(i)+" B")
            poweraxB.set_xticks(xticks)
            poweraxB.set_xticklabels(xticklabels, rotation=45)
            
            sl.pyplot(powerfigB) 
            