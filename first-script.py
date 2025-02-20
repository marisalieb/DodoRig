# copy and paste this code into the script editor in Maya to create the rig skeleton and parent the joints

import maya.cmds as cmds

# function to create each joint
def createJoint(position, name, number, suffix):
    cmds.select(cl=True)
    cmds.joint(p=position, n=name + '_' + 'joint' + '_' + number + '_' + suffix)

# create all joints
# the following positions of the joints are taken from the rig I created manually with the class material from week 4
def createSkeleton():

    # wrist and arm
    createJoint([-1.6505682600999385, 2.1508952347612458, -33.456021712716975], 'arm', '01', 'BIND')
    createJoint([-1.4900971486401118, 1.0638537052446349, -6.594539780295486], 'wrist', '01', 'BIND')

    # wrist orientation ghost joint; this will be deleted later
    createJoint([-1.47333194606537027, 1.0144484021882478, -4.933050745722927], 'wristorient', '01', 'BIND')

    # little finger
    createJoint([0.9798411079998439, 0.986094430276489, -5.210988009657514], 'little', '01', 'BIND')
    createJoint([2.3193828443531617, 0.5837668262353243, 0.9957439268550348], 'little', '02', 'BIND')
    createJoint([3.391113221024536, 0.42868700113127867, 3.8248959324059384], 'little', '03', 'BIND')
    createJoint([4.129768108974929, 0.43553424714623873, 5.640067069625604], 'little', '04', 'BIND')
    createJoint([4.834422313213728, 0.40607403736237935, 7.7863876488927115], 'little', '05', 'END')

    # ring finger
    createJoint([-0.37947801747494236, 0.9872449007606824, -4.981194337730696], 'ring', '01', 'BIND')
    createJoint([0.32208706698349243, 0.6307502292291629, 1.725376374052487], 'ring', '02', 'BIND')
    createJoint([1.2615073867632312, 0.4813793497921086, 6.227649727461657], 'ring', '03', 'BIND')
    createJoint([1.725224427031535, 0.39953860476293607, 9.260438856208978], 'ring', '04', 'BIND')
    createJoint([2.0647595034272577, 0.3361946700030707, 11.726736725666878], 'ring', '05', 'END')

    # middle finger
    createJoint([-1.8333194606537027, 1.0144484021882478, -4.933050745722927], 'middle', '01', 'BIND')
    createJoint([-1.6242907662391648, 0.7221627104559007, 2.173618130655607], 'middle', '02', 'BIND')
    createJoint([-1.674993939614734, 0.5206641168776192, 7.552309677186508], 'middle', '03', 'BIND')
    createJoint([-1.711599955962615, 0.47327294143522775, 10.705641433719551], 'middle', '04', 'BIND')
    createJoint([-1.621788381844184, 0.3761346503912448, 13.285054052271104], 'middle', '05', 'END')

    # index finger
    createJoint([-3.2655443604846663, 0.8887472820756922, -5.011595822638699], 'index', '01', 'BIND')
    createJoint([-3.964217995844865, 0.7118276143380686, 2.232906782116894], 'index', '02', 'BIND')
    createJoint([-4.504183781718757, 0.5041256375350759, 7.525593409214158], 'index', '03', 'BIND')
    createJoint([-4.81827097516097, 0.46187179866449163, 10.313392073794933], 'index', '04', 'BIND')
    createJoint([-5.0030691408657555, 0.4320453720132287, 12.8101065103844], 'index', '05', 'END')

    # thumb
    createJoint([-4.780946623070031, 0.0, -4.146138784839618], 'thumb', '01', 'BIND')
    createJoint([-6.115234571667273, -2.6697535768657814, -0.6213573593982593], 'thumb', '02', 'BIND')
    createJoint([-7.813846844007549, -3.850822918989467, 3.362735765727813], 'thumb', '03', 'BIND')
    createJoint([-8.584198974516648, -4.925693108342289, 6.0567691054614965], 'thumb', '04', 'END')


# parent joints
# add the one you want to parent first and then the parent second
def parentJoints():
    cmds.select(cl=True)

    # parenting wrist to arm
    cmds.parent('wrist_joint_01_BIND', 'arm_joint_01_BIND')

    # this will later be used to orient the wrist to this ghost joint
    cmds.parent('wristorient_joint_01_BIND', 'wrist_joint_01_BIND')
    
    # parenting fingers to the wrist
    cmds.parent('little_joint_01_BIND', 'wrist_joint_01_BIND')
    cmds.parent('ring_joint_01_BIND', 'wrist_joint_01_BIND')
    cmds.parent('middle_joint_01_BIND', 'wrist_joint_01_BIND')
    cmds.parent('index_joint_01_BIND', 'wrist_joint_01_BIND')
    cmds.parent('thumb_joint_01_BIND', 'wrist_joint_01_BIND')

    # parenting the fingers
    cmds.parent('little_joint_05_END', 'little_joint_04_BIND')
    cmds.parent('little_joint_04_BIND', 'little_joint_03_BIND')
    cmds.parent('little_joint_03_BIND', 'little_joint_02_BIND')
    cmds.parent('little_joint_02_BIND', 'little_joint_01_BIND')

    cmds.parent('ring_joint_05_END', 'ring_joint_04_BIND')
    cmds.parent('ring_joint_04_BIND', 'ring_joint_03_BIND')
    cmds.parent('ring_joint_03_BIND', 'ring_joint_02_BIND')
    cmds.parent('ring_joint_02_BIND', 'ring_joint_01_BIND')

    cmds.parent('middle_joint_05_END', 'middle_joint_04_BIND')
    cmds.parent('middle_joint_04_BIND', 'middle_joint_03_BIND')
    cmds.parent('middle_joint_03_BIND', 'middle_joint_02_BIND')
    cmds.parent('middle_joint_02_BIND', 'middle_joint_01_BIND')

    cmds.parent('index_joint_05_END', 'index_joint_04_BIND')
    cmds.parent('index_joint_04_BIND', 'index_joint_03_BIND')
    cmds.parent('index_joint_03_BIND', 'index_joint_02_BIND')
    cmds.parent('index_joint_02_BIND', 'index_joint_01_BIND')

    cmds.parent('thumb_joint_04_END', 'thumb_joint_03_BIND')
    cmds.parent('thumb_joint_03_BIND', 'thumb_joint_02_BIND')
    cmds.parent('thumb_joint_02_BIND', 'thumb_joint_01_BIND')


createSkeleton()
parentJoints()
