import Metashape
import os, sys #system modules
import time #time module

#PROJECT PREP BEGIN
#********************************

#current document instance
doc = Metashape.app.document

#script file path
scriptDir = sys.path[0]

#root path
rootDir = scriptDir[:len(scriptDir)-len("workflow_scripts")]

#input folder path
#inputDir = rootDir+'input/'

#output folder path
outputDir = rootDir+'output/'

#save document instance
doc.open(path = outputDir+'intermediate/dense_step/project-depth.psx')

#********************************

#set refernce to active chunk
chunk = doc.chunk

#store list of network tasks
network_tasks = list()

### build dense cloud task
task = Metashape.Tasks.BuildDenseCloud()
task.point_colors = True
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### build save project task
task = Metashape.Tasks.SaveProject()
task.path = outputDir+'intermediate/dense_step/project-dense.psx'

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### build model task
task = Metashape.Tasks.BuildModel()
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

### build uv task
task = Metashape.Tasks.BuildUV()
task.mapping_mode = Metashape.GenericMapping # [AdaptiveOrthophotoMapping, CameraMapping, GenericMapping, LegacyMapping, OrthophotoMapping, SphericalMapping]

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### build texture task
task = Metashape.Tasks.BuildTexture()
task.blending_mode = BlendingMode = Metashape.MosaicBlending # [AverageBlending, DisabledBlending, MaxBlending, MinBlending, MosaicBlending]
task.texture_size = 4096 # [2048, 4096]

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### Export model task
task = Metashape.Tasks.ExportModel()
task.export_colors = True
task.export_texture = True
task.format = Metashape.ModelFormatOBJ
task.texture_format = Metashape.ImageFormatJPEG
task.path = outputDir+'mesh/project.obj'

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### build save project task
task = Metashape.Tasks.SaveProject()
task.path = outputDir+'main/project.psx'

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### running processing:
client = Metashape.NetworkClient()
serverIP = sys.argv[1] #server ip
client.connect(serverIP)
batch_id = client.createBatch("project-depth.psx", network_tasks) # HAS TO BE NAME OF OPEN PROJECT
client.resumeBatch(batch_id)

### check task progress: keeps script from finishing until NetworkTask is done
taskCheck = True
while(taskCheck):
	batchStat = client.batchStatus(batch_id)
	if batchStat['status'] == "inprogress":
		time.sleep(5)
	else:
		taskCheck = False
