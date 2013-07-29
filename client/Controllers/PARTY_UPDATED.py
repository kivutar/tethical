import json, GUI

def execute(client, iterator):
    client.party['yourturn'] = iterator.getBool()
    client.party['chars'] = json.loads(iterator.getString32())

    client.matrix.clearZone()
    if client.charbars:
        client.charbars.hide()
    if client.charcard:
        client.charcard.hide()
    if client.actionpreview:
        client.actionpreview.hide()
    client.subphase = False

    for x,xs in enumerate(client.party['map']['tiles']):
        for y,ys in enumerate(xs):
            for z,zs in enumerate(ys):
                if not client.party['map']['tiles'][x][y][z] is None:
                    if client.party['map']['tiles'][x][y][z].has_key('char') and client.party['map']['tiles'][x][y][z]['char'] != 0:
                        charid = client.party['map']['tiles'][x][y][z]['char']
                        char = client.party['chars'][charid]

                        if char['active']:
                            client.camhandler.move(client.battleGraphics.logic2terrain((x, y, z)))
                            client.at.showOnSprite(client.matrix.sprites[charid])

                            client.updateCursorPos((x,y,z))

                            client.charcard = GUI.CharCard(char)

                            if client.party['yourturn'] and not char['ai']:
                                if char['canmove'] or char['canact']:
                                    client.showMenu(charid)
                                else:
                                    client.onWaitClicked(charid)
                            else:
                                client.camhandler.ignoreAll()