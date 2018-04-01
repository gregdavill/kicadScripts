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
import subprocess

from svg_processor import SvgProcessor

from pcbnew import *
from datetime import datetime
from shutil import copy


filename=sys.argv[1]
project_name = os.path.splitext(os.path.split(filename)[1])[0]
project_path = os.path.abspath(os.path.split(filename)[0])

output_directory = os.path.join(project_path,'plot')

temp_dir = os.path.join(output_directory, 'temp')
shutil.rmtree(temp_dir, ignore_errors=True)
os.makedirs(temp_dir)


today = datetime.now().strftime('%Y%m%d_%H%M%S')

board = LoadBoard(filename)

pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

popt.SetOutputDirectory(temp_dir)

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
popt.SetPlotReference(False)
popt.SetPlotValue(False)
popt.SetPlotInvisibleText(False)

# This by gerbers only (also the name is truly horrid!)
popt.SetSubtractMaskFromSilk(False) #remove solder mask from silk to be sure there is no silk on pads


# Visual Plot 
def renderPNG(plot_plan, output_filename):
    processed_svg_files = []
    popt.SetDrillMarksType(PCB_PLOT_PARAMS.FULL_DRILL_SHAPE)

    for layer_info in plot_plan:
        if layer_info[4] == "Invert":
            popt.SetNegative(True)
        else:
            popt.SetNegative(False)

        pctl.SetLayer(layer_info[1])
        pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_SVG, layer_info[2])
        print layer_info[0]
        pctl.PlotLayer()
        time.sleep(0.01)
        pctl.ClosePlot()
        processor = SvgProcessor(pctl.GetPlotFileName())
        def colorize(original):
            # For invert to work we need to invert default colours. 
            if layer_info[4] == "Invert":
                if original.lower() == '#000000':
                    return '#ffffff'
                return '#000000'
            else:
                if original.lower() == '#000000':
                    return layer_info[5]
                return original
        processor.apply_color_transform(colorize)
        if layer_info[4] == "Invert":
            # Invert call will group all svg objects into a Mask then create a Blank Rectangel to mask out off.
            processor.Invert(layer_info[5], layer_info[6])
        else:
            processor.wrap_with_group({
            'opacity': str(layer_info[6]),
        })
        output_filename2 = os.path.join(temp_dir, 'processed-' + os.path.basename(pctl.GetPlotFileName()))
        processor.write(output_filename2)
        processed_svg_files.append((output_filename2, processor))


    print 'Merging layers...'
    final_svg = os.path.join(output_directory, project_name + '-merged.svg')

    shutil.copyfile(processed_svg_files[0][0], final_svg) # use first layer SVG as a container.
    processed_svg_files.pop(0) # hack so that the first layer is not rendered twice
    output_processor = SvgProcessor(final_svg)
    for _, processor in processed_svg_files:
        output_processor.import_groups(processor) # add new layers to the file.
    output_processor.write(final_svg)

    print 'Rasterizing...'
    final_png = os.path.join(output_directory, output_filename)

    subprocess.check_call([
        'C:\Program Files\Inkscape\inkscape',
        '--export-area-drawing',
        '--export-dpi=600',
        '--export-png', final_png,
        '--export-background', plot_bg,
        final_svg,
    ])



plot_bg = '#064A00'
# Once the defaults are set it become pretty easy...
# I have a Turing-complete programming language here: I'll use it...
# param 0 is a string added to the file base name to identify the drawing
# param 1 is the layer ID
plot_plan = [
    ( "CuTop", F_Cu, "Top layer", ".gtl", "",'#E8D959',0.85 ),
    ( "MaskTop", F_Mask, "Mask top", ".gts", "Invert" ,'#1D5D17',0.8 ),
    ( "PasteTop", F_Paste, "Paste Top", ".gtp", "" ,'#9E9E9E',0.95 ),
    ( "SilkTop", F_SilkS, "Silk Top", ".gto", "" ,'#fefefe',1.0 ),
    ( "EdgeCuts", Edge_Cuts, "Edges", ".gml", ""  ,'#000000',0.2 ),
]
renderPNG(plot_plan, project_name + '-Front.png')

popt.SetMirror(True)
plot_plan = [
    ( "CuBottom", B_Cu, "Bottom layer", ".gbl", "",'#E8D959',0.85 ),
    ( "MaskBottom", B_Mask, "Mask Bottom", ".gbs", "Invert" ,'#1D5D17',0.8 ),
    ( "PasteBottom", B_Paste, "Paste Bottom", ".gbp", "" ,'#9E9E9E',0.95 ),
    ( "SilkTop", B_SilkS, "Silk Bottom", ".gbo", "" ,'#fefefe',1.0 ),
    ( "EdgeCuts", Edge_Cuts, "Edges", ".gml", ""  ,'#000000',0.2 ),
]
renderPNG(plot_plan, project_name + '-Back.png')

shutil.rmtree(temp_dir, ignore_errors=True)
# We have just generated your plotfiles with a single script
