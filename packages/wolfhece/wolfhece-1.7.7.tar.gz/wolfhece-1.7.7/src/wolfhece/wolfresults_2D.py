import sys
import wx
from os.path import dirname, exists
from math import floor

import numpy.ma as ma
import numpy as np
import matplotlib.path as mpltPath
from enum import Enum
from typing import Literal
import logging

try:
    from OpenGL.GL import *
except:
    msg=_('Error importing OpenGL library')
    msg+=_('   Python version : ' + sys.version)
    msg+=_('   Please check your version of opengl32.dll -- conflict may exist between different fils present on your desktop')
    raise Exception(msg)

from .drawing_obj import Element_To_Draw
from .PyPalette import wolfpalette
from .PyTranslate import _
from .gpuview import GRID_N, Rectangle, VectorField
from .pyshields import get_d_cr,get_d_cr_susp,izbach_d_cr
from .pyviews import WolfViews
from .mesh2d.wolf2dprev import prev_parameters_simul, bloc_file


try:
    from .libs import wolfpy
except Exception as ex:
    # This convoluted error handling is here to catch an issue
    # which was difficult to track down: wolfpy was there
    # but its DLL were not available.

    from importlib.util import find_spec
    s = find_spec('wolfhece.libs.wolfpy')
    from pathlib import Path

    # Not too sure about this find_spec. If the root
    # directory is not the good one, the import search may
    # end up in the site packages, loading the wrong wolfpy.

    base = Path(__file__).parent.parts
    package = Path(s.origin).parent.parts
    is_submodule = (len(base) <= len(package)) and all(i==j for i, j in zip(base, package))

    if is_submodule:
        msg = _("wolfpy was found but we were not able to load it. It may be an issue with its DLL dependencies")
        msg += _("The actual error was: {}").format(str(ex))
    else:
        msg=_('Error importing wolfpy.pyd')
        msg+=_('   Python version : ' + sys.version)
        msg+=_('   If your Python version is not 3.7.x or 3.9.x, you need to compile an adapted library with compile_wcython.py in wolfhece library path')
        msg+=_('   See comments in compile_wcython.py or launch *python compile_wcython.py build_ext --inplace* in :')
        msg+='      ' + dirname(__file__)

    raise Exception(msg)

from .wolf_array import WolfArray, getkeyblock, header_wolf, WolfArrayMB, WolfArrayMNAP, header_wolf
from .mesh2d import wolf2dprev
from .PyVertexvectors import vector

class views_2D(Enum):
    WATERDEPTH = _('Water depth [m]')
    WATERLEVEL = _('Water level [m]')
    TOPOGRAPHY = _('Bottom level [m]')
    QX = _('Discharge X [m2s-1]')
    QY = _('Discharge Y [m2s-1]')
    QNORM = _('Discharge norm [m2s-1]')
    UX  =_('Velocity X [ms-1]')
    UY = _('Velocity Y [ms-1]')
    UNORM = _('Velocity norm [ms-1]')
    HEAD = _('Head [m]')
    FROUDE = _('Froude [-]')
    KINETIC_ENERGY = _('Kinetic energy k')
    EPSILON = _('Rate of dissipation e')
    TURB_VISC_2D = _('Turbulent viscosity 2D')
    TURB_VISC_3D = _('TurbuleD = nt viscosity 3D')
    VECTOR_FIELD_Q = _('Discharge vector field')
    VECTOR_FIELD_U = _('Velocity vector field')
    CRITICAL_DIAMETER_SHIELDS = _('Critical grain diameter - Shields')
    CRITICAL_DIAMETER_IZBACH = _('Critical grain diameter - Izbach')
    CRITICAL_DIAMETER_SUSPENSION_50 = _('Critical grain diameter - Suspension 50%')
    CRITICAL_DIAMETER_SUSPENSION_100 = _('Critical grain diameter - Suspension 100%')
    WL_Q = _('WL + Q')
    WD_U = _('WD + U')
    T_WL_Q = _('Top + WL + Q')
    T_WD_Q = _('Top + WD + Q')
    T_WD_U = _('Top + WD + U')

VIEWS_SEDIMENTARY = [views_2D.CRITICAL_DIAMETER_SHIELDS,
                     views_2D.CRITICAL_DIAMETER_IZBACH,
                     views_2D.CRITICAL_DIAMETER_SUSPENSION_50,
                     views_2D.CRITICAL_DIAMETER_SUSPENSION_100]

VIEWS_COMPLEX = [views_2D.T_WD_Q,
                 views_2D.T_WD_U,
                 views_2D.T_WL_Q,
                 views_2D.WL_Q,
                 views_2D.WD_U]

VIEWS_VECTOR_FIELD = [views_2D.VECTOR_FIELD_Q, views_2D.VECTOR_FIELD_U]

