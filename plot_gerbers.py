'''
    A python script example to create various plot files from a board:
    Fab files
    Doc files
    Gerber files

    Important note:
        this python script does not plot frame references.
        the reason is it is not yet possible from a python script because plotting
        plot frame references needs loading the corresponding page layout file
        (.wks file) or the default template.

        This info (the page layout template) is not stored in the board, and therefore
        not available.

        Do not try to change SetPlotFrameRef(False) to SetPlotFrameRef(true)
        the result is the pcbnew lib will crash if you try to plot
        the unknown frame references template.
'''

import sys
import os
import pcbnew
import time

import logging
import zipfile
import shutil


from pcbnew import *
from datetime import datetime
from shutil import copy


filename=sys.argv[1]
project_name = os.path.splitext(os.path.split(filename)[1])[0]
project_path = os.path.abspath(os.path.split(filename)[0])

output_directory = os.path.join(project_path,'plot')

today = datetime.now().strftime('%Y%m%d_%H%M%S')

board = LoadBoard(filename)

pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

popt.SetOutputDirectory(output_directory)

# Set some important plot options:
popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.35))

popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(False)
popt.SetExcludeEdgeLayer(True);
popt.SetScale(1)
popt.SetUseAuxOrigin(True)
popt.SetNegative(False)
popt.SetPlotReference(True)
popt.SetPlotValue(True)
popt.SetPlotInvisibleText(False)

# This by gerbers only (also the name is truly horrid!)
popt.SetSubtractMaskFromSilk(True) #remove solder mask from silk to be sure there is no silk on pads


plot_plan = [
    ( "CuTop", F_Cu, "Top layer", ".gtl"),
    ( "CuBottom", B_Cu, "Bottom layer", ".gbl"),
    ( "MaskBottom", B_Mask, "Mask Bottom", ".gbs"),
    ( "MaskTop", F_Mask, "Mask top", ".gts"),
    ( "PasteBottom", B_Paste, "Paste Bottom", ".gbp"),
    ( "PasteTop", F_Paste, "Paste Top", ".gtp"),
    ( "SilkTop", F_SilkS, "Silk Top", ".gto"),
    ( "SilkBottom", B_SilkS, "Silk Bottom", ".gbo"),
    ( "EdgeCuts", Edge_Cuts, "Edges", ".gml")
]

popt.SetMirror(False)
popt.SetDrillMarksType(PCB_PLOT_PARAMS.NO_DRILL_SHAPE)
print("Plotting Gerber Layers:")

fab_files = []

# Functional Gerber Plots 
for layer_info in plot_plan:
    pctl.SetLayer(layer_info[1])
    pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
    pctl.PlotLayer()
    time.sleep(0.01)
    pctl.ClosePlot()
    # Create a copy with same filename and Protel extensions.
    srcPlot = pctl.GetPlotFileName()
    dstPlot = os.path.join(output_directory,project_name + layer_info[3])
    shutil.move(srcPlot, dstPlot)
    print(layer_info[0] + " => " + dstPlot)
    fab_files.append(dstPlot)


#generate internal copper layers, if any
lyrcnt = board.GetCopperLayerCount();

for innerlyr in range ( 1, lyrcnt-1 ):
    pctl.SetLayer(innerlyr)
    lyrname = 'inner%s' % innerlyr
    pctl.OpenPlotfile(lyrname, PLOT_FORMAT_GERBER, "inner")
    pctl.PlotLayer()
    time.sleep(0.01)
    pctl.ClosePlot()
    # Create a copy with same filename and Protel extensions.
    srcPlot = pctl.GetPlotFileName()
    dstPlot = os.path.join(output_directory,project_name + '.g' + str(innerlyr + 1))
    shutil.move(srcPlot, dstPlot)
    print(lyrname + " => " + dstPlot)
    fab_files.append(dstPlot)


# Fabricators need drill files.
# sometimes a drill map file is asked (for verification purpose)
drlwriter = EXCELLON_WRITER( board )
drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )

mirror = False
minimalHeader = False
#offset = wxPoint(0,0)
offset = board.GetAuxOrigin()
mergeNPTH = True
drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

metricFmt = True
drlwriter.SetFormat( metricFmt )

genDrl = True
genMap = False
drlwriter.CreateDrillandMapFilesSet( output_directory, genDrl, genMap );

srcPlot = os.path.join(output_directory,project_name + '.drl')
dstPlot = os.path.join(output_directory,project_name + '.txt')
shutil.move(srcPlot, dstPlot)
print(srcPlot + " => " + dstPlot)
fab_files.append(dstPlot)

# One can create a text file to report drill statistics
rptfn = output_directory + '/drill_report.txt'
drlwriter.GenDrillReportFile( rptfn );



#zip up all files
zf = zipfile.ZipFile(os.path.join(output_directory,project_name + '_' + today + '.zip'), "w", zipfile.ZIP_DEFLATED)
abs_src = os.path.abspath(output_directory)
for filename in  fab_files:
        absname = os.path.abspath(filename)
        arcname = absname[len(abs_src) + 1:]
        print('zipping %s as %s' % (filename,
                                    arcname))
        zf.write(absname, arcname)
zf.close()

# We have just generated your plotfiles with a single script
