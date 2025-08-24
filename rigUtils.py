import maya.cmds as cmds
import json
import os
import platform
import sys
 

# Function to adjust joint radius
def adjustJointRadius(radius):
    joints = cmds.ls(type='joint')
    for joint in joints:
        cmds.setAttr(f"{joint}.radius", radius)

def freezeTransforms():
    allJoints = cmds.ls('*_JNT_*')
    # print(allJoints)
    for joint in allJoints:
        cmds.makeIdentity(joint, apply=True, t=True, r=True, s=True)

def freezeOffsetGroups():
    cmds.select(cl=True)
    offsetGroups = cmds.ls('*_OFFSET', type='transform')
    if offsetGroups:
        for group in offsetGroups:
            cmds.makeIdentity(group, apply=True, t=True, r=True, s=True)
        else:
            print("No offset groups found")

def lockToCentre():
    cmds.select(cl=True)
    cmds.select('*C_*_JNT_*')
    selectedJoints = cmds.ls(sl=True)
    for joint in selectedJoints:
        cmds.setAttr(joint + '.tx', lock = True, keyable =True, channelBox = True)

def unlockCentre():
    cmds.select(cl=True)
    cmds.select('*C_*_JNT_*')
    selectedJoints = cmds.ls(sl=True)
    for joint in selectedJoints:
        cmds.setAttr(joint + '.tx', lock = False, keyable =True, channelBox = True)


def selectBind():
    cmds.select(cl=True)

    # Select bind and end joints
    bindJNTS = cmds.ls('*_JNT_BIND*')
    endJNTS = cmds.ls('*_JNT_END*')
    selected_joints = bindJNTS + endJNTS

    # Find joints that should be excluded
    exclude_keywords = ["feather", "Orient", "orient", "tongue", "eye_", "eyeEnd", "Root"] # "squint", "sneer", 
    exclude_joints = cmds.ls([f'*{word}*' for word in exclude_keywords])  # Find all joints with these words

    # Remove excluded joints from selection
    filtered_joints = list(set(selected_joints) - set(exclude_joints))

    # Select only the filtered joints
    cmds.select(filtered_joints)



# create layers for the groups 
def createLayers():
    # Delete all existing display layers (except the default)
    all_layers = cmds.ls(type="displayLayer")  # Get all display layers
    for layer in all_layers:
        if layer not in ["defaultLayer", "initialShadingGroup"]:  # Exclude default and system layers
            cmds.delete(layer)

    print("Deleted all existing display layers.")

    # Define the specific groups you want to create layers for
    specific_groups = ["JOINTS", "CONTROLS", "C_COGFK_CTRL_ZERO", "L_hip_CTRL_ZERO", "R_hip_CTRL_ZERO"]  

    # Create new display layers
    for grp in specific_groups:
        if cmds.objExists(grp):  # Ensure the group exists in the scene
            layer_name = f"{grp}_layer"  # Name the layer after the group

            # Create a new display layer
            cmds.createDisplayLayer(name=layer_name, empty=True)
            
            # Add the group to the layer
            cmds.editDisplayLayerMembers(layer_name, grp, noRecurse=True)

            # Set different properties for each layer
            cmds.setAttr(f"{layer_name}.visibility", 1)  # Visible
            cmds.setAttr(f"{layer_name}.playback", 1)  # Visible during playback
            cmds.setAttr(f"{layer_name}.displayType", 0)  # Normal (Selectable)

    print(f"Recreated layers for: {specific_groups}")
