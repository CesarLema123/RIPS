# test visualizations of lammps outputs
# run file using ovitos program by running '/Applications/Ovito.app/Contents/MacOS/ovitos -g file.py'
#
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# ${DIR}/Ovito.app/Contents/MacOS/ovitos $@
# appDirectory = '/Applications/Ovito.app/Contents/MacOS/ovitos'
# os.system(appDirectory + ' ' + 'hello.py')

import os
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *

class Consts:
    def __init__(self):
        self.filename = "pos.XYZ"    #file should be in same directory

# --------------------- code --------------------------------

consts = Consts()   # Encapsulation of hard coded constants

node = import_file(consts.filename)        #creates and returns an ObjectNode instance

#node.modifiers.append(SelectExpressionModifier(expression="PotentialEnergy<-3.9"))
#node.modifiers.append(DeleteSelectedParticlesModifier())
node.modifiers.append(PolyhedralTemplateMatchingModifier())

inputFile = node.source                      # gets FileSource instance form node
currModifiers = node.modifiers               # gets

print("Hello, this is OVITO %i.%i.%i" % ovito.version)


#  ------------------ Exporting data to a file --------------------------
#export_file(node, "outputdata.dump", "lammps_dump", columns = ["Position.X", "Position.Y", "Position.Z", "Structure Type"])



#  ------------------ Rendering Images --------------------------
vp = Viewport()
vp.type = Viewport.Type.PERSPECTIVE
vp.camera_pos = (-100, -150, 150)
vp.camera_dir = (2, 3, -3)
#vp.fov = math.radians(60.0)

#settings = RenderSettings( filename = "myimage.png", size = (800, 600) ) # prints the simulation to img file


node.add_to_scene()
#vp.render(settings)



