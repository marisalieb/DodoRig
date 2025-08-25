import maya.cmds as cmds
import json
import os
import platform
import sys
import importlib
 

def ensureAttributeExists(ctrl, attr_name, min_val=None, max_val=None):
    if not cmds.attributeQuery(attr_name, node=ctrl, exists=True):
        cmds.addAttr(ctrl, longName=attr_name, attributeType="float", keyable=True, 
                     min=min_val if min_val is not None else -10,  # default min
                     max=max_val if max_val is not None else 10,   # default max
                     defaultValue=0)
        print(f"Attribute '{attr_name}' added to {ctrl}")

def addProxyAttribute(proxy_ctrl, target_ctrl, attr_name):
    if cmds.objExists(proxy_ctrl) and not cmds.attributeQuery(attr_name, node=proxy_ctrl, exists=True):
        cmds.addAttr(proxy_ctrl, ln=attr_name, at="float", keyable=True, 
                     proxy=f"{target_ctrl}.{attr_name}")
        print(f"Proxy attribute '{attr_name}' added to {proxy_ctrl}, referencing {target_ctrl}.{attr_name}")


def setDrivenKey(driver, attr_name, driven_objects, driven_attr, driver_values, driven_values):
    if len(driver_values) != len(driven_values):
        raise ValueError("Driver values and driven values must have same length")

    # Ensure the attribute exists on the driver (FK control)
    ensureAttributeExists(driver, attr_name, min(driver_values), max(driver_values))

    # Set Driven Keyframes for each driven object
    for driven in driven_objects:
        full_attr = f"{driven}.{driven_attr}"
        for d_val, v_val in zip(driver_values, driven_values):
            cmds.setDrivenKeyframe(full_attr, currentDriver=f"{driver}.{attr_name}", 
                                   driverValue=d_val, value=v_val)

def setAllDrivenKeys(configs):
    for config in configs:
        setDrivenKey(**config)
    
    print("Set Driven Keys created successfully.")


def createSetDrivenKeys():
    ensureAttributeExists("L_ankleFK_CTRL", "Toe_Curl", -6, 3)
    addProxyAttribute("L_footIK_CTRL", "L_ankleFK_CTRL", "Toe_Curl")
    ensureAttributeExists("R_ankleFK_CTRL", "Toe_Curl", -6, 3)
    addProxyAttribute("R_footIK_CTRL", "R_ankleFK_CTRL", "Toe_Curl")
    setAllDrivenKeys(sdk_configs)
    setupAllLocators()


