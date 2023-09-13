import maya.cmds as cmds  
import json 
 
 
 
def getRigctrls(): 
    rig =cmds.ls(type='nurbsCurve') 
    ctrls = cmds.listRelatives(rig, parent=1) 
    return (ctrls) 
 
 
def savePoseToFile(): 
    ctrls = getRigctrls() 
     
    dataDic = {} 
     
 
    for channels in ctrls: 
        attrs = cmds.listAttr(channels, k=1) 
        attributesDic = {} 
 
        for number in attrs: 
            if 'translate' in number or 'rotate' in number or 'scale' in number: 
                value = cmds.getAttr(channels + '.' + number) 
 
 
      
                attributesDic[number] = value 
 
        dataDic[channels] = attributesDic    
 
                
                      
                      
    if dataDic: 
        with open ("C:\Users\Mariia Grebeshkova\OneDrive\Desktop\Project_2\pose_1.json", 'w') as f: 
            json.dump(dataDic, f, indent = 4) 
         
 
getRigctrls() 
savePoseToFile()
