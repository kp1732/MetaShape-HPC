
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
doc.open(path = outputDir+'main/project.psx')

#********************************

#set refernce to active chunk
chunk = doc.chunk

#store list of network tasks
network_tasks = list()

### build match photos task
task = Metashape.Tasks.MatchPhotos()
task.downscale = Metashape.Accuracy.HighAccuracy
task.keypoint_limit = 0
task.tiepoint_limit = 0
task.preselection_generic = True
task.preselection_reference = True
task.network_distribute = True

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### build save project task
task = Metashape.Tasks.SaveProject()
task.path = outputDir+'intermediate/align_step/project-match.psx'

n_task = Metashape.NetworkTask()
n_task.name = task.name
n_task.params = task.encode()
n_task.frames.append((chunk.key, 0))
network_tasks.append(n_task)

### running processing:
client = Metashape.NetworkClient()
serverIP = sys.argv[1] #server ip
client.connect(serverIP)
batch_id = client.createBatch("project.psx", network_tasks) # HAS TO BE NAME OF OPEN PROJECT
client.resumeBatch(batch_id)

### check task progress: keeps script from finishing until NetworkTask is done
taskChek = True
while(taskChek):
	batchStat = client.batchStatus(batch_id)
	if batchStat['status'] == "inprogress":
		time.sleep(5)
	else:
		taskChek = False
