import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from Config import *

v = 1.0/120.0
scale = 2*12.0/240.0
whitefont = loader.loadFont(GAME+'/fonts/fftwhite')

def WindowNodeDrawer(w, h, style, title=None):

    # 0 1 2
    # 3 4 5
    # 6 7 8
    w = float(w)
    h = float(h)

    container = NodePath('foo')

    frames = (
        ( -v*(w/2   ), -v*(w/2-16),  v*(h/2-16),  v*(h/2   ) ),
        ( -v*(w/2-16),  v*(w/2-16),  v*(h/2-16),  v*(h/2   ) ),
        (  v*(w/2-16),  v*(w/2   ),  v*(h/2-16),  v*(h/2   ) ),
        ( -v*(w/2   ), -v*(w/2-16),  v*(h/2-16), -v*(h/2-16) ),
        ( -v*(w/2- 2),  v*(w/2- 2), -v*(h/2- 2),  v*(h/2- 2) ), # 4
        (  v*(w/2-16),  v*(w/2   ),  v*(h/2-16), -v*(h/2-16) ),
        ( -v*(w/2   ), -v*(w/2-16), -v*(h/2   ), -v*(h/2-16) ),
        ( -v*(w/2-16),  v*(w/2-16), -v*(h/2   ), -v*(h/2-16) ),
        (  v*(w/2-16),  v*(w/2   ), -v*(h/2   ), -v*(h/2-16) ),
    )

    for i in (4,0,1,2,3,5,6,7,8):

        path = GAME+'/textures/gui/'+THEME+'/'+style+'/'+str(i)+'.png'

        tex = loader.loadTexture(path)
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
        tex.setWrapU(Texture.WMRepeat)
        tex.setWrapV(Texture.WMRepeat)

        cm = CardMaker('card')
        cm.setFrame(frames[i])
        if i == 4:
            cm.setUvRange((0,0), (w/tex.getOrigFileXSize(), h/tex.getOrigFileYSize()))

        card = container.attachNewNode(cm.generate())
        card.setTexture(tex)
        card.setPos(-v*.5, 0, v*.5)

    if title:

        titleLabel = DirectLabel(
            color = (0,0,0,0),
            text = title,
            scale = scale,
            text_font = whitefont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = container,
            pos = (-v*(w/2-2), 0, v*(h/2-6))
        )

    return container