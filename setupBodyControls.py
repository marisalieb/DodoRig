import maya.cmds as cmds
import json
import os
import platform
import sys
import importlib

from controls import createControl, createSquareControl, createPoleVector

 

# create each control with the function above
def createAllControls():
    createControl('main', 'C', [0, 1, 0], 21, 'null', False, False)

    # Spine and Root
    createControl('root', 'C', [0, 1, 0], 24, 'C_root_JNT_BIND', True, True)

    createControl('COGFK', 'C', [1, 0, 0], 1, 'C_COG_JNT_FK', True, True)
    createControl('spineMidFK', 'C', [1, 0, 0], 17, 'C_spineMid_JNT_FK', True, True)
    createControl('spineUpperFK', 'C', [1, 0, 0], 1, 'C_spineUpper_JNT_FK', True, True)
    createControl('neckBaseFK', 'C', [1, 0, 0], 10, 'C_neckBase_JNT_FK', True, True)
    createControl('neckUpperFK', 'C', [1, 0, 0], 8, 'C_neckUpper_JNT_FK', True, True)

    createControl('headBase', 'C', [1, 0, 0], 1, 'C_headBase_JNT_BIND', True, True)

    # Tail
    createControl('tailBase', 'C', [1, 0, 0], 1, 'C_tailBase_JNT_BIND', True, True)
    createControl('tailUpper', 'C', [1, 0, 0], 6, 'C_tailUpper_JNT_BIND', True, True)
    
    createControl('jawStart', 'C', [1, 0, 0], 5, 'C_jawStart_JNT_BIND', True, True)
    
    # Eyes
    createControl('eye', 'L', [1, 0, 0], 1, 'L_eyeEnd_JNT_END', True, True)
    # Arm
    createControl('scapula', 'L', [1, 0, 0], 8, 'L_scapula_JNT_BIND', True, True)

    # Fingers
    createControl('fingerStart01', 'L', [1, 0, 0], 3, 'L_fingerStart01_JNT_BIND', True, True)
    createControl('fingerMid01', 'L', [1, 0, 0], 3, 'L_fingerMid01_JNT_BIND', True, True)
    createControl('fingerStart02', 'L', [1, 0, 0], 3, 'L_fingerStart02_JNT_BIND', True, True)
    createControl('fingerMid02', 'L', [1, 0, 0], 3, 'L_fingerMid02_JNT_BIND', True, True)
    
    # Leg
    createControl('hipFK', 'L', [1, 0, 0], 10, 'L_hip_JNT_FK', True, True)
    
    # Toes
    createControl('footFK', 'L', [1, 0, 0], 1, 'L_heel_JNT_BIND', True, True) # might have to set this to true true, check later 


    # Eyes
    createControl('eye', 'R', [1, 0, 0], 1, 'R_eyeEnd_JNT_END', True, True)
    # Arm
    createControl('scapula', 'R', [1, 0, 0], 8, 'R_scapula_JNT_BIND', True, True)

    # Fingers
    createControl('fingerStart01', 'R', [1, 0, 0], 3, 'R_fingerStart01_JNT_BIND', True, True)
    createControl('fingerMid01', 'R', [1, 0, 0], 3, 'R_fingerMid01_JNT_BIND', True, True)
    createControl('fingerStart02', 'R', [1, 0, 0], 3, 'R_fingerStart02_JNT_BIND', True, True)
    createControl('fingerMid02', 'R', [1, 0, 0], 3, 'R_fingerMid02_JNT_BIND', True, True)

    # Leg
    createControl('hipFK', 'R', [1, 0, 0], 10, 'R_hip_JNT_FK', True, True)

    # # Toes
    createControl('footFK', 'R', [1, 0, 0], 1, 'R_heel_JNT_BIND', True, True)


    # leg FKs
    createControl('femurFK', 'L', [1, 0, 0], 11, 'L_femur_JNT_FK', True, True)
    createControl('kneeFK', 'L', [1, 0, 0], 9, 'L_knee_JNT_FK', True, True)
    createControl('ankleFK', 'L', [1, 0, 0], 6, 'L_ankle_JNT_FK', True, True)
    createControl('femurFK', 'R', [1, 0, 0], 11, 'R_femur_JNT_FK', True, True)
    createControl('kneeFK', 'R', [1, 0, 0], 9, 'R_knee_JNT_FK', True, True)
    createControl('ankleFK', 'R', [1, 0, 0], 6, 'R_ankle_JNT_FK', True, True)

    createControl('shoulder', 'L', [1, 0, 0], 7, 'L_shoulder_JNT_BIND', True, True)
    # elbow a
    createControl('elbowA', 'L', [1, 0, 0], 1, 'L_elbowA_JNT_BIND', True, True)
    createControl('elbowB', 'L', [1, 0, 0], 1, 'L_elbowB_JNT_BIND', True, True)
    createControl('elbowC', 'L', [1, 0, 0], 1, 'L_elbowC_JNT_BIND', True, True)
    createControl('elbowD', 'L', [1, 0, 0], 1, 'L_elbowD_JNT_BIND', True, True)
    createControl('elbowE', 'L', [1, 0, 0], 1, 'L_elbowE_JNT_BIND', True, True)

    createControl('wrist', 'L', [1, 0, 0], 5, 'L_wrist_JNT_BIND', True, True)

    createControl('shoulder', 'R', [1, 0, 0], 7, 'R_shoulder_JNT_BIND', True, True)
    # elbow a
    createControl('elbowA', 'R', [1, 0, 0], 1, 'R_elbowA_JNT_BIND', True, True)
    createControl('elbowB', 'R', [1, 0, 0], 1, 'R_elbowB_JNT_BIND', True, True)
    createControl('elbowC', 'R', [1, 0, 0], 1, 'R_elbowC_JNT_BIND', True, True)
    createControl('elbowD', 'R', [1, 0, 0], 1, 'R_elbowD_JNT_BIND', True, True)
    createControl('elbowE', 'R', [1, 0, 0], 1, 'R_elbowE_JNT_BIND', True, True)

    createControl('wrist', 'R', [1, 0, 0], 5, 'R_wrist_JNT_BIND', True, True)


    createSquareControl("footIK", "L", 5, 'L_leg_IKHandle', True, True)
    createSquareControl("footIK", "R", 5, 'R_leg_IKHandle', True, True)

    createSquareControl("spineIK", "C", 10, 'C_spine_IKHandle', True, True)

    # # create pole vectors for the IK handles
    createPoleVector('legPV', 'L', [0, 1, 0], 'L_hip_JNT_IK', 'L_femur_JNT_IK', 'L_knee_JNT_IK', 'L_ankle_JNT_IK')
    createPoleVector('legPV', 'R', [0, 1, 0], 'R_hip_JNT_IK', 'R_femur_JNT_IK', 'R_knee_JNT_IK', 'R_ankle_JNT_IK')


