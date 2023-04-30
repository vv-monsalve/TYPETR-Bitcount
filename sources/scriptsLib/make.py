# -*- coding: UTF-8 -*-
#
#   Making the separate Bitcount masters, with the pixel shapes filled in.
#
import os, shutil
import codecs

from fontParts.fontshell.font import RFont
from ufo2ft.constants import COLOR_LAYERS_KEY, COLOR_PALETTES_KEY

from scriptsLib import *
from scriptsLib.glyphData import PIXEL_DATA, DEFAULT_PIXEL_NAME # Data of all pixel glyphs
from scriptsLib.masterData import MASTERS_DATA
from scriptsLib.colrv1 import addCOLRv1Layers

BUILD = 8

def getMasterName(md, pd):
    """Calculate the master name from the master data and pixel data location."""
    return f'{BITCOUNT}_{md.variant}_{md.stem}-wght{pd.wght}_OPEN{pd.OPEN}_SHPE{pd.SHPE}_slnt{pd.slnt}.ufo'

def getFamilyName(md):
    return f'{BITCOUNT} {md.variant} {md.stem}'

def getStyleName(pd):
    return f'wght{pd.wght} OPEN{pd.OPEN} SHPE{pd.SHPE} slnt{pd.slnt}'

def deleteUFOs(path):
    """Delete all UFOs in this directory. Faster than removing them one by one."""
    os.system('rm -r %s*.ufo' % path)

def copyMasters(dsName, dsParams, axes):
    """Copy the Bitcount masters into MASTERS_PATH, alther their name an fill in the pixels
    shape at that location in the design space.
    """
    # Make the local _masters/ path. Note that this directory does not commit to Github.
    print('... Cleaning/creating directories in _masters/')
    if not os.path.exists(MASTERS_PATH):
        print('... Make %s folder' % MASTERS_PATH)
        os.mkdir(MASTERS_PATH)
    ufoPath = dsParams['ufoPath']    
    for masterPath in MASTER_PATHS:
        if not os.path.exists(ufoPath):
            os.mkdir(ufoPath)
        else:
            # Remove old UFO masters one by one in case they are here
            deleteUFOs(ufoPath)

    # Copy pixels from this UFO.
    pixels = openFont(UFO_PATH + VARIATION_PIXELS)

    # Open the pixel font, as lead for the masters that need to be generated.
    masterName = dsParams['masterName']
    print('... Copy %s %d location masters (wght=3, open=2, shape=12, slanted=2)' % (masterName, len(PIXEL_DATA)))
    md = MASTERS_DATA[masterName]
    for pName, pd in PIXEL_DATA.items():
        if pd.slnt:
            ufoName = md.italicName
        else:
            ufoName = md.ufoName
        dstName = getMasterName(md, pd) # Calculate master name from master data and pixel data
        dstPath = md.path + dstName
        if not os.path.exists(dstPath):
            srcPath = UFO_PATH + ufoName
            copyUFO(srcPath, dstPath)
            dst = RFont(dstPath)
            dst.info.familyName = getFamilyName(md)
            dst.info.styleName = getStyleName(pd)
            copyGlyph(pixels, pName, dst, PIXEL_NAME)
            addCOLRv1Layers(dst)
            dst.save()
            dst.close()
    
    # COLRv1 axes are independent masters
    stem = dsParams['stem']
    variant = dsParams['variant']
    for LR1S in set((axes['LR1S']['minValue'], axes['LR1S']['maxValue'])):
        for LR1X in set((axes['LR1X']['minValue'], axes['LR1X']['maxValue'])):
            for LR1Y in set((axes['LR1Y']['minValue'], axes['LR1Y']['maxValue'])):
                for LR2S in set((axes['LR2S']['minValue'], axes['LR2S']['maxValue'])):
                    for LR2X in set((axes['LR2X']['minValue'], axes['LR2X']['maxValue'])):
                        for LR2Y in set((axes['LR2Y']['minValue'], axes['LR2Y']['maxValue'])):

                            dstPath = f'_masters/{variant}-{stem}/Bitcount_{variant}_{stem}-LR1S{LR1S}_LR1X{LR1X}_LR1Y{LR1Y}_LR2S{LR2S}_LR2X{LR2X}_LR2Y{LR2Y}.ufo'
                            srcPath = UFO_PATH + md.ufoName
                            copyUFO(srcPath, dstPath)
                            dst = RFont(dstPath)
                            dst.info.familyName = getFamilyName(md)
                            dst.info.styleName = getStyleName(pd)
                            copyGlyph(pixels, DEFAULT_PIXEL_NAME, dst, PIXEL_NAME)
                            addCOLRv1Layers(dst, LR1S, LR1X, LR1Y, LR2S, LR2X, LR2Y)
                            dst.save()
                            dst.close()

    pixels.close()

