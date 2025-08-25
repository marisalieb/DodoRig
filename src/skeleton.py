import maya.cmds as cmds
import json
import os
import platform
import sys

# import ikSpringSolver

# Get the current working directory (where the script is run)
script_dir = os.getcwd()

JOINTS_FILE = os.path.join(script_dir, "joint-positions.json")

print(JOINTS_FILE)

# Load JSON
with open(JOINTS_FILE, "r") as file:
    data = json.load(file)


# Load joint positions from JSON file, first checks if file exists
def loadJointPositions():
    if os.path.exists(JOINTS_FILE):
        with open(JOINTS_FILE, "r") as f: # r for read
            return json.load(f)
    return None  # Return None if file doesn't exist

# Create skeleton from JSON or default positions
def createSkeleton():
    jointPositions = loadJointPositions()

    if not jointPositions:
        print("No joint positions found, create defaults before continuing.")
        # can use createJoint function here to create joints

    else:
        # Load joints from file, iterate over dictionary, name and position are stored as key-value pairs
        for jointName, position in jointPositions.items():
            cmds.select(cl=True)
            cmds.joint(p=position, n=jointName)


# Get positions of all joints in the scene, useful for saving updated positions
def getJointPositions():
    joints = cmds.ls(type="joint")
    jointPositions = {}
    for joint in joints:
        pos = cmds.xform(joint, q=True, ws=True, t=True) # get world space position
        jointPositions[joint] = pos
    return jointPositions


# save joint positions to JSON file, takes dictionary jointPositions
def saveJointPositions(jointPositions):
    roundedPositions = {joint: [round(coord, 3) for coord in pos] for joint, pos in jointPositions.items()}
    
    # with open(JOINTS_FILE, "w") as f: # w for write
    #     json.dump(roundedPositions, f, indent=4)
    with open(JOINTS_FILE, "w") as f:  
        f.write("{\n")  # Start JSON
        for i, (joint, pos) in enumerate(roundedPositions.items()):
            f.write(f'    "{joint}": {json.dumps(pos)}')
            if i < len(roundedPositions) - 1:
                f.write(",\n")  # Add a comma for all but the last entry
            else:
                f.write("\n")  # No comma for last entry
        f.write("}\n")  # End JSON

# Save updated joint positions after moving joints
def saveUpdatedPositions():
    jointPositions = getJointPositions()
    saveJointPositions(jointPositions)
    print("Joint positions saved with 2 decimal precision")


