## Instructions for running the two scripts

There are two scripts to run for setting up the rig for the hand:

1. Copy and paste the first script into Maya to set up the rig skeleton and parent the joints.
2. Before running the next script orient all joint except the end joints. To do this, go to the viewport and right-click on the first joint in the hierarchy (in this case, the arm joint) and click 'Select hierarchy'. Then, go to the Rigging menu -> Skeleton -> Orient Joints. This correctly orients all joints except the end joints.
3. Copy and paste the second script into Maya to orient the end joints, freeze transformations, create the controls and constrain and parent the controls to the joints.

The 'Maya-scenes' folder includes a file with the hand model, which the rig was designed to fit.
You can run the rigging scripts in the hand-model.mb file or in a new Maya scene file, to create the rig.
The folder also contains a file with the hand fully rigged and animated, providing an example of the rig in action.