def isRoboFont():
    try:
        from mojo.roboFont import AllFonts, OpenFont
        return True
    except ModuleNotFoundError: # Not in RoboFont
        pass
    return False

def openFont(nameOrPath, showInterface=False):
    """
    Open a font defined by the name of path. If the font is already open
    in RoboFont, then answer it.
    """
    if nameOrPath.endswith('.otf') or nameOrPath.endswith('.ttf'):
        from fontTools.ttLib.ttFont import TTFont
        return TTFont(nameOrPath)

    if isRoboFont():
        from mojo.roboFont import AllFonts, OpenFont
        for f in AllFonts():
            if nameOrPath == f.info.familyName or f.path.endswith(nameOrPath):
                return f
        assert os.path.exists(nameOrPath)
        try:
            f = OpenFont(nameOrPath, showInterface=False)
        except:
            f = OpenFont(nameOrPath, showUI=False)
        if showInterface:
            f.openInterface()
        return f
        
    # Else not in RoboFont, use plain fontParts instead
    from fontParts.fontshell.font import RFont
    #print('RFONT', nameOrPath) 
    return RFont(nameOrPath, showInterface=showInterface)

def copyUFO(srcPath, dstPath):
    """Copy the UFO in srcPath to dstPath (directory or UFO name).
    Make sure they are not equal and that the srcPath indeed is 
    has a ufo extension.
    """
    assert os.path.exists(srcPath) and srcPath.endswith('.ufo'), ('Wrong source path %s' % srcPath)
    if os.path.exists(dstPath):
        assert os.path.isdir(dstPath) or dstPath.endswith('.ufo'), ('Wrong existing destination path %s' % dstPath)
    else:
        assert dstPath.endswith('.ufo'), ('Wrong destination path %s' % dstPath)
    shutil.copytree(srcPath, dstPath)

def copyGlyph(srcFont, glyphName, dstFont=None, dstGlyphName=None, copyUnicode=True):
    """If dstFont is omitted, then the dstGlyphName (into the same font) should be defined.
    If dstGlyphName is omitted, then dstFont (same glyph into another font) should be defined.
    Note that this also overwrites/copies the anchors.
    """
    if dstFont is None:
        dstFont = srcFont
    if dstGlyphName is None:
        dstGlyphName = glyphName
    assert srcFont != dstFont or glyphName != dstGlyphName, ('### Either dstFont or dstGlyphName should be defined.')
    assert glyphName in srcFont, ('### Glyph /%s does not exist source font "%s"' % (glyphName, srcFont.path))
    #print('@@@', glyphName, dstGlyphName, dstGlyphName in dstFont)
    #print('... Copy pixel /%s to /%s to' % (glyphName, dstGlyphName), dstFont.path)
    srcGlyph = srcFont[glyphName]
    #if not PIXEL_NAME in dstFont:
    #    dstFont.newGlyph(PIXEL_NAME)
    #print('---', srcGlyph.name)
    #dstFont.insertGlyph(srcGlyph, name=dstGlyphName)
    dstFont[dstGlyphName] = srcGlyph
    assert dstGlyphName in dstFont, ('### Glyph /%s does not exist destination font "%s"' % (dstGlyphName, dstFont.path))
    g = dstFont[dstGlyphName]
    #print('@@1', glyphName, PIXEL_NAME, dstGlyphName in dstFont)
    g.changed()
    return g
    #return dstFont[dstGlyphName]
  
