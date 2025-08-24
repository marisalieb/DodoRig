import maya.cmds as cmds
import json
import os
import platform
import sys
import importlib

# for fk ik
def copyAndRenameJointHierarchy(source_joint, new_suffix):

    duplicated_hierarchy = cmds.duplicate(source_joint, renameChildren=True)
    
    new_root_joint = duplicated_hierarchy[0]

    # Rename only the copied hierarchy
    renamed_joints = []
    all_joints = cmds.listRelatives(new_root_joint, allDescendents=True, type="joint") or []
    all_joints.append(new_root_joint)  # Include root joint

    for joint in all_joints:
        original_name = cmds.ls(joint, long=False)[0]

        if "BIND1" in original_name:
            new_name = original_name.replace("BIND1", new_suffix)
            new_name = cmds.rename(joint, new_name)
            renamed_joints.append(new_name)

    return renamed_joints

def deleteJointChildren(parent_joint):
    child_joints = cmds.listRelatives(parent_joint, allDescendents=True, type="joint")

    if child_joints:
        cmds.delete(child_joints)

def unparentJoint(joint_name):

    parent = cmds.listRelatives(joint_name, parent=True)

    if parent:
        cmds.parent(joint_name, world=True)


def setUpFKIKJoints():
    copyAndRenameJointHierarchy("C_COG_JNT_BIND", "FK")
    copyAndRenameJointHierarchy("C_COG_JNT_BIND", "IK")
    deleteJointChildren("C_spineUpper_JNT_FK")
    deleteJointChildren("C_spineUpper_JNT_IK")
    copyAndRenameJointHierarchy("C_neckBase_JNT_BIND", "FK")
    copyAndRenameJointHierarchy("C_neckBase_JNT_BIND", "IK")
    deleteJointChildren("C_neckUpper_JNT_FK")
    deleteJointChildren("C_neckUpper_JNT_IK")
    deleteJointChildren("C_tailUpper_JNT_FK")
    deleteJointChildren("C_tailUpper_JNT_IK")

    unparentJoint("C_COG_JNT_FK")
    unparentJoint("C_COG_JNT_IK")
    unparentJoint("C_neckBase_JNT_FK")
    unparentJoint("C_neckBase_JNT_IK")

    cmds.parent('C_neckBase_JNT_FK', 'C_spineUpper_JNT_FK')
    cmds.parent('C_neckBase_JNT_IK', 'C_spineUpper_JNT_IK')
    
    cmds.delete("C_tailBase_JNT_FK")
    cmds.delete("C_tailBase_JNT_IK")

    copyAndRenameJointHierarchy("L_hip_JNT_BIND", "FK") 
    copyAndRenameJointHierarchy("L_hip_JNT_BIND", "IK") 
    copyAndRenameJointHierarchy("R_hip_JNT_BIND", "FK") 
    copyAndRenameJointHierarchy("R_hip_JNT_BIND", "IK") 
    deleteJointChildren("L_ankle_JNT_FK") 
    deleteJointChildren("L_ankle_JNT_IK") 
    deleteJointChildren("R_ankle_JNT_FK") 
    deleteJointChildren("R_ankle_JNT_IK") 
    unparentJoint("L_hip_JNT_FK") 
    unparentJoint("L_hip_JNT_IK") 
    unparentJoint("R_hip_JNT_FK") 
    unparentJoint("R_hip_JNT_IK") 




def sortIKFK():
    # parent fk
    cmds.parent('L_hip_JNT_FK', 'C_COG_JNT_BIND')
    cmds.parent('R_hip_JNT_FK', 'C_COG_JNT_BIND')
    cmds.parent('L_hip_JNT_IK', 'C_COG_JNT_BIND')
    cmds.parent('R_hip_JNT_IK', 'C_COG_JNT_BIND')

    cmds.parent('C_COG_JNT_FK', 'C_root_JNT_BIND')
    cmds.parent('C_COG_JNT_IK', 'C_root_JNT_BIND')




