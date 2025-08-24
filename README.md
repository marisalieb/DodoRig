# Dodo Auto Rig for the Dodo project
This is my fully scripted set up which creates a rig for the Dodo bird model.

### To run this:
- ensure all python files are in the same folder
- run this MEL command: ikSpringSolver;
- then in the script editor click on 'Source Script...' and select the **rigUI.py** file to run
- now a rig UI window opens

### How it works:
- in the rig UI first create the skeleton, the joints are stored in a json file where you can add more
- adjust the joint positions and click 'Save Joint Positions', adjust and save the position before creating the rest
- adjust the overall joint radius
- then create the body rig, its controls and their custom Set Driven Keys
- set up the face rig, first the joints and then their controls
- if the character model is already in the scene, the eye blink functionality can also be set up
- for a full rigging workflow, bind the body and face joints to the mesh before creating the controls; for this click 'Select all BIND joints' to bind these to the mesh, now weightpaint it and afterwards continue with creating the rest of the controls

### Functionality:
- sets up joints, parents, orients and mirrors them
- sets up IK/FK blend on the legs and spine
- creates and parents controls for everything
- joint based face rig and blinking eye controls
- smooth arm movement using Set Driven Keys from the viewport
- toe curling
- tongue curl up and sideways, twist and rotation
- tail feather curling and rotation
- neck stretch ability, as requested by the animator for the scenes where the dodo is falling at a fast speed
