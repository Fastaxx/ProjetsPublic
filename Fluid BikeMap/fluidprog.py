#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 15:09:28 2022

@author: Louis
"""
import math
import streamlit
import keplergl
import pandas as pd
import gpxpy 
import gpxpy.gpx 

R = 6371000
def distancehaversin(c1, c2):
    "c1= (lat1, long1)"
    lat1, lon1 = c1
    lat2, lon2 = c2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dephi = math.radians(phi2 - phi1)
    delambda = math.radians(lon2 - lon1)
    
    el = (math.sin(dephi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delambda/2)**2
          )
    return 2*R*math.asin(math.sqrt(el))
