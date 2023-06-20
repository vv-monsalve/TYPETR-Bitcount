# -*- coding: UTF-8 -*-
# This is a COLRv1 paint definition file for paintcompiler
import sys
from collections import defaultdict

sys.path.append(".")
from scriptsLib import SMIN, SDEF, SMAX, LDEF, LMIN, LMAX, POST_FIX

P = 100
G = 6*P # Layer grid size, so we can divide into 6 spectrum colors
LS = 1 # Layer scaling of elements

# String additions to the colors, defining standard level of opacity
OPAQUE = "FF"
TRANSPARANT = "AA"
FAINT = "80"

###
# Colors and gradients
###

BLACK = "#000000"
GREY = "#808080"
WHITE = "#FFFFFF"

RED = "#FF0000"  # Red=(1, 0, 0, ?)
ORANGE = "#FFAB00"
YELLOW = "#FFFF00"
GREEN = "#88FF00"
BLUE = "#01A6F0"
PURPLE = "#C700FF"

# Interesting range of colors for the gradient circles
CIRCLE_COLORS = [
    WHITE + OPAQUE,  # white
    GREY + OPAQUE,  # color16=grey
    "#FF00FF80",  # color1 = (1, 0, 1, 0.5)
    "#FFFFFF80",  # color2 = (1, 1, 1, 0.5)
    "#0033FF80",  # color3 = (0, 0.2, 1, 0.5)
    "#FF330080",  # color4 = (1, 0.2, 0, 0.5)
    "#00FF0080",  # color5 = (0, 1, 0, 0.5),
    "#00FFFF80",  # color6 = (0, 1, 1, 0.5),
    BLACK + OPAQUE,  # color7 = (0, 0, 0, 0.5),
    "#0033FFFF",  # color10 = (0, 0.2, 1, 1),
    "#FF3300FF",  # color11 = (1, 0.2, 0, 1),
    "#FF00FFFF",  # color12= (1, 0, 1, 1),
    "#00FF00FF",  # color13= (0, 1, 0, 1),
    WHITE + OPAQUE,  # color14= (1, 1, 1, 1),
    BLACK + OPAQUE,  # color15=(0, 0, 0, 1),
]


# Define our two colour lines for the radial gradient.
# Colour line one is just all the colours spaced out linearly.
COLOR_LINE1 = {ix / len(CIRCLE_COLORS): stop for ix, stop in enumerate(CIRCLE_COLORS)}
COLOR_STOPS1 = ColorLine(COLOR_LINE1)

# Colour line two is white plus all the colours in reverse.
CIRCLE_COLORS2 = [CIRCLE_COLORS[0]] + CIRCLE_COLORS[-1:0:-1]
COLOR_LINE2 = {ix / len(CIRCLE_COLORS): stop for ix, stop in enumerate(CIRCLE_COLORS2)}
COLOR_STOPS2 = ColorLine({ix / len(CIRCLE_COLORS2): stop for ix, stop in enumerate(CIRCLE_COLORS2)})

SPECTRUM = ColorLine({0: RED, 0.25: ORANGE, 0.5: YELLOW, 0.75: GREEN, 1: BLUE})

###
# Elements and layers
###

# The 3 layers are really large areas that can be used to crop pixels shapes from.

## I'm going to define some "elements" here, some of which are just
## simple glyphs, and some are combinations of glyphs. We expect each
## element to be 100x100 and to be placed at the origin. We'll translate
## them to their correct place on the "layer" later.
## These elements come from the UFO Bitcount-LayerElements but when we
## copy them into the current font, we add an POST_FIX (el_) to the start of their
## names.

# "hstripes" is an element made up of a red stripe at the bottom,
# a green stripe in the middle and a blue stripe at the top.

