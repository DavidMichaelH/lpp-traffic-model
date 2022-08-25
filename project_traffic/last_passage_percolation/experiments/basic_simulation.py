from last_passage_percolation.algorithms import LPPLineToOriginModel

import time
from datetime import datetime
from datetime import timedelta
import re



#This function seems to do a good job at prediticing how long the computation will take 
def PredictTimeToComplete(x):
    predictedSeconds = round((0.56)*pow(x/100,3))
    updated_time = datetime.now() + timedelta(seconds=predictedSeconds)
    
    print("Computation started at =", datetime.now().strftime("%I:%M %p"))
    print("Computation predicted to finish about =", updated_time.time().strftime("%I:%M %p"))



#This saves a pdf output since it seems to provided the highest resolution picture 
def SaveFile(FILE_PATH_TO_SAVE_OUTPUT_FILES):
    fileName = "line_to_line_size_" + str(halfSideLength) + "_time_" + re.sub(r'[^\w]', '_', datetime.now().strftime("%I:%M %p"))
    model.SaveFigure(FILE_PATH_TO_SAVE_OUTPUT_FILES + fileName + '.pdf')
    
    
### The fun starts here... 
    
startTime = time.time()


halfSideLength = 1500

PredictTimeToComplete(halfSideLength)


model = LPPLineToOriginModel(halfSideLength)
model.SetExponentialWeights()
 
model.ComputeAllTraffic()
 
model.PlotEmpericalCounter(plotGrid = False,colorMap = "magma")

 



#This needs to be a file path to the folder you want your figures to save into.
FILE_PATH_TO_SAVE_OUTPUT_FILES = 'D:/project_traffic/version_1/figures/'
SaveFile(FILE_PATH_TO_SAVE_OUTPUT_FILES)
 
model.ComputeEmpericalCountAlongMiddleSegmnet()

print("Computation finished at =", datetime.now().strftime("%I:%M %p")) 
 
elapsed = time.time() - startTime
print("The computation finished after " + str(elapsed) + " seconds")