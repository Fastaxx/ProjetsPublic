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

fi = '/Users/Louis/GitHub/ProjetsPublic/Fluid BikeMap/exemple-de-trace-gps.gpx'

def liregpx(fichier):
    " Lecture et Vitesse fichier gpx"
    with open(fichier, "r") as fichiergpx:
        gpx = gpx_parser.parse(fichiergpx)
        
    vitesse = []
    for track in gpx:
        for segment in track:
            point_precedent = None
            t=0
            distance_totale = 0
            for point in segment:
                if point_precedent is not None:
                    distance = distancehaversin((point_precedent.latitude, point_precedent.longitude),(point.latitude, point.longitude))
                    det = point_precedent.time_difference(point)
                    if det==0:
                        continue
                    t+=det
                    distance_totale+=distance
                    
                    vit = distance/det * 3.6
                    vitesse.append((t, distance, distance_totale, vit))
                point_precedent = point
    tab = pd.DataFrame(vitesse)
    tab.columns = ["temps", "distance_segment", "distance", "vitesse"]
    
    return tab
            
            
def floatRgb(mag, cmin, cmax):
    """ https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s11.html
    """
    try:
        x = float(mag - cmin) / (cmax - cmin)
    except ZeroDivisionError:
        x = 0.5  # cmax == cmin
    blue = min((max((4 * (0.75 - x), 0.0)), 1.0))
    red = min((max((4 * (x - 0.25), 0.0)), 1.0))
    green = min((max((4 * math.fabs(x - 0.5) - 1.0, 0.0)), 1.0))
    return red, green, blue


def rgb(mag, cmin, cmax):
    """ Return a tuple of integers, as used in AWT/Java plots. """
    red, green, blue = floatRgb(mag, cmin, cmax)
    return int(red * 255), int(green * 255), int(blue * 255)


def strRgb(mag, cmin, cmax):
    """ Return a hex string, as used in Tk plots. """
    return "#%02x%02x%02x" % rgb(mag, cmin, cmax)


            