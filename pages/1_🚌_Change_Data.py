# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:35:22 2022

@author: damon
"""
import streamlit as sl
import numpy as np
import pandas as pd
from PIL import Image

if sl.session_state['noinput'] == True:
    sl.markdown("No schedule has been uploaded. Please return to the frontpage and upload a schedule.")
    noinputimg = Image.open('Geeninput.png')
    sl.image(noinputimg)
    
if sl.session_state['mismatch'] == True and sl.session_state['noinput']==False:
    sl.markdown("The uploaded schedule is not formatted correctly or does not match the uploaded data. Please check if both are correct.")
    badinputimg = Image.open('Fouteinput.png')
    sl.image(badinputimg)
    
if sl.session_state['mismatch'] == False and sl.session_state['noinput'] == False:
    sl.header("Change Data")
    sl.markdown("On this page you can change the data for routes and the values for both State of Health and Power Usage. By default the tool will be configured for the 400 and 401 busroutes in Eindhoven. The state of health and power usage values have also been given a default value.")
    
    halt1 = False
    halt2 = False
    sl.header("Change Routes")
    sl.write("This tool is capable of analysing schedules created for routes other than the 400 and 401 routes in Eindhoven. In order for the tool to be able to check these schedules additional information must be provided in the form of an excel file. This file must match the format requirements. To learn more about the format requirements please visit the How to Use page. In the uploadbox below you can upload the additional data.")
    with sl.expander("How to change routes"):
        sl.write("If the uploaded schedule concerns itself with different routes, data regarding the new routes must be provided. This can be done on the Change Route page. On the Change Route page you will find an uploadbox where you can upload new data. By default the tool will use data for the 400 and 401 routes. The provided data must be formatted correctly in order for the tool to utilise it.")
        sl.write("The first tab of the data file is called Dienstregeling. It contains the following columns: Startlocatie, vertrektijd, eindlocatie and buslijn.")
        sl.write("The second tab of the data file is called Afstand Matrix. It contains the following columns: startlocatie, eindlocatie, min reistijd in min, max reistijd in min, afstand in meters and buslijn.")
        img1 = Image.open('datainput1.png')
        img2 = Image.open('datainput2.png')
        col1, col2 = sl.columns(2)
        with col1:
            sl.image(img1)
        with col2:
            sl.image(img2)
    new_upload = sl.file_uploader('', type=['xlsx'])
    
    if new_upload is None:
        usedata = sl.session_state['dienstdata']
        usedienst = sl.session_state['dienstregeling']
    if new_upload is not None:
        if (len(pd.ExcelFile(new_upload).sheet_names)<2) or (len(pd.ExcelFile(new_upload).sheet_names)>2):
            sl.header("The worksheets in the uploaded file are incorrect. Please refer to the instruction video.")
            sl.image(Image.open('Fouteinput.png'))
            halt1 = True
        else:
            usedata = pd.read_excel(new_upload, sheet_name=1)
            if (usedata.columns.values.tolist() == ['startlocatie', 'eindlocatie', 'min reistijd in min', 'max reistijd in min', 'afstand in meters', 'buslijn'])==False:
                sl.header("The uploaded format is incorrect on the Afstand matrix page. Please refer to the instruction video for the correct format.")
                sl.image(Image.open('Fouteinput.png'))
                halt1 = True
            else:
                halt1 = False
                sl.session_state['dienstdata2'] = pd.ExcelFile(new_upload)
            
            dienstlijnen = usedata.buslijn.unique()
            dienstlijnen = dienstlijnen[~np.isnan(dienstlijnen)]
            dienstlijnen = dienstlijnen.astype(int)
            
            
            usedata["activiteit"] = ""
            for i in range(len(usedata)):
                if np.isnan(usedata['buslijn'][i]) == False:
                    usedata.activiteit[i] = usedata.startlocatie[i] + usedata.eindlocatie[i] + str(int(usedata.buslijn[i]))
                if np.isnan(usedata['buslijn'][i]) == True:
                    usedata.activiteit[i] = usedata['startlocatie'][i]+usedata['eindlocatie'][i]+'m'
            usedata = usedata.append({'startlocatie':'', 'eindlocatie': '', 'min reistijd in min': 0, 'max reistijd in min': 0, 'afstand in meters': 0, 'buslijn': np.nan, 'activiteit':'idle'}, ignore_index=True)
            usedata = usedata.append({'startlocatie':'', 'eindlocatie': '', 'min reistijd in min': 0, 'max reistijd in min': 0, 'afstand in meters': 0, 'buslijn': np.nan, 'activiteit':'charge'}, ignore_index=True)
            usedienst = pd.read_excel(new_upload)
            if (usedienst.columns.values.tolist()[:4] == ['startlocatie', 'vertrektijd', 'eindlocatie', 'buslijn'])==False:
                sl.markdown(usedienst.columns.values.tolist()[:4])
                sl.header("The uploaded format is incorrect on the Dienstregeling page. Please refer to the instruction video for the correct format.")
                sl.image(Image.open('Fouteinput.png'))
                halt2 = True
            else:
                halt2 = False
            sl.session_state['dienstdata'] = usedata
            sl.session_state['dienstregeling'] = usedienst
    if halt1 == False and halt2 == False:
        activeroutes = usedata.buslijn.unique()
        activeroutes = activeroutes[~np.isnan(activeroutes)]
        
        if(all(x in sl.session_state['dienstdata'].activiteit.unique() for x in sl.session_state['datainput'].type.unique() ))==False:
            sl.session_state['wrongdata'] = True
            sl.image(Image.open('little error.png'))
            sl.markdown("Currently the data is not compatible with the shedule. The following routes are currently active:")
        else:
            sl.markdown("**The following routes are currently active:**")
            sl.session_state['wrongdata'] = False
        activeroutesstr = ""
        for i in activeroutes:
            activeroutesstr = activeroutesstr + str(i)[:3] + "             "
        sl.markdown(activeroutesstr)
        
            
    sl.header("Adjust State of Health Value")
    sl.write("The State of Health or SoH indicates the percentage of the original battery storage the battery can still use. Over time the power storage degrades and can no longer be filled to it's original capacity. Here you may select the state of health to accurately reflect the batteries.")
    soh = sl.slider("", 75, 100, sl.session_state['soc'])
    if sl.session_state['soc'] != soh:
        sl.session_state['soc'] = soh
    sl.write(f"**The current state of health is {soh}%**")

    sl.header("Adjust the Power Usage")
    sl.write("The busses use electricity to propel themselves forward. However the power usage of the busses is not always the same. Here you can adjust the power usage of the busses according to the situation.")
    usage = sl.slider("", 0.1, 3.0, float(sl.session_state['stroomverbruik']*1000), step=0.1)
    if sl.session_state['stroomverbruik'] != usage/1000:
        sl.session_state['stroomverbruik'] = usage/1000
    sl.write(f"**The current usage is {usage} joules per kilometer**")
