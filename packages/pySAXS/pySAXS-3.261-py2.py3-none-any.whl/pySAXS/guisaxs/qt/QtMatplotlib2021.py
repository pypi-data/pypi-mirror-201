from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import colors
import matplotlib.font_manager as font_manager
from pySAXS.guisaxs import pySaxsColors
import os
import itertools
from numpy import *
from matplotlib.widgets import Cursor
import time
import os
import pySAXS
from functools import partial
from pySAXS.guisaxs.qt import matplotlibwidget
from matplotlib import style
style.use("default")
#sys.modules['matplotlibwidget']=matplotlibwidget
ICON_PATH=pySAXS.__path__[0]+os.sep+'guisaxs'+os.sep+'images'+os.sep  
class data:
    def __init__(self,x,y,label=None,id=None,error=None,color=None,selected=False,model=False):
        self.x=x
        self.y=y
        self.label=label
        self.id=id #id in the list of datas
        self.error=error
        self.color=color
        self.selected=selected
        self.model=model
        if len(x)>0:
            self.xmin=x.min()
            self.xmax=x.max()
            self.ymin=y.min()
            self.ymax=y.max()
        else:
            self.xmin=0
            self.xmax=1
            self.ymin=0
            self.ymax=1
        
        
LINLIN='xlin - ylin'
LINLOG='xlin - ylog'
LOGLIN='xlog - ylin'
LOGLOG='xlog - ylog'

