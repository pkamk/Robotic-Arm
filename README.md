# RoboticArm

All of this was made in 2022, before ChatGPT.

The Blender file contains the model of the robotic arm, and has the code required to send the positions of parts of the model to the Arduino. It uses objects called bones and inverse kinematics to send the coordinates and rotations of the parts of the model. 
The Arduino file receives the coordinates sent by the Blender script through the use of SoftwareSerial to enable digital communication on most pins of the Arduino. The program then decodes these coordinates, and sends them as signals into the robotic arm. 
The Python file contains the script code located in the Blender file. It comes with the Blender file, but if the Blender file does not open, then the Python file contains the standalone code.

In order to use:
1. Donwload Blender and open the LeArmBlendFinalPortfolio.blend file.
2. Download the Arduino code.
3. Follow the documentation written in the script tab. In case you do not see it, here it is:  In order to use, connect power supply and usb to LeArm controller board. Connect Rx to Tx and Tx to Rx (see what arduino serial pins are in arduino program) between arduino and robot controller. Connect USB to arduino and upload arduino program first. In blender, press spacebar and start the animation player in the view. Then, run this script. Make sure to only run the script one time. Otherwise, running it multuple times will cause COM3 to fail, as there will already be a connection on it.