# CONTROLS

# constrain controls to each joint
def constrainControls():
    cmds.parentConstraint('C_root_CTRL', 'C_root_JNT_BIND', name = 'C_root_CTRL_parentConst', mo=False)

    cmds.parentConstraint('C_tailBase_CTRL', 'C_tailBase_JNT_BIND', name='C_tailBase_CTRL_parentConst', mo=False)
    cmds.parentConstraint('C_tailUpper_CTRL', 'C_tailUpper_JNT_BIND', name='C_tailUpper_CTRL_parentConst', mo=False)

    # For spine hierarchy
    cmds.parentConstraint('C_COGFK_CTRL', 'C_COG_JNT_FK', name = 'C_COG_CTRLFK_parentConst', mo=False)
    cmds.parentConstraint('C_spineMidFK_CTRL', 'C_spineMid_JNT_FK', name = 'C_spineMid_CTRLFK_parentConst', mo=False)
    cmds.parentConstraint('C_spineUpperFK_CTRL', 'C_spineUpper_JNT_FK', name = 'C_spineUpper_CTRLFK_parentConst', mo=False)
    # For neck hierarchy
    cmds.parentConstraint('C_neckBaseFK_CTRL', 'C_neckBase_JNT_FK', name = 'C_neckBase_CTRLFK_parentConst', mo=False)
    cmds.parentConstraint('C_neckUpperFK_CTRL', 'C_neckUpper_JNT_FK', name = 'C_neckUpper_CTRLFK_parentConst', mo=False)

    # For head hierarchy
    cmds.parentConstraint('C_headBase_CTRL', 'C_headBase_JNT_BIND', name='C_headBase_CTRL_orientConst', mo=False)

    # For jaw and tongue joints
    cmds.parentConstraint('C_jawStart_CTRL', 'C_jawStart_JNT_BIND', name='C_jawStart_CTRL_orientConst', mo=False)

    # For left leg hierarchy
    cmds.parentConstraint('L_hipFK_CTRL', 'L_hip_JNT_FK', name='L_hip_CTRL_orientConst', mo=False)

    cmds.parentConstraint('L_footFK_CTRL', 'L_heel_JNT_BIND', name='L_footFK_CTRL_orientConst', mo=False)


    # For shoulder and arm hierarchy
    cmds.parentConstraint('L_scapula_CTRL', 'L_scapula_JNT_BIND', name='L_scapula_CTRL_orientConst', mo=False)


    # For finger joints
    cmds.parentConstraint('L_fingerStart01_CTRL', 'L_fingerStart01_JNT_BIND', name='L_fingerStart01_CTRL_orientConst', mo=False)
    cmds.parentConstraint('L_fingerMid01_CTRL', 'L_fingerMid01_JNT_BIND', name='L_fingerMid01_CTRL_orientConst', mo=False)
    cmds.parentConstraint('L_fingerStart02_CTRL', 'L_fingerStart02_JNT_BIND', name='L_fingerStart02_CTRL_orientConst', mo=False)
    cmds.parentConstraint('L_fingerMid02_CTRL', 'L_fingerMid02_JNT_BIND', name='L_fingerMid02_CTRL_orientConst', mo=False)


    # add RIGHT SIDE!!!!!
    # For right leg hierarchy
    cmds.parentConstraint('R_hipFK_CTRL', 'R_hip_JNT_FK', name='R_hip_CTRL_orientConst', mo=False)



    cmds.parentConstraint('R_footFK_CTRL', 'R_heel_JNT_BIND', name='R_footFK_CTRL_orientConst', mo=False)

    # For shoulder and arm hierarchy
    cmds.parentConstraint('R_scapula_CTRL', 'R_scapula_JNT_BIND', name='R_scapula_CTRL_orientConst', mo=False)

    # For finger joints
    cmds.parentConstraint('R_fingerStart01_CTRL', 'R_fingerStart01_JNT_BIND', name='R_fingerStart01_CTRL_orientConst', mo=False)
    cmds.parentConstraint('R_fingerMid01_CTRL', 'R_fingerMid01_JNT_BIND', name='R_fingerMid01_CTRL_orientConst', mo=False)
    cmds.parentConstraint('R_fingerStart02_CTRL', 'R_fingerStart02_JNT_BIND', name='R_fingerStart02_CTRL_orientConst', mo=False)
    cmds.parentConstraint('R_fingerMid02_CTRL', 'R_fingerMid02_JNT_BIND', name='R_fingerMid02_CTRL_orientConst', mo=False)

    # legs ik fk 
    
    cmds.parentConstraint('L_femurFK_CTRL', 'L_femur_JNT_FK', name='L_femurFK_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_kneeFK_CTRL', 'L_knee_JNT_FK', name='L_kneeFK_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_ankleFK_CTRL', 'L_ankle_JNT_FK', name='L_ankleFK_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_femurFK_CTRL', 'R_femur_JNT_FK', name='R_femurFK_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_kneeFK_CTRL', 'R_knee_JNT_FK', name='R_kneeFK_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_ankleFK_CTRL', 'R_ankle_JNT_FK', name='R_ankleFK_CTRL_parentConst', mo=False)

    cmds.parentConstraint('L_shoulder_CTRL', 'L_shoulder_JNT_BIND', name='L_shoulder_CTRL_parentConst', mo=False)
    # elbow d
    cmds.parentConstraint('L_elbowA_CTRL', 'L_elbowA_JNT_BIND', name='L_elbowA_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_elbowB_CTRL', 'L_elbowB_JNT_BIND', name='L_elbowB_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_elbowC_CTRL', 'L_elbowC_JNT_BIND', name='L_elbowC_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_elbowD_CTRL', 'L_elbowD_JNT_BIND', name='L_elbowD_CTRL_parentConst', mo=False)
    cmds.parentConstraint('L_elbowE_CTRL', 'L_elbowE_JNT_BIND', name='L_elbowE_CTRL_parentConst', mo=False)

    cmds.parentConstraint('L_wrist_CTRL', 'L_wrist_JNT_BIND', name='L_wrist_CTRL_parentConst', mo=False)

    cmds.parentConstraint('R_shoulder_CTRL', 'R_shoulder_JNT_BIND', name='R_shoulder_CTRL_parentConst', mo=False)
    # elbow d
    cmds.parentConstraint('R_elbowA_CTRL', 'R_elbowA_JNT_BIND', name='R_elbowA_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_elbowB_CTRL', 'R_elbowB_JNT_BIND', name='R_elbowB_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_elbowC_CTRL', 'R_elbowC_JNT_BIND', name='R_elbowC_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_elbowD_CTRL', 'R_elbowD_JNT_BIND', name='R_elbowD_CTRL_parentConst', mo=False)
    cmds.parentConstraint('R_elbowE_CTRL', 'R_elbowE_JNT_BIND', name='R_elbowE_CTRL_parentConst', mo=False)


    cmds.parentConstraint('R_wrist_CTRL', 'R_wrist_JNT_BIND', name='R_wrist_CTRL_parentConst', mo=False)

    cmds.pointConstraint('L_footIK_CTRL', 'L_leg_IKHandle', n='L_footIK_CTRL_Const', mo=True)
    cmds.orientConstraint('L_footIK_CTRL', 'L_leg_IKHandle', n='L_footIK_RotConst', mo=True)
    cmds.orientConstraint('L_leg_IKHandle', 'L_ankle_JNT_IK', mo=True)

    cmds.pointConstraint('R_footIK_CTRL', 'R_leg_IKHandle', n='R_footIK_CTRL_Const', mo=True)
    cmds.orientConstraint('R_footIK_CTRL', 'R_leg_IKHandle', n='R_footIK_RotConst', mo=True)
    cmds.orientConstraint('R_leg_IKHandle', 'R_ankle_JNT_IK', mo=True)


    cmds.pointConstraint('C_spineIK_CTRL', 'C_spine_IKHandle', n='C_spineIK_CTRL_Const', mo=True)
    cmds.orientConstraint('C_spineIK_CTRL', 'C_spine_IKHandle', n='C_spineIK_RotConst', mo=True)
    cmds.orientConstraint('C_spine_IKHandle', 'C_neckUpper_JNT_IK', mo=True)

   
    # # pole vector constraints
    cmds.poleVectorConstraint('L_legPV_CTRL', 'L_leg_IKHandle', n='L_legPV_CTRL_poleVecConst')
    cmds.poleVectorConstraint('R_legPV_CTRL', 'R_leg_IKHandle', n='R_legPV_CTRL_poleVecConst')



