# as described in the README.md file, orient the joints before running this script
# to do this:
# in the viewport RMB click on the first joint in the hierachry (the arm joint here) 
# and click 'select hierarchy', then go to Rigging menu -> Skeleton -> Orient joints
# this correctly orients all but the end joints



# now copy and paste this scipt into the script editor in Maya
import maya.cmds as cmds

# orient end joints
def orientJoint(targetJoint, currentJoint):
    orientedJoint = cmds.aimConstraint(targetJoint, currentJoint, aimVector=[-1, 0, 0], upVector=[0, 1, 0])
    cmds.delete(orientedJoint)


def orientEndJoints():
    orientJoint('little_joint_04_BIND', 'little_joint_05_END')
    orientJoint('ring_joint_04_BIND', 'ring_joint_05_END')
    orientJoint('middle_joint_04_BIND', 'middle_joint_05_END')
    orientJoint('index_joint_04_BIND', 'index_joint_05_END')
    orientJoint('thumb_joint_03_BIND', 'thumb_joint_04_END')
    

# delete the orient wrist joint, as it is not needed anymore
def deleteJoint(joint):
    cmds.delete(joint)


# freeze all transforms on all joints
def freezeTransforms():
    allJoints = cmds.ls('*_joint_*')
    for joint in allJoints:
        cmds.makeIdentity(joint, apply=True, t=True, r=True, s=True)



# controls:

# align control to the joint
def alignControl(control, joint):
    # temporarily parent the control to the joint
    cmds.parent(control, joint) 
    cmds.setAttr(control + '.tx', 0)
    cmds.setAttr(control + '.ty', 0)
    cmds.setAttr(control + '.tz', 0)
    cmds.setAttr(control + '.rx', 0)
    cmds.setAttr(control + '.ry', 0)
    cmds.setAttr(control + '.rz', 0)
    # unparent the control
    cmds.parent(control, w=True)

# create each control with a circle and then group it so the control itself can stay zeroed out
def createControl(controlName, direction, radius, joint):
    name = controlName + '_ctrl'
    cmds.circle(n=name, nr = direction, r=radius)
    # nr is which way the circle is build
    # without direction the circle is build at a differnt angle

    cmds.group(n = name +'_group')
    alignControl(name +'_group', joint)

    # set the color of the control
    shapeNode = cmds.listRelatives(name)
    shapeNode = shapeNode[0]
    cmds.setAttr(shapeNode + '.overrideEnabled', 1)
    cmds.setAttr(shapeNode + '.overrideColor', 4)
    # 4 results in red control circles
    cmds.select(cl=True)

# create each control with the function above
def createAllControls():
    createControl('arm', [1, 0, 0], 6, 'arm_joint_01_BIND')
    createControl('wrist', [1, 0, 0], 4, 'wrist_joint_01_BIND')

    createControl('thumb_start', [1, 0, 0], 3, 'thumb_joint_01_BIND')
    createControl('thumb_mid', [1, 0, 0], 3, 'thumb_joint_02_BIND')
    createControl('thumb_end', [1, 0, 0], 1.7, 'thumb_joint_03_BIND')

    createControl('index_start', [1, 0, 0], 2.7, 'index_joint_02_BIND')
    createControl('index_mid', [1, 0, 0], 1.6, 'index_joint_03_BIND')
    createControl('index_end', [1, 0, 0], 1.2, 'index_joint_04_BIND')

    createControl('middle_start', [1, 0, 0], 2.7, 'middle_joint_02_BIND')
    createControl('middle_mid', [1, 0, 0], 1.6, 'middle_joint_03_BIND')
    createControl('middle_end', [1, 0, 0], 1.2, 'middle_joint_04_BIND')

    createControl('ring_start', [1, 0, 0], 2.7, 'ring_joint_02_BIND')
    createControl('ring_mid', [1, 0, 0], 1.6, 'ring_joint_03_BIND')
    createControl('ring_end', [1, 0, 0], 1.2, 'ring_joint_04_BIND')

    createControl('little_start', [1, 0, 0], 2.7, 'little_joint_02_BIND')
    createControl('little_mid', [1, 0, 0], 1.6, 'little_joint_03_BIND')
    createControl('little_end', [1, 0, 0], 1.2, 'little_joint_04_BIND')


