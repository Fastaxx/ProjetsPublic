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
import gpx_parser
import gpxpy 
import gpxpy.gpx 
import matplotlib as plt
import numpy as np

R = 6371000
def haversine(c1, c2):
    "c1= (lat1, long1)"
    lat1, lon1 = c1
    lat2, lon2 = c2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dephi = math.radians(phi2 - phi1)
    delambda = math.radians(lon2 - lon1)
    
    el = (math.sin(dephi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delambda/2)**2
          )
    return 2*R*math.asin(math.sqrt(el))

fi = '/Users/Louis/GitHub/ProjetsPublic/Fluid BikeMap/exemple-de-trace-gps.gpx'


from collections import namedtuple

GpxPoint = namedtuple(
    "GpxPoint", ["time", "distance", "tot_dist", "speed", "coordinates"]
)


def liregpx(file_name):
    with open(file_name, "r") as gpx_file:
        gpx = gpx_parser.parse(gpx_file)

    tab = []

    for track in gpx:
        for segment in track:
            previous_point = None
            t = 0
            total_distance = 0
            for point in segment:
                if previous_point is not None:
                    distance = haversine(
                        (previous_point.latitude, previous_point.longitude),
                        (point.latitude, point.longitude),
                    )
                    delta_time = previous_point.time_difference(point)
                    if delta_time == 0:
                        continue
                    t += delta_time
                    total_distance += distance

                    speed = distance / delta_time * 3600 / 1000
                    tab.append(
                        GpxPoint(
                            t,
                            distance,
                            total_distance,
                            speed,
                            (point.latitude, point.longitude),
                        )
                    )
                previous_point = point

    return tab

fi2= liregpx(fi)
vitesse_min= 5

def score(points):
    a= len([i for i in points if i[3]<vitesse_min])
    return a/len(points)*100

def creersegment(points):
    seg_av=0
    segments_pts =[]
    segments = []
    for point in points:
        total_distance = point[2]
        seg = total_distance/100
        if seg> seg_av:
            segments.append((seg, score(points), segments_pts))
            segments_pts=[point]
            seg_av=seg
        else:
            segments_pts.append(point)
            
    return segments
    
    
    