hstripes = PaintColrLayers(
    [
        PaintTranslate(
            0, -G/2 + P/2, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(RED + OPAQUE)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 1/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(ORANGE + OPAQUE)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 2/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(YELLOW + OPAQUE)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 3/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(GREEN + OPAQUE)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 4/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(BLUE + OPAQUE)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 5/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(PURPLE + OPAQUE)))
        ),
    ]
)
hstripes_opaque = PaintColrLayers(
    [
        PaintTranslate(
            0, -G/2 + P/2, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(RED + TRANSPARANT)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 1/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(ORANGE + TRANSPARANT)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 2/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(YELLOW + TRANSPARANT)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 3/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(GREEN + TRANSPARANT)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 4/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(BLUE + TRANSPARANT)))
        ),
        PaintTranslate(
            0, -G/2 + P/2 + G * 5/6, PaintScale(LS, PaintGlyph(POST_FIX + "hstripe", PaintSolid(PURPLE + TRANSPARANT)))
        ),
    ]
)
vstripes = PaintColrLayers(
    [
        PaintTranslate(
            -G/2 + P/2, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(RED + OPAQUE)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 1/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(ORANGE + OPAQUE)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 2/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(YELLOW + OPAQUE)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 3/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(GREEN + OPAQUE)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 4/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(BLUE + OPAQUE)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 5/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(PURPLE + OPAQUE)))
        ),
    ]
)
vstripes_opaque = PaintColrLayers(
    [
        PaintTranslate(
            -G/2 + P/2, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(RED + TRANSPARANT)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 1/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(ORANGE + TRANSPARANT)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 2/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(YELLOW + TRANSPARANT)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 3/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(GREEN + TRANSPARANT)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 4/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(BLUE + TRANSPARANT)))
        ),
        PaintTranslate(
            -G/2 + P/2 + G * 5/6, 0, PaintScale(LS, PaintGlyph(POST_FIX + "vstripe", PaintSolid(PURPLE + TRANSPARANT)))
        ),
    ]
)

# boxes is four boxes; the element is 100x100 so we'll scale it down,
# then reposition four copies of it.
boxes = PaintColrLayers(
    [
        PaintTranslate(
            0, G/2, PaintScale(LS, PaintGlyph(POST_FIX + "square", PaintSolid("#F34F1CFF")))
        ),
        PaintTranslate(
            G/2, G/2, PaintScale(LS, PaintGlyph(POST_FIX + "square", PaintSolid("#7FBC00FF")))
        ),
        PaintTranslate(
            0, 0, PaintScale(LS, PaintGlyph(POST_FIX + "square", PaintSolid("#01A6F0FF")))
        ),
        PaintTranslate(
            G/2, 0, PaintScale(LS, PaintGlyph(POST_FIX + "square", PaintSolid("#FFBA01FF")))
        ),
        # Oh look it's the Microsoft logo.
    ]
)

balls = PaintColrLayers(
    [
        PaintTranslate(
            0, G/2, PaintScale(LS, PaintGlyph(POST_FIX + "circle", PaintSolid("#F34F1CFF")))
        ),
        PaintTranslate(
            G/2, G/2, PaintScale(LS, PaintGlyph(POST_FIX + "circle", PaintSolid("#7FBC00FF")))
        ),
        PaintTranslate(
            0, 0, PaintScale(LS, PaintGlyph(POST_FIX + "circle", PaintSolid("#01A6F0FF")))
        ),
        PaintTranslate(
            G/2, 0, PaintScale(LS, PaintGlyph(POST_FIX + "circle", PaintSolid("#FFBA01FF")))
        ),
    ]
)

zigzag_right = PaintScale(
    LS,
    PaintGlyph(
        POST_FIX + "zigzag",
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
    PaintScale(LS, PaintGlyph(POST_FIX + "zigzag", PaintSolid("#FF00FFFF"))),
    center=(G/2, G/2),
)

chess = PaintColrLayers(
    [   
        PaintGlyph(POST_FIX + "chess", PaintRadialGradient((0, 0), 1, (0, 0), G/2, COLOR_STOPS1)),
    ]
)

circle1 = PaintColrLayers(
    [   
        # Start with a gray square to fill the space a bit.
        PaintGlyph(POST_FIX + "square_large", PaintSolid("#DDDDDDFF")),
        # The a white circle as background.
        PaintGlyph(POST_FIX + "circle_large", PaintSolid("#FFFFFFFF")),
        PaintGlyph(POST_FIX + "circle_large", PaintRadialGradient((0, 0), 1, (0, 0), G/2, COLOR_STOPS1)),

    ]
)
circle2 = PaintGlyph(
   POST_FIX + "circle_large", PaintRadialGradient((0, 0), 1, (0, 0), G/2, COLOR_STOPS2)
)
#circle3 = PaintGlyph(
#    POST_FIX + "circle_large", PaintRadialGradient((0, 0), 1, (0, 0), G/2, COLOR_STOPS2)
#)


linear_box1 = PaintGlyph(
    POST_FIX + "square_large", PaintLinearGradient((0, 0), (P/2, P/2), (G/2, G/2), COLOR_STOPS1)
)
linear_box2 = PaintGlyph(
    POST_FIX + "square_large", PaintLinearGradient((0, 0), (P/2, P/2), (G/2, G/2), COLOR_STOPS2)
)
#linear_box3 = PaintGlyph(
#    POST_FIX + "square_large", PaintLinearGradient((0, 0), (P/2, P/2), G/3, COLOR_STOPS1)
#)

concentric_boxes = PaintColrLayers(
    [
        PaintTransform(
            (1.0, 0.0, 0.0, 1.0, 0, 0), PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[1]))
        ),
        PaintTransform(
            (0.75, 0.0, 0.0, 0.75, 12, 12),
            PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[2])),
        ),
        PaintTransform(
            (0.5, 0.0, 0.0, 0.5, 25, 25), PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[3]))
        ),
        PaintTransform(
            (0.25, 0.0, 0.0, 0.25, 37, 37),
            PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[4])),
        ),
    ]
)

