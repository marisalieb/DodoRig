# Python Auto Rig for the Dodo project
This is a fully scripted auto rigging tool for the Dodo bird model.
#

### Full animation [here](https://vimeo.com/1112713658)


![Scene 1](media/dodo.png)

#

## Features:
- sets up joints, parents, orients and mirrors them
- sets up IK/FK blend on the legs and spine
- creates and parents controls for everything
- joint based face rig and blinking eye controls
- smooth arm movement using Set Driven Keys from the viewport
- toe curling
- tongue curl up and sideways, twist and rotation
- tail feather curling and rotation
- neck stretch ability, as requested by the animator for the scenes where the dodo is falling at a fast speed


## How to Run:
1. Ensure all python files are in the same folder
2. In Maya’s MEL command line, enter: 
    ```bash
    ikSpringSolver;
    ``` 

3. Load the script in Maya:
    - Open the Script Editor
    - Go to File → Source Script...
    - Select the `rigUI.py` file.
4. Once sourced, the Rig UI window will appear and you can start using it


#

## How it works:
1. In the rig UI first create the skeleton, the joints are stored in joint-positions.json where more joijnts can be added
2. Adjust the joint positions and click 'Save Joint Positions', adjust and save the position before creating the rest
3. Adjust the overall joint radius
4. Then create the body rig, its controls and their custom Set Driven Keys
5. Set up the face rig, first the joints and then their controls
6. If the character model is already in the scene, the eye blink functionality can also be set up
7. For a full rigging workflow, bind the body and face joints to the mesh before creating the controls; for this click 'Select all BIND joints' to bind these to the mesh, now weightpaint it and afterwards continue with creating the rest of the controls

