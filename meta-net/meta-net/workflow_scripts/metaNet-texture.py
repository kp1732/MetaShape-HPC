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

#output folder path
outputDir = rootDir+'output/'

#open document instance
doc.open(path = outputDir+'intermediate/dense_step/project-dense.psx')

#********************************

#store list of network tasks
network_tasks = list()

#set active chunk to the merged chunk
chunk = doc.chunks[-1]

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
task.texture_size = 2048 # [2048, 4096]

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)


#create batch and send to server
client = Metashape.NetworkClient()
serverIP = sys.argv[1] #server ip
client.connect(serverIP)
batch_id = client.createBatch("project-dense.psx", network_tasks) # HAS TO BE NAME OF OPEN PROJECT
client.resumeBatch(batch_id)


### check task progress: keeps script from finishing until NetworkTask is done
taskCheck = True
while(taskCheck):
	batchStat = client.batchStatus(batch_id)
	if batchStat['status'] == "inprogress":
		time.sleep(5)
	else:
		taskCheck = False
