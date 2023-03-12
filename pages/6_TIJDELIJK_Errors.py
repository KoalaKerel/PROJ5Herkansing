# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 12:08:40 2023

@author: damon
"""

import pandas as pd
import numpy as np 
import streamlit as sl

sl.header("Check for errors")
sl.write("On this page you can view errors that may occur within the planning. There are various types of errors that may be found. For each error the busnumber and timestamp of the start of the activity causing the problem will be given. Generally speaking in order for a schedule to be feasible, there must be no errors.")
with sl.expander("Which types of errors exist?"):
    sl.write("hier moet nog uitleg komen")
    sl.write('Out of power')
    sl.write('Not at Location')
    sl.write('Double Location')
    sl.write('Double Bus')
    sl.write('Unaccounted Idle')
    sl.write('Demand not satisfied')
    
#Hier moet een dataframe uit Danny's script komen
inp = {'Errortype':['Out of power', 'Out of power', 'Out of power', 'Double Location'], 'Bus':['1', '1', '2', '2'], 'Timestamp':['07:51:00', '08:05:55', '23:03:03', '09:45:45']}
df = pd.DataFrame(data=inp)
sl.dataframe(df)  

sl.header("Out of power")
sl.write('If the bus is not charged often enough it will eventually out of power. To make sure that the no busses come to a sudden halt during its operations, charging activities can be added.')
if len(df[df.Errortype == 'Out of power']) > 0:
    sl.write("Errors of this kind have been found. Please see the table below:")
    sl.dataframe(df[df.Errortype == 'Out of power'])
else:
    sl.write('There are no errors of this kind. Well done!')
    
sl.header('Not at Location')
sl.write('If the bus is not at the location it is supposed to start an activity from, this type of error occurs. In order to fix this, check if the end destination of the previous activity matches the start activity of the following activity.')
if len(df[df.Errortype == 'Not at location']) > 0:
    sl.write("Errors of this kind have been found. Please see the table below:")
    sl.dataframe(df[df.Errortype == 'Not at location'])
else:
    sl.write('There are no errors of this kind. Well done!')
    
sl.header('Double Location')
sl.write('If the bus is planned to be at multiple locations at the same time, this error occurs. Check if the timespans of two activities overlap if this error occurs.')
if len(df[df.Errortype == 'Double Location']) > 0:
    sl.write("Errors of this kind have been found. Please see the table below:")
    sl.dataframe(df[df.Errortype == 'Double Location'])
else:
    sl.write('There are no errors of this kind. Well done!')    
