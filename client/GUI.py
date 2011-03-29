import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

u = 1.0/128.0
hover_snd = base.loader.loadSfx("sounds/hover.ogg")
clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")

class Menu(object):

    displayed = False

    def __init__(self, movecommand, attackcommand, waitcommand, cancelcommand):
    
        if not Menu.displayed:

            # Menu frame
            menutexture = loader.loadTexture('textures/gui/menu.png')
            menutexture.setMagfilter(Texture.FTNearest)
            menutexture.setMinfilter(Texture.FTNearest)

            self.frame = DirectFrame(frameTexture = menutexture,
                                    frameColor=(1, 1, 1, 1),
                                    frameSize = ( -.25, .25, -.5, .5 ))
            self.frame.setPos(.75, 0, 0)
            self.frame.setTransparency(True)

            # Move button
            movemaps = loader.loadModel('models/gui/move_btn.egg')
            movebtn  = DirectButton(geom = (movemaps.find('**/move_btn_ready'),
                                            movemaps.find('**/move_btn_pushed'),
                                            movemaps.find('**/move_btn_hover'),
                                            movemaps.find('**/move_btn_disabled')),
                                    command = lambda: self.commandanddestroy(movecommand),
                                    rolloverSound=hover_snd,
                                    clickSound=clicked_snd,
                                    relief=None,
                                    pressEffect=0)
            movebtn.reparentTo(self.frame)
            movebtn.setScale(.5, -1, .125)
            movebtn.setPos(-u*12, 0, u*22)
            movebtn.setTransparency(True)

            # Attack button
            attackmaps = loader.loadModel('models/gui/attack_btn.egg')
            attackbtn  = DirectButton(geom = (attackmaps.find('**/attack_btn_ready'),
                                              attackmaps.find('**/attack_btn_pushed'),
                                              attackmaps.find('**/attack_btn_hover'),
                                              attackmaps.find('**/attack_btn_disabled')),
                                      command = lambda: self.commandanddestroy(attackcommand),
                                      rolloverSound=hover_snd,
                                      clickSound=clicked_snd,
                                      relief=None,
                                      pressEffect=0)
            attackbtn.reparentTo(self.frame)
            attackbtn.setScale(.5, -1, .125)
            attackbtn.setPos(-u*12, 0, u*6)
            attackbtn.setTransparency(True)

            # Wait button
            waitmaps = loader.loadModel('models/gui/wait_btn.egg')
            waitbtn  = DirectButton(geom = (waitmaps.find('**/wait_btn_ready'),
                                            waitmaps.find('**/wait_btn_pushed'),
                                            waitmaps.find('**/wait_btn_hover'),
                                            waitmaps.find('**/wait_btn_disabled')),
                                    command = lambda: self.commandanddestroy(waitcommand),
                                    rolloverSound=hover_snd,
                                    clickSound=clicked_snd,
                                    relief=None,
                                    pressEffect=0)
            waitbtn.reparentTo(self.frame)
            waitbtn.setScale(.5, -1, .125)
            waitbtn.setPos(-u*12, 0, u*-10)
            waitbtn.setTransparency(True)

            # Cancel button
            cancelmaps = loader.loadModel('models/gui/cancel_btn.egg')
            cancelbtn  = DirectButton(geom = (cancelmaps.find('**/cancel_btn_ready'),
                                              cancelmaps.find('**/cancel_btn_pushed'),
                                              cancelmaps.find('**/cancel_btn_hover'),
                                              cancelmaps.find('**/cancel_btn_disabled')),
                                      command = lambda: self.commandanddestroy(cancelcommand),
                                      rolloverSound=hover_snd,
                                      clickSound=clicked_snd,
                                      relief=None,
                                      pressEffect=0)
            cancelbtn.reparentTo(self.frame)
            cancelbtn.setScale(.5, -1, .125)
            cancelbtn.setPos(-u*12, 0, u*-26)
            cancelbtn.setTransparency(True)

            Menu.displayed = True

    def destroy(self):
        self.frame.destroy()
        Menu.displayed = False

    def commandanddestroy(self, command):
        command()
        self.destroy()

