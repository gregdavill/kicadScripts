# kicadScripts
A collection of scripts to automate PCB rendering and exporting gerbers.

### Work inspired form the folling projects:
* [PcbDraw](https://github.com/yaqwsx/PcbDraw)
* [Scott Bezek's SplitFlap](https://github.com/scottbez1/splitflap)

I found PcbDraw after I started writting my own tool to do the same function. It's probably a better tool for rendering nice images of PCBs. 

# Usage #
Currently only a single script:

	python plot_board.py <PathToYourAwesomeProject.kicad_pcb>

Files are placed within a `plot` directory in the folder of the .kicad_pcb file

# Features #

* creates all the gerber/drill files required for fab, renames and zips them up.
* creates an SVG of the top and bottom sides of the board with nice colours and renders these to PNG with inkscape CLI.

# Examples #

![alt-text](example/bosonFrameGrabber-Front.png "bosonFrameGrabber Front")

![alt-text](example/bosonFrameGrabber-Back.png "bosonFrameGrabber Front")

# Improvements

- Draw drill hits properly.
- Trim images around PCB.
- Improve code
- Plot front and back Images next to each other on the same image.
- Remove hardcode of inkscape path.