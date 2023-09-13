
import maya.cmds as cmds
import random 

if cmds.window("MyWindowID", exists=1): 
      cmds.deleteUI("MyWindowID")

if cmds.windowPref("MyWindowID", exists=1):
    cmds.windowPref("MyWindowID", remove=1)
	
cmds.window("MyWindowID", title="Primitives' Creator", width=400, height=300, toolbox=True)


# Creation of main layout (mainLayout):

mainLayout = cmds.columnLayout(adjustableColumn=1, rowSpacing=20)

textFieldForObj = cmds.textField("MyWindowID", placeholderText="Enter name", parent=mainLayout, backgroundColor=(0.609,0.314,0.798)) 


# Creation of middle layout (midLayout) and collections for buttons (collectionOfButtons):

midLayout = cmds.rowLayout(numberOfColumns=3, cw3=[100,100,100], ct3=['left', 'both', 'right'], co3=[10,10,10], p=mainLayout) 

collectionOfButtons = cmds.radioButtonGrp(label="Choose type:", labelArray3=["Sphere", "Cube", "Cone"], numberOfRadioButtons=3, select=1, p=midLayout)

# Creatioin of Checkbox's layout, boxes and slider: 

mid2Layout = cmds.columnLayout(adjustableColumn=1, rowSpacing=15, p=mainLayout, co=['left', 70])

slider = cmds.floatSliderGrp(label='Radius/Height', field=1, parent=mid2Layout, hlc=(0.609,0.314,0.798))

groupBox = cmds.checkBox(label='Put into a group')
moveBox = cmds.checkBox(label='Move obj by 10 units of every axis randomly') 
layerBox = cmds.checkBox(label='Put on layer')
colorBox = cmds.checkBox(label='Assign random color')

# Functions for buttons:

def createObjects():
    chosenObjectType = cmds.radioButtonGrp(collectionOfButtons, query=1, select=1)
    textName = cmds.textField(textFieldForObj, query=1, text=1)
    valueQuery = cmds.floatSliderGrp(slider, query=1, value=1)

    if chosenObjectType == 1:
        object = cmds.polySphere(n=textName, r=valueQuery)[0]

    elif chosenObjectType == 2:
        object = cmds.polyCube(n=textName, h=valueQuery)[0]

    else:
        object = cmds.polyCone(n=textName, h=valueQuery)[0]
   

    if cmds.checkBox(groupBox, query=1, value=1):
        cmds.group(object, name="Group")  

    if cmds.checkBox(layerBox, query=1, value=1):
        layer = cmds.createDisplayLayer()  
        cmds.editDisplayLayerMembers(layer, object)  

    if cmds.checkBox(moveBox, query=1, value=1):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        z = random.randint(-10, 10)
        cmds.xform(object, translation=[x,y,z])

    if cmds.checkBox(colorBox, query=1, value=1):
        r = random.uniform (-1,1)
        g = random.uniform (-1,1)
        b = random.uniform (-1,1)
        shaderObj = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shaderObj + ".color", r, g, b, type="double3")
        cmds.select(object)
        cmds.hyperShade(assign=shaderObj)



# Creation of bottom's layaut 


bottomLayout = cmds.rowLayout(numberOfColumns=2, parent=mainLayout, adjustableColumn3=1, cw2=[100,100], ct2=['left', 'right'], columnOffset2=[50, 0])
cmds.button(label="Apply", p=bottomLayout, c="createObjects()")
cmds.button(label="Cancel", p=bottomLayout, c="cmds.deleteUI('MyWindowID')") 


cmds.showWindow("MyWindowID")   
Script_L4.py
Displaying Script_L4.py.