def create_locator_for_existing_sdk(shoulder_ctrl, alignment, elbow_joint, sdk_attr_x, sdk_attr_y, sdk_attr_z):
    
    locator_name = elbow_joint + "_sdk_LOC"
    
    # Delete if already exists
    if cmds.objExists(locator_name):
        cmds.delete(locator_name)
        
    locator = cmds.spaceLocator(name=locator_name)[0]
    cmds.setAttr(locator + ".overrideEnabled", 1)
    cmds.setAttr(locator + ".overrideColor", 18)  # Blue

    elbow_pos = cmds.xform(elbow_joint, query=True, worldSpace=True, translation=True)
    cmds.xform(locator, worldSpace=True, translation=elbow_pos)

    # freeze transforms to avoid unwanted offsets
    cmds.makeIdentity(locator, apply=True, translate=True)

    # check if the locator is already parented to world (avoid warning)
    if cmds.listRelatives(locator, parent=True) is not None:
        cmds.parent(locator, world=True)

    # Ensure the SDK attributes exist on the shoulder control
    if not cmds.attributeQuery(sdk_attr_x, node=shoulder_ctrl, exists=True):
        print(f"Error: Attribute '{sdk_attr_x}' does not exist on '{shoulder_ctrl}'!")
        return
    if not cmds.attributeQuery(sdk_attr_y, node=shoulder_ctrl, exists=True):
        print(f"Error: Attribute '{sdk_attr_y}' does not exist on '{shoulder_ctrl}'!")
        return
    if not cmds.attributeQuery(sdk_attr_z, node=shoulder_ctrl, exists=True):
        print(f"Error: Attribute '{sdk_attr_z}' does not exist on '{shoulder_ctrl}'!")
        return

    # Create an expression to reverse the rotations for the right side
    if alignment == 'R':
        # For right side, create expressions that reverse the rotation values
        #expr_x = f"{shoulder_ctrl}.{sdk_attr_x} = -{locator}.rotateX"
        cmds.connectAttr(f"{locator}.rotateX", f"{shoulder_ctrl}.{sdk_attr_x}", force=True)

        expr_y = f"{shoulder_ctrl}.{sdk_attr_y} = -{locator}.rotateY"
        expr_z = f"{shoulder_ctrl}.{sdk_attr_z} = -{locator}.rotateZ"
        
        # Create the expressions to inverse the rotation values
        #cmds.expression(name=f"{locator_name}_exprX", string=expr_x)
        cmds.expression(name=f"{locator_name}_exprY", string=expr_y)
        cmds.expression(name=f"{locator_name}_exprZ", string=expr_z)


    elif alignment == 'L':
        # For left side, just connect the rotations normally
        cmds.connectAttr(f"{locator}.rotateX", f"{shoulder_ctrl}.{sdk_attr_x}", force=True)
        cmds.connectAttr(f"{locator}.rotateY", f"{shoulder_ctrl}.{sdk_attr_y}", force=True)
        cmds.connectAttr(f"{locator}.rotateZ", f"{shoulder_ctrl}.{sdk_attr_z}", force=True)

    #if alignment == 'C':
    else:
        # For right side, create expressions that reverse the rotation values
        expr_x = f"{shoulder_ctrl}.{sdk_attr_x} = -{locator}.rotateX"
        expr_y = f"{shoulder_ctrl}.{sdk_attr_y} = -{locator}.rotateY"
        expr_z = f"{shoulder_ctrl}.{sdk_attr_z} = -{locator}.rotateZ"
        
        # Create the expressions to inverse the rotation values
        cmds.expression(name=f"{locator_name}_exprX", string=expr_x)
        cmds.expression(name=f"{locator_name}_exprY", string=expr_y)
        cmds.expression(name=f"{locator_name}_exprZ", string=expr_z)

    print(f"Locator '{locator_name}' created at {elbow_joint} and linked to '{sdk_attr_x}', '{sdk_attr_y}', and '{sdk_attr_z}' on {shoulder_ctrl}.")




