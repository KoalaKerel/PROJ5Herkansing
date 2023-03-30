# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:47:56 2022

@author: damon
"""

import pandas as pd
import streamlit as sl
import numpy as np
from PIL import Image
import pyautogui

sl.set_page_config(
    page_title="Startpagina Tool",
    page_icon="🚌",
)

sl.header("Welcome")
sl.write("Welcome to this tool for examining bus schedules. This tool can be used to find errors in a bus schedule, as well to find useful statistics about the bus schedule that may assist in further optimization. In total two different schedules can be uploaded at the same time and be compared. For further information on how to utilise this tool please watch the video below or visit the How To Use page.")
with sl.expander("Click here to see the instructional video!"):    
    sl.header("Instructional Video:")
    sl.video('https://youtu.be/dQw4w9WgXcQ') #PLACEHOLDER VIDEO!


planningdf = pd.DataFrame(columns=['buslijn']) #Om no input error te vermijden
if 'noinput' not in sl.session_state: 
    sl.session_state['noinput'] = True #Hiermee weet het om aan te geven op andere paginas als er geen input is
if 'mismatch' not in sl.session_state:
    sl.session_state['mismatch'] = False
if 'wrongdata' not in sl.session_state:
    sl.session_state['wrongdata']= False
if 'datainput' not in sl.session_state:
    sl.session_state['datainput'] = pd.read_excel('Empty Schedule.xlsx')
    sl.session_state['dienstdata2'] = pd.ExcelFile("Connexxion data - 2022-2023.xlsx")
if 'full' not in sl.session_state:
    sl.session_state['full']= False
if 'Bactief' not in sl.session_state:
    sl.session_state['Bactief'] = False
#Het uploaden van een planning
sl.header("Upload Schedules")

mismatch = False
mismatchB = False
sl.write("In the upload boxes below you can upload a bus schedule for the tool to examine. In total two schedules can be uploaded. Please ensure that the schedule matches the required format. For more information on the correct format visit the How To Use page. If there is just a single schedule to upload, please use uploadbox A.")
with sl.expander("How to upload a schedule"):
    sl.write("In order to examine a schedule, a schedule must first be uploaded. This can be done on the front page. Below the instructional video you can find the upload section. Here you will find an upload box where you can submit a file. By pressing 'Browse Files' a window will open. In this window you can navigate to the desired file to select it. After uploading a first file you have the option to upload a second file.")
    img1 = Image.open('instruct1.png')
    img2 = Image.open('instruct2.png')
    col1, col2 = sl.columns(2)
    with col1:
        sl.image(img1)
    with col2:
        sl.image(img2)
        
with sl.expander("The correct schedule format"):
    img3 = Image.open('omloopformat.png')
    sl.write("In order for the tool to do it's job correctly the provided schedule must me correctly formatted. The schedule has to be an excel file. Each row portrays an activity undertaking during the schedule. The uploaded schedule must consists of 7 columns labeled as such:")
    sl.write("Startlocatie, eindlocatie, starttijd, eindtijd, activiteit, buslijn, omloopnummer.")
    sl.image(img3)
    sl.markdown('**Startlocatie** contains the starting location of each activity, and **Eindlocatie** contains the ending location of each activity. **Starttijd** shows the time the activity starts, and **eindtijd** shows when the activity ends. The **activiteit** shows what activity the bus undertakes in that row. It can be one of 4 activities: Materiaal rit, dienst rit, idle or opladen. **Buslijn** shows which route the activity is taking place on, if any. **Omloopnummer** shows the number of the bus that relates to the activity in the row.')
    
if sl.session_state['full'] == True:
    sl.markdown("**:red[There are currently already uploaded schedules. Please reset the tool before uploading more.]**")
planning = sl.file_uploader('Upload schedule A here.', type=['xlsx'])
#Hiermee weten de andere paginas dat er een upload is, het update ook alleen de data wanneer er iets upload dus geen reset.
if planning is not None: 
    planningdf = pd.read_excel(planning)
    sl.session_state['datainput'] = planningdf
    sl.session_state['noinput'] = False
    if planningdf.columns.values.tolist() == ['startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'omloop nummer']:
        mismatch = False #De layout komt overeen
        sl.write("Schedule A has been succesfully uploaded and satisfies the format requirements.")
    else:
        mismatch = True #De layout komt niet overeen
        col1, col2 = sl.columns(2)
        with col1:
            sl.image(Image.open('little error.png'))
        with col2: 
            sl.markdown("The format of the uploaded file does not match the requirements. Please refer to the How To Use page for the correct format.")

    

 
planningB = sl.file_uploader('Upload schedule B here.(Optional)', type=['xlsx'])
#Hiermee weten de andere paginas dat er een upload is, het update ook alleen de data wanneer er iets upload dus geen reset.
if planningB is not None: 
    planningdfB = pd.read_excel(planningB)
    sl.session_state['datainputB'] = planningdfB
    sl.session_state['Bactief'] = True
    if planningdfB.columns.values.tolist() == ['startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'omloop nummer']:
        mismatchB = False #De layout komt overeen
        sl.write("Schedule B has been succesfully uploaded and satisfies the format requirements.")
    else:
        mismatchB = True #De layout komt niet overeen
        col1, col2 = sl.columns(2)
        with col1:
            sl.image(Image.open('little error.png'))
        with col2: 
            sl.markdown("The format of the uploaded file does not match the requirements. Please refer to the How To Use page for the correct format.")
        

if (planning is not None) or (planningB is not None):
    sl.session_state['full'] = True
    
if (planning is not None) and (planningB is not None):
    if np.array_equal(planningdf.buslijn.unique(), planningdfB.buslijn.unique(), equal_nan=True)==False:
        sl.markdown("**:red[The two uploaded schedules do not have matching routes. Please check the files that were uploaded. Reset the tool with the button below and try again.]**")
    
if (mismatchB == True) or (mismatch == True):
    sl.write("One of the provided bus schedules does not satisfy the format requirements. Please use the reset button below to remove the schedules and ensure the uploads are correctly formatted. For more information on the correct format please visit the How To Use page.")
    sl.session_state['mismatch'] = True
if (planning is not None) and (planningB is not None) and (mismatch == False) and (mismatchB == False):
    sl.write("Both schedules have been succesfully uploaded and satisfy the format requirements. If you wish to remove the schedules and examine new ones, please press the reset button below.")
    sl.session_state['mismatch'] = False

sl.header("Reset Button.")
sl.write("If you wish to undo your uploads and reupload a new file, you first need to press the button below.")
if sl.button('Reset tool'):
    for key in sl.session_state.keys():
        del sl.session_state[key]
    if 'noinput' not in sl.session_state: 
        sl.session_state['noinput'] = True #Hiermee weet het om aan te geven op andere paginas als er geen input is
    if 'mismatch' not in sl.session_state:
        sl.session_state['mismatch'] = False
    if 'wrongdata' not in sl.session_state:
        sl.session_state['wrongdata']= False
    if 'datainput' not in sl.session_state:
        sl.session_state['datainput'] = pd.read_excel('Empty Schedule.xlsx')
        sl.session_state['dienstdata2'] = pd.ExcelFile("Connexxion data - 2022-2023.xlsx")
    pyautogui.hotkey("ctrl","F5")
    
        
    

dienstdata = pd.read_excel("Connexxion data.xlsx", sheet_name=1)
dienstdata['activiteit'] = ''
for i in range(len(dienstdata)):
    if np.isnan(dienstdata['buslijn'][i])==False:
        dienstdata['activiteit'][i] = dienstdata['startlocatie'][i]+dienstdata['eindlocatie'][i]+str(dienstdata['buslijn'][i])[:-2]
    else:
        dienstdata['activiteit'][i] = dienstdata['startlocatie'][i]+dienstdata['eindlocatie'][i]+'m'
dienstdata = dienstdata.append({'startlocatie':'', 'eindlocatie': '', 'min reistijd in min': 0, 'max reistijd in min': 0, 'afstand in meters': 0, 'buslijn': np.nan, 'activiteit':'idle'}, ignore_index=True)
dienstdata = dienstdata.append({'startlocatie':'', 'eindlocatie': '', 'min reistijd in min': 0, 'max reistijd in min': 0, 'afstand in meters': 0, 'buslijn': np.nan, 'activiteit':'charge'}, ignore_index=True)
dienstregeling = pd.read_excel("Connexxion data.xlsx")
if 'dienstregeling' not in sl.session_state:
    sl.session_state['dienstdata'] =  dienstdata
    sl.session_state['dienstregeling'] = dienstregeling
    sl.session_state['dienstdata2'] = pd.ExcelFile("Connexxion data.xlsx")


    
#Hier kan de state of health door de gebruiker bepaald worden. Uit zichzelf staat er altijd al 90%


if 'soc' not in sl.session_state:
    sl.session_state['soc'] = 90


if 'stroomverbruik' not in sl.session_state:
    sl.session_state['stroomverbruik'] = 0.00100



if planning is not None and mismatch==False:
    #Welke verschillende lijnen zitten er in de omloopplanning
    lijnen = planningdf.buslijn.unique()
    lijnen = lijnen[~np.isnan(lijnen)]
    if 'lijnen' not in sl.session_state:
        sl.session_state['lijnen'] = lijnen
    
    #Dataframe voorbereiden voor de andere paginas
    data = sl.session_state['datainput']
    #lijnen
    lijnen = sl.session_state['lijnen']
    #Het aanmaken van typen rit
    data["type"] = np.nan
    #Alle soorten ritten in kaart brengen
    for i in range(len(data)):
        if data.activiteit[i] == "idle":
            data.type[i] = "idle"
        if data.activiteit[i] == "opladen":
            data.type[i] = "charge"
        if data.activiteit[i] == "dienst rit":
            data.type[i] = data.startlocatie[i] + data.eindlocatie[i] + str(data.buslijn[i])[:-2]
        if data.activiteit[i] == "materiaal rit":
            data.type[i] = data.startlocatie[i] + data.eindlocatie[i] + "m"
    
    for i in range(len(data)):
        data['starttijd'][i] = str(data['starttijd'][i])
        data['eindtijd'][i] = str(data['eindtijd'][i])
    
    data['start_time'] = pd.to_datetime(data.starttijd)
    data['end_time'] = pd.to_datetime(data.eindtijd)
    for i in range(len(data)):
        data['start_time'][i] = data['start_time'][i].minute + 60 * data['start_time'][i].hour
        data['end_time'][i] = data['end_time'][i].minute + 60 * data['end_time'][i].hour
    data['tte'] = data.end_time - data.start_time
    for i in range(len(data)):
        if data['tte'][i]<0:
            data['tte'][i] = data['tte'][i] + 1440
        if data['start_time'][i]<300:
            data['start_time'][i] = data['start_time'][i] + 1440
        if data['end_time'][i]<300:
            data['end_time'][i] = data['end_time'][i] + 1440
        if data['buslijn'][i] not in lijnen:
            data['buslijn'][i] = ""
            
    if sl.session_state['Bactief'] == True:
        #Dataframe voorbereiden voor de andere paginas
        dataB = sl.session_state['datainputB']
        #lijnen
        lijnenB = sl.session_state['lijnen']
        #Het aanmaken van typen rit
        dataB["type"] = np.nan
        #Alle soorten ritten in kaart brengen
        for i in range(len(dataB)):
            if dataB.activiteit[i] == "idle":
                dataB.type[i] = "idle"
            if dataB.activiteit[i] == "opladen":
                dataB.type[i] = "charge"
            if dataB.activiteit[i] == "dienst rit":
                dataB.type[i] = dataB.startlocatie[i] + dataB.eindlocatie[i] + str(dataB.buslijn[i])[:-2]
            if dataB.activiteit[i] == "materiaal rit":
                dataB.type[i] = dataB.startlocatie[i] + dataB.eindlocatie[i] + "m"
        
        for i in range(len(dataB)):
            dataB['starttijd'][i] = str(dataB['starttijd'][i])
            dataB['eindtijd'][i] = str(dataB['eindtijd'][i])
        
        dataB['start_time'] = pd.to_datetime(dataB.starttijd)
        dataB['end_time'] = pd.to_datetime(dataB.eindtijd)
        for i in range(len(dataB)):
            dataB['start_time'][i] = dataB['start_time'][i].minute + 60 * dataB['start_time'][i].hour
            dataB['end_time'][i] = dataB['end_time'][i].minute + 60 * dataB['end_time'][i].hour
        dataB['tte'] = dataB.end_time - dataB.start_time
        for i in range(len(dataB)):
            if dataB['tte'][i]<0:
                dataB['tte'][i] = dataB['tte'][i] + 1440
            if dataB['start_time'][i]<300:
                dataB['start_time'][i] = dataB['start_time'][i] + 1440
            if dataB['end_time'][i]<300:
                dataB['end_time'][i] = dataB['end_time'][i] + 1440
            if dataB['buslijn'][i] not in lijnen:
                dataB['buslijn'][i] = ""
    

if (planning is not None) and (sl.session_state['mismatch'] == False):            
    if(all(x in sl.session_state['dienstdata'].activiteit.unique() for x in sl.session_state['datainput'].type.unique() ))==False:
        sl.session_state['wrongdata'] = True
    else:
        sl.session_state['wrongdata'] = False