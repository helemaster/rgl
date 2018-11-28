#MRGL
Holly LeMaster, 2017-18
Final 1.0.* Release
GitHub repository: https://github.com/helemaster/rgl

#PURPOSE

MRGL is an ASCII roguelike with a modernized setting. Built using the libtcod library, this project was started in 2017 as a project for my degree at Harrisburg University of Science and Technology. 

#HOW TO PLAY

##System Requirements

1. Designed for Microsoft Windows
   - Potentially works on Linux distributions; untested
2. 32-bit Python installation
   -Installation on C: drive recommended

##Launching the game

###METHOD 1: Batch File 

1. Open the game directory.
2. Find the `PLAY.bat` file.
3. Double click it to launch the game.

*Note: modification of the batch file may be necessary depending on the location of your Python installation.*

###METHOD 2: Command Prompt

1. Open a command prompt.
2. Change to the installation directory of the game.
3. Run the following command: `C:\Python27\Python.exe main.py`
4. The game will launch.

##Controls

1. Arrow keys move the player in corresponding directions.
2. Alt+enter toggles fullscreen.
3. Esc exits the game.
4. Bump into monsters to attack them.
5. i: Inventory
6. x: Descend stairs
7. c: View character details
8. t: Talk to NPC

#TROUBLESHOOTING

1. Is Python 2.7 installed to the C: drive?
   - Install Python 2.7 to the C: drive. This is needed for the game to run.
   - Alternatively, modify the batch file or command used to play the game to the correct Python path.
2. The game crashes when I exit: Python.exe has stopped working.
   - This is a bug that should be patched. Please report the bug if it occurs.
	
#REPORTING BUGS

Please report any bugs/issues [here] (https://github.com/helemaster/rgl/issues).