def setupAllLocators():
    # Left arm setup
    shoulder_ctrl_L = "L_shoulder_CTRL"
    elbow_joint_L = "L_elbowC_CTRL"
    sdk_attr_x = "Arm_CurlX"
    sdk_attr_y = "Arm_CurlY"
    sdk_attr_z = "Arm_CurlZ"

    locatorLeft = create_locator_for_existing_sdk(shoulder_ctrl_L, 'L', elbow_joint_L, sdk_attr_x, sdk_attr_y, sdk_attr_z)

    # Right arm setup
    shoulder_ctrl_R = "R_shoulder_CTRL"
    elbow_joint_R = "R_elbowC_CTRL"

    locatorRight = create_locator_for_existing_sdk(shoulder_ctrl_R, 'R', elbow_joint_R, sdk_attr_x, sdk_attr_y, sdk_attr_z)

    locatorL = 'L_elbowC_CTRL_sdk_LOC'
    locatorR = 'R_elbowC_CTRL_sdk_LOC'

    tongue_ctrl = "C_jawStart_CTRL"
    tongue_joint = "C_tongueD_JNT_BIND"
    tongue_sdk_attr_x = "Tongue_Curl_Up"
    tongue_sdk_attr_y = "Tongue_Curl_Side"
    tongue_sdk_attr_z = "Tongue_Twist"
    locatorTongue = create_locator_for_existing_sdk(tongue_ctrl, 'C', tongue_joint, tongue_sdk_attr_x, tongue_sdk_attr_y, tongue_sdk_attr_z)
    locatorTongue = 'C_tongueD_JNT_BIND_sdk_LOC'

    # Function to group locators into OFFSET and ZERO groups
    def group_locator(locator):
        """ Creates an OFFSET and ZERO group for a locator and zeros out the locator. """
        if not locator or not cmds.objExists(locator):
            print(f"Error: Locator '{locator}' does not exist.")
            return None

        offset_grp = cmds.group(locator, name=f"{locator}_OFFSET")
        zero_grp = cmds.group(offset_grp, name=f"{locator}_ZERO")

        # Zero out locator rotations
        cmds.setAttr(f"{locator}.rotateX", 0)
        cmds.setAttr(f"{locator}.rotateY", 0)
        cmds.setAttr(f"{locator}.rotateZ", 0)

        return zero_grp  # Return the top group for parenting

    # Grouping locators
    zero_L = group_locator(locatorL)
    zero_R = group_locator(locatorR)
    zero_Tongue = group_locator(locatorTongue)

    # Ensure locators exist before proceeding
    if zero_L:
        cmds.xform(locatorL, worldSpace=True, translation=(0, 5, 0))
        cmds.parent(zero_L, shoulder_ctrl_L)

    if zero_R:
        cmds.xform(locatorR, worldSpace=True, translation=(0, 5, 0))
        cmds.parent(zero_R, shoulder_ctrl_R)

    if zero_Tongue:
        cmds.xform(locatorTongue, worldSpace=True, translation=(0, 5, 0))
        cmds.parent(zero_Tongue, tongue_ctrl)



