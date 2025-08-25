import maya.cmds as cmds


# align control to the joint
def alignControl(control, joint, trans, rot):
    # temporarily parent the control to the joint
    cmds.parent(control, joint) 
    if trans:
        cmds.setAttr(control + '.tx', 0)
        cmds.setAttr(control + '.ty', 0)
        cmds.setAttr(control + '.tz', 0)
    
    if rot:
        cmds.setAttr(control + '.rx', 0)
        cmds.setAttr(control + '.ry', 0)
        cmds.setAttr(control + '.rz', 0)

    # unparent the control
    cmds.parent(control, w=True)

# create each control with a circle and then group it so the control itself can stay zeroed out
def createControl(controlName, alignment, direction, radius, joint, trans, rot):
    name = alignment + '_' + controlName + '_CTRL'
    cmds.circle(n=name, nr = direction, r=radius)
    # nr is which way the circle is build
    # without direction the circle is build at a differnt angle

    # cmds.group(n = name +'_group')
    cmds.group(n = name +'_OFFSET')
    cmds.group(n = name +'_ZERO')

    if joint != 'null':
        alignControl(name +'_ZERO', joint, trans, rot)

    # set the color of the control
    if alignment == 'C':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 17)

    if alignment == 'L':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 6)

    if alignment == 'R':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 13)

    if joint == 'null':
        # green color for the main control
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 14)

    cmds.select(cl=True)


def createSquareControl(controlName, alignment, size, joint, trans, rot):
    name = alignment + '_' + controlName + '_CTRL'
    
    # Define the square shape using four points
    square_points = [
        (-size, 0, size), (size, 0, size),
        (size, 0, -size), (-size, 0, -size),
        (-size, 0, size)  # Close the loop
    ]
    # Create a square control
    cmds.curve(n=name, d=1, p=square_points)
    
    # Create groups for organization
    cmds.group(n=name + '_OFFSET')
    cmds.group(n=name + '_ZERO')
    if joint != 'null':
        alignControl(name +'_ZERO', joint, trans, rot)

    # set the color of the control
    if alignment == 'C':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 18)

    if alignment == 'L':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 18)

    if alignment == 'R':
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 18)

    # was used for the volume joints and ctrls
    # if 'VOL_' in controlName:
    #     shapeNode = cmds.listRelatives(name)
    #     shapeNode = shapeNode[0]
    #     cmds.setAttr(shapeNode + '.overrideEnabled', 1)
    #     cmds.setAttr(shapeNode + '.overrideColor', 18) # 16 white, 18 turquoise, 19 greenish turquoise, 20 salmon
    
    if joint == 'null':
        # green color for the main control
        shapeNode = cmds.listRelatives(name)
        shapeNode = shapeNode[0]
        cmds.setAttr(shapeNode + '.overrideEnabled', 1)
        cmds.setAttr(shapeNode + '.overrideColor', 14)

    cmds.select(cl=True)

    # Example usage
    # createSquareControl("squareCtrl", "L", 2, None, None, None)



def createPoleVector(controlName, alignment, direction, *joints):

    if len(joints) < 2:
        cmds.warning("You need at least two joints to calculate a valid position.")
        return
    
    name = alignment + '_' + controlName + '_CTRL'
    
    # Create the control circle
    cmds.circle(n=name, nr=direction, r=1)
    cmds.group(n=name + '_OFFSET')
    cmds.group(n=name + '_ZERO')
    
    # Create a point constraint with all provided joints
    constraint_name = name + '_parentConst'
    cmds.pointConstraint(joints, name + '_ZERO', n=constraint_name, mo=False)
    cmds.delete(name + '_parentConst')

    cmds.xform(name + '_ZERO', ws=True, rotation=[0, 0, 0])


   # Determine movement direction based on control name
    #move_distance = -20 if "leg" in controlName.lower() else -20 # redundant now, but havent changed yet

    # Move control based on arm or leg
    cmds.move(0, 0, 15, name + '_ZERO', r=True, ws=True, wd=True) # x 0 again later just for blend rn

    shapeNode = cmds.listRelatives(name)
    shapeNode = shapeNode[0]
    cmds.setAttr(shapeNode + '.overrideEnabled', 1)
    cmds.setAttr(shapeNode + '.overrideColor', 18)
