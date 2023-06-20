# -*- coding: UTF-8 -*-
# This is a COLRv1 paint definition file for paintcompiler
import sys
from collections import defaultdict

sys.path.append(".")
from scriptsLib import SMIN, SDEF, SMAX, LDEF, LMIN, LMAX

P = 100
G = 2*P # Layer grid size
LS = 1 # Layer scaling of elements

###
# Colors and gradients
###

COLORS = [
    "#FFFFFFFF",  # white
    "#808080FF",  # color16=grey
    "#FF00FF80",  # color1 = (1, 0, 1, 0.5)
    "#FFFFFF80",  # color2 = (1, 1, 1, 0.5)
    "#0033FF80",  # color3 = (0, 0.2, 1, 0.5)
    "#FF330080",  # color4 = (1, 0.2, 0, 0.5)
    "#00FF0080",  # color5 = (0, 1, 0, 0.5),
    "#00FFFF80",  # color6 = (0, 1, 1, 0.5),
    "#00000080",  # color7 = (0, 0, 0, 0.5),
    "#0033FFFF",  # color10 = (0, 0.2, 1, 1),
    "#FF3300FF",  # color11 = (1, 0.2, 0, 1),
    "#FF00FFFF",  # color12= (1, 0, 1, 1),
    "#00FF00FF",  # color13= (0, 1, 0, 1),
    "#FFFFFFFF",  # color14= (1, 1, 1, 1),
    "#000000FF",  # color15=(0, 0, 0, 1),
]


# Define our two colour lines for the radial gradient.
# Colour line one is just all the colours spaced out linearly.
COLOR_STOPS1 = ColorLine({ix / len(COLORS): stop for ix, stop in enumerate(COLORS)})

# Colour line two is white plus all the colours in reverse.
COLORS2 = [COLORS[0]] + COLORS[-1:0:-1]
COLOR_STOPS2 = ColorLine({ix / len(COLORS2): stop for ix, stop in enumerate(COLORS2)})


###
# Elements and layers
###

# The 3 layers are really large areas that can be used to crop pixels shapes from.

## I'm going to define some "elements" here, some of which are just
## simple glyphs, and some are combinations of glyphs. We expect each
## element to be 100x100 and to be placed at the origin. We'll translate
## them to their correct place on the "layer" later.
## These elements come from the UFO Bitcount-LayerElements but when we
## copy them into the current font, we add an el_ to the start of their
## names.

# "hstripes" is an element made up of a red stripe at the bottom,
# a green stripe in the middle and a blue stripe at the top.
hstripes = PaintColrLayers(
    [
        PaintScale(0.2, PaintGlyph("el_stripe", PaintSolid("#FF0000FF"))),
        PaintTranslate(
            0, G, PaintScale(LS, PaintGlyph("el_stripe", PaintSolid("#00FF00FF")))
        ),
        PaintTranslate(
            0, G, PaintScale(LS, PaintGlyph("el_stripe", PaintSolid("#0000FFFF")))
        ),
    ]
)
# boxes is four boxes; the element is 100x100 so we'll scale it down,
# then reposition four copies of it.
boxes = PaintColrLayers(
    [
        PaintTranslate(
            0, G/2, PaintScale(LS, PaintGlyph("el_square", PaintSolid("#F34F1CFF")))
        ),
        PaintTranslate(
            G/2, G/2, PaintScale(LS, PaintGlyph("el_square", PaintSolid("#7FBC00FF")))
        ),
        PaintTranslate(
            0, 0, PaintScale(LS, PaintGlyph("el_square", PaintSolid("#01A6F0FF")))
        ),
        PaintTranslate(
            G/2, 0, PaintScale(LS, PaintGlyph("el_square", PaintSolid("#FFBA01FF")))
        ),
        # Oh look it's the Microsoft logo.
    ]
)

