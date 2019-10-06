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
doc.open(path = outputDir+'intermediate/align_step/project-align.psx')

#********************************

#store list of network tasks
network_tasks = list()

for i in range(len(doc.chunks)):

	chunk = doc.chunks[i]

	### build calculate depth maps task
	task = Metashape.Tasks.BuildDepthMaps()
	task.downscale = Metashape.Quality.HighQuality
	task.filter_mode = Metashape.FilterMode.ModerateFiltering
	task.network_distribute = True

	n_task = Metashape.NetworkTask()
	n_task.name = task.name
	n_task.params = task.encode()
	n_task.frames.append((chunk.key, 0))
	network_tasks.append(n_task)

	### build save project task
	task = Metashape.Tasks.SaveProject()
	task.path = outputDir+'intermediate/dense_step/project-depth.psx'

	n_task = Metashape.NetworkTask()
	n_task.name = task.name
	n_task.params = task.encode()
	n_task.frames.append((chunk.key, 0))
	network_tasks.append(n_task)

### running processing:
client = Metashape.NetworkClient()
serverIP = sys.argv[1] #server ip
client.connect(serverIP)
batch_id = client.createBatch("project-align.psx", network_tasks) # HAS TO BE NAME OF OPEN PROJECT
client.resumeBatch(batch_id)

### check task progress: keeps script from finishing until NetworkTask is done
taskCheck = True
while(taskCheck):
	batchStat = client.batchStatus(batch_id)
	if batchStat['status'] == "inprogress":
		time.sleep(5)
	else:
		taskCheck = False
