# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 20:10:26 2023

@author: damon
"""

import streamlit as sl
import pandas as pd
from PIL import Image

sl.header("How to use the tool.")
sl.write("On this page you can find further information of how to use the tool. The instructional video is intended to provide a clear overview of the tool, but further details can be found here. The information is organized into different categories.")


sl.subheader("Uploading")
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
    sl.write("In order for the tool to do it's job correctly the provided schedule must me correctly formatted. (VRAAG OVER NEDERLANDS/ENGELSE EXCEL BEANTWOORD HEBBEN VOORDAT WE DIT AFMAKEN")
    
sl.subheader("Changing Data")
with sl.expander("How to change routes"):
    sl.write("If the uploaded schedule concerns itself with different routes, data regarding the new routes must be provided. This can be done on the Change Route page. On the Change Route page you will find an uploadbox where you can upload new data. By default the tool will use data for the 400 and 401 routes. The provided data must be formatted correctly in order for the tool to utilise it.")
    sl.write("Hier komen nog afbeeldingen en info over format.")