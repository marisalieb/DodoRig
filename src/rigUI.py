import maya.cmds as cmds
import json
import os
import platform
import sys
import importlib
 

# import ikSpringSolver in MEL !!!!
# run ikSpringSolver;


# get script directory
script_dir = os.getcwd() 

if script_dir not in sys.path:
    sys.path.append(script_dir)

# my rig modules
import skeleton
import rigUtils
from setupBodyControls import createAllControls, constrainControls, parentControls, adjustAllJointWeights
from IKFK import createIKs, constrainFKIKToBindJnts, setupIKFKBlendForAll, fixPostIKFK, sortIKFK, setUpFKIKJoints
from setDrivenKeys import sdk_configs, createSetDrivenKeys
from faceRig import *



def createSkeletonBase():
    skeleton.createSkeleton()
    skeleton.lockToCentre()
    cmds.select(cl=True)


def createBaseRig():
    skeleton.parentJoints()
    rigUtils.unlockCentre()
    cmds.select(cl=True)
    skeleton.orientJoints()
    skeleton.orientEndJoints()
    skeleton.deleteOrientJoints()
    rigUtils.freezeTransforms()
    skeleton.mirrorSkeleton()

def createControls():
    setUpFKIKJoints() 
    sortIKFK()
    createIKs()
    constrainFKIKToBindJnts()
    createAllControls()
    constrainControls()
    parentControls()
    rigUtils.createLayers()
    fixPostIKFK()
    setupIKFKBlendForAll()
    adjustAllJointWeights()

    print("Rig created successfully")

# different set up for adjusting the controllers before continuing
def adjustControllers():
    setUpFKIKJoints() # added
    sortIKFK() # TAKE OUT for skinning maybe
    createIKs() # added
    constrainFKIKToBindJnts() # added
    createAllControls()

def finishRig():
    rigUtils.freezeOffsetGroups()
    constrainControls()
    parentControls()
    rigUtils.createLayers()
    fixPostIKFK()
    setupIKFKBlendForAll()
    adjustAllJointWeights()
    print("Rig finished successfully")


# face 
def setupEyeBlink():
    eyeBlink()


def setupFaceJoints():
    parentFaceJoints()
    mirrorFaceJoints()
    orientFaceJoints()
    deleteFaceOrientJoints()
    freezeFaceTransforms()

def setupFaceRig():
    setupEyeControls()
    neckStretch()
    createFaceControls()
    constrainFaceControls()
    parentFaceControls()
    allLipControls()
    connectAllScales()
    print("Face rig created successfully")



###



def createUI():
    # Check if the window exists
    if cmds.window("DodoRig_Window", exists=True):
        cmds.deleteUI("DodoRig_Window")
    
    # Create the window
    window = cmds.window("DodoRig_Window", title="Dodo Rig", widthHeight=(600, 600))
    
    # Create a layout
    layout = cmds.columnLayout()
    
    # Create other buttons
    cmds.text(label="Run ikSpringSolver in MEL before starting!")
    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")

    cmds.text(label="Create Base")
    cmds.button(label="Create Joints", command='createSkeletonBase()')
    cmds.separator(height=10, style="in")

    cmds.button(label="Save New Joint Positions (ONLY use before creating the rig!)", command='skeleton.saveUpdatedPositions()')
    
    cmds.separator(height=10, style="in")

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 100))  
    cmds.button(label="Adjust Joint Radius", command=lambda *args: on_button_click(radius_input))
    radius_input = cmds.floatField(minValue=0.1, value=1) 
    cmds.setParent("..")  # Go back to the parent layout

    # handle the button click with the radius input
    def on_button_click(radius_input):
        radius_value = cmds.floatField(radius_input, query=True, value=True)
        rigUtils.adjustJointRadius(radius_value)


    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")
    cmds.text(label="Create Body Rig")
    cmds.button(label="Create Base Rig", command='createBaseRig()')
    cmds.separator(height=10, style="in")
    cmds.button(label="Create Controls", command='createControls()')
  
    cmds.separator(height=10, style="in")
    # cmds.text(label="Set Driven Keys")
    cmds.button(label="Create Set Driven Keys", command='createSetDrivenKeys()')

    # face 
    cmds.separator(height=10, style="in")
    cmds.separator(height=10, style="in")
    cmds.text(label="Add Face Rig")
    cmds.button(label="Setup Face Joints", command='setupFaceJoints()')
    cmds.separator(height=10, style="in")
    cmds.button(label="Setup Face Rig", command='setupFaceRig()')
    cmds.separator(height=10, style="in")
    cmds.button(label="Setup Eye Blinking (ONLY use when the model is in the scene)", command='setupEyeBlink()')

    # weight painting
    cmds.separator(height=10, style="in")
    cmds.separator(height=10, style="in")
    cmds.text(label="For weight painting")
    cmds.button(label="Select all BIND Joints", command='rigUtils.selectBind()')


    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")
    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")
    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")
    cmds.separator(height=10, style="in")    
    cmds.separator(height=10, style="in")
    cmds.text(label="Adjust Controllers before finishing rig")
    cmds.button(label="Adjust Controllers", command='adjustControllers()')
    cmds.button(label="Finish Rig", command='finishRig()')

    # Show the window
    cmds.showWindow(window)

    
createUI()


