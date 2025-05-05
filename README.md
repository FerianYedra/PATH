# PATH

## Summary
For our degree project we will build a functional quadruped robot under the name PATH (Autonomous Platform for Heterogeneous Terrain. On this repo the team has implemented version control for the code that contains the Control and HMI functions of the code.

## Code Details
For the code we worked using python 3 as we found it to be the most simple way to quickly implement the function for the GPIO's, the HMI using TkInter and some of the other existing libraries like Math, and Time.

The code is separated in two files, the PATH_View.phy file contains the View of the code, however the full Model-Controller-Virew isn't fully implemented. It was just a way for us to make the code a little more simple to document and understand.

## Hardware Details
The hardware used for the quadruped was the following:
- A Raspberry Pi 4 for the microcontroller.
- A Raspberry Pi touchscreen for the implementation of the HMI.
- Eight 1501 MG servomotors, four for the shoulders and four for the elbows of the four bar mechanism.
- (Update later) A LiPo battery.
- Our own dessing for PCB serving as a shield and power stage for the raspberry, it used two LM2596 buck regulator modules.