balls = PaintColrLayers(
    [
        PaintTranslate(
            0, G/2, PaintScale(LS, PaintGlyph("el_circle1", PaintSolid("#F34F1CFF")))
        ),
        PaintTranslate(
            G/2, G/2, PaintScale(LS, PaintGlyph("el_circle1", PaintSolid("#7FBC00FF")))
        ),
        PaintTranslate(
            0, 0, PaintScale(LS, PaintGlyph("el_circle1", PaintSolid("#01A6F0FF")))
        ),
        PaintTranslate(
            G/2, 0, PaintScale(LS, PaintGlyph("el_circle1", PaintSolid("#FFBA01FF")))
        ),
    ]
)

zigzag_right = PaintScale(
    LS,
    PaintGlyph(
        "el_zigzag",
        PaintLinearGradient(
            (G/2, G/2),
            (G/2*10, G/2*10),
            (0, G/2),
            ColorLine(
                {
                    0.0: "#662233A0",
                    1.0: "#226666A0",
                }
            ),
        ),
    ),
)

zigzag_down = PaintRotate(
    90,
    PaintScale(LS, PaintGlyph("el_zigzag", PaintSolid("#FF00FFFF"))),
    center=(G/2, G/2),
)

circle1 = PaintGlyph(
    "el_circle", PaintRadialGradient((0, 0), 1, (0, 0), 8*G, COLOR_STOPS1)
)
circle2 = PaintGlyph(
    "el_circle", PaintRadialGradient((0, 0), 1, (0, 0), 8*G, COLOR_STOPS2)
)


linear_box = PaintGlyph(
    "el_square", PaintLinearGradient((0, 0), (G, G), (4*G, 4*G), COLOR_STOPS1)
)
linear_box2 = PaintGlyph(
    "el_square", PaintLinearGradient((0, 0), (G, G), (4*G, 4*G), COLOR_STOPS2)
)

concentric_boxes = PaintColrLayers(
    [
        PaintTransform(
            (1.0, 0.0, 0.0, 1.0, 0, 0), PaintGlyph("el_square", PaintSolid(COLORS[1]))
        ),
        PaintTransform(
            (0.75, 0.0, 0.0, 0.75, 12, 12),
            PaintGlyph("el_square", PaintSolid(COLORS[2])),
        ),
        PaintTransform(
            (0.5, 0.0, 0.0, 0.5, 25, 25), PaintGlyph("el_square", PaintSolid(COLORS[3]))
        ),
        PaintTransform(
            (0.25, 0.0, 0.0, 0.25, 37, 37),
            PaintGlyph("el_square", PaintSolid(COLORS[4])),
        ),
    ]
)

concentric_boxes2 = PaintColrLayers(
    [
        PaintTransform(
            (1.0, 0.0, 0.0, 1.0, 0, 0), PaintGlyph("el_square", PaintSolid(COLORS[-1]))
        ),
        PaintTransform(
            (0.75, 0.0, 0.0, 0.75, 12, 12),
            PaintGlyph("el_square", PaintSolid(COLORS[-2])),
        ),
        PaintTransform(
            (0.5, 0.0, 0.0, 0.5, 25, 25),
            PaintGlyph("el_square", PaintSolid(COLORS[-3])),
        ),
        PaintTransform(
            (0.25, 0.0, 0.0, 0.25, 37, 37),
            PaintGlyph("el_square", PaintSolid(COLORS[-4])),
        ),
    ]
)

vstripes = PaintRotate(
    90,
    PaintColrLayers(
        [
            PaintScale(LS, PaintGlyph("el_stripe", PaintSolid("#FFFF0033"))),
            PaintTranslate(
                0, G/2, PaintScale(LS, PaintGlyph("el_stripe", PaintSolid("#FFFF0033")))
            ),
            PaintTranslate(
                0, G/2, PaintScale(LS, PaintGlyph("el_stripe", PaintSolid("#00FFFF33")))
            ),
        ]
    ),
    center=(G/2, G/2),
)

