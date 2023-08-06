from datetime import datetime, timedelta
import requests
import pandas as pd
from os.path import join,exists
from os import mkdir
from osgeo import ogr
from osgeo import osr  
import json
import numpy as np
from enum import Enum

import matplotlib.pyplot as plt

from .kiwis import *
from ..RatingCurve import gaugingstation

HECE_CREDENTIAL = 'MTIwNDYzYzgtMjk0ZC00NGE1LTlkMDUtNjg3NmJmNTU1NzUzOjJhMGUzY2EyLWY1MjktNGYxYS04YTJmLWY1N2M5OTMyZTJiZQ=='

class hydrometry_hece(hydrometry):
    
    def __init__(self, url: str = '', urltoken: str = '', credential='', dir='') -> None:
        super().__init__(URL_SPW, URL_TOKEN, HECE_CREDENTIAL, dir)
    
    def get_stations(self):
        '''Obtention des stations pour le serveur courant'''
        
        super().get_stations()
        
        self.mystations={}
        for curmaint in kiwis_maintainers:
            self.mystations[curmaint.value]={}
            for idx,curstation in self.realstations[self.realstations['site_no']==curmaint.value].iterrows():
                newstation = gaugingstation(curstation['station_name'],
                                        curstation['station_no'],
                                        '')
                newstation.x = float(curstation['station_local_x'])
                newstation.y = float(curstation['station_local_y'])
                newstation.maintainer = curmaint.value
                
                self.mystations[curmaint.value][newstation.id]=newstation
    
    def plot(self,size:float=10.):
        for curmaint in kiwis_maintainers:
            for curstation in self.mystations[curmaint.value].values():
                curstation.plot(size)                    
