import maya.cmds as cmds 
import json


def openFromfile ():

    jsinData = {}

    with open("C:\Users\Mariia Grebeshkova\OneDrive\Desktop\Project_2\pose_1.json", 'r') as f:
        jsonData = json.load(f)


    for channels in jsonData:

        for number in jsonData[channels]:
            value = jsonData[channels][number]   

            cmds.setAttr(channels + '.' +  number, value)  


openFromfile ()