def makeDesignSpaceFile(dsName, dsParams, axes):
    """Dynamic generation of the design space file for this number of axes and this variant"""
    print('... Make design space %s' % dsName)
    for pName, pd in PIXEL_DATA.items():
        pass
        #print(pName, pd)

    fin = codecs.open(DESIGNSPACE_TEMPLATE_PATH, 'r', encoding='UTF-8')
    template = fin.read()
    fin.close()

    #wght=dict(minValue=0, default=500, maxValue=1000, name='Weight'),
    #OPEN=dict(minValue=0, default=0, maxValue=1000, name='Open'),
    #SHPE=dict(minValue=0, default=0, maxValue=1000, name='Shape'),
    #slnt=dict(minValue=0, default=0, maxValue=1000, name='Slanted'),
    # COLRv1 axes
    #LR1X=dict(minValue=-500, default=0, maxValue=500, name='Layer1-X'),
    #LR1Y=dict(minValue=-500, default=0, maxValue=500, name='Layer1-Y'),
    #LR2X=dict(minValue=-500, default=0, maxValue=500, name='Layer2-X'),
    #LR2Y=dict(minValue=-500, default=0, maxValue=500, name='Layer2-Y'),

    axisParams = dict(sources='', instances='')
    axisParams['title'] = 'Design space of Bitcount %(variant)s %(stem)s'
    axisParams['stem'] = stem = dsParams['stem']
    axisParams['variant'] = variant = dsParams['variant']
           
    for tag, axis in axes.items():
        axisParams[tag+'Min'] = axis['minValue']
        axisParams[tag+'Def'] = axis['default']
        axisParams[tag+'Max'] = axis['maxValue']

    # Layer axes are independent from main Bitcount shape axes
    LR1S = axes['LR1S']['default']
    LR1X = axes['LR1X']['default']
    LR1Y = axes['LR1Y']['default']
    LR2S = axes['LR2S']['default']
    LR2X = axes['LR2X']['default']
    LR2Y = axes['LR2Y']['default']
    for wght in set((axes['wght']['minValue'], axes['wght']['default'], axes['wght']['maxValue'])):
        # minValue is the same as default
        for OPEN in set((axes['OPEN']['default'], axes['OPEN']['maxValue'])):
            # minValue is the same as default
            for SHPE in SHAPES:
                # minValue is the same as default
                for slnt in set((axes['slnt']['default'], axes['slnt']['maxValue'])):
                    if (wght, OPEN, SHPE, slnt) == DEFAULT_LOCATION:
                        info = '<info copy="1"/>'
                    else: 
                        info = ''
                    path = f'_masters/{variant}-{stem}/Bitcount_{variant}_{stem}-wght{wght}_OPEN{OPEN}_SHPE{SHPE}_slnt{slnt}.ufo'

                    axisParams['sources'] += f"""
        <source familyname="Bitcount {variant} {stem}" 
            filename="{path}" 
            name="Bitcount {variant} {stem}" 
            stylename="wght{wght} OPEN{OPEN} SHPE{SHPE} slnt{slnt}">
            <location>
                <dimension name="Weight" xvalue="{wght}"/>
                <dimension name="Open" xvalue="{OPEN}"/>
                <dimension name="Shape" xvalue="{SHPE}"/>
                <dimension name="Slanted" xvalue="{slnt}"/>
                <!-- COLRv1 axes -->
                <dimension name="Layer1-Scale" xvalue="{LR1S}"/>
                <dimension name="Layer1-X" xvalue="{LR1X}"/>
                <dimension name="Layer1-Y" xvalue="{LR1Y}"/>
                <dimension name="Layer2-Scale" xvalue="{LR2S}"/>
                <dimension name="Layer2-X" xvalue="{LR2X}"/>
                <dimension name="Layer2-Y" xvalue="{LR2Y}"/>
            </location>
            {info}
        </source>
            """

    # COLRv1 axes
    wght = axes['wght']['default']
    OPEN = axes['OPEN']['default']
    SHPE = axes['SHPE']['default']
    slnt = axes['slnt']['default']
    for LR1S in set((axes['LR1S']['minValue'], axes['LR1S']['maxValue'])):
        for LR1X in set((axes['LR1X']['minValue'], axes['LR1X']['maxValue'])):
            for LR1Y in set((axes['LR1Y']['minValue'], axes['LR1Y']['maxValue'])):
                for LR2S in set((axes['LR2S']['minValue'], axes['LR2S']['maxValue'])):
                    for LR2X in set((axes['LR2X']['minValue'], axes['LR2X']['maxValue'])):
                        for LR2Y in set((axes['LR2Y']['minValue'], axes['LR2Y']['maxValue'])):

                            path = f'_masters/{variant}-{stem}/Bitcount_{variant}_{stem}-LR1S{LR1S}_LR1X{LR1X}_LR1Y{LR1Y}_LR2S{LR2S}_LR2X{LR2X}_LR2Y{LR2Y}.ufo'

                            axisParams['sources'] += f"""
                <source familyname="Bitcount {variant} {stem}" 
                    filename="{path}" 
                    name="Bitcount {variant} {stem}" 
                    stylename="wght{wght} OPEN{OPEN} SHPE{SHPE} slnt{slnt}">
                    <location>
                        <dimension name="Weight" xvalue="{wght}"/>
                        <dimension name="Open" xvalue="{OPEN}"/>
                        <dimension name="Shape" xvalue="{SHPE}"/>
                        <dimension name="Slanted" xvalue="{slnt}"/>
                        <!-- COLRv1 axes -->
                        <dimension name="Layer1-Scale" xvalue="{LR1S}"/>
                        <dimension name="Layer1-X" xvalue="{LR1X}"/>
                        <dimension name="Layer1-Y" xvalue="{LR1Y}"/>
                        <dimension name="Layer2-Scale" xvalue="{LR2S}"/>
                        <dimension name="Layer2-X" xvalue="{LR2X}"/>
                        <dimension name="Layer2-Y" xvalue="{LR2Y}"/>
                    </location>
                    {info}
                </source>
                    """

    xml = template % axisParams
    fds = codecs.open(dsName, 'w', encoding='UTF-8')
    fds.write(xml)
    fds.close()