concentric_boxes2 = PaintColrLayers(
    [
        PaintTransform(
            (1.0, 0.0, 0.0, 1.0, 0, 0), PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[-1]))
        ),
        PaintTransform(
            (0.75, 0.0, 0.0, 0.75, 12, 12),
            PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[-2])),
        ),
        PaintTransform(
            (0.5, 0.0, 0.0, 0.5, 25, 25),
            PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[-3])),
        ),
        PaintTransform(
            (0.25, 0.0, 0.0, 0.25, 37, 37),
            PaintGlyph(POST_FIX + "square", PaintSolid(CIRCLE_COLORS[-4])),
        ),
    ]
)

# Now we make the layers, by transforming those elements into place in a grid
layer1 = PaintColrLayers(
    [
        PaintTranslate(-G + P/2, G + P/2, hstripes),
        PaintTranslate(P/2, G + P/2, chess),
        PaintTranslate(G + P/2, G + P/2, vstripes),
        PaintTranslate(-G + P/2, P/2, circle1),
        PaintTranslate(P/2, P/2, circle1),
        PaintTranslate(G + P/2, P/2, circle1),
        PaintTranslate(-G + P/2, -G + P/2, circle1),
        PaintTranslate(P/2, -G + P/2, circle1),
        PaintTranslate(G + P/2, -G + P/2, circle1),
    ]
)

# The layer now gets shifted and scaled based on the value of the
# LR1X/LR1Y/LR1S coords
scale_factor1 = {
    (("LR1S", SMIN),): 0, 
    (("LR1S", SDEF),): 1, 
    (("LR1S", SMAX),): 20,
}
# Position of the pixels in normal glyphs
x_pixel1 = {
    (("LR1X", LMIN),): - 2 * G,
    (("LR1X", LDEF),): 0,
    (("LR1X", LMAX),): 2 * G,
}
y_pixel1 = {
    (("LR1Y", LMIN),): - 2 * G,
    (("LR1Y", LDEF),): 0,
    (("LR1Y", LMAX),): 2 * G,
}
# Position of the pixels in the /canvas glyph
x_canvas1 = {
    (("LR1X", LMIN),): 500 - P/2 - 2 * G,
    (("LR1X", LDEF),): 500 - P/2,
    (("LR1X", LMAX),): 500 - P/2 + 2 * G,
}
y_canvas1 = {
    (("LR1Y", LMIN),): P - 2 * G,
    (("LR1Y", LDEF),): P,
    (("LR1Y", LMAX),): P + 2 * G,
}

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

        PaintTranslate(-G + P/2, G + P/2, vstripes_opaque),
        PaintTranslate(P/2, G + P/2, chess),
        PaintTranslate(G + P/2, G + P/2, hstripes_opaque),
        PaintTranslate(-G + P/2, P/2, circle2),
        PaintTranslate(P/2, P/2, circle2),
        PaintTranslate(G + P/2, P/2, circle2),
        PaintTranslate(-G + P/2, -G + P/2, circle2),
        PaintTranslate(P/2, -G + P/2, circle2),
        PaintTranslate(G + P/2, -G + P/2, circle2),
    ]
)
scale_factor2 = {
    (("LR2S", SMIN),): 0, 
    (("LR2S", SDEF),): 1, 
    (("LR2S", SMAX),): 20,
}
# Position of the pixels in normal glyphs
x_pixel2 = {
    (("LR2X", LMIN),): -2 * G,
    (("LR2X", LDEF),): 0,
    (("LR2X", LMAX),): 2 * G,
}
y_pixel2 = {
    (("LR2Y", LMIN),): -2 * G,
    (("LR2Y", LDEF),): 0,
    (("LR2Y", LMAX),): 2 * G,
}
# Position of the pixels in the /canvas glyph
x_canvas2 = {
    (("LR2X", LMIN),): 500 - P/2 - 2 * G,
    (("LR2X", LDEF),): 500 - P/2,
    (("LR2X", LMAX),): 500 - P/2 + 2 * G,
}
y_canvas2 = {
    (("LR2Y", LMIN),): P - 2 * G,
    (("LR2Y", LDEF),): P,
    (("LR2Y", LMAX),): P + 2 * G
}

