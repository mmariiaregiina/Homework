from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds 
import os
import json


ROOT = str(os.path.dirname(__file__))

class MyMimeData(QtCore.QMimeData):
  
    def __init__(self):
        super(MyMimeData, self).__init__()

        self.tool = None


class WidgetButton(QtWidgets.QWidget):
    """
    A class of WidgetButton
    """
    def __init__(self, label = "TEST"):
        super(WidgetButton, self).__init__()

        self.setMinimumHeight(40)

        # background color:
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(80, 80, 80))
        self.setPalette(self.p)

        # main layout:
        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_layout.setSpacing(1)
        self.m_layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.m_layout)

        # label:
        self.label = QtWidgets.QLabel(label)
        self.m_layout.addWidget(self.label)
        self.m_layout.setAlignment(QtCore.Qt.AlignCenter) # center alignment

    def set_label(self, text):
        self.label.setText(text)

    def mousePressEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton: 
            return   
            
        mimeData = MyMimeData()
        mimeData.tool = self.label.text()

        # creation of ghosty image behind the moving mouse cursor:
        self.pixmap = self.grab()
        painter = QtGui.QPainter(self.pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 127))
        painter.end()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(event.pos())
        
        drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)


class WidgetField(QtWidgets.QWidget):
    """
    A class of Field Widget that accepts drops
    """
    def __init__(self):
        super(WidgetField, self).__init__()

        self.setFixedSize(240, 490)
        self.setAcceptDrops(True)

        # background color:
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(40, 40, 40))
        self.setPalette(self.p)

        # main layout:
        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.m_layout)

        # scroll area:
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus) 
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(8, 8, 8, 8)
        self.scroll_layout.setSpacing(5)
        self.scroll_area_widget.setLayout(self.scroll_layout)
        
        self.m_layout.addWidget(self.scroll_area)
        
    def dropEvent(self, event):
        mimeData = event.mimeData()
        label = mimeData.tool
        self.label = WidgetButton(label=label)
        self.scroll_layout.addWidget(self.label)    
        event.source().deleteLater()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()


    def create_widget(self, label):
        button = WidgetButton(label=label)
        self.scroll_layout.addWidget(button)


class MyDialog(QtWidgets.QDialog):
    """
    creates a window to choose set of functions
    """
    updateList = QtCore.Signal(bool)
    def __init__(self, classList = []):
        super(MyDialog, self).__init__()
        self.classList = classList
        
        self.setObjectName("My_setsUI")
        self.setWindowTitle("MY SET OF FUNCTIONS")
        self.setFixedSize(500, 570)
        
        # background color:
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 255))
        self.setPalette(self.p)

        self.createUI()
        self.read_JSON()

    def createUI(self):

        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.m_layout)

        self.widget_layout = QtWidgets.QHBoxLayout()
        self.m_layout.addLayout(self.widget_layout)

        self.widget_1 = WidgetField()
       
        self.widget_2 = WidgetField()
        self.widget_layout.addWidget(self.widget_1)
        self.widget_layout.addWidget(self.widget_2)

        # button to save functions for dock widget:
        self.button_s = QtWidgets.QPushButton("SAVE")
        self.button_s.clicked.connect(self.save_JSON)
        self.m_layout.addWidget(self.button_s)

    def read_JSON(self):
        json_file_path = os.path.join(ROOT,"chosen_tools.json")
        json_data = []
        if os.path.isfile(json_file_path):
            
            with open (json_file_path, 'r') as f:
                json_data = json.load(f)

        for tool in self.classList:
            if tool in json_data:
                self.widget_2.create_widget(label=tool)
            else:
                self.widget_1.create_widget(label=tool)

    def save_JSON(self):

        list_of_funcs = []
      
        if self.widget_2.scroll_layout.count():
            for i in range(self.widget_2.scroll_layout.count()):
                item = self.widget_2.scroll_layout.itemAt(i)
                widget = item.widget()

                label = widget.label.text()

                list_of_funcs.append(label)

        json_file_path = os.path.join(ROOT,"chosen_tools.json")          

        with open(json_file_path,'w') as outfile:
            outfile.write(json.dumps(list_of_funcs, indent=4, sort_keys=True)) 

        self.updateList.emit(True)
        self.close()