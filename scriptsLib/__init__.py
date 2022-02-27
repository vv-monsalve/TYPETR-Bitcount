#
#   Bitcount production scripts
#
SOURCES_PATH = 'sources/'
UFO_PATH = SOURCES_PATH + 'ufo/'
FEATURES_PATH = SOURCES_PATH + 'features/'
MASTERS_PATH = '_masters/'

# Name parts to auto-construct generated master UFO names.
BITCOUNT = 'Bitcount'
GRID = 'Grid'
MONO = 'Mono'
PROP = 'Prop'
TYPES = (GRID, MONO, PROP)
SINGLE = 'Single'
DOUBLE = 'Double'
STEMS = (SINGLE, DOUBLE)

# Source masters in sources/ufo/, used to copy into _masters/ with replaced pixel shape.
VARIATION_PIXELS = 'Bitcount-VariationPixels.ufo'
GRID_DOUBLE = 'Bitcount_Grid_Double.ufo'
GRID_SINGLE_ITALIC = 'Bitcount_Grid_Single_Italic.ufo'
GRID_SINGLE = 'Bitcount_Grid_Single.ufo'
GRID_SINGLE_ITALIC = 'Bitcount_Grid_Single_Italic.ufo'
MONO_DOUBLE = 'Bitcount_Mono_Double.ufo'
MONO_DOUBLE_ITALIC = 'Bitcount_Mono_Double-Italic.ufo'
MONO_SINGLE = 'Bitcount_Mono_Single.ufo'
MONO_SINGLE_ITALIC = 'Bitcount_Mono_Single-Italic.ufo'
PROP_DOUBLE = 'Bitcount_Prop_Double.ufo'
PROP_DOUBLE_ITALIC = 'Bitcount_Prop_Double-Italic.ufo'
PROP_SINGLE = 'Bitcount_Prop_Single.ufo'
PROP_SINGLE_ITALIC = 'Bitcount_Prop_Single-Italic.ufo'

# Pixel weight sizes in pixel glyph names, this is the stem width of Bitcount glyphs
THIN = 60
BOOK = 80
REGULAR = 100 
SEMIBOLD = 116
BOLD = 160
BLACK = 200
WEIGHTS = (THIN, BOOK, REGULAR, SEMIBOLD, BOLD, BLACK)

CLOSED_QUAD = 0
OPEN_QUAD = 1000

FILLED = 0
LINE = 1000

# Shapes
CIRCLE = 0
SQUARE = 500
PLUS = 1000
SHAPE_NAMES = {
    CIRCLE: 'Circle', 
    SQUARE: 'Square', 
    PLUS: 'Plus',
}

ROMAN = 0
ITALIC = 1000

# Axis values: Minimum, Default, Maximum
wght_MIN, wght_DEF, wght_MAX = wght_AXIS = (THIN, REGULAR, BLACK) 
OPEN_MIN, OPEN_DEF, OPEN_MAX = OPEN_AXIS = (CLOSED_QUAD, CLOSED_QUAD, OPEN_QUAD) # Connected or open quadrants
LINE_MIN, LINE_DEF, LINE_MAX = LINE_AXIS = (FILLED, FILLED, LINE) # Thickness of outline
SHPE_MIN, SHPE_DEF, SHPE_MAX = SHPE_AXIS = (CIRCLE, CIRCLE, PLUS) # Catalog of a sequence of pixel variations
slnt_MIN, slnt_DEF, slnt_MAX = slnt_AXIS = (ROMAN, ROMAN, ITALIC) # Slant angle

# Total number of masters:
# 3 (slnt) x 3 (OPEN) x 3 (LINE) x 6 (wght) x 
def makePixelMasters():
    """Copy the Bitcount masters into MASTERS_PATH, alther their name an fill in the pixels
    shape at that location in the design space.
    """
    print('--- Making pixel masters')
    
    # Make the local masters path. Note that this directory does not commit to Github.
    if not os.path.exists(MASTERS_PATH):
        os.mkdir(MASTERS_PATH)

    # Remove old UFO masters here
    for fileName in os.listdir(MASTERS_PATH):
        if fileName.endswith('.ufo'):
            deleteUFO(dstPath)


def XXXcopyUfoMasters():
    print('--- Copy masters from', UFO_PATH, 'to', MASTERS_PATH)
    if not os.path.exists(MASTERS_PATH):
        os.mkdir(MASTERS_PATH)
    # Copy feature sources
    shutil.copytree(mastersData.path + FEATURES_PATH, MASTERS_PATH + FEATURES_PATH, dirs_exist_ok=True)
    # Copy ufo4/ to masters4/
    for ufoName, d in sorted(mastersData.items()):
        srcPath = masterData.path + ufoName
        dstPath = MASTERS_PATH + ufoName #+ name2MasterName(ufoName)
        if os.path.exists(dstPath):
            deleteUFO(dstPath)
        if VERBOSE:
            print('... Copy', srcPath, 'to', dstPath)
        copyUFO(srcPath, dstPath)

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


def deleteUFO(path):
    assert path.endswith('.ufo')
    if os.path.exists(path):
        shutil.rmtree(path)

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

def copyUFOs(srcDirPath, dstDirPath):
    """Copy all UFO's in the srcDirPath to dstDirPath.
    """
    if not srcDirPath.endswith('/'):
        srcDirPath += '/'
    if not dstDirPath.endswith('/'):
        dstDirPath += '/'
    assert os.path.isdir(srcDirPath)
    copiedFiles = []
    for fileName in os.listdir(srcDirPath):
        if fileName.endswith('.ufo'):
            shutil.copytree(srcDirPath + fileName, dstDirPath + fileName)
            copiedFiles.append(fileName)
    return copiedFiles
   
 