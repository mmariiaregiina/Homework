import maya.cmds as cmds
import maya.mel as mel


class Rocket(object):

    def __init__(self, bodyParts=None, noseConeHeight=None, fuelTanks=None):
        self.bodyParts = bodyParts
        self.noseConeHeight = noseConeHeight
        self.fuelTanks = fuelTanks
       
        self.cleanUpSceen()
        self.createBody()
        self.createCone()
        self.createTanks()
       

    def createBody(self):
        '''
        The function creates body parts of the Rocket
        '''
        heightBodyparts = 2

        if self.bodyParts == 0 or self.bodyParts == 1 or self.bodyParts == 3:
            cmds.inViewMessage( amg='ERROR: <hl>you have to set int bodyParts > 3</hl>.', pos='midCenter', fade=1)
            cmds.error("ERROR: you have to set bodyParts > 0")
        else:
            for part in range(self.bodyParts):
                heightBodyparts = heightBodyparts 
                rocketBody = cmds.polyCylinder(name="partBody") 
                cmds.move(0, heightBodyparts, 0)
                heightBodyparts = heightBodyparts + 2


            a = cmds.ls(type='mesh') # a - select mesh cylinders to assign color
            for part in a:
                shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
                cmds.setAttr(shader + ".color", 1, 0.3, 0.7, type="double3")
                cmds.select(part)
                cmds.hyperShade(assign=shader) 


    def createCone(self):
        '''
        The function creates nose of the Rocket
        '''
        if self.noseConeHeight == 0:
             cmds.inViewMessage( amg='ERROR: <hl>you have to set noseConeHeight > 0</hl>.', pos='midCenter', fade=1)
             cmds.error("ERROR: you have to setnoseConeHeight > 0")
        else:
            cmds.polyCone(n="noseCone", h=self.noseConeHeight)

        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shader + ".color", 1, 0.004, 0.674, type="double3")
        cmds.select("noseCone")
        cmds.hyperShade(assign=shader) 

        a = cmds.ls(type='mesh') #  a - select mesh cylinders 
        b = cmds.listRelatives(a, parent=1) [-2] # b - penultimate in the list 
        trYPartBodylast = cmds.xform(b, q=1, t=1 ) [1] 
        trUpCone = self.noseConeHeight/2 + trYPartBodylast + 1 # 1 is a half of Cylinder r
        cmds.xform("noseCone", t=(0, trUpCone, 0))


    def createTanks(self):
        '''
        The function creates fuel tanks of the Rocket:
        '''
        heightnoseCone = cmds.polyCone("noseCone", q=1, h=1)
        heightTanks = heightnoseCone/2
        radiusnoseCone = cmds.polyCone("noseCone", q=1, r=1)
        radiusTanks = radiusnoseCone/2
        fuelTank = cmds.polyCone(n="fuelTank", h=heightTanks, r=radiusTanks)

        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shader + ".color", 1, 0.004, 0.674, type="double3")
        cmds.select("fuelTank")
        cmds.hyperShade(assign=shader) 

        group = cmds.group(fuelTank, n="fuelTank_grp")
        a = cmds.ls(type='mesh') [0] # a - select mesh cone for tank among all mesh
        b = cmds.listRelatives(a, parent=1) # b - select translate node         
        cmds.xform(b, t=(radiusnoseCone, heightTanks/2, 0))


        if self.fuelTanks == 1:
            turn = 180 # turn for fuel tanks 
            for fuelTank_grp in range(self.fuelTanks):
                turn = turn
                mel.eval('duplicate "fuelTank_grp"')
                s = cmds.xform("fuelTank_grp", ro=(0, turn, 0))
                turn = turn + 180
        elif self.fuelTanks == 4:
            turn = 73 # turn for fuel tanks 
            for fuelTank_grp in range(self.fuelTanks):
                turn = turn
                mel.eval('duplicate "fuelTank_grp"')
                s = cmds.xform("fuelTank_grp", ro=(0, turn, 0))
                turn = turn + 73
        else:
            self.cleanUpSceen()
            cmds.inViewMessage( amg='ERROR: <hl>you have to set fuelTanks 1 or 4</hl>.', pos='midCenter', fade=1)
            cmds.error("ERROR: you have to set fuelTanks 1 in order to craete 2 tanks and 4 in order to create 5 tanks > 0")

    def cleanUpSceen(self):
        allTr = cmds.ls(tr = 1) 
        allTr.remove ("persp")
        allTr.remove ("front")
        allTr.remove ("side")
        allTr.remove ("top")
        cmds.delete(allTr)

class RocketNew(Rocket):
    def __init__(self, escapeSystem=None, fins=None, bodyParts=None,  noseConeHeight=None, fuelTanks=None):
        super(RocketNew, self).__init__(bodyParts,  noseConeHeight,  fuelTanks)

        self.escapeSystem = escapeSystem 
        self.fins = fins   

        if escapeSystem:
            self.createEscapeSystem()
        
        if fins:
            self.createFins()


    def createEscapeSystem(self):
        '''
        The functuin creates Escape system on the top of the rocket
        '''
        createES = cmds.polyCylinder(n="escapeSystem", r=0.1, h=self.noseConeHeight)

        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shader + ".color", 1, 0.004, 0.674, type="double3")
        cmds.select("escapeSystem")
        cmds.hyperShade(assign=shader) 

        a = cmds.xform("noseCone", q=1, t=1) [1] # a - in order to find out translation Y of noseCone
        heightES = cmds.polyCylinder("escapeSystem", q=1, h=1)
        cmds.xform(createES, t=(0, a + heightES/2, 0))
   

    def createFins(self):
        '''
        The function creates 4 fins for the rocket
        '''
        fin = cmds.polyCube(n="fin",w=self.bodyParts/2, h=1, d=0.1) 
        wFin = cmds.polyCube("fin",q=1, w=1) 
        cmds.xform("fin", t=(wFin/2, 4, 0))

        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)
        cmds.setAttr(shader + ".color", 1, 0.004, 0.674, type="double3")
        cmds.select("fin")
        cmds.hyperShade(assign=shader) 
        groupFin = cmds.group(n="fin_grp", empty=1)
        cmds.group(fin, parent = groupFin)

        turn = 90 # turn for fins 
        for groupFin in range(3):
            turn = turn
            mel.eval('duplicate "fin_grp"')
            s = cmds.xform("fin_grp", ro=(0, turn, 0))
            turn = turn + 90
        

            

myRocket = RocketNew(bodyParts=4, noseConeHeight=2, fuelTanks=4, escapeSystem=1, fins=1)


# there is a a limit for fuelTanks, have to set 1 or 4, indicated in error message
# height of fuel tanks depends on Nose cone, therefore appearance of the rocket changes
# height of Escape system depends on cone's height 
# fins depen on amount of bodyParts