# parent the controls
def parentControls():
    # correct this for ends of each limb
    cmds.parent('C_root_CTRL_ZERO', 'C_main_CTRL') # 'L_wrist_CTRL_ZERO', 'R_wrist_CTRL_ZERO', /// 'R_heel_CTRL_ZERO', 'L_heel_CTRL_ZERO',, 'L_heel_CTRL_ZERO', 'R_heel_CTRL_ZERO', # 'L_armIK_CTRL_ZERO', 'R_armIK_CTRL_ZERO', 'L_legIK_CTRL_ZERO', 'R_legIK_CTRL_ZERO',
    
    # now parent one by one in pairs in the order so to parent, parent second
    cmds.parent('C_spineIK_CTRL_ZERO', 'C_root_CTRL')

    # parent cog to root
    cmds.parent('C_COGFK_CTRL_ZERO', 'C_root_CTRL')

    # # Spine hierarchy
    cmds.parent('C_spineMidFK_CTRL_ZERO', 'C_COGFK_CTRL')
    cmds.parent('C_spineUpperFK_CTRL_ZERO', 'C_spineMidFK_CTRL')

    # # Neck hierarchy
    cmds.parent('C_neckBaseFK_CTRL_ZERO', 'C_spineMidFK_CTRL')
    cmds.parent('C_neckUpperFK_CTRL_ZERO', 'C_neckBaseFK_CTRL')

    # Tail 
    cmds.parent('C_tailBase_CTRL_ZERO', 'C_root_CTRL')
    cmds.parent('C_tailUpper_CTRL_ZERO', 'C_tailBase_CTRL')

    cmds.parent('C_headBase_CTRL_ZERO', 'C_root_CTRL')


    # Jaw and tongue hierarchy
    cmds.parent('C_jawStart_CTRL_ZERO', 'C_headBase_CTRL')

    # Eye hierarchy
    cmds.parent('L_eye_CTRL_ZERO', 'C_headBase_CTRL')

    # Left leg hierarchy
    cmds.parent('L_hipFK_CTRL_ZERO', 'C_root_CTRL')

    # # heel
    cmds.parent('L_footFK_CTRL_ZERO', 'C_root_CTRL') #'L_hipFK_CTRL')

    # Arm hierarchy
    cmds.parent('L_scapula_CTRL_ZERO', 'C_root_CTRL')

    # Fingers hierarchy
    cmds.parent('L_fingerStart01_CTRL_ZERO', 'L_wrist_CTRL')
    cmds.parent('L_fingerMid01_CTRL_ZERO', 'L_fingerStart01_CTRL')

    cmds.parent('L_fingerStart02_CTRL_ZERO', 'L_wrist_CTRL')
    cmds.parent('L_fingerMid02_CTRL_ZERO', 'L_fingerStart02_CTRL')

    # Right side

    # Eye hierarchy
    cmds.parent('R_eye_CTRL_ZERO', 'C_headBase_CTRL')

    # Right leg hierarchy
    cmds.parent('R_hipFK_CTRL_ZERO', 'C_root_CTRL')

    # Toes hierarchy (starting from heel joint)
    cmds.parent('R_footFK_CTRL_ZERO', 'C_root_CTRL')

    # Arm hierarchy
    cmds.parent('R_scapula_CTRL_ZERO', 'C_root_CTRL')


    # Fingers hierarchy
    cmds.parent('R_fingerStart01_CTRL_ZERO', 'R_wrist_CTRL')
    cmds.parent('R_fingerMid01_CTRL_ZERO', 'R_fingerStart01_CTRL')

    cmds.parent('R_fingerStart02_CTRL_ZERO', 'R_wrist_CTRL')
    cmds.parent('R_fingerMid02_CTRL_ZERO', 'R_fingerStart02_CTRL')

    # legs ik fk, add femur

    cmds.parent('L_femurFK_CTRL_ZERO', 'L_hipFK_CTRL')
    cmds.parent('L_kneeFK_CTRL_ZERO', 'L_femurFK_CTRL')
    cmds.parent('L_ankleFK_CTRL_ZERO', 'L_kneeFK_CTRL')

    cmds.parent('R_femurFK_CTRL_ZERO', 'R_hipFK_CTRL')
    cmds.parent('R_kneeFK_CTRL_ZERO', 'R_femurFK_CTRL')
    cmds.parent('R_ankleFK_CTRL_ZERO', 'R_kneeFK_CTRL')

    cmds.parent('L_shoulder_CTRL_ZERO', 'L_scapula_CTRL') # scapula !!!!!!!
    # elbow d

    cmds.parent('L_elbowA_CTRL_ZERO', 'L_shoulder_CTRL')
    cmds.parent('L_elbowB_CTRL_ZERO', 'L_elbowA_CTRL')
    cmds.parent('L_elbowC_CTRL_ZERO', 'L_elbowB_CTRL')
    cmds.parent('L_elbowD_CTRL_ZERO', 'L_elbowC_CTRL')
    cmds.parent('L_elbowE_CTRL_ZERO', 'L_elbowD_CTRL')

    cmds.parent('L_wrist_CTRL_ZERO', 'L_elbowE_CTRL')

    cmds.parent('R_shoulder_CTRL_ZERO', 'R_scapula_CTRL')
    # elbow d

    cmds.parent('R_elbowA_CTRL_ZERO', 'R_shoulder_CTRL')
    cmds.parent('R_elbowB_CTRL_ZERO', 'R_elbowA_CTRL')
    cmds.parent('R_elbowC_CTRL_ZERO', 'R_elbowB_CTRL')
    cmds.parent('R_elbowD_CTRL_ZERO', 'R_elbowC_CTRL')
    cmds.parent('R_elbowE_CTRL_ZERO', 'R_elbowD_CTRL')

    cmds.parent('R_wrist_CTRL_ZERO', 'R_elbowE_CTRL')

    # pole and ik
    cmds.parent('L_legPV_CTRL_ZERO', 'C_main_CTRL') # or C_root_CTRL
    cmds.parent('R_legPV_CTRL_ZERO', 'C_main_CTRL') # or C_root_CTRL
    cmds.parent('L_footIK_CTRL_ZERO', 'C_main_CTRL')
    cmds.parent('R_footIK_CTRL_ZERO', 'C_main_CTRL')

    cmds.select(cl=True)
    cmds.group('L_leg_IKHandle', 'R_leg_IKHandle', 'C_spine_IKHandle', n='IKs') # 'C_spine_IKHandle',       'L_arm_IKHandle', 'R_arm_IKHandle', 'L_leg_IKHandle', 'R_leg_IKHandle'
    cmds.group('C_main_CTRL_ZERO', n='CONTROLS') # 'R_legPV_CTRL_ZERO', 'L_legPV_CTRL_ZERO', 'L_footIK_CTRL_ZERO'
    cmds.group('C_root_JNT_BIND', n= 'JOINTS')
    cmds.group('JOINTS', 'CONTROLS', 'IKs',  n='Dodo_Rig') #'IKs',