# parent joints
# add the one you want to parent first and then the parent second
def parentJoints():
    cmds.select(cl=True)

    # Spine and Neck
    cmds.parent('C_COG_JNT_BIND', 'C_root_JNT_BIND')
    # C_COG_JNT_BIND
    cmds.parent('C_spineBase_JNT_BIND', 'C_COG_JNT_BIND')
    cmds.parent('C_spineMid_JNT_BIND', 'C_spineBase_JNT_BIND')
    cmds.parent('C_spineUpper_JNT_BIND', 'C_spineMid_JNT_BIND')
    cmds.parent('C_neckBase_JNT_BIND', 'C_spineUpper_JNT_BIND')
    cmds.parent('C_neckMid_JNT_BIND', 'C_neckBase_JNT_BIND')
    cmds.parent('C_neckUpper_JNT_BIND', 'C_neckMid_JNT_BIND')
    cmds.parent('C_headBase_JNT_BIND', 'C_neckUpper_JNT_BIND')
    cmds.parent('C_headMid_JNT_BIND', 'C_headBase_JNT_BIND')
    cmds.parent('C_headUpper_JNT_END', 'C_headMid_JNT_BIND')

    # Tail
    cmds.parent('C_tailBase_JNT_BIND', 'C_COG_JNT_BIND')
    cmds.parent('C_tailMid_JNT_BIND', 'C_tailBase_JNT_BIND')
    cmds.parent('C_tailUpper_JNT_BIND', 'C_tailMid_JNT_BIND')
    
    # Eyes
    cmds.parent('L_eye_JNT_BIND', 'C_headMid_JNT_BIND')
    cmds.parent('L_eyeEnd_JNT_END', 'L_eye_JNT_BIND')

    #face
    cmds.parent('C_face_JNT_BIND', 'C_headBase_JNT_BIND')

    # Beak
    cmds.parent('C_beakStart_JNT_BIND', 'C_face_JNT_BIND')
    cmds.parent('C_beakEnd_JNT_END', 'C_beakStart_JNT_BIND')

    # Jaw
    cmds.parent('C_jawStart_JNT_BIND', 'C_face_JNT_BIND')
    cmds.parent('C_jawEnd_JNT_END', 'C_jawStart_JNT_BIND')
    
    # Tongue
    cmds.parent('C_tongueA_JNT_BIND', 'C_jawStart_JNT_BIND')
    cmds.parent('C_tongueB_JNT_BIND', 'C_tongueA_JNT_BIND')
    cmds.parent('C_tongueC_JNT_BIND', 'C_tongueB_JNT_BIND')
    cmds.parent('C_tongueD_JNT_BIND', 'C_tongueC_JNT_BIND')
    cmds.parent('C_tongueE_JNT_BIND', 'C_tongueD_JNT_BIND')
    cmds.parent('C_tongueF_JNT_END', 'C_tongueE_JNT_BIND')
    
    # Leg
    cmds.parent('L_hip_JNT_BIND', 'C_root_JNT_BIND')
    cmds.parent('L_femur_JNT_BIND', 'L_hip_JNT_BIND')
    cmds.parent('L_knee_JNT_BIND', 'L_femur_JNT_BIND')
    cmds.parent('L_ankle_JNT_BIND', 'L_knee_JNT_BIND')
    cmds.parent('L_heel_JNT_BIND', 'L_ankle_JNT_BIND')
    
    # Toes
    cmds.parent('L_toe02_JNT_BIND', 'L_heel_JNT_BIND')
    cmds.parent('L_toeEnd02_JNT_END', 'L_toe02_JNT_BIND')
    cmds.parent('L_toe01_JNT_BIND', 'L_heel_JNT_BIND')
    cmds.parent('L_toeEnd01_JNT_END', 'L_toe01_JNT_BIND')
    cmds.parent('L_toe03_JNT_BIND', 'L_heel_JNT_BIND')
    cmds.parent('L_toeEnd03_JNT_END', 'L_toe03_JNT_BIND')
    cmds.parent('L_toe04_JNT_BIND', 'L_heel_JNT_BIND')
    cmds.parent('L_toeEnd04_JNT_END', 'L_toe04_JNT_BIND')
    
    # Arm
    cmds.parent('L_scapula_JNT_BIND', 'C_spineUpper_JNT_BIND')
    cmds.parent('L_shoulder_JNT_BIND', 'L_scapula_JNT_BIND')
    cmds.parent('L_elbowA_JNT_BIND', 'L_shoulder_JNT_BIND')
    cmds.parent('L_elbowB_JNT_BIND', 'L_elbowA_JNT_BIND')
    cmds.parent('L_elbowC_JNT_BIND', 'L_elbowB_JNT_BIND')
    cmds.parent('L_elbowD_JNT_BIND', 'L_elbowC_JNT_BIND')
    cmds.parent('L_elbowE_JNT_BIND', 'L_elbowD_JNT_BIND')
    cmds.parent('L_wrist_JNT_BIND', 'L_elbowE_JNT_BIND')
    
    # orient joint
    cmds.parent('L_wristOrient_JNT_BIND', 'L_wrist_JNT_BIND')
    cmds.parent('C_tailUpperOrient_JNT_BIND', 'C_tailUpper_JNT_BIND')


    # Fingers
    cmds.parent('L_fingerStart02_JNT_BIND', 'L_wrist_JNT_BIND')
    cmds.parent('L_fingerMid02_JNT_BIND', 'L_fingerStart02_JNT_BIND')
    cmds.parent('L_fingerEnd02_JNT_END', 'L_fingerMid02_JNT_BIND')
    
    cmds.parent('L_fingerStart01_JNT_BIND', 'L_wrist_JNT_BIND')
    cmds.parent('L_fingerMid01_JNT_BIND', 'L_fingerStart01_JNT_BIND')
    cmds.parent('L_fingerEnd01_JNT_END', 'L_fingerMid01_JNT_BIND')
    
    
    # feathers
    cmds.parent('C_feather01A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('C_feather01B_JNT_BIND', 'C_feather01A_JNT_BIND')
    cmds.parent('C_feather01C_JNT_BIND', 'C_feather01B_JNT_BIND')
    cmds.parent('C_feather01D_JNT_BIND', 'C_feather01C_JNT_BIND')
    cmds.parent('C_feather01E_JNT_BIND', 'C_feather01D_JNT_BIND')
    cmds.parent('C_feather01F_JNT_END', 'C_feather01E_JNT_BIND')

    cmds.parent('L_feather02A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather02B_JNT_BIND', 'L_feather02A_JNT_BIND')
    cmds.parent('L_feather02C_JNT_BIND', 'L_feather02B_JNT_BIND')
    cmds.parent('L_feather02D_JNT_BIND', 'L_feather02C_JNT_BIND')
    cmds.parent('L_feather02E_JNT_BIND', 'L_feather02D_JNT_BIND')
    cmds.parent('L_feather02F_JNT_END', 'L_feather02E_JNT_BIND')

    cmds.parent('L_feather03A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather03B_JNT_BIND', 'L_feather03A_JNT_BIND')
    cmds.parent('L_feather03C_JNT_BIND', 'L_feather03B_JNT_BIND')
    cmds.parent('L_feather03D_JNT_BIND', 'L_feather03C_JNT_BIND')
    cmds.parent('L_feather03E_JNT_BIND', 'L_feather03D_JNT_BIND')
    cmds.parent('L_feather03F_JNT_END', 'L_feather03E_JNT_BIND')

    cmds.parent('L_feather04A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather04B_JNT_BIND', 'L_feather04A_JNT_BIND')
    cmds.parent('L_feather04C_JNT_BIND', 'L_feather04B_JNT_BIND')
    cmds.parent('L_feather04D_JNT_BIND', 'L_feather04C_JNT_BIND')
    cmds.parent('L_feather04E_JNT_BIND', 'L_feather04D_JNT_BIND')
    cmds.parent('L_feather04F_JNT_END', 'L_feather04E_JNT_BIND')

    cmds.parent('L_feather05A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather05B_JNT_BIND', 'L_feather05A_JNT_BIND')
    cmds.parent('L_feather05C_JNT_BIND', 'L_feather05B_JNT_BIND')
    cmds.parent('L_feather05D_JNT_BIND', 'L_feather05C_JNT_BIND')
    cmds.parent('L_feather05E_JNT_BIND', 'L_feather05D_JNT_BIND')
    cmds.parent('L_feather05F_JNT_END', 'L_feather05E_JNT_BIND')

    cmds.parent('L_feather06A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather06B_JNT_BIND', 'L_feather06A_JNT_BIND')
    cmds.parent('L_feather06C_JNT_BIND', 'L_feather06B_JNT_BIND')
    cmds.parent('L_feather06D_JNT_BIND', 'L_feather06C_JNT_BIND')
    cmds.parent('L_feather06E_JNT_BIND', 'L_feather06D_JNT_BIND')
    cmds.parent('L_feather06F_JNT_END', 'L_feather06E_JNT_BIND')

    cmds.parent('L_feather07A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather07B_JNT_BIND', 'L_feather07A_JNT_BIND')
    cmds.parent('L_feather07C_JNT_BIND', 'L_feather07B_JNT_BIND')
    cmds.parent('L_feather07D_JNT_BIND', 'L_feather07C_JNT_BIND')
    cmds.parent('L_feather07E_JNT_BIND', 'L_feather07D_JNT_BIND')
    cmds.parent('L_feather07F_JNT_END', 'L_feather07E_JNT_BIND')

    cmds.parent('L_feather08A_JNT_BIND', 'C_tailUpper_JNT_BIND')
    cmds.parent('L_feather08B_JNT_BIND', 'L_feather08A_JNT_BIND')
    cmds.parent('L_feather08C_JNT_BIND', 'L_feather08B_JNT_BIND')
    cmds.parent('L_feather08D_JNT_BIND', 'L_feather08C_JNT_BIND')
    cmds.parent('L_feather08E_JNT_BIND', 'L_feather08D_JNT_BIND')
    cmds.parent('L_feather08F_JNT_END', 'L_feather08E_JNT_BIND')



# Define the root joint
def orientJoints():
    root_joint = "C_root_JNT_BIND"
    # Select the root joint and its hierarchy
    cmds.select(cl=True)
    cmds.select(root_joint, hierarchy=True)
    # orient them all
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='xup', ch=True, zso=True)