# constrain controls to each joint
def constrainControls():
    # mo at the end of the line means maintain offset
    cmds.parentConstraint('arm_ctrl', 'arm_joint_01_BIND', name = 'arm_CTRL_parentConstraint', mo=False)
    cmds.orientConstraint('wrist_ctrl', 'wrist_joint_01_BIND', name = 'wrist_CTRL_orientConstraint', mo=False)

    cmds.orientConstraint('thumb_start_ctrl', 'thumb_joint_01_BIND', name = 'thumb_start_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('thumb_mid_ctrl', 'thumb_joint_02_BIND', name = 'thumb_mid_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('thumb_end_ctrl', 'thumb_joint_03_BIND', name = 'thumb_end_CTRL_orientConstraint', mo=False)

    cmds.orientConstraint('index_start_ctrl', 'index_joint_02_BIND', name = 'index_start_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('index_mid_ctrl', 'index_joint_03_BIND', name = 'index_mid_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('index_end_ctrl', 'index_joint_04_BIND', name = 'index_end_CTRL_orientConstraint', mo=False)

    cmds.orientConstraint('middle_start_ctrl', 'middle_joint_02_BIND', name = 'middle_start_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('middle_mid_ctrl', 'middle_joint_03_BIND', name = 'middle_mid_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('middle_end_ctrl', 'middle_joint_04_BIND', name = 'middle_end_CTRL_orientConstraint', mo=False)

    cmds.orientConstraint('ring_start_ctrl', 'ring_joint_02_BIND', name = 'ring_start_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('ring_mid_ctrl', 'ring_joint_03_BIND', name = 'ring_mid_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('ring_end_ctrl', 'ring_joint_04_BIND', name = 'ring_end_CTRL_orientConstraint', mo=False)
    
    cmds.orientConstraint('little_start_ctrl', 'little_joint_02_BIND', name = 'little_start_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('little_mid_ctrl', 'little_joint_03_BIND', name = 'little_mid_CTRL_orientConstraint', mo=False)
    cmds.orientConstraint('little_end_ctrl', 'little_joint_04_BIND', name = 'little_end_CTRL_orientConstraint', mo=False)


# parent the controls
def parentControls():
    cmds.parent('wrist_ctrl_group', 'arm_ctrl')

    cmds.parent('thumb_start_ctrl_group', 'wrist_ctrl')
    cmds.parent('thumb_mid_ctrl_group', 'thumb_start_ctrl')
    cmds.parent('thumb_end_ctrl_group', 'thumb_mid_ctrl')

    cmds.parent('index_start_ctrl_group', 'wrist_ctrl')
    cmds.parent('index_mid_ctrl_group', 'index_start_ctrl')
    cmds.parent('index_end_ctrl_group', 'index_mid_ctrl')

    cmds.parent('middle_start_ctrl_group', 'wrist_ctrl')
    cmds.parent('middle_mid_ctrl_group', 'middle_start_ctrl')
    cmds.parent('middle_end_ctrl_group', 'middle_mid_ctrl')

    cmds.parent('ring_start_ctrl_group', 'wrist_ctrl')
    cmds.parent('ring_mid_ctrl_group', 'ring_start_ctrl')
    cmds.parent('ring_end_ctrl_group', 'ring_mid_ctrl')

    cmds.parent('little_start_ctrl_group', 'wrist_ctrl')
    cmds.parent('little_mid_ctrl_group', 'little_start_ctrl')
    cmds.parent('little_end_ctrl_group', 'little_mid_ctrl')


# run the functions
cmds.select(cl=True)
orientEndJoints()
deleteJoint('wristorient_joint_01_BIND')
freezeTransforms()
createAllControls()
constrainControls()
parentControls()
  