layer2_pixel = PaintTranslate(
    x_pixel2, y_pixel2, PaintTransform((scale_factor2, 0, 0, scale_factor2, 0, 0), layer2)
)
layer2_canvas = PaintTranslate(
    x_canvas2, y_canvas2, PaintTransform((scale_factor2, 0, 0, scale_factor2, 0, 0), layer2)
)

if 0:
    # Same deal for layer 3
    layer3 = PaintColrLayers(
        [
            PaintTranslate(-G + P/2, G + P/2, linear_box3),
            PaintTranslate(P/2, G + P/2, linear_box3),
            PaintTranslate(G + P/2, G + P/2, linear_box3),
            PaintTranslate(-G + P/2, P/2, circle3),
            PaintTranslate(P/2, P/2, circle3),
            PaintTranslate(G + P/2, P/2, circle3),
            PaintTranslate(-G + P/2, -G + P/2, circle3),
            PaintTranslate(P/2, -G + P/2, circle3),
            PaintTranslate(G + P/2, -G + P/2, circle3),
        ]
    )
    scale_factor3 = {
        (("LR3S", SMIN),): 0, 
        (("LR3S", SDEF),): 0, # By default layer #2 and layer #3 are not visible
        (("LR3S", SMAX),): 20,
    }
    x_pixel3 = {
        (("LR3X", LMIN),): -2 * G,
        (("LR3X", LDEF),): 0,
        (("LR3X", LMAX),): 2 * G,
    }
    y_pixel3 = {
        (("LR3Y", LMIN),): -2 * G,
        (("LR3Y", LDEF),): 0,
        (("LR3Y", LMAX),): 2 * G,
    }
    x_canvas3 = {
        (("LR3X", LMIN),): 500 - P/2 - 2 * G,
        (("LR3X", LDEF),): 500 - P/2,
        (("LR3X", LMAX),): 500 - P/2 + 2 * G,
    }
    y_canvas3 = {
        (("LR3Y", LMIN),): P - 2 * G,
        (("LR3Y", LDEF),): P,
        (("LR3Y", LMAX),): P + 2 * G
    }

    layer3_pixel = PaintTranslate(
        x_pixel3, y_pixel3, PaintTransform((scale_factor3, 0, 0, scale_factor3, 0, 0), layer3)
    )
    layer3_canvas = PaintTranslate(
        x_canvas3, y_canvas3, PaintTransform((scale_factor3, 0, 0, scale_factor3, 0, 0), layer3)
    )

##
# Applying the pixels
##


# To build a pixel glyph, we paint each pixel twice, once with each
# layer. We might want to change this to clever compositing/blending
# later, depending on how things look when we have the layers working
# correctly. So this function returns a paint tree with a PaintColrLayers
# operation, containing two layers for each pixel.
def buildPixelGlyph(pixelGlyphName, pixelPositions, layer1, layer2): #, layer3):
    layers = []
    for x, y in pixelPositions:
        layers.append(PaintTranslate(x, y, PaintGlyph(pixelGlyphName, layer1)))
        layers.append(PaintTranslate(x, y, PaintGlyph(pixelGlyphName, layer2)))
        # 3 layers gets too slow in t FontGoggles to select something
        # So we better can stay with 2 layers. That's still a lot to choose from.
        #layers.append(PaintTranslate(x, y, PaintGlyph(pixelGlyphName, layer3)))
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
            # 3 layers gets too slow in t FontGoggles to select something
            # So we better can stay with 2 layers. That's still a lot to choose from.
            #layer3_canvas,
        )
    else:
        glyphs[glyphName] = buildPixelGlyph(
            "px",
            pixelPositions(font, glyphName),
            layer1_pixel,
            layer2_pixel,
            # 3 layers gets too slow in t FontGoggles to select something
            # So we better can stay with 2 layers. That's still a lot to choose from.
            #layer3_pixel,
        )

# We have a problem; we have added six new axes to the font at this point,
# and while the gvar table can cope with that because it gets rebuilt when
# the font is saved, the HVAR table is not fully decompiled by fontTools,
# so it still refers to four axes, which makes it invalid when you try
# to save the font. Thankfully, HVAR isn't very necessary anyway, so we
# just get rid of it.
del font["HVAR"]