def createIKs():
    left_ik_handle = cmds.ikHandle(
        sj='L_hip_JNT_IK', 
        ee='L_ankle_JNT_IK', 
        n='L_leg_IKHandle', 
        sol='ikSpringSolver'  
    )[0]
    cmds.setAttr(f'{left_ik_handle}.inheritsTransform', 0)

    right_ik_handle = cmds.ikHandle(
        sj='R_hip_JNT_IK',
        ee='R_ankle_JNT_IK',
        n='R_leg_IKHandle',
        sol='ikSpringSolver'
    )[0]
    cmds.setAttr(f'{right_ik_handle}.inheritsTransform', 0) 

    
    spine_ik_handle = cmds.ikHandle(
        sj='C_COG_JNT_IK', 
        ee='C_neckUpper_JNT_IK', 
        n='C_spine_IKHandle', 
        sol='ikRPsolver'
    )[0]
    cmds.setAttr(f'{spine_ik_handle}.inheritsTransform', 0)



def constrainFKIKToBindJnts():
    
    cmds.parentConstraint('L_hip_JNT_FK', 'L_hip_JNT_BIND', name='L_hip_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('L_femur_JNT_FK', 'L_femur_JNT_BIND', name='L_femur_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('L_knee_JNT_FK', 'L_knee_JNT_BIND', name='L_knee_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('L_ankle_JNT_FK', 'L_ankle_JNT_BIND', name='L_ankle_JNT_FK_parentConst', mo=False)

    cmds.parentConstraint('R_hip_JNT_FK', 'R_hip_JNT_BIND', name='R_hip_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('R_femur_JNT_FK', 'R_femur_JNT_BIND', name='R_femur_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('R_knee_JNT_FK', 'R_knee_JNT_BIND', name='R_knee_JNT_FK_parentConst', mo=False)
    cmds.parentConstraint('R_ankle_JNT_FK', 'R_ankle_JNT_BIND', name='R_ankle_JNT_FK_parentConst', mo=False)

    cmds.parentConstraint('L_hip_JNT_IK', 'L_hip_JNT_BIND', name='L_hip_JNT_IK_parentConst', mo=False)
    cmds.parentConstraint('L_femur_JNT_IK', 'L_femur_JNT_BIND', name='L_femur_JNT_IK_parentConst', mo=False) 
    cmds.parentConstraint('L_knee_JNT_IK', 'L_knee_JNT_BIND', name='L_knee_JNT_IK_parentConst', mo=False) 
    cmds.parentConstraint('L_ankle_JNT_IK', 'L_ankle_JNT_BIND', name='L_ankle_JNT_IK_parentConst', mo=False)

    cmds.parentConstraint('R_hip_JNT_IK', 'R_hip_JNT_BIND', name='R_hip_JNT_IK_parentConst', mo=False)
    cmds.parentConstraint('R_femur_JNT_IK', 'R_femur_JNT_BIND', name='R_femur_JNT_IK_parentConst', mo=False)
    cmds.parentConstraint('R_knee_JNT_IK', 'R_knee_JNT_BIND', name='R_knee_JNT_IK_parentConst', mo=False)
    cmds.parentConstraint('R_ankle_JNT_IK', 'R_ankle_JNT_BIND', name='R_ankle_JNT_IK_parentConst', mo=False)

    cmds.parentConstraint('C_COG_JNT_FK', 'C_COG_JNT_BIND', name='C_COG_JNT_FK_parentConst', mo=True)
    cmds.parentConstraint('C_COG_JNT_IK', 'C_COG_JNT_BIND', name='C_COG_JNT_IK_parentConst', mo=True)

    cmds.parentConstraint('C_spineBase_JNT_FK', 'C_spineBase_JNT_BIND', name='C_spineBase_JNT_FK_parentConst', mo=True)
    cmds.parentConstraint('C_spineMid_JNT_FK', 'C_spineMid_JNT_BIND', name='C_spineMid_JNT_FK_parentConst', mo=True)
    cmds.parentConstraint('C_spineUpper_JNT_FK', 'C_spineUpper_JNT_BIND', name='C_spineUpper_JNT_FK_parentConst', mo=True)

    cmds.parentConstraint('C_spineBase_JNT_IK', 'C_spineBase_JNT_BIND', name='C_spineBase_JNT_IK_parentConst', mo=True)
    cmds.parentConstraint('C_spineMid_JNT_IK', 'C_spineMid_JNT_BIND', name='C_spineMid_JNT_IK_parentConst', mo=True)
    cmds.parentConstraint('C_spineUpper_JNT_IK', 'C_spineUpper_JNT_BIND', name='C_spineUpper_JNT_IK_parentConst', mo=True)

    cmds.parentConstraint('C_neckBase_JNT_FK', 'C_neckBase_JNT_BIND', name='C_neckBase_JNT_FK_parentConst', mo=True)
    cmds.parentConstraint('C_neckMid_JNT_FK', 'C_neckMid_JNT_BIND', name='C_neckMid_JNT_FK_parentConst', mo=True)
    cmds.parentConstraint('C_neckUpper_JNT_FK', 'C_neckUpper_JNT_BIND', name='C_neckUpper_JNT_FK_parentConst', mo=True)

    cmds.parentConstraint('C_neckBase_JNT_IK', 'C_neckBase_JNT_BIND', name='C_neckBase_JNT_IK_parentConst', mo=True)
    cmds.parentConstraint('C_neckMid_JNT_IK', 'C_neckMid_JNT_BIND', name='C_neckMid_JNT_IK_parentConst', mo=True)
    cmds.parentConstraint('C_neckUpper_JNT_IK', 'C_neckUpper_JNT_BIND', name='C_neckUpper_JNT_IK_parentConst', mo=True)






def setupIKFKBlend(main_ctrl, fk_joints, ik_joints, bind_joints, switch_attr):
    # Check if the switch attribute exists on the main control, if not, create it
    if not cmds.attributeQuery(switch_attr, node=main_ctrl, exists=True):
        cmds.addAttr(main_ctrl, ln=switch_attr, at="float", min=0, max=1, defaultValue=0, k=True)

    # Loop through all joints to connect the IK/FK blending
    for i in range(len(bind_joints)):
        # Find the parent constraint on the bind joint
        constraints = cmds.listRelatives(bind_joints[i], type="parentConstraint") or []
        if not constraints:
            print(f"Warning: No parentConstraint found on {bind_joints[i]}")
            continue  # Skip this joint if no constraint is found
        
        parent_constraint = constraints[0]  # Get the first (and only) parentConstraint

        # Get the constraint target weights
        targets = cmds.parentConstraint(parent_constraint, query=True, targetList=True)
        if len(targets) != 2:
            print(f"Warning: Expected 2 targets (FK & IK) in {parent_constraint}, but found {len(targets)}")
            continue  # Skip if there aren't exactly 2 targets

        fk_weight_attr = f"{parent_constraint}.w0"  # First target Fk in this case
        ik_weight_attr = f"{parent_constraint}.w1"  

        # Connect the IK/FK switch to the constraint weights
        cmds.connectAttr(f"{main_ctrl}.{switch_attr}", ik_weight_attr, force=True)
        
        # Reverse the FK weight so that when IK is 1, FK is 0, and vice versa
        rev_node = cmds.shadingNode("reverse", asUtility=True, name=f"ikFkReverse_{bind_joints[i]}")
        cmds.connectAttr(f"{main_ctrl}.{switch_attr}", f"{rev_node}.inputX", force=True)
        cmds.connectAttr(f"{rev_node}.outputX", fk_weight_attr, force=True)

    for ctrl in fk_joints + ik_joints:
        if cmds.objExists(ctrl) and not cmds.attributeQuery(switch_attr, node=ctrl, exists=True):
            cmds.addAttr(ctrl, ln=switch_attr, at="float", min=0, max=1, k=True,
                            proxy=f"{main_ctrl}.{switch_attr}")

    print("IK/FK blending setup completed for all joints.")


def setupIKFKBlendForAll():
    main_ctrl = "C_main_CTRL"  # main controller

    L_fk_joints = ["L_hipFK_CTRL", "L_femurFK_CTRL", "L_kneeFK_CTRL", "L_ankleFK_CTRL"]  # FK joints
    L_ik_joints = ["L_footIK_CTRL"]  # IK joints
    L_bind_joints = ["L_hip_JNT_BIND","L_femur_JNT_BIND", "L_knee_JNT_BIND", "L_ankle_JNT_BIND", "L_footFK_CTRL_ZERO"] # , "L_footFK_CTRL_ZERO"
    L_switch_attr = "L_Leg_IK_FK_Blend"
    setupIKFKBlend(main_ctrl, L_fk_joints, L_ik_joints, L_bind_joints, L_switch_attr)

    L_fk_joints_vis = ["L_hipFK_CTRL", "L_femurFK_CTRL", "L_kneeFK_CTRL", "L_ankleFK_CTRL", "L_hip_JNT_FK", "L_femur_JNT_FK", "L_knee_JNT_FK", "L_ankle_JNT_FK"]  # FK joints
    L_ik_joints_vis = ["L_footIK_CTRL", "L_hip_JNT_IK", "L_femur_JNT_IK", "L_knee_JNT_IK", "L_ankle_JNT_IK"]  # IK joints
    setupIKFKVisibility(main_ctrl, L_fk_joints_vis, L_ik_joints_vis, L_switch_attr)

    R_fk_joints = ["R_hipFK_CTRL", "R_femurFK_CTRL", "R_kneeFK_CTRL", "R_ankleFK_CTRL"]  # FK joints
    R_ik_joints = ["R_footIK_CTRL"]  # IK joints
    R_bind_joints = ["R_hip_JNT_BIND", "R_femur_JNT_BIND", "R_knee_JNT_BIND", "R_ankle_JNT_BIND", "R_footFK_CTRL_ZERO"]
    R_switch_attr = "R_Leg_IK_FK_Blend"
    setupIKFKBlend(main_ctrl, R_fk_joints, R_ik_joints, R_bind_joints, R_switch_attr)

    R_fk_joints_vis = ["R_hipFK_CTRL", "R_femurFK_CTRL", "R_kneeFK_CTRL", "R_ankleFK_CTRL", "R_hip_JNT_FK", "R_femur_JNT_FK", "R_knee_JNT_FK", "R_ankle_JNT_FK"]  # FK joints
    R_ik_joints_vis = ["R_footIK_CTRL", "R_hip_JNT_IK", "R_femur_JNT_IK", "R_knee_JNT_IK", "R_ankle_JNT_IK"]  # IK joints

    setupIKFKVisibility(main_ctrl, R_fk_joints_vis, R_ik_joints_vis, R_switch_attr)

    spineFKJoints = ["C_COGFK_CTRL", "C_spineMidFK_CTRL", "C_spineUpperFK_CTRL", "C_neckBaseFK_CTRL", "C_neckUpperFK_CTRL"]
    spineIKJoints = ["C_spineIK_CTRL"]
    spineBindJoints = ["C_COG_JNT_BIND", "C_spineBase_JNT_BIND", "C_spineMid_JNT_BIND", "C_spineUpper_JNT_BIND", "C_neckBase_JNT_BIND", "C_neckMid_JNT_BIND", "C_neckUpper_JNT_BIND", "C_headBase_CTRL_ZERO", "C_tailBase_CTRL_ZERO", "L_scapula_CTRL_ZERO", "R_scapula_CTRL_ZERO"] #!!!!
    spineSwitch = "Spine_IK_FK_Blend"
    setupIKFKBlend(main_ctrl, spineFKJoints, spineIKJoints, spineBindJoints, spineSwitch)
    setupIKFKVisibility(main_ctrl, spineFKJoints, spineIKJoints, spineSwitch)
   


def setupIKFKVisibility(main_ctrl, fk_controls, ik_controls, switch_attr):

    # Expression for FK visibility (visible when switch_attr is between 0 and 0.995)
    fk_expr = 'if ({0}.{1} <= 0.995) {{\n'.format(main_ctrl, switch_attr)
    for ctrl in fk_controls:
        fk_expr += '{0}.visibility = 1;\n'.format(ctrl)  # Make FK controls visible
    fk_expr += '} else {\n'
    for ctrl in fk_controls:
        fk_expr += '{0}.visibility = 0;\n'.format(ctrl)  # Hide FK controls
    fk_expr += '}\n'

    # Create the expression for FK visibility
    cmds.expression(s=fk_expr, name="fkVisibilityExpr", alwaysEvaluate=True)

    # Expression for IK visibility (visible when switch_attr is between 0.005 and 1)
    ik_expr = 'if ({0}.{1} >= 0.005) {{\n'.format(main_ctrl, switch_attr)
    for ctrl in ik_controls:
        ik_expr += '{0}.visibility = 1;\n'.format(ctrl)  # Make IK controls visible
    ik_expr += '} else {\n'
    for ctrl in ik_controls:
        ik_expr += '{0}.visibility = 0;\n'.format(ctrl)  # Hide IK controls
    ik_expr += '}\n'

    # Create the expression for IK visibility
    cmds.expression(s=ik_expr, name="ikVisibilityExpr", alwaysEvaluate=True)

    print("IK/FK visibility switching setup with expressions completed.")


def fixPostIKFK(): # like the joints and controls that come after the IK FK blend so they follow both ik and fk correctly
    cmds.parentConstraint('L_ankle_JNT_FK', 'L_footFK_CTRL_ZERO', name='L_footIFK_parentConst', mo=True)
    cmds.parentConstraint('L_ankle_JNT_IK', 'L_footFK_CTRL_ZERO', name='L_footIFK_parentConst', mo=True)

    cmds.parentConstraint('R_ankle_JNT_FK', 'R_footFK_CTRL_ZERO', name='R_footIFK_parentConst', mo=True)
    cmds.parentConstraint('R_ankle_JNT_IK', 'R_footFK_CTRL_ZERO', name='R_footIFK_parentConst', mo=True)


    # spine fixes
    cmds.parentConstraint('C_neckUpper_JNT_FK', 'C_headBase_CTRL_ZERO', name='C_headIFK_parentConst', mo=True)
    cmds.parentConstraint('C_neckUpper_JNT_IK', 'C_headBase_CTRL_ZERO', name='C_headIFK_parentConst', mo=True)

    cmds.parentConstraint('C_COG_JNT_FK', 'C_tailBase_CTRL_ZERO', name='C_tailIFK_parentConst', mo=True)
    cmds.parentConstraint('C_COG_JNT_IK', 'C_tailBase_CTRL_ZERO', name='C_tailIFK_parentConst', mo=True)

    cmds.parentConstraint('C_spineUpper_JNT_FK', 'L_scapula_CTRL_ZERO', name='L_scapulaIFK_parentConst', mo=True) # !!!
    cmds.parentConstraint('C_spineUpper_JNT_IK', 'L_scapula_CTRL_ZERO', name='L_scapulaIFK_parentConst', mo=True)# !!!!

    cmds.parentConstraint('C_spineUpper_JNT_FK', 'R_scapula_CTRL_ZERO', name='R_scapulaIFK_parentConst', mo=True)
    cmds.parentConstraint('C_spineUpper_JNT_IK', 'R_scapula_CTRL_ZERO', name='R_scapulaIFK_parentConst', mo=True)