# for Fk spine joints and neck joints, adjust rotation weights for more antural movement
def adjustJointWeights(ctrl1, ctrl2, mid_joints):
    # Get number of joints for even weight distribution
    num_joints = len(mid_joints) + 1  # +1 because we have two controllers

    # Apply constraints with proportional weights
    for i, joint in enumerate(mid_joints):
        weight1 = 1.0 - (i + 1) / num_joints  # Influence from the first controller
        weight2 = (i + 1) / num_joints  # Influence from the second controller
        
        # Create the point constraint with calculated weights
        constraint = cmds.orientConstraint(ctrl1, ctrl2, joint, mo=True)[0]
        
        # Get constraint target weight attributes
        target_weights = cmds.orientConstraint(constraint, q=True, weightAliasList=True)
        
        # Set individual weights correctly
        cmds.setAttr(f"{constraint}.{target_weights[0]}", weight1)
        cmds.setAttr(f"{constraint}.{target_weights[1]}", weight2)

    print("Constraints applied successfully!")



def adjustAllJointWeights():
    ctrl1Neck = "C_neckBaseFK_CTRL"  # The upper controller
    ctrl2Neck = "C_neckUpperFK_CTRL"  # The lower controller
    midJointsNeck = ["C_neckMid_JNT_FK"]  # The joints to adjust between the controllers
    adjustJointWeights(ctrl1Neck, ctrl2Neck, midJointsNeck)

    ctrl1Tail = "C_tailUpper_CTRL" 
    ctrl2Tail = "C_COGFK_CTRL" 
    midJointsTail = ["C_tailMid_JNT_BIND"]
    adjustJointWeights(ctrl1Tail, ctrl2Tail, midJointsTail)

    ctrl1Spine = "C_spineMidFK_CTRL" 
    ctrl2Spine = "C_COGFK_CTRL" 
    midJointsSpine = ["C_spineBase_JNT_FK"] 
    adjustJointWeights(ctrl1Spine, ctrl2Spine, midJointsSpine)

    ctrl1NeckSpine = "C_spineMidFK_CTRL"
    ctrl2NeckSpine = "C_neckBaseFK_CTRL"
    midJointsNeckSpine = ["C_spineUpperFK_CTRL"]
    adjustJointWeights(ctrl1NeckSpine, ctrl2NeckSpine, midJointsNeckSpine)