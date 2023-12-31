import maya.cmds as cmds
cmds.polySphere (r=5, name="My_Sphere")
cmds.move (-10, 0, 0)
cmds.playbackOptions (animationStartTime=1,animationEndTime=200)
cmds.currentTime (1)
cmds.setKeyframe (v=-10, at='translateX')
cmds.setKeyframe (v=10, at='translateY')
cmds.setKeyframe (v=0, at='translateZ')
cmds.currentTime (200)
cmds.setKeyframe (v=10, at='translateX')
cmds.setKeyframe (v=10, at='translateY')
cmds.setKeyframe (v=0, at='translateZ')


import maya.cmds as cmds
cmds.polyCube (sx=10, sy=15, sz=10, name="My_Cube")
cmds.currentTime (1)
cmds.move (-10, 0, 10)
cmds.parentConstraint('My_Sphere', 'My_Cube', mo=1)
cmds.bakeSimulation ('My_Cube', t=(1,200), at={"tx", "ty", "tz", "rx", "ry", "rz"})
cmds.delete ('My_Cube_parentConstraint1')
print ("The script is accomplished")
