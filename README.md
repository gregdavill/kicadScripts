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

- Draw drill hits properly.
- Trim images around PCB.
- Improve code
- Plot front and back Images next to each other on the same image.
- Remove hardcode of inkscape path.