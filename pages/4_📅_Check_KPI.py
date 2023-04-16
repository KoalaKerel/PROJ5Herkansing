# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 19:31:54 2022

@author: damon
"""

import pandas as pd
import numpy as np 
import streamlit as sl
import matplotlib.pyplot as plt
import datetime 
from PIL import Image

sl.set_page_config(page_title="Information", page_icon="📈")
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

    sl.header("Check KPI")
    sl.write("On this page the KPIs can be checked and compared. KPI stands for Key Performance Indicator. There are statistics that give insight into how well the schedule preforms. Below you will find a table that expresses these statistics aswell as a visualisation of the amount of power used by the busses during the day.")
    with sl.expander("What KPIs are used?"):
        sl.write("This tool uses 8 different statistics to express the quality of the schedule. Here each statistic will be explained and indicated wether or not it is should be decreased or increased for more success.")
        sl.write("**DD** is a KPI provided by Conexxion. It is defined as the total time divided by the time proividing a servce. It is generally advised to keep this number as low as possible.")
        sl.write("**Distance** reports the distance traveled during the timespan indicated by the schedule. Each activity has a set distance associated with it. Because higher distance traveled causes higher energy costs, it is recommended that distance is minimized.")
        sl.write("**Activity time** and **Passenger time** are values used in the calculation of the DD score. These can be used to explain the DD score. Generally a high amount of time with passengers is recommended. The difference between activity time and time with passengers is the time that could be further optimized.")
        sl.write("**Time spent idling** is the time in which the bus undertakes the idle activity. This means it is stationary and does not transport any passengers and uses a low amount of power.")
        sl.write("**Time spent charging** is the time in which the bus is recharging its battery. This amount should be minimized if possible so the time can be used more effectively. However, if it is lowered too much the bus will run out of power during its activities. To check if the bus can complete its tasks without coming to an unexpected standstill please check the Check for Errors page")
        sl.write("**Amount of busses** indicates how many buses the schedule in question uses. To satisfy the requirements it is certain mutliple busses will be needed. However, generally a lower amount of busses is prefered. When the amount of busses is low it will ease the creation of schedules for other bus routes.")
        sl.write("**Activity score** is a score based on a ranking of activities. Not all activities are equally useful. In order to judge if schedules use effective methods, a point based system has been developed. Passenger trips and charging are considered the best activities and are awarded 2 points. Idling is considered the best alternative because of it's low power usage and is awarded 1 point. Material trips are considered unoptimal and are not awarded any point. A higher score indicates a more effective planning.")

    
    #basedata = {'activiteit':['ehvaptehvbst400', 'ehvbstehvapt400', 'ehvaptehvbst401', 'ehvbstehvapt401', 'ehvbstehvaptm', 'ehvaptehvbstm', 'ehvbstehvgarm', 'ehvgarehvbstm', 'ehvaptehvgarm', 'ehvgarehvaptm', 'charge', 'idle'],
    #            'mint':[22, 22, 22, 22, 20, 20, 4, 4, 20, 20, 0, 0],
    #            'maxt':[24, 24, 25, 24, 20, 20, 4, 4, 20, 20, 0, 0],
    #            'afstand':[10250, 10708, 9050, 9003, 8600, 8600, 1650, 1650, 9000, 9000, 0, 0]
    #            }
    #idata = pd.DataFrame(data=basedata)
    idata = sl.session_state['dienstdata']
    data = sl.session_state['datainput']
    if sl.session_state['Bactief'] == True:
        dataB = sl.session_state['datainputB']
   
    totdist = 0
    totscore = 0
    for ind in range(len(data)):
        totdist = totdist + idata.loc[idata['activiteit']==data.type[ind], 'afstand in meters'].iloc[0]
        if (data.activiteit[ind] == 'dienst rit') or (data.activiteit[ind] == 'opladen'):
            totscore = totscore + 2
        if data.activiteit[ind] == 'idle':
            totscore = totscore + 1
    toturen = sum(data.tte)
    totdienst = sum(data.tte[data.activiteit=="dienst rit"])
    totdd = toturen/totdienst#alle uren gedeeld door diensturen    
    totusage = totdist * 1.5
    totidle = sum(data.tte[data.activiteit=="idle"]) #Totale idletijd
    totcharge = sum(data.tte[data.type=="charge"])
    
    if sl.session_state['Bactief'] == True:
        totdistB = 0
        totscoreB = 0
        for ind in range(len(dataB)):
            totdistB = totdistB + idata.loc[idata['activiteit']==dataB.type[ind], 'afstand in meters'].iloc[0]
            if (dataB.activiteit[ind] == 'dienst rit') or (dataB.activiteit[ind] == 'opladen'):
                totscoreB = totscoreB + 2
            if dataB.activiteit[ind] == 'idle':
                totscoreB = totscoreB + 1
        toturenB = sum(dataB.tte)
        totdienstB = sum(dataB.tte[dataB.activiteit=="dienst rit"])
        totddB = toturenB/totdienstB#alle uren gedeeld door diensturen    
        totusageB = totdistB * 1.5
        totidleB = sum(dataB.tte[dataB.activiteit=="idle"]) #Totale idletijd
        totchargeB = sum(dataB.tte[dataB.type=="charge"])
        inp = {'Statistic': ['DD', 'Total distance (m)', 'Total time of activity', 'Total time with passengers', 'Total time spent idling', 'Total time spent charging', 'Amount of busses in schedule', 'Activity Score'],'Planning A':[totdd, int(totdist), datetime.timedelta(minutes=toturen), datetime.timedelta(minutes=totdienst), datetime.timedelta(minutes=totidle), datetime.timedelta(minutes=totcharge), max(data['omloop nummer']), totscore], 'Planning B':[totddB, int(totdistB), datetime.timedelta(minutes=toturenB), datetime.timedelta(minutes=totdienstB), datetime.timedelta(minutes=totidleB), datetime.timedelta(minutes=totchargeB), max(dataB['omloop nummer']), totscoreB], 'Difference (A-B)':[totdd - totddB, int(totdist - totdistB), abs(datetime.timedelta(minutes = toturen) - datetime.timedelta(minutes=toturenB)),abs(datetime.timedelta(minutes=totdienst) - datetime.timedelta(minutes=totdienstB)), abs(datetime.timedelta(minutes= totidle) -datetime.timedelta(minutes=totidleB)), abs(datetime.timedelta(minutes=totcharge) - datetime.timedelta(minutes=totchargeB)), max(data['omloop nummer']) - max(dataB['omloop nummer']), totscore- totscoreB]}
    else:
        inp = {'Statistic': ['DD', 'Total distance (m)', 'Total time of activity', 'Total time with passengers', 'Total time spent idling', 'Total time spent charging', 'Amount of busses in schedule', 'Activity Score'], 'Planning A':[totdd, int(totdist), datetime.timedelta(minutes=toturen), datetime.timedelta(minutes=totdienst), datetime.timedelta(minutes=totidle), datetime.timedelta(minutes=totcharge), max(data['omloop nummer']), totscore]}
    totdf = pd.DataFrame(data=inp)  
    sl.header("Totals of all busses:")
    sl.write("Here you can find information on the sum of various values expressed through the schedule.")
    sl.dataframe(totdf)  
        
    bussen = max(data['omloop nummer'])
    businfo = []
    timespan = max(data['end_time']) - min(data['start_time'])
    
    dists = []
    uren = []
    diensts = []
    idles = []
    charges =[]
    percs = []
    dds = []
    scores = []
    
    for i in range(bussen+1)[1:]:
        tempdata = data[data['omloop nummer']==i]
        
        tempdist = 0
        tempscore = 0
        for ind in list(tempdata.index.values):
            tempdist = tempdist + idata.loc[idata['activiteit']==tempdata.type[ind], 'afstand in meters'].iloc[0]
            if (data.activiteit[ind] == 'dienst rit') or (data.activiteit[ind] == 'opladen'):
                tempscore = tempscore + 2
            if data.activiteit[ind] == 'idle':
                tempscore = tempscore + 1
        dists.append(tempdist)
        scores.append(tempscore)
        
        tempuren = sum(tempdata.tte)
        uren.append(tempuren)
        
        tempdienst = sum(tempdata.tte[tempdata.activiteit=="dienst rit"])
        diensts.append(tempdienst)
        
        if tempdienst > 0:
            tempdd = tempuren/tempdienst #alle uren gedeeld door diensturen    
        else:
            tempdd = 0
        dds.append(tempdd)
        
        tempusage = tempdist * 1.5
        
        tempidle = sum(tempdata.tte[tempdata.activiteit=="idle"]) #Totale idletijd
        idles.append(tempidle)
        
        tempcharge = sum(tempdata.tte[tempdata.type=="charge"])
        charges.append(tempcharge)
        
        tempperc = 100 * tempuren / timespan
        percs.append(tempperc)
        tempinp = {'Statistic': ['DD', 'Total distance (m)', 'Percentage of time active', 'Amount of time active', 'Time with passengers', 'Time spent idling', 'Time spent charging', 'Activity Score'], 'Value':[ tempdd, tempdist, tempperc, datetime.timedelta(minutes=tempuren), datetime.timedelta(minutes=tempdienst), datetime.timedelta(minutes=tempidle), datetime.timedelta(minutes=tempcharge), tempscore]}
        tempdf = pd.DataFrame(data=tempinp)    
        businfo.append(tempdf)
        
    #Zelfde traject voor schedule B
    if sl.session_state['Bactief'] == True:
        bussenB = max(dataB['omloop nummer'])
        businfoB = []
        timespan = max(dataB['end_time']) - min(dataB['start_time'])
        distsB = []
        urenB = []
        dienstsB = []
        idlesB = []
        chargesB =[]
        percsB = []
        ddsB = []
        scoresB = []
        
        for i in range(bussenB+1)[1:]:
            tempdata = dataB[dataB['omloop nummer']==i]
            
            tempdist = 0
            tempscore = 0
            for ind in list(tempdata.index.values):
                tempdist = tempdist + idata.loc[idata['activiteit']==tempdata.type[ind], 'afstand in meters'].iloc[0]
                if (dataB.activiteit[ind] == 'dienst rit') or (dataB.activiteit[ind] == 'opladen'):
                    tempscore = tempscore + 2
                if dataB.activiteit[ind] == 'idle':
                    tempscore = tempscore + 1
            distsB.append(tempdist)
            scoresB.append(tempscore)
            
            tempuren = sum(tempdata.tte)
            urenB.append(tempuren)
            
            tempdienst = sum(tempdata.tte[tempdata.activiteit=="dienst rit"])
            dienstsB.append(tempdienst)
            
            if tempdienst > 0:
                tempdd = tempuren/tempdienst #alle uren gedeeld door diensturen    
            else:
                tempdd = 0
            ddsB.append(tempdd)
            
            tempusage = tempdist * 1.5
            
            tempidle = sum(tempdata.tte[tempdata.activiteit=="idle"]) #Totale idletijd
            idlesB.append(tempidle)
            
            tempcharge = sum(tempdata.tte[tempdata.type=="charge"])
            chargesB.append(tempcharge)
            
            tempperc = 100 * tempuren / timespan
            percsB.append(tempperc)
            tempinp = {'Statistic': ['DD', 'Total distance (m)', 'Percentage of time active', 'Amount of time active', 'Time with passengers', 'Time spent idling', 'Time spent charging', 'Activity Score'], 'Value':[ tempdd, tempdist, tempperc, datetime.timedelta(minutes=tempuren), datetime.timedelta(minutes=tempdienst), datetime.timedelta(minutes=tempidle), datetime.timedelta(minutes=tempcharge), tempscore]}
            tempdf = pd.DataFrame(data=tempinp)    
            businfoB.append(tempdf)
        
        
     
    sl.header("Average Statistics of all busses:")   
    sl.write("Here you may find the statistics of the average bus in each schedule. The types of statistics are the same as the totals table shown above.")
    if sl.session_state['Bactief'] == True:
        avginp = {'Statistic': ['Average DD', 'Average distance (m)', 'Average percentage of time active', 'Average amount of time active', 'Average time with passengers', 'Average time spent idling', 'Average time spent charging', 'Average activity score'], 'Schedule A':[ sum(dds)/len(dds), sum(dists)/len(dists), sum(percs)/len(percs), datetime.timedelta(minutes=sum(uren)/len(uren)), datetime.timedelta(minutes=sum(diensts)/len(diensts)), datetime.timedelta(minutes=sum(idles)/len(idles)), datetime.timedelta(minutes=sum(charges)/len(charges)), sum(scores)/len(scores)], 'Schedule B':[ sum(ddsB)/len(ddsB), sum(distsB)/len(distsB), sum(percsB)/len(percsB), datetime.timedelta(minutes=sum(urenB)/len(urenB)), datetime.timedelta(minutes=sum(dienstsB)/len(dienstsB)), datetime.timedelta(minutes=sum(idlesB)/len(idlesB)), datetime.timedelta(minutes=sum(chargesB)/len(chargesB)), sum(scoresB)/len(scoresB)], 'Difference (A - B)': [sum(dds)/len(dds) - sum(ddsB)/len(ddsB), sum(dists)/len(dists) - sum(distsB)/len(distsB), sum(percs)/len(percs) - sum(percsB)/len(percsB), abs(datetime.timedelta(minutes=sum(uren)/len(uren))- datetime.timedelta(minutes=sum(urenB)/len(urenB))), abs(datetime.timedelta(minutes=sum(diensts)/len(diensts)) - datetime.timedelta(minutes=sum(dienstsB)/len(dienstsB))), abs(datetime.timedelta(minutes=sum(idles)/len(idles)) - datetime.timedelta(minutes=sum(idlesB)/len(idlesB)) ), abs(datetime.timedelta(minutes=sum(charges)/len(charges)) - datetime.timedelta(minutes=sum(chargesB)/len(chargesB))), sum(scores)/len(scores) - sum(scoresB)/len(scoresB)] } 
    else:
        avginp = {'Statistic': ['Average DD', 'Average distance (m)', 'Average percentage of time active', 'Average amount of time active', 'Average time with passengers', 'Average time spent idling', 'Average time spent charging', 'Average activity score'], 'Schedule A':[ sum(dds)/len(dds), sum(dists)/len(dists), sum(percs)/len(percs), datetime.timedelta(minutes=sum(uren)/len(uren)), datetime.timedelta(minutes=sum(diensts)/len(diensts)), datetime.timedelta(minutes=sum(idles)/len(idles)), datetime.timedelta(minutes=sum(charges)/len(charges)), sum(scores)/len(scores)]} 
    avgdf = pd.DataFrame(data=avginp)  
    sl.dataframe(avgdf) 
        
    #Plaatsen als colommen
    sl.header("Statistics of individual busses:")
    sl.write("In some anomalous cases it might be prudent to check the statistics of individuals bussen in order to find which bus causes the anomaly. Below you will find the statistics of each individual bus.")
    
    a = 1
    if sl.button("Click here to see the individual statistics for the busses in schedule A!"):
        for i in range(int((len(businfo)))):
            col1, col2 = sl.columns(2)
            head1 = "Bus " + str(a)+ " A"
            a = a+1
            with sl.expander(head1):
                sl.dataframe(businfo[i])
                
                
    if sl.session_state['Bactief'] == True:
        bussen = max(dataB['omloop nummer'])
        businfoB = []
        timespan = max(dataB['end_time']) - min(dataB['start_time'])
        
        dists = []
        uren = []
        diensts = []
        idles = []
        charges =[]
        percs = []
        dds = []
        scores = []
        
        for i in range(bussen+1)[1:]:
            tempdata = dataB[dataB['omloop nummer']==i]
            
            tempdist = 0
            tempscore = 0
            for ind in list(tempdata.index.values):
                tempdist = tempdist + idata.loc[idata['activiteit']==tempdata.type[ind], 'afstand in meters'].iloc[0]
                if (dataB.activiteit[ind] == 'dienst rit') or (dataB.activiteit[ind] == 'opladen'):
                    tempscore = tempscore + 2
                if dataB.activiteit[ind] == 'idle':
                    tempscore = tempscore + 1
            dists.append(tempdist)
            scores.append(tempscore)
            
            tempuren = sum(tempdata.tte)
            uren.append(tempuren)
            
            tempdienst = sum(tempdata.tte[tempdata.activiteit=="dienst rit"])
            diensts.append(tempdienst)
            
            if tempdienst > 0:
                tempdd = tempuren/tempdienst #alle uren gedeeld door diensturen    
            else:
                tempdd = 0
            dds.append(tempdd)
            
            tempusage = tempdist * 1.5
            
            tempidle = sum(tempdata.tte[tempdata.activiteit=="idle"]) #Totale idletijd
            idles.append(tempidle)
            
            tempcharge = sum(tempdata.tte[tempdata.type=="charge"])
            charges.append(tempcharge)
            
            tempperc = 100 * tempuren / timespan
            percs.append(tempperc)
            tempinp = {'Statistic': ['DD', 'Total distance (m)', 'Percentage of time active', 'Amount of time active', 'Time with passengers', 'Time spent idling', 'Time spent charging', 'Activity Score'], 'Value':[ tempdd, tempdist, tempperc, datetime.timedelta(minutes=tempuren), datetime.timedelta(minutes=tempdienst), datetime.timedelta(minutes=tempidle), datetime.timedelta(minutes=tempcharge), tempscore]}
            tempdf = pd.DataFrame(data=tempinp)    
            businfoB.append(tempdf)
                
        if sl.button("Click here to see the individual statistics for the busses in schedule B!"):
            for i in range(int((len(businfoB)))):
                col1, col2 = sl.columns(2)
                head1 = "Bus " + str(a)+" B"
                a = a+1
                with sl.expander(head1):
                    sl.dataframe(businfoB[i])