# orient end joints
def orientEndJoint(targetJoint, currentJoint):
    cmds.select(cl=True)
    orientedJoint = cmds.aimConstraint(targetJoint, currentJoint, aimVector=[-1, 0, 0], upVector=[0, 0, 0])
    cmds.delete(orientedJoint)

def orientEndJoints():
    orientEndJoint('C_headMid_JNT_BIND', 'C_headUpper_JNT_END')
    
    orientEndJoint('C_jawStart_JNT_BIND', 'C_jawEnd_JNT_END')
    orientEndJoint('C_beakStart_JNT_BIND', 'C_beakEnd_JNT_END')
    orientEndJoint('C_tongueE_JNT_BIND', 'C_tongueF_JNT_END')
    orientEndJoint('L_eye_JNT_BIND', 'L_eyeEnd_JNT_END')
    orientEndJoint('L_toe01_JNT_BIND', 'L_toeEnd01_JNT_END')
    orientEndJoint('L_toe02_JNT_BIND', 'L_toeEnd02_JNT_END')
    orientEndJoint('L_toe03_JNT_BIND', 'L_toeEnd03_JNT_END')
    orientEndJoint('L_toe04_JNT_BIND', 'L_toeEnd04_JNT_END')
    orientEndJoint('L_fingerMid01_JNT_BIND', 'L_fingerEnd01_JNT_END')
    orientEndJoint('L_fingerMid02_JNT_BIND', 'L_fingerEnd02_JNT_END')

    #feathers
    orientEndJoint('C_feather01E_JNT_BIND', 'C_feather01F_JNT_END')
    orientEndJoint('L_feather02E_JNT_BIND', 'L_feather02F_JNT_END')
    orientEndJoint("L_feather03E_JNT_BIND", "L_feather03F_JNT_END")
    orientEndJoint("L_feather04E_JNT_BIND", "L_feather04F_JNT_END")
    orientEndJoint("L_feather05E_JNT_BIND", "L_feather05F_JNT_END")
    orientEndJoint("L_feather06E_JNT_BIND", "L_feather06F_JNT_END")
    orientEndJoint("L_feather07E_JNT_BIND", "L_feather07F_JNT_END")
    orientEndJoint("L_feather08E_JNT_BIND", "L_feather08F_JNT_END")


def deleteOrientJoints():
    cmds.delete('C_tailUpperOrient_JNT_BIND')
    cmds.delete('L_wristOrient_JNT_BIND')



def lockToCentre():
    cmds.select(cl=True)
    cmds.select('*C_*_JNT_*')
    selectedJoints = cmds.ls(sl=True)
    for joint in selectedJoints:
        cmds.setAttr(joint + '.tx', lock = True, keyable =True, channelBox = True)


def mirrorSkeleton():
    cmds.select(cl=True)
    cmds.mirrorJoint('L_hip_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))


    cmds.mirrorJoint('L_scapula_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    # mirror eye
    cmds.mirrorJoint('L_eye_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))

    # miroor feathers
    cmds.mirrorJoint('L_feather02A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather03A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather04A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather05A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather06A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather07A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))
    cmds.mirrorJoint('L_feather08A_JNT_BIND', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L_', 'R_'))

