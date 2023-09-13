
import maya.cmds as cmds 
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin 


class MySetWidget(MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self):
        super(MySetWidget, self).__init__()

        self.createUI()
        self.selection()
      
        # context menu: 
        self.popMenu = QtWidgets.QMenu(self)
        self.popMenu.setStyleSheet("background-color:rgb(50, 108, 131);")

        self.popMenuAdd = QtWidgets.QAction('Add object', self)
        self.popMenu.addAction(self.popMenuAdd)
        self.popMenuAdd.triggered.connect(self.add_object)

        # separator:
        self.separator = QtWidgets.QAction(self)
        self.separator.setSeparator(True)
        self.popMenu.addAction(self.separator) 

        self.popMenuDel = QtWidgets.QAction('Remove object', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.remove_object)   

        # separator:
        self.separator = QtWidgets.QAction(self)
        self.separator.setSeparator(True)
        self.popMenu.addAction(self.separator) 

        # separator:
        self.separator = QtWidgets.QAction(self)
        self.separator.setSeparator(True)
        self.popMenu.addAction(self.separator)  

        self.popMenuDel = QtWidgets.QAction('Select objects', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.sel_objects) 

        # separator:
        self.separator = QtWidgets.QAction(self)
        self.separator.setSeparator(True)
        self.popMenu.addAction(self.separator) 

        self.popMenuDel = QtWidgets.QAction('Delete set', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.del_set) 
       
        self.setMouseTracking(True)  
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def selection(self):
        self.selection = cmds.ls(selection=1, long=1) 
        cmds.listRelatives(self.selection, parent=1) 
    

    def createUI(self):
        self.wgt_Layout = QtWidgets.QHBoxLayout() 
        self.setLayout(self.wgt_Layout)
        self.label = QtWidgets.QLabel() 
        self.wgt_Layout.addWidget(self.label)

        # color for sets (wgt_Layout):
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(50, 108, 131))
        self.setPalette(self.p)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            cmds.select(self.selection)
        
        elif event.button() == QtCore.Qt.RightButton:
            self.context()

    # functions for context menu:
    def onContextMenu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    def add_object(self):
        selection = cmds.ls(selection=1, long=1)
        self.selection.extend(selection)

    def remove_object(self):
        selection = cmds.ls(selection=1, long=1)
        for i in selection:
            self.selection.remove(i)

    def sel_objects(self):
        cmds.select(self.selection)

    def del_set(self):
        self.deleteLater()

   



class MyWindow(MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.checkUI()
        self.createUI()
 

    def createUI(self):
        '''
        The functions creates UI and buttons "plus", "delete"
        '''
        self.setObjectName("MyTool")
        self.setWindowTitle("Selection Tool")
        self.setMinimumSize(500, 500)
        self.setMaximumSize(700, 1000)
        self.resize(500,500)
        
        # set main_Layout:
        self.main_Layout = QtWidgets.QVBoxLayout()
        self.main_Layout.setAlignment(QtCore.Qt.AlignCenter)
        self.main_Layout.setContentsMargins(10, 10, 10, 10)  
        self.main_Layout.setSpacing(10) 
        self.setLayout(self.main_Layout) 

        # color of mLayout: 
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(255,255,255))
        self.setPalette(self.p)

        # text field: 
        self.text_Field = QtWidgets.QLineEdit()
        self.text_Field.setPlaceholderText("Name the selection set and press enter...")
        self.text_Field.setStyleSheet("background-color:rgb(50, 108, 131);")
        #self.validatorStr = QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z-_]+$"), self.text_Field) 
        #self.text_Field.setValidator(self.validatorStr)
        self.main_Layout.addWidget(self.text_Field) 

        # add_button "plus" in main_layout:
        self.add_button = QtWidgets.QPushButton("ADD SET")
        self.add_button.setObjectName("MyCustomButtonAdd")
        self.main_Layout.addWidget(self.add_button)
        self.add_button.setMaximumWidth(30)
        self.button2Style = """
                QPushButton#MyCustomButtonAdd {
                background-color: rgb(50, 108, 131);
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: black;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton#MyCustomButtonAdd:pressed {
                background-color: rgb(225, 255, 255);
                border-style: inset;
            }
                }
                """                   
        self.add_button.setStyleSheet(self.button2Style)
        
        self.add_button.clicked.connect(self.addSetSelection) # here have to connect function for "plus" button
        self.main_Layout.addWidget(self.add_button)

        # del_button "delete all" in main_layout:
        self.del_button = QtWidgets.QPushButton("DELETE ALL")
        self.del_button.setObjectName("MyCustomButtonDel")
        self.main_Layout.addWidget(self.del_button)
        self.del_button.setMaximumWidth(30)
        self.button2Style = """
                QPushButton#MyCustomButtonDel {
                background-color: rgb(50, 108, 131);
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: black;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton#MyCustomButtonDel:pressed {
                background-color: rgb(225, 255, 255);
                border-style: inset;
            }
                }
                """                   
        self.del_button.setStyleSheet(self.button2Style)
        
        self.del_button.clicked.connect(self.delit_all) 
        self.main_Layout.addWidget(self.del_button)

     # scroll layout:
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.scrollArea.setMinimumHeight(200)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumWidth(390)
        self.scrollArea.setFocusPolicy( QtCore.Qt.NoFocus )
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(10,10,10,10)
        self.scroll_layout.setSpacing(5) 
        self.scroll_area_widget.setLayout(self.scroll_layout)

        # set color for slider:
        self.style = """
                QScrollBar:vertical {
                border: 2px solid grey;
                background-color: rgb(50, 108, 131);
                width: 15px;
                margin: 20px 0 20px 0;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                border: 2px solid grey;
                background-color: rgb(50, 108, 131);
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                border: 2px solid grey;
                background-color: rgb(50, 108, 131);
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: 2px solid grey;
                width: 3px;
                height: 3px;
                background: white;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
                }
                """                   
        self.scrollArea.setStyleSheet(self.style)

        self.main_Layout.addWidget(self.scrollArea) 

    # functions:
    
    def addSetSelection(self, event):
        """
        The function adds sets into scroll widget
        """
        self.addSet = MySetWidget()
        if len(self.text_Field.text()) == 0:
            cmds.inViewMessage( amg='ERROR: <hl>You have to type name</hl>!', pos='midCenter', fade=1)
            cmds.error("ERROR: you have to type name")
            
        else:
            self.addSet.label.setText(self.text_Field.text())  
            
        self.scroll_layout.addWidget(self.addSet)
        

    def keyPressEvent(self, event): 
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter: 
            self.text_Field.clearFocus()


    def delit_all(self):
        '''
        The function deletes all sets in MySetWidget and connected to button "delete all"
        '''
        self.deleteLater() 
      
    def checkUI(self):
        if cmds.window("MyTool", query=1, exists=1):
            cmds.deleteUI("MyTool")
        if cmds.windowPref("MyTool", exists=1):
            cmds.windowPref("MyTool", remove=1)
        

     
myUI = MyWindow()
myUI.show()  

# _______questions:__________
# clean focus
# delete_all function 




Script_L7_v005.py
Displaying Script_L7_v005.py.