class QtMatplotlib():#lQtWidgets.QMainWindow):
    def __init__(self, parent=None):
        #QtWidgets.QWidget.__init__(self, parent)
        #self.parent.ui = QtMatplotlibui.parent.ui_MainWindow()
        #self.parent.ui = uic.loadUi(pySAXS.parent.ui_PATH+"QtMatplotlib.parent.ui", self)#
        #if parent is not None:
            #print "icon"
        #    self.setWindowIcon(parent.windowIcon())
        #self.parent.ui.setupUi(self)
        #self.parent.ui.show()
        self.parent=parent
        #-------- toolbar
        self.parent.ui.navi_toolbar = NavigationToolbar(self.parent.ui.mplwidget, self.parent)
        #self.parent.ui.verticalLayout.addWidget(self.parent.ui.navi_toolbar)
        self.parent.ui.verticalLayout.insertWidget(0,self.parent.ui.navi_toolbar)
        #remove the Pan tool
        l=self.parent.ui.navi_toolbar.actions()
        for i in l:
            #print i.text()
            if i.text()=='Pan':
                panAction=i
            if i.text()=='Customize':
                customizeAction=i
            if i.text()=='Subplots':
                subplotAction=i
            
        #self.parent.ui.navi_toolbar.removeAction(panAction)
        self.parent.ui.navi_toolbar.removeAction(customizeAction)
        self.parent.ui.navi_toolbar.removeAction(subplotAction)
        #QObject::connect(myAction, SIGNAL(triggered()),this, SLOT(myActionWasTriggered()))
        
        
        
        #----- Menu plot
        #PlotButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"CurveStyle.png"),"Plot",self.parent)
        #PlotMenu=QtWidgets.QMenu()#'Curves Style',self)
        #--set grid on
        #self.actionGridON= QtWidgets.QAction('Grid ON', self)
        #self.actionGridON.triggered.connect(self.OnMenuGridOnOff)
        #PlotMenu.addAction(self.actionGridON)
        #--set legend on
        #self.setLegendON= QtWidgets.QAction('Legend ON', self)
        #self.setLegendON.triggered.connect(self.OnMenuLegendOnOff)
        #PlotMenu.addAction(self.setLegendON)
        #--set Title
        self.setTitleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'title.png'),'Set Title')#, self)'X label')#, self)
        self.setTitleAction.triggered.connect(self.OnSetTitle)
        self.parent.ui.toolBar.addAction(self.setTitleAction)
        #--set x label
        self.setXlabelAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'xlabel.png'),'Set Q label')#, self)'X label')#, self)
        self.setXlabelAction.triggered.connect(self.OnSetXLabel)
        self.parent.ui.toolBar.addAction(self.setXlabelAction)
        #--set y label
        self.setYlabelAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'ylabel.png'),'Set I label')#, self)'X label')#, self)
        self.setYlabelAction.triggered.connect(self.OnSetYLabel)
        self.parent.ui.toolBar.addAction(self.setYlabelAction)
        #--set x scale
        self.setXScaleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'xrange.png'),'Set X Scale')#, self)
        self.setXScaleAction.triggered.connect(self.OnSetXRange)
        self.parent.ui.toolBar.addAction(self.setXScaleAction)
        #--set y scale
        self.setYScaleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'yrange.png'),'Set Y Scale')#, self)
        self.setYScaleAction.triggered.connect(self.OnSetYRange)
        self.parent.ui.toolBar.addAction(self.setYScaleAction)
        
        #-- error bar   
        self.actionError_Bar= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'errorbar.png'),'display Error Bar')#, self)'X label')#, self)
        #self.setTitleAction.triggered.connect(self.OnSetTitle)
        #self.actionError_Bar = CurveStyleMenu.addAction("Error Bar")#,checkable=True)
        #self.actionError_Bar.setIcon(QtGui.QIcon(ICON_PATH+'errorbar.png'))
        #self.actionError_Bar = CurveStyleMenu.addAction(errorbarAction)#,checkable=True)
        self.parent.ui.toolBar.addAction(self.actionError_Bar)
        
        #-- error shaded
        self.actionError_Bar.setCheckable(True)
        self.actionError_Shaded =QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'errorshaded.png'),'display Error shaded')#, self)'X label')#, self)
        #self.actionError_Shaded = CurveStyleMenu.addAction("Error Shaded")#,checkable=True)
        self.parent.ui.toolBar.addAction(self.actionError_Shaded)
        #self.actionError_Shaded.setIcon(QtGui.QIcon(ICON_PATH+'errorshaded.png'))
        self.actionError_Shaded.setCheckable(True)
        
                
        #------ scale toolbar
        self.axesButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"line-chart-line.png"),"Axes",self.parent)
        #line-chart-line.png
        #self.parent.ui.navi_toolbar.addAction(self.axesButton)
        
        menuAxes = QtWidgets.QMenu()
        self.scaleList=[LINLIN,LINLOG,LOGLIN,LOGLOG]
        self.scaleDictAction={}
        self.axetype=self.scaleList[0]
        first=True
        self.scaleActionGroup = QtWidgets.QActionGroup(self.parent)#, exclusive=True)
        for item in self.scaleList:
            entry = menuAxes.addAction(item) #add in the menu, and remove the first number
            entry.setCheckable(True)
            self.scaleDictAction[item]=entry
            self.scaleActionGroup.addAction(entry)
            if first:
                entry.setChecked(True)
                self.axetype=item
            first=False
            #self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.setAxesFormat(item))
            #entry.triggered[()].connect(lambda item=item: self.setAxesFormat(item))
            entry.triggered.connect(partial(self.setAxesFormat,item))
        self.axesButton.setMenu(menuAxes)
        #self.parent.ui.navi_toolbar.addWidget(self.axesButton)
        self.parent.ui.toolBar.addWidget(self.axesButton)
        
        #------ line style  toolbar
        LineStyleButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"LineStyle.png"),"",self.parent)
        LineStyleMenu=QtWidgets.QMenu()#'Line Style',self.parent)
        actionLine = LineStyleMenu.addAction("Set Line Witdth")
        
        LineStyleMenu.addSeparator()
        
        self.marker_cycle=itertools.cycle(['.','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p','|','_'])
        self.marker_fixed=['.','-','.-','o',',','x']
        self.markerSize=5
        self.markerdict={'0No Marker':'','1Point':'.','2Circle':'o','3Diamond':'d','4Cross':'x','5Square':'s'}#need to set the menu priority
        self.linedict={'5No Line':'','1Solid':'-','2Dashed':'--','3Dash-dot':'-.','4Dotted':':'}
        #--------------- LINE FORMAT
        #self.parent.ui.actionSet_Line_Width.triggered.connect(self.OnMenuLineWidth) #change line size menu
        actionLine.triggered.connect(self.OnMenuLineWidth) #change line size menu
        
        self.lineformat='-'
        self.linewidth=1
        first=True
        self.lineActionGroup = QtWidgets.QActionGroup(self.parent)#, exclusive=True)
        sortedlist=list(self.linedict.keys())
        sortedlist.sort() #sort the menu
        for item in sortedlist:
            #entry = self.parent.ui.menuLines.addAction(item[1:]) #add in the menu, and remove the first number
            entry=LineStyleMenu.addAction(item[1:]) 
            entry.setCheckable(True)
            self.lineActionGroup.addAction(entry)
            if first:
                entry.setChecked(True)
                self.lineformat=self.linedict[item]
                #self.parent.ui.menuLines.addSeparator()
                LineStyleMenu.addSeparator()
                
            first=False
            #self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.OnPlotLineFormat(item))
            #entry.triggered.connect(lambda item=item: self.OnPlotLineFormat(item))
            #entry.triggered.connect(lambda truc=item: self.OnPlotLineFormat(truc))
            entry.triggered.connect(partial( self.OnPlotLineFormat, item))
        
        
        #---------------    MARKERS FORMAT
        MarkerMenu=QtWidgets.QMenu('Marker',self.parent)
        actionMarker = MarkerMenu.addAction("Set Marker size")
        MarkerMenu.addSeparator()
        #self.parent.ui.actionSet_marker_size.triggered.connect(self.OnMenuMarkerSize) #change marker size menu
        actionMarker.triggered.connect(self.OnMenuMarkerSize) #change marker size menu
        self.marker=''
        self.markerActionGroup = QtWidgets.QActionGroup(self.parent)#, exclusive=True)
        first=True
        sortedlist=list(self.markerdict.keys())
        sortedlist.sort()
        for item in sortedlist:
            #entry = self.parent.ui.menuMarker.addAction(item[1:])#add in the menu, and remove the first number
            entry = MarkerMenu.addAction(item[1:])#add in the menu, and remove the first number
            entry.setCheckable(True)
            self.markerActionGroup.addAction(entry)
            if first:
                entry.setChecked(True)
                self.marker=self.markerdict[item]
                first=False
                #self.parent.ui.menuMarker.addSeparator()
                MarkerMenu.addSeparator()
                #MarkerMenu
            #self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.OnPlotMarkerFormat(item))
            #entry.triggered[()].connect(lambda item=item: self.OnPlotMarkerFormat(item))
            entry.triggered.connect(partial(self.OnPlotMarkerFormat,item))
        
        
        
        #CurveStyleButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"LineStyle.png"),"Style",self.parent)
        #CurveStyleButton.setToolTip("set Line Style")
        #CurveStyleMenu=QtWidgets.QMenu()#'Curves Style',self)
        LineStyleButton.setMenu(LineStyleMenu)
        #CurveStyleMenu.addMenu(LineStyleMenu)
        #CurveStyleMenu.addMenu(MarkerMenu)
        #CurveStyleMenu.addMenu(self.plotypeMenu)
        
        
        
        #CurveStyleButton.setMenu(CurveStyleMenu)
        #self.parent.ui.navi_toolbar.addWidget(CurveStyleButton)
        #self.parent.ui.toolBar.addWidget(CurveStyleButton)
        self.parent.ui.toolBar.addWidget(LineStyleButton)
        
        MarkerStyleButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"markerStyle2.png"),"",self.parent)
        MarkerStyleButton.setToolTip("set Marker Style")
        MarkerStyleButton.setMenu(MarkerMenu)
        self.parent.ui.toolBar.addWidget(MarkerStyleButton)
        
        #---------------   xy type of plot
        self.plotexp=0 #x vs y
        self.plotlist=['Normal','I.Q','I.Q^2','I.Q^3','I.Q^4']
        PlotMenuButton=QtWidgets.QPushButton(QtGui.QIcon(ICON_PATH+"IQn.png"),"IQ exp",self.parent)
        #PlotMenuButton.setToolButtonStyle()
        PlotMenuButton.setToolTip("I.Q exp")
        self.plotypeMenu=QtWidgets.QMenu('IQ exp',self.parent)
        
        self.plotypeActionGroup = QtWidgets.QActionGroup(self.parent)#, exclusive=True)
        
        for item in range(len(self.plotlist)):
            entry = self.plotypeMenu.addAction(self.plotlist[item])
            entry.setCheckable(True)
            self.plotypeActionGroup.addAction(entry)
            if item==0:
                entry.setChecked(True)
                self.plotexp=item
            #self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.OnPlotType(item))
            #entry.triggered[()].connect(lambda item=item: self.OnPlotType(item))
            entry.triggered.connect(partial(self.OnPlotType,item))
        PlotMenuButton.setMenu(self.plotypeMenu)
        #self.parent.ui.navi_toolbar.addWidget(PlotMenuButton)
        self.parent.ui.toolBar.addWidget(PlotMenuButton)
        
        
        
        
        #--grid button
        self.GridAction = QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'grid.png'), 'Grid On/Off', self.parent)
        self.GridAction.setCheckable(True)
        self.GridAction.setChecked(True)
        self.GridAction.triggered.connect(self.OnButtonGridOnOff)
        self.parent.ui.navi_toolbar.addAction(self.GridAction)
        
        #--Legend
        self.LegendAction = QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'legend.png'), 'Legend On/Off', self.parent)
        self.LegendAction.setCheckable(True)
        self.LegendAction.setChecked(True)
        self.LegendAction.triggered.connect(self.OnButtonLegendOnOff)
        self.parent.ui.navi_toolbar.addAction(self.LegendAction)
        #--Autoscale
        self.AutoscaleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'AutoScale.png'),'Autoscale', self.parent)
        self.AutoscaleAction.triggered.connect(self.OnAutoscale)
        self.parent.ui.navi_toolbar.addAction(self.AutoscaleAction)
        #-- fix scale
        self.FixScaleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'magnet.png'),'Fix Scale', self.parent)
        self.FixScaleAction.setCheckable(True)
        self.FixScaleAction.setChecked(False)
        self.FixScaleAction.triggered.connect(self.OnButtonFixScale)
        self.parent.ui.navi_toolbar.addAction(self.FixScaleAction)
        
        
        '''self.scaleList=[LINLIN,LINLOG,LOGLIN,LOGLOG]
        self.scaleDictAction={}
        self.axetype=self.scaleList[0]
        first=True
        self.scaleActionGroup = QtWidgets.QActionGroup(self.parent)#, exclusive=True)
        for item in self.scaleList:
            entry = self.parent.ui.menuAxes.addAction(item) #add in the menu, and remove the first number
            entry.setCheckable(True)
            self.scaleDictAction[item]=entry
            self.scaleActionGroup.addAction(entry)
            if first:
                entry.setChecked(True)
                self.axetype=item
            first=False
            #self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.setAxesFormat(item))
            #entry.triggered[()].connect(lambda item=item: self.setAxesFormat(item))
            entry.triggered.connect(partial(self.setAxesFormat,item))'''
        #---------------    
        
        
        #QtCore.QObject.connect(self.parent.ui.actionGridON,QtCore.SIGNAL("triggered()"),self.OnMenuGridOnOff)
        #self.parent.ui.actionGridON.triggered.connect(self.OnMenuGridOnOff)
        #QtCore.QObject.connect(self.parent.ui.actionLegend_ON,QtCore.SIGNAL("triggered()"),self.OnMenuLegendOnOff)
        #self.parent.ui.actionLegend_ON.triggered.connect(self.OnMenuLegendOnOff)
        #QtCore.QObject.connect(self.parent.ui.actionError_Bar,QtCore.SIGNAL("triggered()"),self.OnMenuErrorOnOff)
        #self.parent.ui.actionError_Bar.triggered.connect(self.OnMenuErrorOnOff)
        #self.parent.ui.actionError_Shaded.triggered.connect(self.OnMenuErrorShadedOnOff)
        self.actionError_Bar.triggered.connect(self.OnMenuErrorOnOff)
        self.actionError_Shaded.triggered.connect(self.OnMenuErrorShadedOnOff)
        '''self.parent.ui.actionSave_As.triggered.connect(self.OnMenuFileSaveAs)
        self.parent.ui.actionAutoscaling.triggered.connect(self.OnAutoscale)
        self.parent.ui.actionSet_X_range.triggered.connect(self.OnSetXRange)
        self.parent.ui.actionSet_Y_range.triggered.connect(self.OnSetYRange)
        self.parent.ui.actionSetTitle.triggered.connect(self.OnSetTitle)
        self.parent.ui.actionX_label.triggered.connect(self.OnSetXLabel)
        self.parent.ui.actionY_label.triggered.connect(self.OnSetYLabel)
        self.parent.ui.actionClassic.triggered.connect(self.OnSetClassic)
        self.parent.ui.actionSeaborn.triggered.connect(self.OnSetSeaborn)
        self.parent.ui.actionWhite.triggered.connect(self.OnSetWhite)'''
                                                 
        
        self.datalist=[]#list of datas
        self.linelist=[]#list of lines
        self.gridON=True
        self.legendON=True
        self.colors=pySaxsColors.pySaxsColors()
        self.errbar=False
        self.errshaded=False
        #self.parent.ui.actionError_Bar.setChecked(self.errbar)
        #self.parent.ui.actionError_Shaded.setChecked(self.errshaded)
        self.actionError_Bar.setChecked(self.errbar)
        self.actionError_Shaded.setChecked(self.errshaded)
        
        
        self.styleWhite=False
        
        self.ylabel=""
        self.xlabel=""
        self.title=""
        
        
        self.plt=self.parent.ui.mplwidget.figure
        #self.plt.patch.set_facecolor('White')
        self.canvas = FigureCanvas(self.plt)
        self.canvas.mpl_connect('motion_notify_event', self.OnClickOnFigure)
        self.axes = self.plt.gca()
        try:
            self.axes.hold(True)
        except:
            #no more supported ? jan 2019
            pass
        self.replot()
                
    
    def closeEvent(self, event):
        #self.emit(QtCore.SIGNAL('closing()'))
        #self.closing.emit()
        self.close()
        #print "closing"
           
    def close_event(self):
        print("close event")
    
    
    def OnClickOnFigure(self):
        print('on click')
    
    def OnMenuFileSaveAs(self):
        """
        Handles File->Save menu events.
        """
        #-- open dialog for parameters
        fd = QtWidgets.QFileDialog(self)
        #get the filenames, and the filter
        wc = "Portable Network Graphics (*.png);;Scalable Vector Graphics SVG (*.svg);;Encapsulated Postscript (*.eps);;All files (*.*)"
        filename=fd.getSaveFileName (filter=wc)#,directory=self.workingdirectory)[0]
        filename=str(filename)
        #self.setWorkingDirectory(filename) #set working dir
        if  filename=="":
            return

        path, ext = os.path.splitext(filename)
        ext = ext[1:].lower()

        if ext != 'png' and ext != 'eps' and ext!='svg':
            error_message = 'Only the PNG,SVG and EPS image formats are supported.\n'+ 'A file extension of \'png\', \'svg\' or \'eps\' must be used.'
            QtWidgets.QMessageBox.critical(self,'Error', error_message, buttons=QtWidgets.QMessageBox.Ok)
            return

        try:
            
            self.plt.savefig(filename)
        except IOError as e:
            if e.strerror:
                err = e.strerror
            else:
                err = e

            error_message ='Could not save file: ' +str(err)
            QtWidgets.QMessageBox.critical(self,'Error', error_message, buttons=QtWidgets.QMessageBox.Ok)    
    
    def setAxesFormat(self,axeformat=LINLIN,changeMenu=False):
        '''
        change the Axes format (lin-lin, log-log,...)
        '''
        self.axetype=axeformat
        self.replot()
        if changeMenu:
            if axeformat in self.scaleDictAction:
                self.scaleDictAction[axeformat].setChecked(True)
        
    
    def OnButtonFixScale(self):
        #memorize the current scale"
        self.xlim_min,self.xlim_max=self.axes.get_xlim()
        self.ylim_min,self.ylim_max=self.axes.get_ylim()
        #print self.xlim_min,self.xlim_max," - ",self.ylim_min,self.ylim_max
        
    
    def OnMenuMarkerSize(self):
        '''
        user want to change the marker size
        '''
       
        size, ok=QtWidgets.QInputDialog.getInt(self.parent, "Marker size", "specify the marker size", value=self.markerSize, min=0, max=20, step=1)
        if ok:
            self.markerSize=size
            self.replot()
    
    def OnMenuLineWidth(self):
        '''
        user want to change the line width
        '''
       
        width, ok=QtWidgets.QInputDialog.getInt(self.parent, "Line Width", "specify the line width", value=self.linewidth, min=0, max=20, step=1)
        if ok:
            self.linewidth=width
            self.replot()
        
    #QtCore.pyqtSlot()
    def OnPlotLineFormat(self,item,val):
        try:
            self.lineformat=self.linedict[item]
            self.replot()
        except:
            pass
    
    def OnPlotMarkerFormat(self, item,val):
        self.marker=self.markerdict[item]
        self.replot()
    
    def OnPlotType(self,item,val):
        '''
        user changed the plotexp
        '''
        #print item
        self.plotexp=item
        self.replot()
        

    def plotData(self, d,bold=None):
        """
        plot the datas
        """
        #which color ?
        col = self.colors.getColor(d.id) #get a new color
        if d.color is not None:
            col = d.color
    #print d.label,d.y,d.color
        linewidth = self.linewidth
        if d.selected:
            linewidth += 1
        if bold:
            linewidth += 2
        linestyle = self.get_linestyle()
        #if d.model :
        #print(d.model)
        if d.model :
            #print("model %s"%d.label)
            linestyle='--'
    
        l = None
        if d.error is not None:
            if self.errbar:
            #print "with errorbar"
                d.error = abs(d.error)
                if d.id is not None:
                    #print("ID : "+str(d.id))
                    l = self.axes.errorbar(d.x, d.y * (d.x ** self.plotexp), yerr=d.error * (d.y ** self.plotexp), 
                        linestyle=linestyle, 
                        marker=self.get_marker(), 
                        linewidth=linewidth, 
                        #ecolor='b',\
                        antialiased=True, 
                        label=d.label, 
                        markersize=self.markerSize, 
                        color=col) #,label=d.label,markersize=5,fmt=None)
                else:
                    print("ID is None ")
                    l = self.axes.errorbar(d.x, d.y * (d.x ** self.plotexp), yerr=d.error, 
                        linestyle=linestyle, 
                        marker=self.get_marker(), 
                        linewidth=linewidth, 
                        label=d.label, 
                        markersize=self.markerSize, 
                        color=col) #,label=d.label,markersize=5,fmt=None)
                    #print d.x,d.y
            if self.errshaded:
                l = self.axes.plot(d.x, d.y * (d.x ** self.plotexp), 
                    linestyle=linestyle, 
                    marker=self.get_marker(), 
                    linewidth=linewidth, 
                        #ecolor='b',\
                    antialiased=True, 
                    label=d.label, markersize=self.markerSize, color=col) #,label=d.label,markersize=5,fmt=None)
                d.error = abs(d.error)
                ok = where(d.y > d.error)
                self.axes.fill_between(d.x[ok], 
                    d.y[ok] * (d.x[ok] ** self.plotexp) - d.error[ok] * (d.x[ok] ** self.plotexp), 
                    d.y[ok] * (d.x[ok] ** self.plotexp) + d.error[ok] * (d.x[ok] ** self.plotexp), 
                    alpha=0.2, edgecolor=col, facecolor=col, antialiased=True)
            if (not self.errshaded) and (not self.errbar):
                l = self.axes.plot(d.x, d.y * (d.x ** self.plotexp), 
                    linestyle=linestyle, 
                    marker=self.get_marker(), 
                    linewidth=linewidth, 
                #ecolor='b',\
                    antialiased=True, 
                    label=d.label, markersize=self.markerSize, color=col) #,label=d.label,markersize=5,fmt=None)
        elif col is not None:
            l, = self.axes.plot(d.x, d.y * (d.x ** self.plotexp), 
                linestyle=linestyle, 
                marker=self.get_marker(), 
                label=d.label, 
                linewidth=linewidth, 
                color=col, 
                markersize=self.markerSize)
        else:
            l, = self.axes.plot(d.x, d.y * (d.x ** self.plotexp), 
                linestyle=linestyle, 
                marker=self.get_marker(), 
                label=d.label, markersize=self.markerSize, linewidth=linewidth) #print "plot"
        self.linelist.append(l)

    def replot(self,currentItem=None):
        #print("on replot")
        #t0=time.time()
        
        
        #keep in memory the options
        self.xlim_min,self.xlim_max=self.axes.get_xlim()
        self.ylim_min,self.ylim_max=self.axes.get_ylim()
        
        xlabel=self.axes.get_xlabel()
        ylabel=self.axes.get_ylabel()
        #self.title=self.axes.get_title()
        #print self.title
        
        #clear axes --> lose all the axes options
        self.axes.cla() 
        
        #--- fix scale
        if self.FixScaleAction.isChecked():
            #axes limits should have been memorized
            self.axes.set_xlim((self.xlim_min,self.xlim_max))
            self.axes.set_ylim((self.ylim_min,self.ylim_max))
        self.linelist=[]
        currentItemPos=None
        for d in self.datalist:
            if d.label == currentItem:
                currentItemPos=d
            else:
                self.plotData(d)
            
            
        if currentItemPos is not None:
                #print("trying to bold %s"%currentItem)
                self.plotData(currentItemPos,bold=True)
        #--scale
        if self.axetype==LOGLOG:
            self.axes.set_xscale('log')
            self.axes.set_yscale('log')
        if self.axetype==LOGLIN:
            self.axes.set_xscale('log')
            self.axes.set_yscale('linear')
        if self.axetype==LINLOG:
            self.axes.set_xscale('linear')
            self.axes.set_yscale('log')
        if self.axetype==LINLIN:
            self.axes.set_xscale('linear')
            self.axes.set_yscale('linear')
        
        #--legend    
        if self.legendON:
            font=font_manager.FontProperties(style='italic',size='x-small')
            leg=self.axes.legend(loc='upper right',prop=font)
            #leg.get_frame().set_alpha(0.5)
        else:
            self.axes.legend_ = None
            
         #--grid
        #print self.gridON
        self.axes.get_xaxis().grid(self.gridON)
        self.axes.get_yaxis().grid(self.gridON)
        
        #-- x and y label
        self.setScaleLabels(xlabel, ylabel)
        #self.setTitle(self.title)
        if self.title !="":
            self.axes.set_title(self.title)
        if self.styleWhite:
            self.axes.set_facecolor("w")
        else:
            self.axes.set_facecolor("#EBEBF2")
        
        self.draw('r')
        
    def OnScale(self):
        #check which scale
        #self.scaleActionGroup.actions()
        wscale=[self.parent.ui.actionXlin_ylin,self.parent.ui.actionXlog_ylin,self.parent.ui.actionXlin_ylog,self.parent.ui.actionXlog_ylog]
        scaletype=[4,2,3,1]
        #print "on scale"
        for i in range(len(wscale)):
            s=wscale[i]
            if s.isChecked():
                self.axetype=scaletype[i]
        self.replot()
            
    
    def OnMenuGridOnOff(self):
        #self.gridON=self.actionGridON.isChecked()
        #self.GridAction.setChecked(self.gridON)
        #self.replot()
        pass
    
    def OnButtonGridOnOff(self):
        self.gridON=self.GridAction.isChecked()
        #self.actionGridON.setChecked(self.gridON)
        self.replot()
        
    def OnMenuLegendOnOff(self):
        #self.legendON=self.parent.ui.actionLegend_ON.isChecked()
        #self.LegendAction.setChecked(self.legendON)
        #self.replot()
        pass
    
    def OnButtonLegendOnOff(self):
        self.legendON=self.LegendAction.isChecked()
        #self.parent.ui.actionLegend_ON.setChecked(self.legendON)
        self.replot()
        
    def OnMenuErrorOnOff(self):
        #print('error on/off')
        self.errbar=self.actionError_Bar.isChecked()
        self.replot()
    
    def OnMenuErrorShadedOnOff(self):
        self.errshaded=self.actionError_Shaded.isChecked()
        self.replot()
        
    def OnAutoscale(self):
        '''
        user click on autoscale
        '''
        if len(self.datalist)>0:
            self.xlim_min,self.ylim_min,self.xlim_max,self.ylim_max=self.getXYminMax()
            #print self.xlim_min,self.ylim_min,self.xlim_max,self.ylim_max
            self.axes.set_xlim((self.xlim_min,self.xlim_max))
            self.axes.set_ylim((self.ylim_min,self.ylim_max))
        self.replot()
        

    def addData(self,x,y,label=None,id=None,error=None,color=None,model=False):
        ''' datas to the plot
        x and y are datas
        label : the name of datas
        id : no of datas in a list -> give the colors
        '''
        if id is None:
            id=len(self.datalist)
        
        newdata=data(x,y,label,id,error,color=color,model=model)
        self.datalist.append(newdata)
        return id
    
    def changeData(self,x,y,id,label=None,error=None,color=None,model=False):
        self.datalist[id]=data(x,y,label,id,error,color=color,model=model)
        
    def changeDataAndUpdate(self,x,y,id):
        self.changeData(x, y, id)
        self.linelist[id].set_ydata(y)
        self.linelist[id].set_xdata(x)
        self.draw('c')
        
    
    def clearData(self):
        self.datalist=[]
        
    def get_marker(self):
        """ Return an infinite, cycling iterator over the available marker symbols.
        or a fixed marker symbol
        """
        return self.marker#+self.lineformat
        '''#--line style
        if self.linetype<=5:
            #predifined marker
            lstyle=self.marker_fixed[self.linetype]
            #print lstyle
            return lstyle
        else:
            #automatic marker
            return self.marker_cycle.next()+'-'
        '''
    def set_marker(self,marker='.'):
       '''
       change the curve marker
       '''
       self.marker=marker
       
       
    def get_linestyle(self):
        return self.lineformat

    def OnSetXRange(self):
        '''
        user clicked on set x range
        '''
        self.axes = self.plt.gca()
        #self.axes.hold(False)
        self.xlim_min,self.xlim_max=self.axes.get_xlim()
        xlim, ok=QtWidgets.QInputDialog.getDouble(self.parent, "Setting X scale", "x min :", value=self.xlim_min,decimals=6)
        if ok:
            self.xlim_min=xlim
            self.axes.set_xlim((self.xlim_min,self.xlim_max))
            self.FixScaleAction.setChecked(True)
            self.replot()
        xlim, ok=QtWidgets.QInputDialog.getDouble(self.parent, "Setting X scale", "x max :", value=self.xlim_max,decimals=6)
        if ok:
            self.xlim_max=xlim
            self.axes.set_xlim((self.xlim_min,self.xlim_max))
            self.FixScaleAction.setChecked(True)
            self.replot()
            
    def OnSetYRange(self):
        '''
        user clicked on set y range
        '''
        self.axes = self.plt.gca()
        self.ylim_min,self.ylim_max=self.axes.get_ylim()
        ylim, ok=QtWidgets.QInputDialog.getDouble(self.parent, "Setting Y scale", "y min :", value=self.ylim_min,decimals=6)
        if ok:
            self.ylim_min=ylim
            self.axes.set_ylim((self.ylim_min,self.ylim_max))
            self.FixScaleAction.setChecked(True)
            self.replot()
        ylim, ok=QtWidgets.QInputDialog.getDouble(self.parent, "Setting Y scale", "y max :", value=self.ylim_max,decimals=6)
        if ok:
            self.ylim_max=ylim
            self.axes.set_ylim((self.ylim_min,self.ylim_max))
            self.FixScaleAction.setChecked(True)
            self.replot()
    
    def OnSetTitle(self):
        title, ok=QtWidgets.QInputDialog.getText(self.parent, "Setting Graph Title", "title :", text=self.title)
        if ok:
            print('set title %s'%title)
            self.title=title
            #self.axes.set_title(title)
            self.replot()
    
    def OnSetXLabel(self):
        
        label, ok=QtWidgets.QInputDialog.getText(self.parent, "Setting X label", "label :", text=self.xlabel)
        if ok:
            self.setScaleLabels(label)
            self.replot()
    
    def OnSetYLabel(self):
        label, ok=QtWidgets.QInputDialog.getText(self.parent, "Setting Y label", "label :", text=self.ylabel)
        if ok:
            self.setScaleLabels(xlabel=None,ylabel=label)
            self.replot()
    
    '''def setTitle(self,title):
        if title!=self.title:
            self.title=title
            self.axes.set_title(title)
            self.draw('t')
    '''

    def setScaleLabels(self,xlabel=None,ylabel=None,size=None):
        #print "set scale"
        self.axes = self.plt.gca()
        if xlabel is not None :
            if xlabel!=self.axes.get_xlabel():
                self.axes.set_xlabel(xlabel)
                self.xlabel=xlabel
                if size is not None:
                    self.axes.set_xlabel(xlabel,fontsize=size,labelpad=-2)
        if ylabel is not None :
            if ylabel!=self.axes.get_ylabel():
                self.axes.set_ylabel(ylabel)
                self.ylabel=ylabel
                if size is not None:
                    self.axes.set_ylabel(ylabel,fontsize=size)
                    
    def annotate(self,x,y,text):
        #print "annotate ",text, " at ",x,y
        #self.axes = self.plt.gca()
        #self.axes.hold(False)
        self.axes.annotate(text, xy=(x, y),  xycoords='data',\
                                            xytext=(20, 20), textcoords='offset points', \
                                            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=10"),\
                                            fontsize=10,)
        self.draw('a')
    
    def text(self,x=0.5,y=0.5,text='test'):
        self.axes.text(x,y,text,transform = self.axes.transAxes,bbox=dict(boxstyle='square',facecolor='gray', alpha=0.5))
        self.draw('tt')
        
    def draw(self,text=''):
        '''
        draw the plot
        text is here for tracking
        '''
        #print 'draw ',text
        #if text is '' : do not draw
        if text!='':
            self.parent.ui.mplwidget.draw()
        
        
    
    def getXYminMax(self):
        '''
        return xmin,ymin,xmax,ymax on all the datas
        '''
        xminlist=[]
        xmaxlist=[]
        yminlist=[]
        ymaxlist=[]
        for d in self.datalist:
            xminlist.append(d.xmin)
            xmaxlist.append(d.xmax)
            yminlist.append(d.ymin)
            ymaxlist.append(d.ymax)
        return min(xminlist),min(yminlist),max(xmaxlist),max(ymaxlist) 
    
    def getAxes(self):
        return self.axes
    
    def getFig(self):
        return self.plt
    
    def changeFaceColor(self,color='None'):
        self.plt.patch.set_facecolor(color)
        
    def OnSetClassic(self):
        style.use("default")
        self.styleWhite=False
        self.replot()
        
    def OnSetSeaborn(self):
        style.use("seaborn")
        self.styleWhite=False
        self.replot()
    
    def OnSetWhite(self):
        style.use("default")
        self.plt.patch.set_facecolor('White')
        self.styleWhite=True
        self.replot()
        

if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)
      myapp = QtMatplotlib()
      myapp.show()
      from pySAXS.models import Gaussian

      modl=Gaussian()
      x=modl.q
      y=modl.getIntensity()
      err=ones(shape(x))#random.rand(len(x))/10
      #err=err*y
      #print err
      myapp.addData(x, y, label='gaussian',error=err)
      myapp.addData(x, -y*1.51, label='gaussian2',error=err)
      i=myapp.addData(x, y*2, label='gaussian3',error=err)
      myapp.replot()
      myapp.setScaleLabels('$q(\AA^{-1})$', "I",15)
      myapp.setAxesFormat(LINLIN)
      myapp.setTitle('DEMO')
      myapp.annotate(1.0, 1.0, "text")
      myapp.annotate(1.0, 20.0, "text")
      myapp.annotate(-2.0, 1.0, "text")
      myapp.text(0.05,0.05,"test of text\nldqksj\ndlqks\nklfqlkjf\nqsdqs qsd\nqsd qsd")
      sys.exit(app.exec_())
