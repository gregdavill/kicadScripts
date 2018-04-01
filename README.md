# kicadScripts
A collection of scripts to automate PCB rendering and exporting gerbers.

### Work inspired form the folling projects:
* [PcbDraw](https://github.com/yaqwsx/PcbDraw)
* [Scott Bezek's SplitFlap](https://github.com/scottbez1/splitflap)

I found PcbDraw after I started writting my own tool to do the same function. It's probably a better tool for rendering nice images of PCBs. 

# Usage #
## Create Pretty PNGs

`python plot_board.py <PathToYourAwesomeProject.kicad_pcb>`

## Create a GerberZip

`python plot_gerbers.py <PathToYourAwesomeProject.kicad_pcb>`

Files are placed within a `plot` directory in the folder of the .kicad_pcb file

# Features #

### plot_board.py

* Uses Kicad python bindings to render board layers as SVG
* Recolours SVGs
* Stacks SVGs with user defined colour/opacity
* Creates a drill layer
* Mirrors the backside of the PCB.
* Render to PNG with Inkscape CLI

### plot_gerbers.py

* creates all the gerber/drill files.
* Renames with Protel Extensions `gtl,gts,gto,gml...`
* Puts all files into a single zip
* Renames Zip: `<Project><Date>_<Time>.zip` for easy tracking of versions.


# Examples #

![alt-text](example/bosonFrameGrabber-Front.png "bosonFrameGrabber Front")

![alt-text](example/bosonFrameGrabber-Back.png "bosonFrameGrabber Front")

# Improvements

- Correctly Trim images around PCB. (bounding box of PCB is too large.)
- Generally Cleanup/Improve code
- Plot front and back Images next to each other on the same image.
- Better Handling of colours (Add OSHPark colours)