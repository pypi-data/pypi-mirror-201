from wx import App

from .PyTranslate import _

class Element_To_Draw:
    """
    Base class of element to add into WolfMapViewer or another GUI
    """

    def __init__(self, idx:str = '', plotted:bool = True, mapviewer = None, need_for_wx:bool = False) -> None:

        self.idx = idx  # identifier
        self.xmin=0.    # spatial extension - lower left corner X
        self.ymin=0.    # spatial extension - lower left corner Y
        self.xmax=0.    # spatial extension - upper right corner X
        self.ymax=0.    # spatial extension - upper right corner Y

        self.plotted = plotted  # boolean if plotting action must be processed
        self.plotting = False   # plotting operations are underway

        self.mapviewer = mapviewer  # WolfMapViewer instance attached to the object
        self.wx_exists = App.Get() is not None  # test if wx App is running

        if need_for_wx and (not self.wx_exists):
            raise NameError(_('wx App is not running or you need it --> check your code and retry !'))

    def get_mapviewer(self):
        """
        Return the mapviewer
        """
        return self.mapviewer

    def set_mapviewer(self, newmapviewer = None):
        """
        Attach a (new) mapviewer to the object
        """
        self.mapviewer = newmapviewer

    def check_plot(self):
        """
        Generic function responding to check operation from mapviewer
        """
        self.plotted = True

    def uncheck_plot(self, unload:bool = True):
        """
        Generic function responding to uncheck operation from mapviewer
        """
        self.plotted = False

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        """
        Plot data in OpenGL context
        """
        if self.plotted:

            self.plotting = True

            # do something in OpenGL...

            self.plotting = False

    def find_minmax(self,update=False):
        """
        Generic function to find min and max spatial extent in data

        example : a WolfMapViewer instance needs spatial extent to zoom or test if
                  element must be plotted
        """

        self.xmin=0.    # spatial extension - lower left corner X
        self.ymin=0.    # spatial extension - lower left corner Y
        self.xmax=0.    # spatial extension - upper right corner X
        self.ymax=0.    # spatial extension - upper right corner Y

        pass
