
import maya.cmds as cmds
import random 

def cleanScene():
    Spheres_Groups = cmds.ls(tr = 1) 
    Spheres_Groups.remove ("persp")
    Spheres_Groups.remove ("front")
    Spheres_Groups.remove ("side")
    Spheres_Groups.remove ("top")
    cmds.delete(Spheres_Groups)
    
    
def createPlanet(o,f):
    radiusPlanet = random.randint (o,f)
    Planet = cmds.polySphere (n="My_Planet", r=radiusPlanet)

def CreateMoons(minMoons, maxMoons):
    amountMoons = random.randint(minMoons, maxMoons)
    
    distance = cmds.polySphere('My_Planet', q=1, r=1)
    
    for i in range(amountMoons):
        Moon = cmds.polySphere(r=2)[0]
        R_Moon = cmds.polySphere(Moon, q=1, r=1)
        
        
        distance = distance + R_Moon
        Y = random.randint (-distance, distance) 
        cmds.xform(Moon, translation = [distance,Y,0])
        R = random.randint (0,45) # inclination of the planet's axis (used x and z axis)
        cmds.xform(Moon, ro = (R,0,R))
         
        if i > 0 :
            distance = distance # make a row of moons according x
        cmds.xform(Moon, translation = [distance,Y,0])
        distance =  distance + R_Moon     
        
        P = random.randint (-100,10)
        cmds.xform(Moon, r=1, translation=[0,0,P]) # random z coordinate
        
        
        a = "{}_moon_rotation".format(Moon) # rotation relative to the Planet
        cmds.group(empty=1, r=1, n=a)
        Moon_N = cmds.xform (Moon, q=1, worldSpace=1, translation=1)
        cmds.xform (a, cpc=1)                            # center pivot
        cmds.xform (worldSpace=1, rotatePivot=Moon_N)
        cmds.xform (worldSpace=1, scalePivot=Moon_N)
        cmds.parent(Moon,a) 
        YGP = random.randint (0,360)
        cmds.xform(a, ro=(0,YGP,0))
        b = "{}_animation".format(a)
        cmds.group(empty=1, r=1, n=b)
        cmds.parent(a,b) 
        
        # make a circle around the Planet
        minTime = cmds.playbackOptions(query=1, minTime=True)
        maxTime = cmds.playbackOptions(query=1, maxTime=True)
        cmds.setKeyframe(b + ".ry", time=minTime, value=0)
        cmds.setKeyframe(b + ".ry", time=maxTime, value=360)
        cmds.keyTangent (b + ".ry", itt='linear', ott='linear')
        
        # moon rotation around axis
        m = cmds.getAttr (a + ".ry")
        cmds.setKeyframe(a + ".ry", time=minTime, value=m)
        cmds.setKeyframe(a + ".ry", time=maxTime, value=m+3600)
        cmds.keyTangent (a + ".ry", itt='linear', ott='linear')
        
        # assign shading with color to My_Planet
        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shader + ".color", 1, 0.004, 0.674, type="double3")
        cmds.select("My_Planet")
        cmds.hyperShade(assign=shader)
        
        # assign shading with color to different moons
        G = random.uniform (0.05,0.5)
        shader_moon = cmds.shadingNode("lambert", n="lambertPink_m", asShader=1)
        cmds.setAttr(shader_moon + ".color", 1, G, 0.674, type="double3")
        cmds.select(Moon)
        cmds.hyperShade(assign=shader_moon)
       
      

       
cleanScene ()
createPlanet(3,10)
CreateMoons(2,10)
Script_lesson_2.py
Displaying Script_lesson_2.py.
