from Config import GAME
import GUI

def execute(client, iterator):
    if client.charbars:
        client.charbars.hide()
    if client.charcard:
        client.charcard.hide()
    if client.actionpreview:
        client.actionpreview.hide()
    for i,charid in enumerate(client.matrix.sprites):
        if client.matrix.sprites[charid].animation == 'walk':
            client.updateSpriteAnimation(charid, 'stand')
    client.music.stop()
    client.music = base.loader.loadSfx(GAME+'/music/13.ogg')
    client.music.play()
    GUI.BrownOverlay(GUI.Congratulations, client.end)