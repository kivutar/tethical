from panda3d.core import GeomVertexFormat, Geom, GeomVertexData, GeomVertexWriter, GeomTristrips, VBase4, GeomNode, NodePath

# Draw the gradient background representing the sky during a battle
class Sky(object):

    def __init__(self, mp):
        vdata = GeomVertexData('name_me', GeomVertexFormat.getV3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        primitive = GeomTristrips(Geom.UHStatic)
        film_size = base.cam.node().getLens().getFilmSize()
        x = film_size.getX() / 2.0
        z = x * 256.0/240.0
        vertex.addData3f( x, 90,  z)
        vertex.addData3f(-x, 90,  z)
        vertex.addData3f( x, 90, -z)
        vertex.addData3f(-x, 90, -z)
        color.addData4f(VBase4(*mp['backgroundcolor1']))
        color.addData4f(VBase4(*mp['backgroundcolor1']))
        color.addData4f(VBase4(*mp['backgroundcolor2']))
        color.addData4f(VBase4(*mp['backgroundcolor2']))
        primitive.addNextVertices(4)
        primitive.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(primitive)
        self.node = GeomNode('sky')
        self.node.addGeom(geom)
        base.camera.attachNewNode(self.node)

    def remove(self):
        NodePath(self.node).removeNode()