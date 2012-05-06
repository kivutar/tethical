def execute(client, iterator):
    charid = iterator.getString()
    x2 = iterator.getUint8()
    y2 = iterator.getUint8()
    z2 = iterator.getUint8()

    (x1, y1, z1) = client.matrix.getCharacterCoords(charid)
    del client.party['map']['tiles'][x1][y1][z1]['char']
    client.party['map']['tiles'][x2][y2][z2]['char'] = charid
    client.send.UPDATE_PARTY()