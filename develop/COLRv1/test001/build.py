# -*- coding: UTF-8 -*-
#
#   Build a variants of Bitcount VF/TTF/OTF from here.
#   Optionally add COLRv1 pixels into the UFO.
#
#   https://github.com/googlefonts/colr-gradients-spec
#
import os
import ufoLib2
from ufo2ft.constants import COLOR_LAYERS_KEY, COLOR_PALETTES_KEY
from fontTools.ttLib.tables import otTables as ot

def parseColorTable(colorTable):
    colorNames = []
    colors = []
    for line in colorTable.splitlines():
        line = line.strip()
        if not line:
            continue
        colorName, *hexColors = line.split()
        colorNames.append(colorName)
        colors.append([colorFromHex(hexColor) for hexColor in hexColors])

    palettes = [list(palette) for palette in zip(*colors)]
    colorIndices = {colorName: i for i, colorName in enumerate(colorNames)}
    return palettes, colorIndices


def colorFromHex(hexString):
    assert len(hexString) in [6, 8]
    channels = []
    for i in range(0, len(hexString), 2):
        channels.append(int(hexString[i : i + 2], 16) / 255)
    if len(channels) == 3:
        channels.append(1)
    return channels

colorTableSpice = """
    color1     C90900  132A66  038F60
    color2     FFD700  60A0EF  ABFE37
"""
colorTableSpice = """
    color1     FFD700  da2345  fab540
    color2     001100  003322  03d2a4
"""


f1 = ufoLib2.Font.open('ufo/Bitcount_Mono_Double1.ufo')
f2 = ufoLib2.Font.open('ufo/Bitcount_Mono_Double2.ufo')

palettes, colorIndexSpice = parseColorTable(colorTableSpice)

gradient_color1 = colorIndexSpice["color1"]
gradient_color2 = colorIndexSpice["color2"]

gradient_color1_color2 = {
    "Format": ot.PaintFormat.PaintLinearGradient,
    "ColorLine": {
        "ColorStop": [(0.0, gradient_color1), (1.0, gradient_color2)],
        "Extend": "reflect",
    },
    "x0": -1000,
    "y0": 0,
    "x1": 0,
    "y1": 900,
    "x2": 700,
    "y2": 0,
}

gradient_color2_color1 = {
    "Format": ot.PaintFormat.PaintLinearGradient,
    "ColorLine": {
        "ColorStop": [(0.0, gradient_color1), (1.0, gradient_color2)],
        "Extend": "reflect",
    },
    #"x0": 1000,
    #"y0": 0,
    #"x1": 2000,
    #"y1": 0,
    #"x2": 3000,
    #"y2": 0,
    "x0": 1000,
    "y0": 0,
    "x1": 2000,
    "y1": 1000,
    "x2": 1100,
    "y2": 2000,
}

colorGlyphs1 = {}
colorGlyphs2 = {}

for f, colorGlyphs, gradient_color_color in (
		(f1, colorGlyphs1, gradient_color2_color1), 
		(f2, colorGlyphs2, gradient_color1_color2)):
	for glyphName in sorted(f.keys()):

	    gradientLayers = [
	        {
	            "Format": ot.PaintFormat.PaintGlyph,
	            "Paint": gradient_color_color,
	            "Glyph": glyphName,
	        }
	    ]
	    colorGlyphs[glyphName] = (ot.PaintFormat.PaintColrLayers, gradientLayers)


	f.lib[COLOR_PALETTES_KEY] = palettes
	f.lib[COLOR_LAYERS_KEY] = colorGlyphs


f1.save()
f2.save()

os.system('fontmake -m BitcountMono_Double2-TEST.designspace -o variable')

print('--- Done')

