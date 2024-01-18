# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 11:55:15 2022

@author: Henry
"""

def getAPI_key():
    f = open("api_key.txt", "r")
    return f.read()

def elo_score(tier, division):
    return tier*10+(division-1)*2.5



