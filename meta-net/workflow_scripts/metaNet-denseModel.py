
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
doc.open(path = outputDir+'intermediate/dense_step/project-depth.psx')

#********************************

#store list of network tasks
network_tasks = list()

#create list of all chunk keys in doc
chunkKeys = []

#loop through all doc chunks and process til model
for i in range(len(doc.chunks)):

	chunk = doc.chunks[i]
	chunkKeys.append(chunk.key)

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
	task.face_count = Metashape.LowFaceCount
	task.network_distribute = True

	n_task = Metashape.NetworkTask()
	n_task.name = task.name
	n_task.params = task.encode()
	n_task.frames.append((chunk.key, 0))
	network_tasks.append(n_task)


#align all chunks
task = Metashape.Tasks.AlignChunks()
task.chunks = chunkKeys
task.align_method = 2 # 2 = camera alignment?
task.match_downscale = 1

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
for key in chunkKeys: #add all chunk keys to task frames
	n_task.frames.append((key, 0))
network_tasks.append(n_task)


#merge all chunks
task = Metashape.Tasks.MergeChunks()
task.chunks = chunkKeys
task.merge_tiepoints = False
task.merge_dense_clouds = False
task.merge_models = True # 

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
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