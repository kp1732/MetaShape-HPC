import Metashape #metashape module
import os, sys #OS and system modules

#Important Notes
#chunk = doc.chunk must be done after each save or else referrence to active chunk will be lost. Dense clouds and model will not be built otherwise. 

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

#chunk label - format will be "label + chunk #"
chunkLabel = "chunk"

#number of chunks to create
numChunk = 1

#create project chunks
for i in range(numChunk):
    chunk = doc.addChunk()
    chunk.label = chunkLabel+"_"+str(i+1)

#********************************

#photos list
photoList = os.listdir(inputDir)

#create photo list with paths for each
for i in range(len(photoList)):
    photoList[i] = inputDir+photoList[i]

#add photos to project from input fodler
chunk.addPhotos(photoList)

#save document instance
doc.save(path = outputDir+'main/project.psx')

#********************************
#PROJECT PREP END
