"""
WxPython  Graphical User Interface for walloon hydrometry website : https://hydrometrie.wallonie.be/

@authors : Loïc Archambeau, Pierre Archambeau
@affiliation : ULiège - HECE
"""
import wx
import wx.adv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt, timedelta

#Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
import os
import gettext
if os.path.exists(os.path.dirname(__file__)+'\\..\\locales'):
    t = gettext.translation('base', localedir=os.path.dirname(__file__)+'\\..\\locales', languages=['fr'])
    t.install()
else:
    try:
        t = gettext.translation('base', localedir='wolfhece\\locales', languages=['fr'])
        t.install()
    except:
        pass

_=gettext.gettext

from .kiwis import hydrometry, kiwis_keywords_horq, kiwis_keywords_rain

class hydrometry_gui(wx.Frame): 
    """
    wxFrame for data selection 
    
    General configuration :
      - sites
      - stations
      - timeseries par station
      --> plot
    """

    def __init__(self, credential='', *args, **kw):
        
        super().__init__(None,-1,_('Data collector'), size=(1024,600))    
        self.panel = wx.Panel(self)

        colonne = wx.BoxSizer(wx.VERTICAL)

        ligne = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox1 = wx.ListBox(self.panel,-1,choices=[],style=wx.LB_EXTENDED)
        self.listbox2 = wx.ListBox(self.panel,-1,choices=[],style=wx.LB_EXTENDED)
        self.listbox3 = wx.ListBox(self.panel,-1,choices=[],style=wx.LB_EXTENDED)

        self.button0 = wx.Button(self.panel,-1,_('Get sites'))

        self.button1 = wx.Button(self.panel,-1,_('Get stations'))
        self.button2 = wx.Button(self.panel,-1,_('Get timeseries list'))

        colplot = wx.BoxSizer(wx.VERTICAL)
        self.button3 = wx.Button(self.panel,-1,_('Get data and new plot...'))
        self.button4 = wx.Button(self.panel,-1,_('Get data and add to plot...'))
        self.button5 = wx.Button(self.panel,-1,_('Export to CSV...'))
        colplot.Add(self.button3, 1, wx.EXPAND, 0)
        colplot.Add(self.button4, 1, wx.EXPAND, 0)
        colplot.Add(self.button5, 1, wx.EXPAND, 0)
        
        #organizing gui Get->Sites->select->Stations->select->Timeseries->Plot
        ligne.Add(self.button0,0,wx.EXPAND,0)
        ligne.Add(self.listbox1,1,wx.EXPAND,0)
        ligne.Add(self.button1,0,wx.EXPAND,0)
        ligne.Add(self.listbox2,1,wx.EXPAND,0)
        ligne.Add(self.button2,0,wx.EXPAND,0)
        ligne.Add(self.listbox3,1,wx.EXPAND,0)
        ligne.Add(colplot, 0, wx.EXPAND, 0)

        ligne2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.cal1 = wx.adv.CalendarCtrl(self.panel,-1,style=wx.adv.CAL_MONDAY_FIRST)
        self.cal2 = wx.adv.CalendarCtrl(self.panel,-1,style=wx.adv.CAL_MONDAY_FIRST)

        col_dates = wx.BoxSizer(wx.VERTICAL)
        self.oneweek = wx.Button(self.panel,-1,_('Today minus one week'))
        self.onemonth = wx.Button(self.panel,-1,_('Today minus one month'))
        self.oneyear = wx.Button(self.panel,-1,_('Today minus one year'))
        self.tenyears = wx.Button(self.panel,-1,_('Today minus ten years'))
        
        col_dates.Add(self.oneweek,1,wx.EXPAND,0)
        col_dates.Add(self.onemonth,1,wx.EXPAND,0)
        col_dates.Add(self.oneyear,1,wx.EXPAND,0)
        col_dates.Add(self.tenyears,1,wx.EXPAND,0)
        
        self.cal2.SetDate(dt.today())
        self.cal1.SetDate(dt.today()-timedelta(60))
        
        ligne2.Add(self.cal1,1,wx.EXPAND,0)
        ligne2.Add(self.cal2,1,wx.EXPAND,0)
        ligne2.Add(col_dates,0,wx.EXPAND,0)

        #zonage
        ligne3 = wx.BoxSizer(wx.HORIZONTAL)
        colxy1 = wx.BoxSizer(wx.VERTICAL)
        colxy2 = wx.BoxSizer(wx.VERTICAL)
        colbut = wx.BoxSizer(wx.VERTICAL)
        
        ligne3.Add(colxy1, 1, wx.EXPAND)
        ligne3.Add(colxy2, 1, wx.EXPAND)
        ligne3.Add(colbut, 1, wx.EXPAND)
        
        self.x_nearest = wx.TextCtrl(self.panel, style = wx.TE_CENTRE |wx.TE_CENTER)
        self.y_nearest = wx.TextCtrl(self.panel, style = wx.TE_CENTRE|wx.TE_CENTER)
        self.x_ur = wx.TextCtrl(self.panel, style = wx.TE_CENTRE|wx.TE_CENTER)
        self.y_ur = wx.TextCtrl(self.panel, style = wx.TE_CENTRE|wx.TE_CENTER)
        self.x_ll = wx.TextCtrl(self.panel, style = wx.TE_CENTRE|wx.TE_CENTER)
        self.y_ll = wx.TextCtrl(self.panel, style = wx.TE_CENTRE|wx.TE_CENTER)

        self.x_nearest.SetToolTip(_('X coordinate for nearest search'))
        self.y_nearest.SetToolTip(_('Y coordinate for nearest search'))

        self.x_ll.SetToolTip(_('X lower left coordinate for interior serach'))
        self.y_ll.SetToolTip(_('Y lower left coordinate for interior serach'))
        self.x_ur.SetToolTip(_('X upper right coordinate for interior serach'))
        self.y_ur.SetToolTip(_('Y upper right coordinate for interior search'))


        self.find_nearest = wx.Button(self.panel,-1,_('Find nearest'))
        self.select_inside = wx.Button(self.panel,-1,_('Select inside'))
        colbut.Add(self.find_nearest, 1, wx.EXPAND)
        colbut.Add(self.select_inside, 1, wx.EXPAND)
        
        colxy1.Add(self.x_nearest, 1, wx.EXPAND)
        colxy1.Add(self.x_ur, 1, wx.EXPAND)
        colxy1.Add(self.x_ll, 1, wx.EXPAND)

        colxy2.Add(self.y_nearest, 1, wx.EXPAND)
        colxy2.Add(self.y_ur, 1, wx.EXPAND)
        colxy2.Add(self.y_ll, 1, wx.EXPAND)

        colonne.Add(ligne, 1, wx.EXPAND)
        colonne.Add(ligne2, 1, wx.EXPAND)
        colonne.Add(ligne3, 0, wx.EXPAND)

        self.panel.SetSizer(colonne)

        self.button0.Bind(wx.EVT_BUTTON, self.getsites)
        self.button1.Bind(wx.EVT_BUTTON, self.getstations)
        self.button2.Bind(wx.EVT_BUTTON, self.gettimeseries)
        self.button3.Bind(wx.EVT_BUTTON, self.getdataandplot)
        self.button4.Bind(wx.EVT_BUTTON, self.getdataandplot)
        self.button5.Bind(wx.EVT_BUTTON, self.exportcsv)
        self.find_nearest.Bind(wx.EVT_BUTTON, self.nearest)
        self.select_inside.Bind(wx.EVT_BUTTON, self.inside)

        self.oneweek.Bind(wx.EVT_BUTTON, self.setdate)
        self.onemonth.Bind(wx.EVT_BUTTON, self.setdate)
        self.oneyear.Bind(wx.EVT_BUTTON, self.setdate)
        self.tenyears.Bind(wx.EVT_BUTTON, self.setdate)

        self.hydro = hydrometry(credential=credential)
        
        self.figsaxes=[]

        self.Show()
        
    def setdate(self, event:wx.CommandEvent):
        
        mybut = event.GetEventObject()
        
        self.cal2.SetDate(dt.today())
        if mybut == self.oneweek:
            decal = timedelta(7)
        elif mybut == self.onemonth:
            decal = timedelta(31)
        elif mybut == self.oneyear:
            decal = timedelta(365)
        elif mybut == self.tenyears:
            decal = timedelta(3652)
        
        self.cal1.SetDate(dt.today()-decal)
    
    def getsites(self, event:wx.CommandEvent):
        """
        Get global sites 
        """
        self.listbox1.Clear()
        self.listbox1.Append(self.hydro._get_sites_pythonlist())
        self.panel.Layout()
    
    def getstations(self, event:wx.CommandEvent):
        """
        Get stations for a specific selected site or multisites
        
        Store a list of these stations in self.stations_list
        """
        sel1 = self.listbox1.GetSelections()
        
        self.stations_list=[]
        for cur in sel1:
            self.stations_list += self.hydro._get_stations_pythonlist(self.hydro.sites['site_no'][cur])
            
        self._fill_list2()
        
    def _fill_list2(self):
        self.stations_list.sort()
        self.listbox2.Clear()
        self.listbox2.Append(self.stations_list)
        self.panel.Layout()
    
    def _getname_code_fromindex(self,index):
        stationname = self.stations_list[index].split('---')[0][:-1]
        stationcode = self.stations_list[index].split('---')[1][1:]

        return stationname, stationcode
    
    def gettimeseries(self, event:wx.CommandEvent):
        """
        Get the timeseries for a selected station
        """        
        to_exclude = ['alarm', 'batterie']
        
        #treat only the first one if multiple selections
        stationname, stationcode = self._getname_code_fromindex(self.listbox2.GetSelections()[0])
        
        id,self.timeseries = self.hydro.timeseries_list(stationcode=stationcode)
        
        self.timeseries.sort_values('ts_name', inplace=True)
        
        self.listbox3.Clear()

        for curkey in kiwis_keywords_horq:
            eltoadd = self.timeseries[self.timeseries['ts_name'].str.lower().str.contains(curkey.value)]['ts_name'].to_list()
            if len(eltoadd)>0:
                for i, curel in reversed(list(enumerate(eltoadd))):
                    for curexc in to_exclude:
                        if curexc in curel.lower():
                            eltoadd.pop(i)
                            break                        
                self.listbox3.Append(eltoadd)
                
        for curkey in kiwis_keywords_rain:
            eltoadd = self.timeseries[self.timeseries['ts_name'].str.lower().str.contains(curkey.value)]['ts_name'].to_list()
            if len(eltoadd)>0:
                for i, curel in reversed(list(enumerate(eltoadd))):
                    for curexc in to_exclude:
                        if curexc in curel.lower():
                            eltoadd.pop(i)
                            break
                self.listbox3.Append(eltoadd)
        
        self.listbox3.Append('--')
        
        self.listbox3.Append(self.timeseries['ts_name'].tolist())
        self.panel.Layout()

    def _get_data(self):
        """
        Download data 
        """
        sel2 = self.listbox2.GetSelections()
        sel3 = self.listbox3.GetSelections()
        
        if len(sel3)==0:
            return None, None, None, None
        
        self.recup_date()
        
        stationname, stationcode = self._getname_code_fromindex(self.listbox2.GetSelections()[0])
        data=[]
        tsname=[]
    
        for cur in sel3:
            #filtre sur base du nom stocké dans le wxListbox
            locname = self.listbox3.GetItems()[cur]
            if locname !='--':
                interval=300
                if "1h" in locname.lower():
                    interval = 3600
                elif "5min" in locname.lower():
                    interval = 300
                elif "10min" in locname.lower():
                    interval = 600
                elif "2min" in locname.lower():
                    interval = 120
                elif "jour" in locname.lower():
                    interval = 24*3600
                elif "mois" in locname.lower():
                    interval = 24*30*3600

                tsname.append('{} - {}'.format(stationname,locname))
                tsid=self.timeseries[self.timeseries['ts_name']==locname]['ts_id'].iloc[0]
                
                locdata = self.hydro.timeseries(fromdate=self.datefrom, todate=self.dateto, ts_id=tsid, interval=interval)
                data.append(locdata)
                
        return stationname, stationcode, data, tsname
    
    def getdataandplot(self,event:wx.CommandEvent):
        """
        Download data and plot
        """
        stationname, stationcode, data, tsname = self._get_data()
        if stationname is None:
            return
        
        if event.GetEventObject() == self.button3 or len(self.figsaxes)==0:
            fig,ax = plt.subplots(1,1)
            self.figsaxes.append([fig,ax])
        else:
            fig, ax = self.figsaxes[-1]
            try:
                ax.set_title('{} - {}'.format(stationcode,stationname))
            except:
                fig,ax = plt.subplots(1,1)
                self.figsaxes.append([fig,ax])
                
        ax.set_title('{} - {}'.format(stationcode,stationname))
        ax.set_xlabel(_('Time'))
        
        for curdata, curname in zip(data,tsname):
            if curdata is not None:
                if len(curdata)>1:
                    ax.step(curdata.index,curdata,where='post', label=curname)
            
        ax.legend()
        plt.show()
        
    def exportcsv(self,event:wx.CommandEvent):
        """
        Download data and export to csv
        """
        stationname, stationcode, data, tsname = self._get_data()
        if stationname is None:
            return

        for curdata, curname in zip(data,tsname):
            if curdata is not None:
                if len(curdata)>1:
                    curdata.to_csv('{}-{}.csv'.format(stationcode,curname), date_format="%Y%m%d%H%M%S", sep=";")
            
    def nearest(self, event:wx.CommandEvent):
        x = float(self.x_nearest.GetValue())
        y = float(self.y_nearest.GetValue())
        
        self.stations_list = self.hydro.find_nearest(x,y,True)

        self._fill_list2()
        
        self.listbox2.SetSelection(0)
        
    def inside(self,event:wx.CommandEvent):
        xll = float(self.x_ll.GetValue())
        yll = float(self.y_ll.GetValue())
        xur = float(self.x_ur.GetValue())
        yur = float(self.y_ur.GetValue())
        
        self.stations_list = self.hydro.select_inside(xll,yll,xur,yur,True)
        
        self._fill_list2()
    
    def recup_date(self):
        """
        Get date from calendars and store in self.datefrom and self.dateto
        """
        sel4 = self.cal1.GetDate()
        sel5 = self.cal2.GetDate()
        self.datefrom = dt(sel4.year,sel4.month+1,sel4.day)
        self.dateto = dt(sel5.year,sel5.month+1,sel5.day)



