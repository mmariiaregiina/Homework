import maya.cmds as cmds 
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin # to put MyWindow on top

class MyWindow(MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.checkUI()
        self.createUI()
 

    def createUI(self):
        '''
        The functions creates Layouts 
        '''
        self.setObjectName("TheWindow")
        self.setWindowTitle("Objects' Creator 2.0")
        self.setMinimumSize(300, 300)
        self.setMaximumSize(700, 700)
        self.resize(500,500)
        

        self.mLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mLayout) # to put the layout into MyWindow 


        # Creation of text field:
        self.tField = QtWidgets.QLineEdit()
        self.mLayout.addWidget(self.tField)
        self.tField.setPlaceholderText("Enter name...")
        self.validatorStr = QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z]+$"), self.tField) # can type only letters 
        self.tField.setValidator(self.validatorStr)
  

        # Creation of radial buttons and bind them to rgroupLayout:
        self.rgroup = QtWidgets.QGroupBox()
        self.rgroup.setMaximumHeight(50) 
        self.rgroupLayout = QtWidgets.QHBoxLayout() # layout for radial buttons 
        self.rgroup.setLayout(self.rgroupLayout) # put rgroupLayout into rgroup
        self.mLayout.addWidget(self.rgroup) # put rgroup into mLayout 


        self.rSphere = QtWidgets.QRadioButton("Sphere")
        self.rgroupLayout.addWidget(self.rSphere)
        self.rSphere.setStyleSheet("QRadioButton::indicator:checked"
                                        "{"
                                        "background-color : darkcyan;"
                                        "}")
        self.rSphere.setChecked(True) # already chosen when the script is opened
    

        self.rLocator = QtWidgets.QRadioButton("Locator")
        self.rgroupLayout.addWidget(self.rLocator)
        self.rLocator.setStyleSheet("QRadioButton::indicator:checked"
                                        "{"
                                        "background-color : darkcyan;"
                                        "}")
        

        self.rCube= QtWidgets.QRadioButton("Cube")
        self.rgroupLayout.addWidget(self.rCube)
        self.rCube.setStyleSheet("QRadioButton::indicator:checked"
                                        "{"
                                        "background-color : darkcyan;"
                                        "}")
        

        # Creation of QSlider:
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(30)
        self.sLayout = QtWidgets.QHBoxLayout() # layout for the slider
        self.sLayout.addWidget(self.slider)
        self.mLayout.addLayout(self.sLayout)

        self.slider_tField = QtWidgets.QLineEdit()
        self.slider_tField.setFixedSize(100, 40)
        self.sLayout.addWidget(self.slider_tField)
        self.validatorInt = QtGui.QIntValidator() # to limit the input, only numbers 
        self.slider_tField.setValidator(self.validatorInt)

        self.slider.sliderMoved.connect(self.valueStField) # takes from def valueStField(self, value)
        self.slider_tField.returnPressed.connect(self.valueSlider_tField) # takes from def valueSlider_tField(self)

        # Creation of bottom buttons and bind them to bLayout:

        self.bLayout = QtWidgets.QHBoxLayout() # layout for buttons, horizontal 
        self.mLayout.addLayout(self.bLayout) # bind to mLayout 
        self.bLayout.setSpacing(10)

        self.bAdd = QtWidgets.QPushButton("Add")
        self.bLayout.addWidget(self.bAdd)
        self.bAdd.clicked.connect(self.on_button_Add_clicked)

        self.bApply = QtWidgets.QPushButton("Apply")
        self.bLayout.addWidget(self.bApply)
        self.bApply.clicked.connect(self.on_button_Apply_clicked)

        self.bClose = QtWidgets.QPushButton("Close")
        self.bLayout.addWidget(self.bClose)
        self.bClose.clicked.connect(self.close)
   

    def valueStField(self, value):
        self.slider_tField.setText(str(value))

    def valueSlider_tField(self):
        value = int(self.slider_tField.text())
        self.slider.setValue(value)


    def on_button_Add_clicked(self): 
        self.on_button_Apply_clicked()
        self.close() 

    def on_button_Apply_clicked(self): 
        objName =  self.tField.text()

        if self.rSphere.isChecked():
            object = cmds.polySphere(n=objName)
        elif self.rLocator.isChecked():
            object = cmds.spaceLocator(n=objName)
        elif self.rCube.isChecked():
            object = cmds.polyCube(n=objName)

        slidValue = self.slider.value()

        cmds.xform(object, t=[slidValue,0,0] )


    def checkUI(self):
        if cmds.window("TheWindow", q=1, exists=1):
            cmds.deleteUI("TheWindow")
        if cmds.windowPref("TheWindow", exists=1):
            cmds.windowPref("TheWindow", remove=1)


     
myUI = MyWindow()
myUI.show()  