# Now we make the layers, by transforming those elements into place in a
# grid
layer1 = PaintColrLayers(
    [
        PaintTranslate(-G, G, circle1),
        PaintTranslate(0, G, circle1),
        PaintTranslate(G, G, circle1),
        PaintTranslate(-G, 0, circle1),
        PaintTranslate(0, 0, circle1),
        PaintTranslate(G, 0, circle1),
        PaintTranslate(-G, -G, circle1),
        PaintTranslate(0, -G, circle1),
        PaintTranslate(G, -G, circle1),
    ]
)

# The layer now gets shifted and scaled based on the value of the
# BG-X/BG-Y/BG-S coords
scale_factor1 = {
    (("BG-S", SMIN),): 0.1, 
    (("BG-S", SDEF),): 1.0, 
    (("BG-S", SMAX),): 5,
}
x_pixel1 = {
    (("BG-X", LMIN),): - 2 * G,
    (("BG-X", LDEF),): 0,
    (("BG-X", LMAX),): 2 * G,
}
y_pixel1 = {
    (("BG-Y", LMIN),): - 2 * G,
    (("BG-Y", LDEF),): 0,
    (("BG-Y", LMAX),): 2 * G,
}
x_canvas1 = {
    (("BG-X", LMIN),): 500 - P/2 - 2 * G,
    (("BG-X", LDEF),): 500 - P/2,
    (("BG-X", LMAX),): 500 - P/2 + 2 * G,
}
y_canvas1 = {
    (("BG-Y", LMIN),): P - 2 * G,
    (("BG-Y", LDEF),): P,
    (("BG-Y", LMAX),): P + 2 * G,
}

#layer1_pixel = PaintTransform(
#    (scale_factor1, 0, 0, scale_factor1, 0, 0), PaintTranslate(x_pixel1, y_pixel1, layer1)
#)
#layer1_canvas = PaintTransform(
#    (scale_factor1, 0, 0, scale_factor1, 0, 0), PaintTranslate(x_canvas1, y_canvas1, layer1)
#    #x_canvas1, y_canvas1, PaintTransform((scale_factor1, 0, 0, scale_factor1, 0, 0), layer1)
#)
layer1_pixel = PaintTranslate(
    x_pixel1, y_pixel1, PaintTransform((scale_factor1, 0, 0, scale_factor1, 0, 0), layer1)
)
layer1_canvas = PaintTranslate(
    x_canvas1, y_canvas1, PaintTransform((scale_factor1, 0, 0, scale_factor1, 0, 0), layer1)
)

# Same deal for layer 2
layer2 = PaintColrLayers(
    [
        #PaintTranslate(-2*G, G, vstripes),
        #PaintTranslate(-G, G, balls),
        #PaintTranslate(G, 2*G, zigzag_right),
        #PaintTranslate(-2*G, 0, circle2),
        #PaintTranslate(-G, 0, linear_box2),
        #PaintTranslate(5G 0, concentric_boxes2),

        PaintTranslate(-G, G, circle2),
        PaintTranslate(0, G, circle2),
        PaintTranslate(G, G, circle2),
        PaintTranslate(-G, 0, circle2),
        PaintTranslate(0, 0, circle2),
        PaintTranslate(G, 0, circle2),
        PaintTranslate(-G, -G, circle2),
        PaintTranslate(0, -G, circle2),
        PaintTranslate(G, -G, circle2),
    ]
)
scale_factor2 = {
    (("FG-S", SMIN),): 0.1, 
    (("FG-S", SDEF),): 1.0, 
    (("FG-S", SMAX),): 5,
}
x_pixel2 = {
    (("FG-X", LMIN),): -2 * G,
    (("FG-X", LDEF),): 0,
    (("FG-X", LMAX),): 2 * G,
}
y_pixel2 = {
    (("FG-Y", LMIN),): -2 * G,
    (("FG-Y", LDEF),): 0,
    (("FG-Y", LMAX),): 2 * G,
}
x_canvas2 = {
    (("FG-X", LMIN),): 500 - P/2 - 2 * G,
    (("FG-X", LDEF),): 500 - P/2,
    (("FG-X", LMAX),): 500 - P/2 + 2 * G,
}
y_canvas2 = {
    (("FG-Y", LMIN),): P - 2 * G,
    (("FG-Y", LDEF),): P,
    (("FG-Y", LMAX),): P + 2 * G
}