class OneWolfResult:
    """
    Stockage des résultats d'un bloc de modèle WOLF2D
    """
    def __init__(self, idx=0):

        self.idx = idx          # index du bloc en numérotation Python --> penser à ajouter 1 si retour type VB6/Fortran
        self.linkedvec = None
        self.epsilon = 0.

        self.waterdepth = WolfArray()
        self.top = WolfArray()
        self.qx = WolfArray()
        self.qy = WolfArray()
        self.rough_n = WolfArray()
        self.set_current(views_2D.WATERDEPTH)

        self.k = WolfArray()
        self.eps = WolfArray()

        self.critShields = None
        self.critIzbach = None
        self.critSusp50 = None
        self.critSusp100 = None

    @property
    def current(self):
        return self._current

    def set_linkedvec(self,link):
        self.linkedvec = link

    def set_epsilon(self,eps):
        self.epsilon = eps

    def filter_inundation(self):
        """
        Apply filter on array :
            - mask data below eps
            - mask data outisde linkedvec
        """
        self._current.filter_inundation(self.epsilon)

    def set_current(self,which):
        self._which_current = which

        if which==views_2D.WATERDEPTH:
            self._current=self.waterdepth
        elif which==views_2D.TOPOGRAPHY:
            self._current=self.top
        elif which==views_2D.QX:
            self._current=self.qx
        elif which==views_2D.QY:
            self._current=self.qy
        elif which==views_2D.QNORM:
            self._current=(self.qx**2.+self.qy**2.)**.5
        elif which==views_2D.UNORM:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth
        elif which==views_2D.UX:
            self._current=self.qx/self.waterdepth
        elif which==views_2D.UY:
            self._current=self.qy/self.waterdepth
        elif which==views_2D.WATERLEVEL:
            self._current=self.waterdepth+self.top
        elif which==views_2D.FROUDE:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(self.waterdepth*9.81)**.5
        elif which==views_2D.HEAD:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(2.*9.81)+self.waterdepth+self.top
        elif which==views_2D.KINETIC_ENERGY:
            self._current=self.k
        elif which==views_2D.EPSILON:
            self._current=self.eps
        elif which==views_2D.VECTOR_FIELD_Q:
            self._current=(self.qx**2.+self.qy**2.)**.5
            self._vec_field = VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)
        elif which==views_2D.VECTOR_FIELD_U:
            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth
            self._current=(ux**2.+uy**2.)**.5
            self._vec_field = VectorField(ux.array, uy.array, ux.get_bounds(), ux.dx, ux.dy)

        elif which ==views_2D.WL_Q:

            self._current = self.waterdepth+self.top
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._view.add_elemts([self._current, VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which ==views_2D.WD_U:

            self._current = self.waterdepth
            self._view = WolfViews()
            self._view.add_elemts([self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which ==views_2D.T_WL_Q:

            self._current = self.waterdepth+self.top
            self._view = WolfViews()

            self._view.add_elemts([self.top, self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which ==views_2D.T_WD_Q:

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()

            self._view.add_elemts([self.top, self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which ==views_2D.T_WD_U:

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._view.add_elemts([self.top, self._current, VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which==views_2D.CRITICAL_DIAMETER_SHIELDS:
            if self.critShields is None:
                self.critShields = self.get_critdiam(0)
            self._current = self.critShields
        elif which==views_2D.CRITICAL_DIAMETER_IZBACH:
            if self.critIzbach is None:
                self.critIzbach = self.get_critdiam(1)
            self._current = self.critIzbach
        elif which==views_2D.CRITICAL_DIAMETER_SUSPENSION_50:
            if self.critSusp50 is None:
                self.critSusp50 = self.get_critsusp(50)
            self._current = self.critSusp50
        elif which==views_2D.CRITICAL_DIAMETER_SUSPENSION_100:
            if self.critSusp100 is None:
                self.critSusp100 = self.get_critsusp(100)
            self._current = self.critSusp100


        self._current.linkedvec = self.linkedvec

    def update_zoom_vectorfield(self,factor):

        self._vec_field.zoom_factor *= factor

    def update_arrowpixelsize_vectorfield(self,factor):

        self._vec_field.arrow_pixel_size *= factor
        self._vec_field.arrow_pixel_size = int(self._vec_field.arrow_pixel_size)

    def update_pal(self,curpal:wolfpalette,graypal=None,bluepal=None):
        which = self._which_current

        self._current.mypal = curpal
        self._current.rgb = curpal.get_rgba(self._current.array)
        self._current.rgb[self._current.array.mask] = [1., 1., 1., 1.]

        if which == 'wd_u':
            self._view.pals = [bluepal,curpal]
        elif which =='t_wl_q':
            self._view.pals = [graypal,curpal,None]
        elif which =='t_wd_q':
            self._view.pals = [graypal,bluepal,None]
        elif which =='t_wd_u':
            self._view.pals = [graypal,bluepal,None]

    def get_critdiam(self,which):

        with wx.lib.busy.BusyInfo(_('Computing critical diameters')):
            wait = wx.BusyCursor()

            ij = np.argwhere(self.waterdepth.array>0.)

            diamcrit = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask

            if which==0:
                diam = np.asarray([get_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j])[which] for i,j in ij])
            else:
                diam = np.asarray([izbach_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j]) for i,j in ij])

            diamcrit.array[ij[:,0],ij[:,1]] = diam

            del wait
            return diamcrit

    def get_critsusp(self,which=50):

        with wx.lib.busy.BusyInfo(_('Computing critical diameters')):
            wait = wx.BusyCursor()
            ij = np.argwhere(self.waterdepth.array>0.)

            diamcrit = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask

            diam = np.asarray([get_d_cr_susp(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j],which=which) for i,j in ij])

            diamcrit.array[ij[:,0],ij[:,1]] = diam

            del wait
            return diamcrit

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None):
        if self._which_current in VIEWS_VECTOR_FIELD:
            self._vec_field.plot(sx, sy,xmin,ymin,xmax,ymax)
        elif self._which_current in VIEWS_COMPLEX:
            self._view.plot(sx, sy,xmin,ymin,xmax,ymax)
        else:
            self._current.plot(sx, sy,xmin,ymin,xmax,ymax)

    def get_values_labels(self, i, j):
        which = self._which_current

        mylab = [which.value]
        myval = [self._current.array[i,j]]

        if which in VIEWS_COMPLEX:

            mylab = [views_2D.TOPOGRAPHY.value,
                     views_2D.WATERDEPTH.value,
                     views_2D.WATERLEVEL.value,
                     views_2D.QX.value,
                     views_2D.QY.value,
                     views_2D.QNORM.value,
                     views_2D.UX.value,
                     views_2D.UY.value,
                     views_2D.UNORM.value,
                     views_2D.FROUDE.value]

            top = self.top.array[i,j]
            h  = self.waterdepth.array[i,j]

            sl = h+top

            qx = self.qx.array[i,j]
            qy = self.qy.array[i,j]
            qnorm = (qx**2.+qy**2.)**.5

            ux = qx/h
            uy = qy/h

            unorm = (ux**2.+uy**2.)**.5

            fr = unorm/(9.81*h)**.5
            myval = [top,
                     h,
                     sl,
                     qx,
                     qy,
                     qnorm,
                     ux,
                     uy,
                     unorm,
                     fr]

        return myval,mylab

class Wolfresults_2D(Element_To_Draw):
    """
    Manipulation des résultats d'un modèle WOLF2D en multiblocs

    La classe hérite de 'Element_To_Draw' afin d'être sûr de disposer des informations pour un éventuel affichage dans un viewer 'WolfMapViewer'

    ATTENTION :
     - la classe contient un dictionnaire 'myblocks' d'objets 'OneWolfResult'
     - les clés du dictionnaire sont de type 'block1', 'block2'... 'blockn' --> voir fonction 'getkeyblock'
     - les entrées ne sont PAS des matrices multiblocks 'WolfArrayMB' mais une classe 'OneWolfResult' contient plusieurs matrices pour chaque type de résultat (water depth, dischargeX, dischargeY, ...)

     - la classe se comporte donc un peu comme une généralisation d'une matrice 'WolfArrayMB' mais il ne s'agit pas d'une extension par polymorphisme
     - on retrouve cependant plusieurs routines similaires afin de faciliter l'intégration dans un viewer WX
    """
    myblocks:dict[str, OneWolfResult]
    head_blocks:dict[str, header_wolf]

    myparam:prev_parameters_simul
    myblocfile:bloc_file
    mymnap:WolfArrayMNAP

    def __init__(self, fname = None, mold = None, eps=0., idx: str = '', plotted: bool = True, mapviewer=None, need_for_wx: bool = False) -> None:
        super().__init__(idx, plotted, mapviewer, need_for_wx)

        """
        Initialisation
        """
        self.filename=""
        self.filenamegen=self.filename

        self.linkedvec = None # vecteur d'exclusion de données
        self.epsilon = eps

        self.nb_blocks = 0
        self.loaded=True
        self.current_result = -1
        self.mypal = wolfpalette(None,'Colors')
        self.mypal.default16()
        self.mypal.automatic = True

        self.nbnotnull=99999

        self.plotted=False
        self.plotting=False

        self._which_current_view = views_2D.WATERDEPTH # _('Water depth [m]')

        if fname is not None:
            self.filename = fname
            self.filenamegen=self.filename

            with open(self.filename + '.trl') as f:
                trl=f.read().splitlines()
                self.translx=float(trl[1])
                self.transly=float(trl[2])

            self.myblocks={}
            self.head_blocks={}
            self.read_param_simul()

            if exists(self.filename+'.head'):
                wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
                self.nb_blocks = wolfpy.r2d_nbblocks()

                for i in range(self.nb_blocks):
                    curblock = OneWolfResult(i)
                    self.myblocks[getkeyblock(i)] = curblock

                    nbx,nby,dx,dy,ox,oy,tx,ty = wolfpy.r2d_hblock(i+1)

                    curhead = self.head_blocks[getkeyblock(i)]=header_wolf()
                    curhead.nbx = nbx
                    curhead.nby = nby
                    curhead.origx = ox
                    curhead.origy = oy
                    curhead.dx = dx
                    curhead.dy = dy
                    curhead.translx = self.translx
                    curhead.transly = self.transly

                    self.myblocks[getkeyblock(i)].waterdepth.dx = dx
                    self.myblocks[getkeyblock(i)].waterdepth.dy = dy
                    self.myblocks[getkeyblock(i)].waterdepth.nbx = nbx
                    self.myblocks[getkeyblock(i)].waterdepth.nby = nby
                    self.myblocks[getkeyblock(i)].waterdepth.origx = ox
                    self.myblocks[getkeyblock(i)].waterdepth.origy = oy
                    self.myblocks[getkeyblock(i)].waterdepth.translx = self.translx
                    self.myblocks[getkeyblock(i)].waterdepth.transly = self.transly

                    self.myblocks[getkeyblock(i)].top.dx = dx
                    self.myblocks[getkeyblock(i)].top.dy = dy
                    self.myblocks[getkeyblock(i)].top.nbx = nbx
                    self.myblocks[getkeyblock(i)].top.nby = nby
                    self.myblocks[getkeyblock(i)].top.origx = ox
                    self.myblocks[getkeyblock(i)].top.origy = oy
                    self.myblocks[getkeyblock(i)].top.translx = self.translx
                    self.myblocks[getkeyblock(i)].top.transly = self.transly

                    self.myblocks[getkeyblock(i)].qx.dx = dx
                    self.myblocks[getkeyblock(i)].qx.dy = dy
                    self.myblocks[getkeyblock(i)].qx.nbx = nbx
                    self.myblocks[getkeyblock(i)].qx.nby = nby
                    self.myblocks[getkeyblock(i)].qx.origx = ox
                    self.myblocks[getkeyblock(i)].qx.origy = oy
                    self.myblocks[getkeyblock(i)].qx.translx = self.translx
                    self.myblocks[getkeyblock(i)].qx.transly = self.transly

                    self.myblocks[getkeyblock(i)].qy.dx = dx
                    self.myblocks[getkeyblock(i)].qy.dy = dy
                    self.myblocks[getkeyblock(i)].qy.nbx = nbx
                    self.myblocks[getkeyblock(i)].qy.nby = nby
                    self.myblocks[getkeyblock(i)].qy.origx = ox
                    self.myblocks[getkeyblock(i)].qy.origy = oy
                    self.myblocks[getkeyblock(i)].qy.translx = self.translx
                    self.myblocks[getkeyblock(i)].qy.transly = self.transly

                    self.myblocks[getkeyblock(i)].rough_n.dx = dx
                    self.myblocks[getkeyblock(i)].rough_n.dy = dy
                    self.myblocks[getkeyblock(i)].rough_n.nbx = nbx
                    self.myblocks[getkeyblock(i)].rough_n.nby = nby
                    self.myblocks[getkeyblock(i)].rough_n.origx = ox
                    self.myblocks[getkeyblock(i)].rough_n.origy = oy
                    self.myblocks[getkeyblock(i)].rough_n.translx = self.translx
                    self.myblocks[getkeyblock(i)].rough_n.transly = self.transly

            else:
                self.nb_blocks = self.myblocfile.nb_blocks

                for i in range(self.nb_blocks):
                    curblock = OneWolfResult(i)
                    self.myblocks[getkeyblock(i)] = curblock
                    curblock.waterdepth.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                    curblock.top.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                    curblock.qx.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                    curblock.qy.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                    curblock.rough_n.set_header(self.mymnap.head_blocks[getkeyblock(i)])

            self.allocate_ressources()
            self.read_topography()
            self.read_ini_mb()

            self.loaded_rough = False

        self.nbx = 1
        self.nby = 1

        ox=99999.
        oy=99999.
        ex=-99999.
        ey=-99999.
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curhead:header_wolf
            curhead=curblock.waterdepth.get_header(False)
            ox=min(ox,curhead.origx)
            oy=min(oy,curhead.origy)
            ex=max(ex,curhead.origx+float(curhead.nbx)*curhead.dx)
            ey=max(ey,curhead.origy+float(curhead.nby)*curhead.dy)
        self.dx = ex-ox
        self.dy = ey-oy
        self.origx = ox
        self.origy = oy

    def find_minmax(self,update=False):
        """Find spatial bounds"""
        self.xmin = self.origx + self.translx
        self.xmax = self.origx + self.translx + float(self.nbx) * self.dx
        self.ymin = self.origy + self.transly
        self.ymax = self.origy + self.transly + float(self.nby) * self.dy

    def update_arrowpixelsize_vectorfield(self,factor):
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock.update_arrowpixelsize_vectorfield(factor)

    def get_dxdy_min(self):
        """Return the minimal size into blocks"""
        dmin=99999
        for curblock in self.myblocks.values():
            dmin = min(dmin,curblock.waterdepth.dx)
            dmin = min(dmin,curblock.waterdepth.dy)

        return dmin

    def get_dxdy_max(self):
        """Return the maximal size into blocks"""
        dmax=-99999
        for curblock in self.myblocks.values():
            dmax = max(dmax,curblock.waterdepth.dx)
            dmax = max(dmax,curblock.waterdepth.dy)

        return dmax

    def read_param_simul(self):
        """Read simulation parameters from files"""
        self.myparam = prev_parameters_simul(self)
        self.myparam.read_file(self.filename)

        self.myblocfile = bloc_file(self)
        self.myblocfile.read_file()

        self.mymnap = WolfArrayMNAP(self.filename)

    def get_currentview(self):
        """Return the current view"""
        return self._which_current_view

    def filter_inundation(self, eps=None, linkedvec = None):
        """
        Apply filter on array :
            - mask data below eps
            - mask data outisde linkedvec
        """

        if eps is not None:
            self.epsilon = eps
        if linkedvec is not None:
            self.linkedvec = linkedvec

        self.mimic_plotdata()

        for curblock in self.myblocks.values():
            curblock.filter_inundation()

    def set_currentview(self,which=None):
        """Set the current view --> see 'views_2D' for supported values"""
        if which is None:
            which = self._which_current_view

        if which in views_2D:
            self.delete_lists()

            self._which_current_view = which

            self.plotting=True
            self.mimic_plotdata()

            # self.delete_lists() #on efface les listes OpenGL car on va remplacer l'objet, or il peut être nue combinaison de cartes de base

            if which in VIEWS_SEDIMENTARY:

                if not self.loaded_rough:
                    self.read_roughness_param()

            for curblock in self.myblocks.values():
                curblock:OneWolfResult
                curblock.set_current(which)

            self.filter_inundation()

            self.mypal.automatic = True
            self.reset_plot()

            self.plotting=False
            self.mimic_plotdata()

    def allocate_ressources(self):
        """Allocation de l'espace mémoire utile pour le stockage des résultats de chaque bloc"""
        for curblock in self.myblocks.values():
            curblock.waterdepth.allocate_ressources()
            curblock.top.allocate_ressources()
            curblock.qx.allocate_ressources()
            curblock.qy.allocate_ressources()

    def read_topography(self):
        """Lecture de la topographie de modélisation"""
        with open(self.filename.strip() + '.topini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks[getkeyblock(i)].top.nbx
                nby=self.myblocks[getkeyblock(i)].top.nby
                nbbytes=nbx*nby*4
                self.myblocks[getkeyblock(i)].top.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                self.myblocks[getkeyblock(i)].top.array = self.myblocks[getkeyblock(i)].top.array.reshape(nbx,nby,order='F')

    def read_ini_mb(self):
        """Lecture des conditions initiales"""
        if exists(self.filename.strip() + '.hbinb'):
            with open(self.filename.strip() + '.hbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].waterdepth.nbx
                    nby=self.myblocks[getkeyblock(i)].waterdepth.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].waterdepth.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].waterdepth.array = self.myblocks[getkeyblock(i)].waterdepth.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qxbinb'):
            with open(self.filename.strip() + '.qxbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qx.nbx
                    nby=self.myblocks[getkeyblock(i)].qx.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qx.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qx.array = self.myblocks[getkeyblock(i)].qx.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qybinb'):
            with open(self.filename.strip() + '.qybinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qy.nbx
                    nby=self.myblocks[getkeyblock(i)].qy.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qy.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qy.array = self.myblocks[getkeyblock(i)].qy.array.reshape(nbx,nby,order='F')

    def read_roughness_param(self):
        """Lecture du frottement de modélisation"""
        with open(self.filename.strip() + '.frotini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks[getkeyblock(i)].rough_n.nbx
                nby=self.myblocks[getkeyblock(i)].rough_n.nby
                nbbytes=nbx*nby*4
                self.myblocks[getkeyblock(i)].rough_n.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                self.myblocks[getkeyblock(i)].rough_n.array = self.myblocks[getkeyblock(i)].rough_n.array.reshape(nbx,nby,order='F')
        self.loaded_rough = True

    def get_nbresults(self):
        """Récupération du nombre de pas sauvegardés --> utilisation de la librairie Fortran"""
        if exists(self.filename+'.head'):
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            return  wolfpy.r2d_getnbresults()
        else:
            return 1

    def read_oneblockresult_withoutmask(self,which:int=-1,whichblock:int=-1):
        """Lecture d'un résultat pour un bloc spécifique --> utilisation de la librairie Fortran"""
        if whichblock!=-1:
            block = self.myblocks[getkeyblock(whichblock,False)]
            nbx = block.waterdepth.nbx
            nby = block.waterdepth.nby
            block.waterdepth.array, block.qx.array, block.qy.array = wolfpy.r2d_getresults(which,nbx,nby,whichblock)

    def read_oneblockresult(self,which:int=-1,whichblock:int=-1):
        """
        Lecture d'un résultat pour un bloc spécifique et application d'un masque sur base d'nu epsilon de hauteur d'eau

        which: result number to read; 0-based; -1 == last one
        """
        if whichblock!=-1:

            self.read_oneblockresult_withoutmask(which,whichblock)

            if self.epsilon > 0.:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.array=ma.masked_less_equal(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array,self.epsilon)
            else:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.array=ma.masked_equal(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array,0.)

            self.myblocks[getkeyblock(whichblock,False)].qx.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qx.array)
            self.myblocks[getkeyblock(whichblock,False)].qy.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qy.array)

            self.myblocks[getkeyblock(whichblock,False)].waterdepth.count()
            self.myblocks[getkeyblock(whichblock,False)].qx.count()
            self.myblocks[getkeyblock(whichblock,False)].qy.count()

            if self.epsilon > 0.:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.set_nullvalue_in_mask()
                self.myblocks[getkeyblock(whichblock,False)].qx.set_nullvalue_in_mask()
                self.myblocks[getkeyblock(whichblock,False)].qy.set_nullvalue_in_mask()

    def read_oneresult(self,which=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """

        if exists(self.filename+'.head'):
            logging.info(_('Reading from results - step :{}'.format(which)))
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            for i in range(self.nb_blocks):
                self.read_oneblockresult(which,i+1)
        else:
            logging.info(_('No ".head" file --> Initial Conditions'))

        self.current_result = which
        self.loaded=True

    def get_h_for_block(self, block: int) -> WolfArray:
        """
        Retourne la matrice de hauteur d'eau pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        return self.myblocks[getkeyblock(block,False)].waterdepth

    def get_qx_for_block(self, block: int) -> WolfArray:
        """
        Retourne la matrice de débit selon X pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        return self.myblocks[getkeyblock(block,False)].qx

    def get_qy_for_block(self, block: int) -> WolfArray:
        """
        Retourne la matrice de débit selon Y pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        return self.myblocks[getkeyblock(block,False)].qy

    def get_values_as_wolf(self, i:int, j:int, which_block:int=1):
        """
        Retourne les valeurs associées à des indices (i,j) et un numéro de block

        which_block : numéro du bloc; 1-based;

        ***
        ATTENTION :
            Les indices sont passés comme WOLF --> en numérottaion Fortran (démarrage à 1 et non à 0)
        ***
        """
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1

        nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
        nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby

        if(i>0 and i<=nbx and j>0 and j<=nby):
            h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
            top = self.myblocks[getkeyblock(which_block,False)].top.array[i-1,j-1]
            qx = self.myblocks[getkeyblock(which_block,False)].qx.array[i-1,j-1]
            qy = self.myblocks[getkeyblock(which_block,False)].qy.array[i-1,j-1]
            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5

        return h,qx,qy,vx,vy,vabs,fr,h+top,top

    def get_header_block(self, which_block=1) -> header_wolf:
        """
        Obtention du header_wolf d'un block

        which_block : numéro du bloc; 1-based;
        """

        return self.head_blocks[getkeyblock(which_block,False)]

    def get_xy_infootprint_vect(self, myvect: vector, which_block=1) -> np.ndarray:

        """
        Returns:
            numpy array content les coordonnées xy des mailles dans l'empreinte du vecteur
        """

        myptsij = self.get_ij_infootprint_vect(myvect, which_block)
        mypts=np.asarray(myptsij.copy(),dtype=np.float64)

        lochead = self.get_header_block(which_block)

        mypts[:,0] = (mypts[:,0]+.5)*lochead.dx +lochead.origx +lochead.translx
        mypts[:,1] = (mypts[:,1]+.5)*lochead.dy +lochead.origy +lochead.transly

        return mypts,myptsij

    def get_ij_infootprint_vect(self, myvect: vector, which_block=1) -> np.ndarray:

        """
        Returns:
            numpy array content les indices ij des mailles dans l'empreinte du vecteur
        """

        lochead = self.get_header_block(which_block)
        nbx = lochead.nbx
        nby = lochead.nby

        i1, j1 = self.get_ij_from_xy(myvect.xmin, myvect.ymin, which_block)
        i2, j2 = self.get_ij_from_xy(myvect.xmax, myvect.ymax, which_block)
        i1 = max(i1,0)
        j1 = max(j1,0)
        i2 = min(i2,nbx-1)
        j2 = min(j2,nby-1)
        xv,yv = np.meshgrid(np.arange(i1,i2+1),np.arange(j1,j2+1))
        mypts = np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis]))

        return mypts

    def get_xy_inside_polygon(self, myvect: vector, usemask=True):
        '''
        Obtention des coordonnées contenues dans un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        myvect.find_minmax()

        mypointsxy={}

        myvert = myvect.asnparray()
        path = mpltPath.Path(myvert)

        for curblock in range(self.nb_blocks):
            locpointsxy,locpointsij = self.get_xy_infootprint_vect(myvect,curblock+1)
            inside = path.contains_points(locpointsxy)

            locpointsxy = locpointsxy[np.where(inside)]

            if usemask and len(locpointsxy)>0:
                locpointsij = locpointsij[np.where(inside)]
                mymask = np.logical_not(self.myblocks[getkeyblock(curblock)].current.array.mask[locpointsij[:, 0], locpointsij[:, 1]])
                locpointsxy = locpointsxy[np.where(mymask)]

            mypointsxy[getkeyblock(curblock)]=locpointsxy

        return mypointsxy

    def get_xy_under_polyline(self, myvect: vector) -> dict[str, (int,int)]:
        '''
        Obtention des coordonnées (x,y) sous une polyligne avec séparation despoints par bloc
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        ds = self.get_dxdy_min()  # récupération de la taille la plus fine
        pts = myvect._refine2D(ds)# récupération des (x,y) selon le vecteur au pas le plus fin

        mypoints={}
        for idx in range(self.nb_blocks):
            mypoints[getkeyblock(curblock)]=[]

        for curpt in pts:
            i,j,curblock = self.get_blockij_from_xy(curpt.x, curpt.y, aswolf=False)
            if curblock>-1:
                mypoints[getkeyblock(curblock)].append([curpt.x, curpt.y])

        return mypoints

    def get_values_insidepoly(self,myvect:vector, usemask=True, agglo=True, getxy=False):
        """
        Retourne les valeurs des mailles contenues dans un polygone
        Traite la matrice courante et l'altitude de fond si on est en vue 'views_2D.WATERLEVEL'

        Return:
          - dictionnaire

        """
        myvalues={}
        myvaluesel={}
        mypoints = self.get_xy_inside_polygon(myvect, usemask)

        for curblock in range(self.nb_blocks):
            curkey = getkeyblock(curblock)
            if len(mypoints[curkey])>0:
                locval = np.asarray([self.get_value(cur[0], cur[1]) for cur in mypoints[curkey]])
                locel = np.asarray([self.get_value_elevation(cur[0],cur[1]) for cur in mypoints[curkey]])

                locval=locval[np.where(locval!=-1)]
                locel=locel[np.where(locel!=-1)]

                myvalues[curkey]=locval
                myvaluesel[curkey]=locel
            else:
                myvalues[curkey]=np.asarray([])
                myvaluesel[curkey]=np.asarray([])

        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            myvaluesel = np.concatenate([cur for cur in myvaluesel.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])

        if self._which_current_view == views_2D.WATERLEVEL:
            if getxy:
                return myvalues,myvaluesel,mypoints
            else:
                return myvalues,myvaluesel
        else:
            if getxy:
                return myvalues,None,mypoints
            else:
                return myvalues,None

    def get_all_values_insidepoly(self,myvect:vector, usemask=True, agglo=True, getxy=False):
        """
        Récupération de toutes les valeurs dans un polygone

        usemask (optional) restreint les éléments aux éléments non masqués de la matrice
        getxy (optional) retourne en plus les coordonnées des points
        """

        myvalues={}
        mypoints = self.get_xy_inside_polygon(myvect, usemask)

        for curblock in range(self.nb_blocks):
            if len(mypoints[getkeyblock(curblock)])>0:
                locval = np.asarray([self.get_values_from_xy(cur[0], cur[1]) for cur in mypoints[getkeyblock(curblock)]], dtype=object)

                locval=np.asarray([tuple(valloc) for valloc in locval if tuple(valloc)!=((-1,-1,-1,-1,-1,-1,-1),('-','-','-'))], dtype=object)

                myvalues[getkeyblock(curblock)]=locval
            else:
                myvalues[getkeyblock(curblock)]=np.empty([0,2])

        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])

        if getxy:
            return myvalues,mypoints
        else:
            return myvalues

    def get_all_values_underpoly(self,myvect:vector, usemask=True, agglo=True, getxy=False):
        """
        Récupération de toutes les valeurs sous la polyligne

        usemask (optional) restreint les éléments aux éléments non masqués de la matrice
        getxy (optional) retourne en plus les coordonnées des points
        """
        myvalues={}
        mypoints = self.get_xy_under_polyline(myvect)

        for curkey, ptsblock in mypoints.items():
            if len(ptsblock)>0:
                myvalues[curkey]=np.asarray([self.get_values_from_xy(cur[0], cur[1]) for cur in ptsblock], dtype=object)
            else:
                myvalues[curkey]=np.empty([0,2])

        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])

        if getxy:
            return myvalues,mypoints
        else:
            return myvalues

    def get_values_from_xy(self, x:float, y:float, aswolf=True):
        """
        Retrouve les valeurs sur base de la coordonnée (x,y)

        aswolf : (optional) si True alors ajoute 1 à i et j pour se retrouver en numérotation VB6/Fortran
        """
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1

        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            top = curblock.top.array[i,j]
            qx = curblock.qx.array[i,j]
            qy = curblock.qy.array[i,j]

            exists = top>0.

            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5
                exists=True
            if exists:
                break

        if exists:
            if aswolf:
                return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i+1,j+1,curblock.idx+1)
            else:
                return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i,j,curblock.idx)
        else:
            return (-1,-1,-1,-1,-1,-1,-1),('-','-','-')

    def get_value(self, x:float, y:float, nullvalue=-1):
        """
        Return the value of the current array at (X,Y) position
        """
        h=-1
        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            val = curblock.current.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            return val
        else:
            return nullvalue

    def get_values_labels(self,x:float, y:float):
        """
        Return the values and labels of the current view at (X,Y) position
        """
        h=-1
        exists=False

        for i,j, curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            vals,labs = curblock.get_values_labels(i,j)
            return vals,labs
        else:
            return -1

    def get_value_elevation(self, x:float, y:float, nullvalue=-1):
        """Return the value of the bed elevation at (X,Y) position"""

        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            val = curblock.top.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            return val
        else:
            return nullvalue

    def get_xy_from_ij(self, i, j, which_block, aswolf=False, abs=True):
        """
        Retourne les coordonnées (x,y) depuis les indices (i,j) et le numéro de block
        """

        x,y = self.myblocks[getkeyblock(which_block,False)].waterdepth.get_xy_from_ij(i, j, aswolf=aswolf, abs=abs)
        return x,y

    def get_ij_from_xy(self, x:float, y:float, which_block, aswolf=False, abs=True):
        """
        Retrouve les indices d'un point (x,y) dans un bloc spécifique

        Utilise la routine du même nom dans la martrice 'waterdepth'
        """

        i,j = self.myblocks[getkeyblock(which_block,False)].waterdepth.get_ij_from_xy(x,y, aswolf=aswolf, abs=abs)

        return i,j # Par défaut en indices Python et non WOLF (VB6/Fortran)

    def _test_bounds_block(self, x:float, y:float, curblock:OneWolfResult):
        """
        Teste les bornes d'un bloc versus les coordonnées (x,y) d'un point
        """
        nbx = curblock.waterdepth.nbx
        nby = curblock.waterdepth.nby
        i,j = curblock.waterdepth.get_ij_from_xy(x, y, aswolf=False)

        if(i>=0 and i<nbx and j>=0 and j<nby):
            return True
        else:
            return False

    def enum_block_xy(self, x:float, y:float, aswolf=False, abs=True):
        """
        Enumération des blocs contenant la coordonnée (x,y)

        aswolf : True ajoute 1 à i et j pour corresppondre au format de numérotation VB6/Fortran
        """
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            if self._test_bounds_block(x, y, curblock):

                i,j=curblock.waterdepth.get_ij_from_xy(x, y, aswolf=aswolf, abs=abs)

                yield i,j,curblock

    def get_blockij_from_xy(self, x:float, y:float, abs=True, aswolf=True):
        """
        Retourne les indices i,j et le numéro du block depuis les coordonnées (x,y)

        aswolf : True ajoute 1 à i et j pour corresppondre au format de numérotation VB6/Fortran
        """
        exists = False
        for i, j, curblock in self.enum_block_xy(x,y):
            if not curblock.waterdepth.array.mask[i, j]:
                exists = True
                break

        if exists:
            if aswolf:
                return i+1, j+1, curblock.idx+1
            else:
                return i, j, curblock.idx
        else:
            return -1, -1, -1

    def check_plot(self):
        """
        L'objet est coché/à traiter dans une fenêtre graphique 'WolfMapViewer'
        """
        self.plotted = True
        self.mimic_plotdata()

        if not self.loaded and self.filename!='':
            self.read_oneresult(self.current_result)
            self.reset_plot()

    def uncheck_plot(self, unload=False):
        """
        L'objet est décoché/pas à traiter dans une fenêtre graphique 'WolfMapViewer'
        """
        self.plotted = False
        self.mimic_plotdata()

    def link_palette(self):
        """
        Applique la même palette de couleur/colormap à tous les blocs
        """
        for curblock in self.myblocks.values():
            curblock.update_pal(self.mypal,self.palgray,self.palblue)

    def get_min_max(self, which:Literal[views_2D.TOPOGRAPHY, views_2D.WATERDEPTH, 'current']):
        """
        Retourne la valeur min et max de la topo, de la hauteur d'eau ou de la matrice courante
        """
        if which == views_2D.TOPOGRAPHY:
            min = np.min([np.min(curblock.top.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.top.array) for curblock in self.myblocks.values()])
        elif which == views_2D.WATERDEPTH:
            min = np.min([np.min(curblock.waterdepth.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.waterdepth.array) for curblock in self.myblocks.values()])
        elif which == 'current':
            min = np.min([np.min(curblock.current.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.current.array) for curblock in self.myblocks.values()])

        return min,max

    def get_working_array(self,onzoom=[]):
        """
        Délimitation d'une portion de matrice sur base de bornes

        onzoom : Liste Python de type [xmin, xmax, ymin, ymax]
        """

        if onzoom!=[]:
            allarrays=[]
            for curblock in self.myblocks.values():
                istart,jstart = curblock._current.get_ij_from_xy(onzoom[0],onzoom[2])
                iend,jend = curblock._current.get_ij_from_xy(onzoom[1],onzoom[3])

                istart= 0 if istart < 0 else istart
                jstart= 0 if jstart < 0 else jstart
                iend= curblock._current.nbx if iend > curblock._current.nbx else iend
                jend= curblock._current.nby if jend > curblock._current.nby else jend

                partarray=curblock._current.array[istart:iend,jstart:jend]
                partarray=partarray[partarray.mask==False]
                if len(partarray)>0:
                    allarrays.append(partarray.flatten())

            allarrays=np.concatenate(allarrays)
        else:
            allarrays = np.concatenate([curblock.current.array[curblock.current.array.mask==False].flatten() for curblock in self.myblocks.values()])

        self.nbnotnull = allarrays.count()

        return allarrays

    def updatepalette(self,which=0,onzoom=[]):
        """
        Mise à jour des palettes de couleur/colormaps

        palgray : niveaux de gris
        palblue : niveaux de bleu
        mypal   : coloration paramétrique
        """
        self.palgray = wolfpalette()
        self.palblue = wolfpalette()

        self.palgray.defaultgray()
        self.palblue.defaultblue()

        self.palgray.values[0],self.palgray.values[-1] = self.get_min_max(views_2D.TOPOGRAPHY)
        self.palblue.values[0],self.palblue.values[-1] = self.get_min_max(views_2D.WATERDEPTH)

        if self.mypal.automatic:
            self.mypal.default16()
            self.mypal.isopop(self.get_working_array(onzoom=onzoom),self.nbnotnull)

        self.link_palette()

    def delete_lists(self):
        """
        Reset des listes OpenGL de la matrice courante
        """
        for curblock in self.myblocks.values():
            curblock._current.delete_lists()

    def mimic_plotdata(self, plotting=False):
        """
        Force la mise à jour de paramètres entre tous les blocs
        """
        self.plotting=plotting
        for curblock in self.myblocks.values():
            curblock._current.plotted = self.plotted
            curblock._current.plotting = self.plotting

            curblock.set_linkedvec(self.linkedvec)
            curblock.set_epsilon(self.epsilon)

    def plot(self, sx=None, sy=None,xmin=None,ymin=None,xmax=None,ymax=None):
        """Dessin OpenGL"""
        self.mimic_plotdata(True)

        for curblock in self.myblocks.values():
            curblock.plot(sx, sy,xmin,ymin,xmax,ymax)

        if self.myparam is not None:
            #conditions limites faibles
            self.myparam.clfbx.myzones.plot()
            self.myparam.clfby.myzones.plot()

        self.mimic_plotdata(False)

    def fillonecellgrid(self,curscale,loci,locj,force=False):
        """Dessin d'une fraction de la matrice pour tous les blocs"""
        for curblock in self.myblocks.values():
            curblock._current.fillonecellgrid(curscale,loci,locj,force)

    def set_current(self,which):
        """Change le type de résultat à présenter/traiter  --> see 'views_2D' for supported values"""
        for curblock in self.myblocks.values():
            curblock.set_current(which)

    def next_result(self):
        """Lecture du pas suivant"""
        nb = self.get_nbresults()

        if self.current_result==-1:
            self.read_oneresult(-1)
        else:
            self.current_result+=1
            self.current_result = min(nb,self.current_result)
            self.read_oneresult(self.current_result)

            self.reset_plot()

    def reset_plot(self,whichpal=0):
        """Reset du dessin"""
        self.delete_lists()
        self.get_working_array()
        self.updatepalette(whichpal)