# Example configurations:
sdk_configs = [
    {
        "driver": "C_tailUpper_CTRL",
        "attr_name": "Feather_Curl",
        "driven_objects": [
            "C_feather01A_JNT_BIND", "C_feather01B_JNT_BIND", "C_feather01C_JNT_BIND", "C_feather01D_JNT_BIND", "C_feather01E_JNT_BIND",
            "L_feather02A_JNT_BIND", "L_feather02B_JNT_BIND", "L_feather02C_JNT_BIND", "L_feather02D_JNT_BIND", "L_feather02E_JNT_BIND",
            "R_feather02A_JNT_BIND", "R_feather02B_JNT_BIND", "R_feather02C_JNT_BIND", "R_feather02D_JNT_BIND", "R_feather02E_JNT_BIND",
            "L_feather03A_JNT_BIND", "L_feather03B_JNT_BIND", "L_feather03C_JNT_BIND", "L_feather03D_JNT_BIND", "L_feather03E_JNT_BIND",
            "R_feather03A_JNT_BIND", "R_feather03B_JNT_BIND", "R_feather03C_JNT_BIND", "R_feather03D_JNT_BIND", "R_feather03E_JNT_BIND",
            "L_feather04A_JNT_BIND", "L_feather04B_JNT_BIND", "L_feather04C_JNT_BIND", "L_feather04D_JNT_BIND", "L_feather04E_JNT_BIND",
            "R_feather04A_JNT_BIND", "R_feather04B_JNT_BIND", "R_feather04C_JNT_BIND", "R_feather04D_JNT_BIND", "R_feather04E_JNT_BIND",
            "L_feather05A_JNT_BIND", "L_feather05B_JNT_BIND", "L_feather05C_JNT_BIND", "L_feather05D_JNT_BIND", "L_feather05E_JNT_BIND",
            "R_feather05A_JNT_BIND", "R_feather05B_JNT_BIND", "R_feather05C_JNT_BIND", "R_feather05D_JNT_BIND", "R_feather05E_JNT_BIND",
            "L_feather06A_JNT_BIND", "L_feather06B_JNT_BIND", "L_feather06C_JNT_BIND", "L_feather06D_JNT_BIND", "L_feather06E_JNT_BIND",
            "R_feather06A_JNT_BIND", "R_feather06B_JNT_BIND", "R_feather06C_JNT_BIND", "R_feather06D_JNT_BIND", "R_feather06E_JNT_BIND",
            "L_feather07A_JNT_BIND", "L_feather07B_JNT_BIND", "L_feather07C_JNT_BIND", "L_feather07D_JNT_BIND", "L_feather07E_JNT_BIND",
            "R_feather07A_JNT_BIND", "R_feather07B_JNT_BIND", "R_feather07C_JNT_BIND", "R_feather07D_JNT_BIND", "R_feather07E_JNT_BIND",
            "L_feather08A_JNT_BIND", "L_feather08B_JNT_BIND", "L_feather08C_JNT_BIND", "L_feather08D_JNT_BIND", "L_feather08E_JNT_BIND",
            "R_feather08A_JNT_BIND", "R_feather08B_JNT_BIND", "R_feather08C_JNT_BIND", "R_feather08D_JNT_BIND", "R_feather08E_JNT_BIND"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-5, 0, 3],  # Driver Attribute Values
        "driven_values": [20, 0, -12]  # Corresponding Driven Attribute Values
    },
    {
        "driver": "C_tailUpper_CTRL",
        "attr_name": "Feather_Up",
        "driven_objects": [
            "C_feather01A_JNT_BIND",
            "L_feather02A_JNT_BIND",
            "R_feather02A_JNT_BIND",
            "L_feather03A_JNT_BIND",
            "R_feather03A_JNT_BIND",
            "L_feather04A_JNT_BIND",
            "R_feather04A_JNT_BIND",
            "L_feather05A_JNT_BIND",
            "R_feather05A_JNT_BIND",
            "L_feather06A_JNT_BIND",
            "R_feather06A_JNT_BIND",
            "L_feather07A_JNT_BIND",
            "R_feather07A_JNT_BIND",
            "L_feather08A_JNT_BIND",
            "R_feather08A_JNT_BIND",
        ],
        "driven_attr": "rotateY",
        "driver_values": [-10, 0, 10],  # Driver Attribute Values
        "driven_values": [40, 0, -40]  # Corresponding Driven Attribute Values
    },
    { 
        "driver": "C_jawStart_CTRL",
        "attr_name": "Tongue_Rotate_Up",
        "driven_objects": [
            "C_tongueA_JNT_BIND"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-10, 0, 10],  
        "driven_values": [40, 0, -40] 
    },
    { 
        "driver": "C_jawStart_CTRL",
        "attr_name": "Tongue_Curl_Up",
        "driven_objects": [
            "C_tongueB_JNT_BIND",
            "C_tongueC_JNT_BIND",
            "C_tongueD_JNT_BIND",
            "C_tongueE_JNT_BIND",
            "C_tongueF_JNT_END"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-100, 0, 100],  
        "driven_values": [40, 0, -40] 
    },
    { 
        "driver": "C_jawStart_CTRL",
        "attr_name": "Tongue_Curl_Side",
        "driven_objects": [
            "C_tongueB_JNT_BIND",
            "C_tongueC_JNT_BIND",
            "C_tongueD_JNT_BIND",
            "C_tongueE_JNT_BIND",
            "C_tongueF_JNT_END"
        ],
        "driven_attr": "rotateZ",
        "driver_values": [-100, 0, 100],  
        "driven_values": [40, 0, -40]  
    },
    { 
        "driver": "C_jawStart_CTRL",
        "attr_name": "Tongue_Twist",
        "driven_objects": [
            "C_tongueB_JNT_BIND",
            "C_tongueC_JNT_BIND",
            "C_tongueD_JNT_BIND",
            "C_tongueE_JNT_BIND",
            "C_tongueF_JNT_END"
        ],
        "driven_attr": "rotateX",
        "driver_values": [-60, 0, 60],  
        "driven_values": [12, 0, -12]  
    },
    {
        "driver": "L_ankleFK_CTRL",
        "attr_name": "Toe_Curl",
        "driven_objects": [
            "L_toe01_JNT_BIND",
            "L_toe02_JNT_BIND",
            "L_toe03_JNT_BIND"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-6, 0, 3],  
        "driven_values": [60, 0, -30]  
    },
    {
        "driver": "L_ankleFK_CTRL",
        "attr_name": "Toe_Curl",
        "driven_objects": [
            "L_toe04_JNT_BIND"       
        ],
        "driven_attr": "rotateY",
        "driver_values": [-6, 0, 3],  
        "driven_values": [-60, 0, 30]  
    },
    {
        "driver": "R_ankleFK_CTRL",
        "attr_name": "Toe_Curl",
        "driven_objects": [
            "R_toe01_JNT_BIND",
            "R_toe02_JNT_BIND",
            "R_toe03_JNT_BIND"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-6, 0, 3],  
        "driven_values": [60, 0, -30] 
    },
    {
        "driver": "R_ankleFK_CTRL",
        "attr_name": "Toe_Curl",
        "driven_objects": [
            "R_toe04_JNT_BIND"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-6, 0, 3],  
        "driven_values": [-60, 0, 30]  
    },
    {
        "driver": "L_shoulder_CTRL",
        "attr_name": "Arm_CurlX",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "L_elbowA_CTRL", "L_elbowB_CTRL", "L_elbowC_CTRL", "L_elbowD_CTRL", "L_elbowE_CTRL"
        ],
        "driven_attr": "rotateX",
        "driver_values": [-200, 0, 200],  
        "driven_values": [-20, 0, 20] 
    },
    {
        "driver": "L_shoulder_CTRL",
        "attr_name": "Arm_CurlY",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "L_elbowA_CTRL", "L_elbowB_CTRL", "L_elbowC_CTRL", "L_elbowD_CTRL", "L_elbowE_CTRL"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-200, 0, 200], 
        "driven_values": [-20, 0, 20]  
    },
    {
        "driver": "L_shoulder_CTRL",
        "attr_name": "Arm_CurlZ",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "L_elbowA_CTRL", "L_elbowB_CTRL", "L_elbowC_CTRL", "L_elbowD_CTRL", "L_elbowE_CTRL"
        ],
        "driven_attr": "rotateZ",
        "driver_values": [-200, 0, 200],  
        "driven_values": [-20, 0, 20]  
    },
    {
        "driver": "R_shoulder_CTRL",
        "attr_name": "Arm_CurlX",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "R_elbowA_CTRL", "R_elbowB_CTRL", "R_elbowC_CTRL", "R_elbowD_CTRL", "R_elbowE_CTRL"
        ],
        "driven_attr": "rotateX",
        "driver_values": [-200, 0, 200],  
        "driven_values": [-20, 0, 20]  
    },
    {
        "driver": "R_shoulder_CTRL",
        "attr_name": "Arm_CurlY",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "R_elbowA_CTRL", "R_elbowB_CTRL", "R_elbowC_CTRL", "R_elbowD_CTRL", "R_elbowE_CTRL"
        ],
        "driven_attr": "rotateY",
        "driver_values": [-200, 0, 200],  
        "driven_values": [-20, 0, 20]  
    },
    {
        "driver": "R_shoulder_CTRL",
        "attr_name": "Arm_CurlZ",
        "driven_objects": [
            #"L_elbowA_JNT_BIND", "L_elbowB_JNT_BIND", "L_elbowC_JNT_BIND", "L_elbowD_JNT_BIND", "L_elbowE_JNT_BIND", "L_elbowF_JNT_BIND", "L_elbowG_JNT_BIND", "L_elbowH_JNT_BIND", "L_elbowI_JNT_BIND", "L_elbowJ_JNT_BIND", "L_wrist_CTRL"
            "R_elbowA_CTRL", "R_elbowB_CTRL", "R_elbowC_CTRL", "R_elbowD_CTRL", "R_elbowE_CTRL"
        ],
        "driven_attr": "rotateZ",
        "driver_values": [-200, 0, 200], 
        "driven_values": [-20, 0, 20] 
    }
]