#layer2_pixel = PaintTransform(
#    (scale_factor2, 0, 0, scale_factor2, 0, 0), PaintTranslate(x_pixel2, y_pixel2, layer2)
#)
#layer2_canvas = PaintTransform(
#    (scale_factor2, 0, 0, scale_factor2, 0, 0), PaintTranslate(x_canvas2, y_canvas2, layer2)
#    #x_canvas2, y_canvas2, PaintTransform((scale_factor2, 0, 0, scale_factor2, 0, 0), layer2)
#)
layer2_pixel = PaintTranslate(
    x_pixel2, y_pixel2, PaintTransform((scale_factor2, 0, 0, scale_factor2, 0, 0), layer2)
)
layer2_canvas = PaintTranslate(
    x_canvas2, y_canvas2, PaintTransform((scale_factor2, 0, 0, scale_factor2, 0, 0), layer2)
)

##
# Applying the pixels
##


# To build a pixel glyph, we paint each pixel twice, once with each
# layer. We might want to change this to clever compositing/blending
# later, depending on how things look when we have the layers working
# correctly. So this function returns a paint tree with a PaintColrLayers
# operation, containing two layers for each pixel.
def buildPixelGlyph(pixelGlyphName, pixelPositions, layer1, layer2):
    layers = []
    for x, y in pixelPositions:
        layers.append(PaintTranslate(x, y, PaintGlyph(pixelGlyphName, layer1)))
        layers.append(PaintTranslate(x, y, PaintGlyph(pixelGlyphName, layer2)))
    return PaintColrLayers(layers)


# Now admittedly this is complicated, because the "pixel position"
# differs across the design space. To make this work, the returned
# coordinates will actually be "variable points" like those we
# created above (for the centers of our radial gradients), specifying
# how each pixel moves in the designspace.
# Thankfully, the pixel only differs when the "slnt" axis is applied
# (at this point - I think we might need to do the same for the width
# axis in compressed fonts), so we gather each pixel position at the
# extremes of that axis, and turn them into a dictionary.
def pixelPositions(f, gName):
    positions_x = defaultdict(dict)
    positions_y = defaultdict(dict)
    for slnt_ax in [0, 1000]:
        location = {"slnt": slnt_ax}
        # We are working on the (binary) TTFont, so we have to do
        # horrible magic to find the component locations.
        gs = font.getGlyphSet(location=location)
        glyph = gs[gName]._getGlyphInstance()
        if not hasattr(glyph, "components"):
            return []
        for ix, component in enumerate(glyph.components):
            positions_x[ix][tuple(location.items())] = component.x
            positions_y[ix][tuple(location.items())] = component.y
    return list(zip(list(positions_x.values()), list(positions_y.values())))


# OK, we are finally ready to create the paint trees for each glyph.
# We do this by adding an entry into the "glyphs" dictionary mapping
# the glyph name to the paint tree.
for glyphName in font.getGlyphOrder():
    if glyphName == "canvas":
        glyphs[glyphName] = buildPixelGlyph(
            "_canvas",
            pixelPositions(font, glyphName),
            layer1_canvas,
            layer2_canvas,
        )
    else:
        glyphs[glyphName] = buildPixelGlyph(
            "px",
            pixelPositions(font, glyphName),
            layer1_pixel,
            layer2_pixel,
        )

# We have a problem; we have added six new axes to the font at this point,
# and while the gvar table can cope with that because it gets rebuilt when
# the font is saved, the HVAR table is not fully decompiled by fontTools,
# so it still refers to four axes, which makes it invalid when you try
# to save the font. Thankfully, HVAR isn't very necessary anyway, so we
# just get rid of it.
del font["HVAR"]
