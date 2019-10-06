
import Metashape
import os, sys #system modules

#PROJECT PREP BEGIN
#********************************

#current document instance
doc = Metashape.app.document

#script file path
scriptDir = sys.path[0]

#root path
rootDir = scriptDir[:len(scriptDir)-len("workflow_scripts")]

#input folder path
inputDir = rootDir+'input/'

#output folder path
outputDir = rootDir+'output/'

#********************************

#set refernce to active chunk
chunk = doc.chunk

#store list of network tasks
network_tasks = list()

### match photos
task = Metashape.Tasks.MatchPhotos()
task.downscale = Metashape.Accuracy.HighAccuracy
task.keypoint_limit = 40000
task.tiepoint_limit = 4000
task.preselection_generic = True
task.preselection_reference = True
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

###align cameras
task = Metashape.Tasks.AlignCameras()
task.adaptive_fitting = False
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### depth maps
task = Metashape.Tasks.BuildDepthMaps()
task.downscale = Metashape.Quality.MediumQuality
task.filter_mode = Metashape.FilterMode.MildFiltering
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### dense cloud
task = Metashape.Tasks.BuildDenseCloud()
task.point_colors = True
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### model
task = Metashape.Tasks.buildModel()
task.surface_type = Metashape.Arbitrary # [Arbitrary, HeightField]
task.interpolation = Metashape.EnabledInterpolation # [DisabledInterpolation, EnabledInterpolation, Extrapolated]
task.vertex_colors = True
task.face_count = Metashape.HighFaceCount
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### uv
task = Metashape.Tasks.buildUV()
task.mapping_mode = Metashape.GenericMapping # [AdaptiveOrthophotoMapping, CameraMapping, GenericMapping, LegacyMapping, OrthophotoMapping, SphericalMapping]
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### texture
task = Metashape.Tasks.buildTexture()
task.blending_mode = BlendingMode = Metashape.MosaicBlending # [AverageBlending, DisabledBlending, MaxBlending, MinBlending, MosaicBlending]
task.texture_size = 4096 # [2048, 4096]
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)


### running processing:
client = Metashape.NetworkClient()
client.connect("172.16.0.13") #server ip
batch_id = client.createBatch("project.psx", network_tasks)
client.resumeBatch(batch_id) 