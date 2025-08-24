import maya.cmds as cmds
import json
import os
import platform
import sys
import importlib


from controls import createControl, createSquareControl


def setupEyeControls():

    cmds.xform('L_eye_CTRL_OFFSET', relative=True, objectSpace=True, translation=(3, 0, 0))
    cmds.xform('R_eye_CTRL_OFFSET', relative=True, objectSpace=True, translation=(-3, 0, 0))

    # also freeze transforms on offset groups
    cmds.makeIdentity('L_eye_CTRL_OFFSET', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('R_eye_CTRL_OFFSET', apply=True, translate=True, rotate=True, scale=True)

    cmds.aimConstraint('L_eye_CTRL', 'L_eyeEnd_JNT_END', maintainOffset=False, weight=1, aimVector=[1, 0, 0], upVector=[0, 0, 1])
    cmds.aimConstraint('R_eye_CTRL', 'R_eyeEnd_JNT_END', maintainOffset=False, weight=1, aimVector=[-1, 0, 0], upVector=[0, 0, -1])


# this eyeblink function is based on how the eyeblink works on the model, so with a sweep of a circle
def eyeBlink():
    # Define the control and the NURBS spheres for both left and right eyes
    ctrlLeft = "L_eye_CTRL"  # Left eye control object name, eyelid_lft
    nurbs_sphereLeft = "makeNurbSphere2"  # Left eye NURBS sphere object name
    ctrlRight = "R_eye_CTRL" 
    nurbs_sphereRight = "makeNurbSphere3" 

    # Function to create and connect math nodes for either eye
    def create_eye_blink(ctrl, nurbs_sphere):
        attr_name = "Blink"
        
        # Add the attribute if it doesn't exist, and set a default value of 30
        if not cmds.attributeQuery(attr_name, node=ctrl, exists=True):
            cmds.addAttr(ctrl, longName=attr_name, attributeType="double", min=0, max=60, defaultValue=30, keyable=True)

        # Create a floatMath node to add 300 to the attribute for endSweep
        add_node = cmds.createNode("floatMath", name="addNode")
        cmds.setAttr(f"{add_node}.operation", 0)  # Operation 0 = Addition
        cmds.setAttr(f"{add_node}.floatB", 300)  # Add 300

        # Connect the control's attribute to the add node input
        cmds.connectAttr(f"{ctrl}.{attr_name}", f"{add_node}.floatA", force=True)

        # Connect the add node output to the NURBS sphere's endSweep
        cmds.connectAttr(f"{add_node}.outFloat", f"{nurbs_sphere}.endSweep", force=True)

        # Create a floatMath node to subtract the attribute from 60 for startSweep
        subtract_node = cmds.createNode("floatMath", name="subtractNode")
        cmds.setAttr(f"{subtract_node}.operation", 1)  # Operation 1 = Subtraction
        cmds.setAttr(f"{subtract_node}.floatA", 60)  # Subtract from 60

        # Connect the control's attribute to the subtract node input
        cmds.connectAttr(f"{ctrl}.{attr_name}", f"{subtract_node}.floatB", force=True)

        # Connect the subtract node output to the NURBS sphere's startSweep
        cmds.connectAttr(f"{subtract_node}.outFloat", f"{nurbs_sphere}.startSweep", force=True)

        # Print the result as in MEL format
        print(f"// Result: Connected {ctrl}.{attr_name} to {nurbs_sphere}.startSweep and {nurbs_sphere}.endSweep.")

    # Call the function for both the left and right eyes
    create_eye_blink(ctrlLeft, nurbs_sphereLeft)
    create_eye_blink(ctrlRight, nurbs_sphereRight)



def neckStretch():
    # create locators at position of neck base bind joints and upper 
    joint1 = "C_neckBase_JNT_IK"
    joint2 = "C_neckUpper_JNT_IK"
    joint3 = "C_neckMid_JNT_IK"

    if not cmds.objExists(joint1) or not cmds.objExists(joint2):
        print("One or both joints do not exist.")
        return None

    # Get world positions of joints
    pos1 = cmds.xform(joint1, query=True, worldSpace=True, translation=True)
    pos2 = cmds.xform(joint2, query=True, worldSpace=True, translation=True)

    # Create the distance dimension tool (automatically creates two locators)
    dist_node = cmds.distanceDimension(sp=pos1, ep=pos2)
    locators = cmds.listConnections(dist_node, type="locator")

    # multiply divide node and connect distance to input x
    multiply_node = cmds.shadingNode("multiplyDivide", asUtility=True, name="distance_multiplier")
    cmds.setAttr(f"{multiply_node}.operation", 2)  # Divide
    cmds.connectAttr(f"distanceDimensionShape1.distance", f"{multiply_node}.input1X", force=True)
    # set inout2 to 9
    cmds.setAttr(f"{multiply_node}.input2X", 9.414)

    # create condition ode set to greater than
    condition_node = cmds.shadingNode("condition", asUtility=True, name="distance_condition")
    cmds.setAttr(f"{condition_node}.operation", 2)  # Greater than
    cmds.connectAttr(f"{multiply_node}.outputX", f"{condition_node}.firstTerm", force=True)
    # also outputx to colour if tru R
    cmds.connectAttr(f"{multiply_node}.outputX", f"{condition_node}.colorIfTrueR", force=True)

    # # connect colour r of condition to joint scales
    cmds.connectAttr(f"{condition_node}.outColorR", f"{joint1}.scaleX", force=True)
    cmds.connectAttr(f"{condition_node}.outColorR", f"{joint3}.scaleX", force=True)

    spine_ctrl = "C_spineIK_CTRL"

    # # parent the locators to the ik spine ctrl
    cmds.parent('locator1', spine_ctrl)
    cmds.parent('locator2', spine_ctrl)
    cmds.parent('distanceDimension1', spine_ctrl)

    # Name of the locator to scale
    locator_name = "locator2"

    scale_factor = 7.0  

    # Set the locator's localScale attribute
    cmds.setAttr(f"{locator_name}.localScaleX", scale_factor)
    cmds.setAttr(f"{locator_name}.localScaleY", scale_factor)
    cmds.setAttr(f"{locator_name}.localScaleZ", scale_factor)

    # # create selectable set 
    cmds.sets(spine_ctrl, 'locator2', name='neckStretch')



def parentFaceJoints():
    cmds.parent('L_lipBase_JNT_END', 'L_lipBaseRoot_JNT_BIND')
    cmds.parent('L_lipMid_JNT_END', 'L_lipMidRoot_JNT_BIND')
    cmds.parent('L_lipUpper_JNT_END', 'L_lipUpperRoot_JNT_BIND')

    cmds.parent('L_cheek_JNT_END', 'C_headBase_JNT_BIND')
    cmds.parent('L_eyebrowFront_JNT_END', 'C_headBase_JNT_BIND')
    cmds.parent('L_eyebrowMid_JNT_END', 'C_headBase_JNT_BIND')
    cmds.parent('L_eyebrowBack_JNT_END', 'C_headBase_JNT_BIND')

    cmds.parent('L_lipUpperRoot_JNT_BIND', 'C_headBase_JNT_BIND')
    cmds.parent('L_lipMidRoot_JNT_BIND', 'C_headBase_JNT_BIND')
    cmds.parent('L_lipBaseRoot_JNT_BIND', 'C_headBase_JNT_BIND') # or jaw possibly

    cmds.parent('L_cheekOrient_JNT_END', 'L_cheek_JNT_END')


    cmds.parent('L_eyebrowFrontOrient_JNT_END', 'L_eyebrowFront_JNT_END')
    cmds.parent('L_eyebrowMidOrient_JNT_END', 'L_eyebrowMid_JNT_END')
    cmds.parent('L_eyebrowBackOrient_JNT_END', 'L_eyebrowBack_JNT_END')

    cmds.parent('L_lipBaseOrient_JNT_END', 'L_lipBase_JNT_END')
    cmds.parent('L_lipMidOrient_JNT_END', 'L_lipMid_JNT_END')
    cmds.parent('L_lipUpperOrient_JNT_END', 'L_lipUpper_JNT_END')



def freezeFaceTransforms():
    cmds.makeIdentity('L_lipBaseRoot_JNT_BIND', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('L_lipBase_JNT_END', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('L_lipMidRoot_JNT_BIND', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('L_lipMid_JNT_END', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('L_lipUpperRoot_JNT_BIND', apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity('L_lipUpper_JNT_END', apply=True, translate=True, rotate=True, scale=True)

def orientFaceJoints():
    cmds.select(cl=True)
    # create list of root joints
    rootJoints = cmds.ls('*Root_JNT_BIND')
    # select all root joints
    cmds.select(rootJoints)
    #cmds.joint(e=True, oj='xyz', secondaryAxisOrient='xup', ch=True, zso=True)
    cmds.joint(e=True, oj='zxy', secondaryAxisOrient='xup', ch=True, zso=True)

    cmds.select(cl=True)
    faceJoints = ["L_cheek_JNT_END", "L_eyebrowFront_JNT_END",  "L_eyebrowBack_JNT_END", "L_eyebrowMid_JNT_END", "L_lipBase_JNT_END", "L_lipMid_JNT_END", "L_lipUpper_JNT_END", "R_cheek_JNT_END", "R_eyebrowFront_JNT_END",  "R_eyebrowBack_JNT_END", "R_eyebrowMid_JNT_END", "R_lipBase_JNT_END", "R_lipMid_JNT_END", "R_lipUpper_JNT_END"]
    # Select the root joint and its hierarchy
    cmds.select(faceJoints)
    # orient them all
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='xup', ch=True, zso=True)



def mirrorFaceJoints():
    cmds.select(cl=True)
    cmds.mirrorJoint('L_lipBaseRoot_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_lipMidRoot_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_lipUpperRoot_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))

    cmds.mirrorJoint('L_cheek_JNT_END', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_eyebrowFront_JNT_END', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_eyebrowMid_JNT_END', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_eyebrowBack_JNT_END', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))

def deleteFaceOrientJoints():
    cmds.delete('L_lipBaseOrient_JNT_END')
    cmds.delete('L_lipMidOrient_JNT_END')
    cmds.delete('L_lipUpperOrient_JNT_END')

    cmds.delete('L_cheekOrient_JNT_END')
    cmds.delete('L_eyebrowFrontOrient_JNT_END')
    cmds.delete('L_eyebrowMidOrient_JNT_END')
    cmds.delete('L_eyebrowBackOrient_JNT_END')

    cmds.delete('R_lipBaseOrient_JNT_END')
    cmds.delete('R_lipMidOrient_JNT_END')
    cmds.delete('R_lipUpperOrient_JNT_END')

    cmds.delete('R_cheekOrient_JNT_END')
    cmds.delete('R_eyebrowFrontOrient_JNT_END')
    cmds.delete('R_eyebrowMidOrient_JNT_END')
    cmds.delete('R_eyebrowBackOrient_JNT_END')

def freezeFaceTransforms():
    faceJoints = ["L_cheek_JNT_END", "L_eyebrowFront_JNT_END",  "L_eyebrowBack_JNT_END", "L_eyebrowMid_JNT_END", "L_lipBase_JNT_END", "L_lipMid_JNT_END", "L_lipUpper_JNT_END", "R_cheek_JNT_END", "R_eyebrowFront_JNT_END",  "R_eyebrowBack_JNT_END", "R_eyebrowMid_JNT_END", "R_lipBase_JNT_END", "R_lipMid_JNT_END", "R_lipUpper_JNT_END"]

    for joint in faceJoints:
        cmds.makeIdentity(joint, apply=True, t=True, r=True, s=True)


def createFaceControl(controlName, alignment, direction, radius, joint, trans, rot):
    name = alignment + '_' + controlName + '_CTRL'
    cmds.circle(n=name, nr = direction, r=radius)
    # nr is which way the circle is build
    # without direction the circle is build at a differnt angle

    # cmds.group(n = name +'_group')
    cmds.group(n = name +'_OFFSET')
    cmds.group(n = name +'_ZERO')

    shapeNode = cmds.listRelatives(name)
    shapeNode = shapeNode[0]
    cmds.setAttr(shapeNode + '.overrideEnabled', 1)
    cmds.setAttr(shapeNode + '.overrideColor', 20)

    cmds.select(cl=True)

def createFaceControls():
    faceJoints = ["L_cheek_JNT_END", "L_eyebrowFront_JNT_END",  "L_eyebrowBack_JNT_END", "L_eyebrowMid_JNT_END", "L_lipBase_JNT_END", "L_lipMid_JNT_END", "L_lipUpper_JNT_END", "R_cheek_JNT_END", "R_eyebrowFront_JNT_END",  "R_eyebrowBack_JNT_END", "R_eyebrowMid_JNT_END", "R_lipBase_JNT_END", "R_lipMid_JNT_END", "R_lipUpper_JNT_END"]

    for joint in faceJoints:

        side = "L" if joint.startswith("L_") else "R"
        ctrl_name = joint.replace("L_", "").replace("R_", "").replace("_JNT_END", "").replace("_JNT_BIND", "")

        # Get joint position in world space
        joint_pos = cmds.xform(joint, query=True, worldSpace=True, translation=True)

        createFaceControl(ctrl_name, side, [1, 0, 0], 0.5, joint, True, True)

        # Move control to joint position
        offset_grp = f"{side}_{ctrl_name}_CTRL_ZERO"
        cmds.xform(offset_grp, worldSpace=True, translation=joint_pos)

        # Apply offset in object space
        move_offset = 1 if side == "L" else -1
        offset_grp = f"{side}_{ctrl_name}_CTRL_OFFSET"
        cmds.xform(offset_grp, relative=True, objectSpace=True, translation=(move_offset, 0, 0))

        # Freeze transforms
        cmds.makeIdentity(offset_grp, apply=True, translate=True, rotate=True, scale=True)

    
    faceMainCtrls = ["L_eyebrowMid_JNT_END",  "R_eyebrowMid_JNT_END"] # "L_lipMid_JNT_END",, "R_lipMid_JNT_END"

    for joint in faceMainCtrls:
        side = "L" if joint.startswith("L_") else "R"
        ctrl_name = joint.replace("L_", "").replace("R_", "").replace("Mid_JNT_END", "").replace("_JNT_BIND", "")

        # Get joint position in world space
        joint_pos = cmds.xform(joint, query=True, worldSpace=True, translation=True)

        # Create control
        createFaceControl(ctrl_name, side, [0, 0, 1], 1.2, joint, True, True)

        # Move control to joint position
        zero_grp = f"{side}_{ctrl_name}_CTRL_ZERO"
        cmds.xform(zero_grp, worldSpace=True, translation=joint_pos)

        # Apply offset in object space
        offset_grp = f"{side}_{ctrl_name}_CTRL_OFFSET"
        move_offset = 1.4 if side == "L" else -1.4
        cmds.xform(offset_grp, relative=True, objectSpace=True, translation=(move_offset, 0, 0))

        # **Rotate the actual control, not the offset**
        ctrl = f"{side}_{ctrl_name}_CTRL"
        rotate_value = -90 if side == "L" else 90
        cmds.rotate(0, rotate_value, 0, ctrl, relative=True, objectSpace=True, fo=True)  # Rotate control
        
        cmds.makeIdentity(ctrl, apply=True, translate=False, rotate=True, scale=True)  # Freeze transforms

        # Freeze transforms
        cmds.makeIdentity(offset_grp, apply=True, translate=True, rotate=False, scale=True)
    
def constrainFaceControls():
    cmds.parentConstraint('L_cheek_CTRL', 'L_cheek_JNT_END', name='L_cheek_parentConst', mo=True)
    cmds.parentConstraint('L_eyebrowFront_CTRL', 'L_eyebrowFront_JNT_END', name='L_eyebrowFront_parentConst', mo=True)
    cmds.parentConstraint('L_eyebrowMid_CTRL', 'L_eyebrowMid_JNT_END', name='L_eyebrowMid_parentConst', mo=True)
    cmds.parentConstraint('L_eyebrowBack_CTRL', 'L_eyebrowBack_JNT_END', name='L_eyebrowBack_parentConst', mo=True)

    cmds.parentConstraint('R_cheek_CTRL', 'R_cheek_JNT_END', name='R_cheek_parentConst', mo=True)
    cmds.parentConstraint('R_eyebrowFront_CTRL', 'R_eyebrowFront_JNT_END', name='R_eyebrowFront_parentConst', mo=True)
    cmds.parentConstraint('R_eyebrowMid_CTRL', 'R_eyebrowMid_JNT_END', name='R_eyebrowMid_parentConst', mo=True)
    cmds.parentConstraint('R_eyebrowBack_CTRL', 'R_eyebrowBack_JNT_END', name='R_eyebrowBack_parentConst', mo=True)


def parentFaceControls():
    cmds.parent('L_eyebrowFront_CTRL_ZERO', 'L_eyebrow_CTRL')
    cmds.parent('L_eyebrowMid_CTRL_ZERO', 'L_eyebrow_CTRL')
    cmds.parent('L_eyebrowBack_CTRL_ZERO', 'L_eyebrow_CTRL')

    cmds.parent('L_lipBase_CTRL_ZERO', 'C_headBase_CTRL') # L_lip_CTRL
    cmds.parent('L_lipMid_CTRL_ZERO', 'C_headBase_CTRL')
    cmds.parent('L_lipUpper_CTRL_ZERO', 'C_headBase_CTRL')

    cmds.parent('R_eyebrowFront_CTRL_ZERO', 'R_eyebrow_CTRL')
    cmds.parent('R_eyebrowMid_CTRL_ZERO', 'R_eyebrow_CTRL')
    cmds.parent('R_eyebrowBack_CTRL_ZERO', 'R_eyebrow_CTRL')

    cmds.parent('R_lipBase_CTRL_ZERO', 'C_headBase_CTRL')
    cmds.parent('R_lipMid_CTRL_ZERO', 'C_headBase_CTRL')
    cmds.parent('R_lipUpper_CTRL_ZERO', 'C_headBase_CTRL')

    cmds.parent('L_cheek_CTRL_ZERO', 'C_headBase_CTRL')

    cmds.parent('R_cheek_CTRL_ZERO', 'C_headBase_CTRL')

    cmds.parent('L_eyebrow_CTRL_ZERO', 'C_headBase_CTRL')
    cmds.parent('R_eyebrow_CTRL_ZERO', 'C_headBase_CTRL')



def connectLipControlToJoint(ctrl1, joint1, joint2):
    translateZ_value = cmds.getAttr(f"{joint2}.translateZ")

    # create attributeson ctrl
    cmds.addAttr(ctrl1, longName='Gradient', attributeType='float', min=0, max=1, defaultValue=.1, keyable=True)
    cmds.addAttr(ctrl1, longName='Offset', attributeType='float', min=0, max=60, defaultValue=translateZ_value, keyable=True)
    cmds.addAttr(ctrl1, longName='Movement', attributeType='float',min=0, max=20, defaultValue=10,  keyable=True)

    multiNode1 = cmds.shadingNode("multiplyDivide", asUtility=True, name=f"{ctrl1}_multOrient")
    cmds.setAttr(f"{multiNode1}.operation", 1) 
    cmds.connectAttr(f"{ctrl1}.translateY", f"{multiNode1}.input1Z", force=True) # or Y input and y at the other
    cmds.connectAttr(f"{multiNode1}.outputY", f"{joint1}.rotateY", force=True)

    cmds.connectAttr(f"{ctrl1}.translateZ", f"{multiNode1}.input1Y", force=True)
    cmds.connectAttr(f"{multiNode1}.outputZ", f"{joint1}.rotateX", force=True)

    invertMultNode = cmds.createNode("multiplyDivide", name=f"{ctrl1}_invert_MDL")
    # Set the multiply value to -1 (inverting the movement)
    cmds.setAttr(f"{invertMultNode}.input2X", -1)
    cmds.setAttr(f"{invertMultNode}.input2Y", -1)
    cmds.setAttr(f"{invertMultNode}.input2Z", -1)

    # Connect the control's Movement attribute to the multiply node
    cmds.connectAttr(f"{ctrl1}.Movement", f"{invertMultNode}.input1X", force=True)

    cmds.connectAttr(f"{ctrl1}.Movement", f"{multiNode1}.input2Y",  force=True)
    # Connect the inverted output to the desired inputs
    cmds.connectAttr(f"{invertMultNode}.outputX", f"{multiNode1}.input2Z", force=True)

    multiNode2 = cmds.shadingNode("multiplyDivide", asUtility=True, name=f"{ctrl1}_multTrans")
    cmds.setAttr(f"{multiNode2}.operation", 1) 
    cmds.connectAttr(f"{ctrl1}.translateY", f"{multiNode2}.input1Y", force=True)
    
    node3 = cmds.shadingNode("plusMinusAverage", asUtility=True, name=f"{ctrl1}_offset")
    cmds.setAttr(f"{node3}.operation", 2)
    cmds.connectAttr(f"{multiNode2}.outputY", f"{node3}.input1D[0]", force=True)

    cmds.connectAttr(f"{ctrl1}.Offset", f"{node3}.input1D[1]",  force=True)

    multiNode4 = cmds.shadingNode("multiplyDivide", asUtility=True, name=f"{ctrl1}_multInvertReverse")
    cmds.setAttr(f"{multiNode4}.operation", 1)
    cmds.connectAttr(f"{node3}.output1D", f"{multiNode4}.input1X")
    cmds.setAttr(f"{multiNode4}.input2X", -1)

    cmds.connectAttr(f"{multiNode4}.outputX", f"{joint2}.translateZ", force=True)

    multiNode5 = cmds.shadingNode("multiplyDivide", asUtility=True, name=f"{ctrl1}_multGradient")
    cmds.setAttr(f"{multiNode5}.operation", 1)
    cmds.connectAttr(f"{ctrl1}.translateY", f"{multiNode5}.input1Y")
    cmds.connectAttr(f"{ctrl1}.Gradient", f"{multiNode5}.input2Y")
    cmds.connectAttr(f"{multiNode5}.outputY", f"{multiNode2}.input2Y", force=True)


def allLipControls():
    connectLipControlToJoint("L_lipMid_CTRL", "L_lipMidRoot_JNT_BIND", "L_lipMid_JNT_END")
    connectLipControlToJoint("L_lipBase_CTRL", "L_lipBaseRoot_JNT_BIND", "L_lipBase_JNT_END")
    connectLipControlToJoint("L_lipUpper_CTRL", "L_lipUpperRoot_JNT_BIND", "L_lipUpper_JNT_END")

    connectLipControlToJoint("R_lipMid_CTRL", "R_lipMidRoot_JNT_BIND", "R_lipMid_JNT_END")
    connectLipControlToJoint("R_lipBase_CTRL", "R_lipBaseRoot_JNT_BIND", "R_lipBase_JNT_END")
    connectLipControlToJoint("R_lipUpper_CTRL", "R_lipUpperRoot_JNT_BIND", "R_lipUpper_JNT_END")

def connectScaleControlToJoint(ctrl, joint):
    cmds.connectAttr(f"{ctrl}.scaleX", f"{joint}.scaleX", force=True)
    cmds.connectAttr(f"{ctrl}.scaleY", f"{joint}.scaleY", force=True)
    cmds.connectAttr(f"{ctrl}.scaleZ", f"{joint}.scaleZ", force=True)

def connectAllScales():
    cmds.select(cl=True)
    connectScaleControlToJoint("L_cheek_CTRL", "L_cheek_JNT_END")
    connectScaleControlToJoint("L_eyebrowFront_CTRL", "L_eyebrowFront_JNT_END")
    connectScaleControlToJoint("L_eyebrowMid_CTRL", "L_eyebrowMid_JNT_END")
    connectScaleControlToJoint("L_eyebrowBack_CTRL", "L_eyebrowBack_JNT_END")

    connectScaleControlToJoint("R_cheek_CTRL", "R_cheek_JNT_END")
    connectScaleControlToJoint("R_eyebrowFront_CTRL", "R_eyebrowFront_JNT_END")
    connectScaleControlToJoint("R_eyebrowMid_CTRL", "R_eyebrowMid_JNT_END")
    connectScaleControlToJoint("R_eyebrowBack_CTRL", "R_eyebrowBack_JNT_END")
