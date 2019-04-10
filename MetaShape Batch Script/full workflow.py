import Metashape #metashape module
import os, sys #system modules

#Important Notes
#chunk = doc.chunk must be done after each save or else referrence to active chunk will be lost. Dense clouds and model will not be built otherwise. 


#PROJECT PREP BEGIN
#********************************

#current document instance
doc = Metashape.app.document

#script file path
scriptDir = sys.path[0]

#input folder path
inputDir = scriptDir+'/input'

#output folder path
outputDir = scriptDir+'/output'

#save document instance
doc.save(path = outputDir+'/main/project1 main.psx')

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
print(photoList)

#create photo list with paths for each
for i in range(len(photoList)):
    photoList[i] = inputDir+'/'+photoList[i]

#add photos to project from input fodler
chunk.addPhotos(photoList)

#********************************
#PROJECT PREP END


#PROJECT PARAMETERS BEGIN
#********************************
#CONFIRGURE PARAMETERS OF PROJECT HERE

#alignment parameters - CHANGE HERE
Accuracy = Metashape.LowAccuracy # [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
genPreselection = True # [True, False]
refPreselection = False # [True, False]
filterMask = False # [True, False]
maskTiepoints = False # [True, False]
keypointLimit = 40,000 # [int]
tiepointLimit = 4,000 # [int]
keepKeypoints = True # [True, False]
Pairs = list() # [user defined list of cameras to match]

#depth map parameters
Quality = Metashape.LowQuality # [LowestQuality, LowQuality, MediumQuality, HighQuality, UltrahighQuality]
Filter = Metashape.AggressiveFiltering # [NoFiltering, ModerateFiltering, MildFiltering, AggressiveFiltering]

#model parameters
Surface = Metashape.Arbitrary # [Arbitrary, HeightField]
Interpolation = Metashape.EnabledInterpolation # [DisabledInterpolation, EnabledInterpolation, Extrapolated]

#UV parameters
Mapping = Metashape.GenericMapping # [AdaptiveOrthophotoMapping, CameraMapping, GenericMapping, LegacyMapping, OrthophotoMapping, SphericalMapping]

#Texture parameters
BlendingMode = Metashape.MosaicBlending # [AverageBlending, DisabledBlending, MaxBlending, MinBlending, MosaicBlending]
TextureSize = 2048 # [2048, 4096]
#********************************
#PROJECT PARAMETERS END


#PROJECT BUILD BEGIN
#********************************
#DO NOT MODIFY THIS CODE, CHANGE PARAMETERS ABOVE

#align photos
chunk.matchPhotos(accuracy=Accuracy, generic_preselection=genPreselection, reference_preselection=refPreselection)
chunk.alignCameras()

#save intermediate
doc.save(path = outputDir+'/intermediate/align step/project1-align step.psx')
chunk = doc.chunk

#build depth map & dense cloud
chunk.buildDepthMaps(quality=Quality, filter=Filter)
chunk.buildDenseCloud()

#save intermediate
doc.save(path = outputDir+'/intermediate/dense cloud step/project1-dense cloud step.psx')
chunk = doc.chunk

#build model
chunk.buildModel(surface=Surface, interpolation=Interpolation)

#save intermediate
doc.save(path = outputDir+'/intermediate/model step/project1-model step.psx')
chunk = doc.chunk

#build UV
chunk.buildUV(mapping = Mapping)

#build Texture
chunk.buildTexture(blending = BlendingMode, size = TextureSize)

#export model
chunk.exportModel(path = outputDir+'/mesh/project1-mesh.obj')

#********************************
#PROJECT BUILD END


#********************************
#save MetaShape main project
doc.save(path = outputDir+'/main/project1 main.psx')
#********************************