def addCOLRv1toVF(vfPath):
    dstPath = vfPath.replace('.ttf', '_COLRv1.ttf')
    print('--- Adding COLORv1 pixels to', dstPath)
    shutil.copy(vfPath, dstPath)
    add_colorv1(dstPath)

def ZZZaddCOLRv1toUFO(designSpacePath, variant):
    # Open the pixel font, as lead for the masters that need to be generated.
    print('--- Adding COLORv1 layers')
    for masterName, md in MASTERS_DATA.items():
        if md.variant == variant:
            for pName, pd in PIXEL_DATA.items():
                # Bitcount generated masters, that include location-bound pixel shape, typically is called
                # BitcountMono_DoubleCircleSquare_LINE0_OPEN0_SHPE0_slnt0_wght500.ufo
                ufoName = getMasterName(md, pd) # Calculate master name from master data and pixel data
                dstPath = md.path + ufoName
                f = openFont(dstPath)
                print('... Adding COLRv1 layers to', dstPath)
                addCOLRv1(f)
                #f.lib[COLOR_PALETTES_KEY] = palettesRegular
                #f.lib[COLOR_LAYERS_KEY] = colorGlyphsRegular
                f.save()

def addCOLRv1toUFO(designSpacePath, variant):
    # Open the pixel font, as lead for the masters that need to be generated.
    print('--- Adding COLORv1 layers')
    ufoName1 = '_masters/Mono/BitcountMono_Double_OPEN0_SHPE0_slnt0_wght500.ufo'
    ufoName2 = '_masters/Mono/BitcountMono_Double_OPEN0_SHPE0_slnt0_wght0.ufo'

    f1 = openFont(ufoName1)
    f2 = openFont(ufoName2)
    print('... Adding COLRv1 layers to', ufoName1)
    print('... Adding COLRv1 layers to', ufoName2)
    addCOLRv1(f1, f2)
    f1.save()
    f2.save()
    