from direct.showbase.DirectObject import DirectObject
from Config import *
import GUI

class KeyboardTileTraverser(DirectObject):

    def __init__(self, client):
        DirectObject.__init__(self)
        self.client = client

    def acceptAll(self):
        self.accept(CIRCLE_BTN,                   self.onCircleClicked        )
        self.accept(CROSS_BTN,                    self.onCrossClicked         )
        self.accept("arrow_up",           lambda: self.onArrowClicked('up'   ))
        self.accept("arrow_down",         lambda: self.onArrowClicked('down' ))
        self.accept("arrow_left",         lambda: self.onArrowClicked('left' ))
        self.accept("arrow_right",        lambda: self.onArrowClicked('right'))
        self.accept("arrow_up-repeat",    lambda: self.onArrowClicked('up'   ))
        self.accept("arrow_down-repeat",  lambda: self.onArrowClicked('down' ))
        self.accept("arrow_left-repeat",  lambda: self.onArrowClicked('left' ))
        self.accept("arrow_right-repeat", lambda: self.onArrowClicked('right'))

    def onArrowClicked(self, direction):
        x = self.client.cursor.x
        y = self.client.cursor.y

        h = self.client.camhandler.container.getH()
        while h > 180:
            h -= 360
        while h < -180:
            h += 360

        if direction == 'up':
            if h >=    0 and h <  90:
                self.client.findTileAndUpdateCursorPos((x+1, y  ))
            if h >=  -90 and h <   0:
                self.client.findTileAndUpdateCursorPos((x  , y-1))
            if h >= -180 and h < -90:
                self.client.findTileAndUpdateCursorPos((x-1, y  ))
            if h >=   90 and h < 180:
                self.client.findTileAndUpdateCursorPos((x  , y+1))
        elif direction == 'down':
            if h >=    0 and h <  90:
                self.client.findTileAndUpdateCursorPos((x-1, y  ))
            if h >=  -90 and h <   0:
                self.client.findTileAndUpdateCursorPos((x  , y+1))
            if h >= -180 and h < -90:
                self.client.findTileAndUpdateCursorPos((x+1, y  ))
            if h >=   90 and h < 180:
                self.client.findTileAndUpdateCursorPos((x  , y-1))
        elif direction == 'left':
            if h >=    0 and h <  90:
                self.client.findTileAndUpdateCursorPos((x  , y+1))
            if h >=  -90 and h <   0:
                self.client.findTileAndUpdateCursorPos((x+1, y  ))
            if h >= -180 and h < -90:
                self.client.findTileAndUpdateCursorPos((x  , y-1))
            if h >=   90 and h < 180:
                self.client.findTileAndUpdateCursorPos((x-1, y  ))
        elif direction == 'right':
            if h >=    0 and h <  90:
                self.client.findTileAndUpdateCursorPos((x  , y-1))
            if h >=  -90 and h <   0:
                self.client.findTileAndUpdateCursorPos((x-1, y  ))
            if h >= -180 and h < -90:
                self.client.findTileAndUpdateCursorPos((x  , y+1))
            if h >=   90 and h < 180:
                self.client.findTileAndUpdateCursorPos((x+1, y  ))

    # You clicked on a tile, this can mean different things, so this is a dispatcher
    def onCircleClicked(self):
        if self.client.cursor.x is not False and self.client.party['yourturn']:

            x = self.client.cursor.x
            y = self.client.cursor.y
            z = self.client.cursor.z

            if self.client.charcard:
                self.client.charcard.hide()

            # we clicked an active walkable tile, let's move the character
            if self.client.party['map']['tiles'][x][y][z].has_key('walkablezone'):
                charid = self.client.party['map']['tiles'][x][y][z]['walkablezone']
                self.client.clicked_snd.play()
                dest = (x, y, z)
                self.client.send.GET_PATH(charid, dest)
                return

            # we clicked on a character
            if self.client.party['map']['tiles'][x][y][z].has_key('char'):
                charid = self.client.party['map']['tiles'][x][y][z]['char']
                self.client.clicked_snd.play()

                # we clicked on a target, let's attack it!
                if self.client.party['map']['tiles'][x][y][z].has_key('attackablezone'):
                    attackable = self.client.party['map']['tiles'][x][y][z]['attackablezone']
                    self.ignoreAll()
                    if self.client.charbars:
                        self.client.charbars.hide()
                    self.client.actionpreview = GUI.ActionPreview(
                        self.client.party['chars'][attackable],
                        self.client.party['chars'][charid],
                        16,
                        99,
                        lambda: GUI.AttackCheck(
                            lambda: self.client.send.ATTACK(attackable, charid),
                            self.client.send.UPDATE_PARTY
                        ),
                        self.client.send.UPDATE_PARTY
                    )

                # we clicked on the currently active character, let's display the menu
                elif self.client.party['chars'][charid]['active'] and self.client.party['yourturn']:
                    self.client.send.UPDATE_PARTY()
            else:
                self.client.clicked_snd.play()
                self.client.send.UPDATE_PARTY()
    
    def onCrossClicked(self):
        if self.client.cursor.x is not False and self.client.party['yourturn']:

            x = self.client.cursor.x
            y = self.client.cursor.y
            z = self.client.cursor.z

            if self.client.subphase == 'free':
                # if we clicked on a character
                if self.client.party['map']['tiles'][x][y][z].has_key('char'):
                    charid = self.client.party['map']['tiles'][x][y][z]['char']
                    self.client.send.GET_PASSIVE_WALKABLES(charid)

            elif self.client.subphase == 'passivewalkables':
                self.client.matrix.clearZone()
                self.client.cancel_snd.play()
                self.client.subphase = 'free'

            elif self.client.subphase == 'move':
                self.client.matrix.clearZone()
                self.client.cancel_snd.play()
                self.client.subphase = None
                self.client.send.UPDATE_PARTY()

            elif self.client.subphase == 'attack':
                self.client.matrix.clearZone()
                self.client.cancel_snd.play()
                self.client.subphase = None
                self.client.send.UPDATE_PARTY()