from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds 
import maya.mel as mel
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from sets_Window import MyDialog
import os 
import json


class Basic_Tool(QtWidgets.QWidget):
  
    def __init__(self, label = "TEST"):
        super(Basic_Tool, self).__init__()

        self.setMinimumHeight(80)

        # background color:
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(120, 120, 120))
        self.setPalette(self.p)

        # main layout:
        self.m_layout = QtWidgets.QHBoxLayout()
        self.m_layout.setSpacing(1)
        self.m_layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.m_layout)

        # label:
        self.label = QtWidgets.QLabel(label)
        self.label.setFont(QtGui.QFont("Arial", 10))
        self.m_layout.addWidget(self.label)
        self.m_layout.setAlignment(QtCore.Qt.AlignCenter)


    def mousePressEvent(self, event):
        print ("The function is accomplished")
       
# CLASSES OF TOOLS A, B, C, D:

class Channel_Filter(Basic_Tool):
  
    def __init__(self, label = "Channel_Filter"):
        super(Channel_Filter, self).__init__(label = label)

    def mousePressEvent(self, event):
        mel.eval("filterUISelectAttributes graphEditor1OutlineEd")
        super(Channel_Filter, self).mousePressEvent(event)


class Graph_Editor(Basic_Tool):
  
    def __init__(self, label = "Graph_Editor"):
        super(Graph_Editor, self).__init__(label = label)

    def mousePressEvent(self, event):
        a = 'graphEditor1Window'
        if cmds.window(a, exists=True):
            cmds.deleteUI(a)
        else:
            cmds.GraphEditor()
        super(Graph_Editor, self).mousePressEvent(event)


class Motion_Trail(Basic_Tool):
  
    def __init__(self, label = "Motion_Trail"):
        super(Motion_Trail, self).__init__(label = label)

    def mousePressEvent(self, event):
       
        if cmds.objExists("My_MTHandle"):
            cmds.delete("My_MTHandle")
        else:
            start_time = cmds.playbackOptions(query=True, min=True)
            end_time = cmds.playbackOptions(query=True, max=True)
            my_trail = cmds.snapshot(motionTrail=1, increment=1, startTime=start_time, endTime=end_time, n="My_MT")
            cmds.setAttr(my_trail[0] + "Shape.trailColor", 0.49, 0, 0.0337529, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.trailColor", 1, 0, 0.0688834, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.extraTrailColor", 0.0337529, 0, 0.49, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.extraTrailColor", 0.0688834, 0, 1, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.showFrameMarkers", 1)
            cmds.setAttr(my_trail[0] + "Shape.frameMarkerColor", 0.0550512, 0.553, 0, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.frameMarkerColor", 0.09955, 1, 0, type='double3')
            cmds.setAttr(my_trail[0] + "Shape.frameMarkerSize", 5)

        super(Motion_Trail, self).mousePressEvent(event)

  
class Create_LOC(Basic_Tool):
  
    def __init__(self, label = "Create_LOC"):
        super(Create_LOC, self).__init__(label = label)

    def mousePressEvent(self, event):
        cmds.spaceLocator( p=(10, 10, 10) )
        super(Create_LOC, self).mousePressEvent(event)


LIST = ["Channel_Filter", "Graph_Editor", "Motion_Trail", "Create_LOC"]
ROOT = str(os.path.dirname(__file__))


class DockWidget(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):
    """
    creates a dock widget
    """
    def __init__(self):

        super(DockWidget,self).__init__()

        self.setObjectName("My_ToolsID")

        self.setupUI()
        self.read_JSON()

    def setupUI(self):

        #self.setMinimumWidth(100)
        #self.setMinimumHeight(100)
        self.setWindowTitle("MY TOOLS")
        self.setFont(QtGui.QFont("Arial", 10))
        self.setDockableParameters(widht = 200)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setSpacing(1)
        self.main_layout.setContentsMargins(15, 5, 5, 15)
        self.main_widget = QtWidgets.QWidget()
        self.setWidget(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        
        # scroll layout:
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus) 
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(20)
        self.scroll_area_widget.setLayout(self.scroll_layout)
        
        self.main_layout.addWidget(self.scroll_area)

        # button to open additional window: 
        self.button = QtWidgets.QPushButton("OPTIONS")
        self.button.setFont(QtGui.QFont("Arial", 10))
        self.button.clicked.connect(self.openSets)
        self.main_layout.addWidget(self.button)

    def read_JSON(self):
         # delete widgets:
         if self.scroll_layout.count():
            for i in range(self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                widget = item.widget()
                widget.deleteLater()

         json_file_path = os.path.join(ROOT,"chosen_tools.json")
         json_data = []
         if os.path.isfile(json_file_path):
            
            with open (json_file_path, 'r') as f:
                json_data = json.load(f)

         for tool in json_data:
            # exec("button = {}()".format(tool))
            # self.scroll_layout.addWidget(button)
            button_class = globals().get(tool, None)
            if button_class:
                btn = button_class(label=tool)
                self.scroll_layout.addWidget(btn)
                
      
    def openSets(self):
        if cmds.window("My_setsUI", query=1, exists=1):
            cmds.deleteUI("My_setsUI")
        if cmds.windowPref("My_setsUI", exists=1):
            cmds.windowPref("My_setsUI", remove=1)
         
        self.mySets = MyDialog(classList = LIST)
        self.mySets.updateList.connect(self.read_JSON)
        self.mySets.show() 
         

def main():
    
    if cmds.workspaceControl('My_ToolsIDWorkspaceControl', exists=True):
        cmds.deleteUI('My_ToolsIDWorkspaceControl', control = True)
        
    if cmds.workspaceControlState('My_ToolsIDrWorkspaceControl', exists=True):
        cmds.workspaceControlState('My_ToolsIDWorkspaceControl', remove=1)
        
    myUI = DockWidget()
    myUI.show(dockable = True, area='right', allowedArea='right', floating=True)
    
    cmds.workspaceControl('My_ToolsIDWorkspaceControl',
                            label = 'SceneChecker',
                            edit = 1,
                            tabToControl = ['AttributeEditor', 0], # -1 adds widget to the bottom
                            widthProperty = 'fixed',
                            initialWidth = 400)

main()